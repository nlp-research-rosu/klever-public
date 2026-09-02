# Exhaustive K source inventory

Generated from the recursively byte-identical trusted/candidate supplied semantics plus the candidate proof-local files. Every declaration, configuration, context, rule, and claim is source-positioned below.

## Totals

- Source files: 26
- Inventory entries: 1128
- `claim` entries: 3
- `configuration` entries: 1
- `context` entries: 5
- `endmodule` entries: 27
- `imports` entries: 88
- `module` entries: 27
- `requires` entries: 29
- `rule` entries: 711
- `syntax` entries: 237
- `concrete-only-rule`: 54
- `equational-rule`: 467
- `function-declaration`: 148
- `macro-declaration`: 8
- `named-symbol`: 25
- `opaque-symbol`: 22
- `operational-rule`: 244
- `owise-rule`: 29
- `priority-rule`: 47
- `reachability-claim`: 3
- `total-declaration`: 110

## Per-file counts

- `trusted-reference-semantics/semantics.k`: endmodule=2, imports=23, module=2, requires=23
- `trusted-reference-semantics/semantics/assert.k`: endmodule=1, imports=1, module=1, rule=3
- `trusted-reference-semantics/semantics/bool.k`: context=1, endmodule=1, imports=1, module=1, rule=13
- `trusted-reference-semantics/semantics/builtins.k`: endmodule=1, imports=7, module=1, rule=137, syntax=38
- `trusted-reference-semantics/semantics/call.k`: endmodule=1, imports=3, module=1, rule=21, syntax=3
- `trusted-reference-semantics/semantics/comprehension.k`: endmodule=1, imports=5, module=1, rule=7, syntax=3
- `trusted-reference-semantics/semantics/concrete.k`: endmodule=1, imports=1, module=1, rule=16, syntax=5
- `trusted-reference-semantics/semantics/controls.k`: endmodule=1, imports=3, module=1, requires=1, rule=34, syntax=3
- `trusted-reference-semantics/semantics/core.k`: configuration=1, endmodule=1, imports=7, module=1, requires=1, rule=46, syntax=37
- `trusted-reference-semantics/semantics/dict.k`: endmodule=1, imports=4, module=1, rule=28, syntax=12
- `trusted-reference-semantics/semantics/float.k`: endmodule=1, imports=3, module=1, rule=121, syntax=34
- `trusted-reference-semantics/semantics/functions.k`: endmodule=1, imports=1, module=1, requires=1, rule=15, syntax=4
- `trusted-reference-semantics/semantics/int.k`: endmodule=1, imports=1, module=1, rule=16, syntax=1
- `trusted-reference-semantics/semantics/iter.k`: endmodule=1, imports=1, module=1, syntax=1
- `trusted-reference-semantics/semantics/list.k`: endmodule=1, imports=3, module=1, rule=27, syntax=5
- `trusted-reference-semantics/semantics/methods.k`: endmodule=1, imports=4, module=1, rule=75, syntax=27
- `trusted-reference-semantics/semantics/operators.k`: context=2, endmodule=1, imports=2, module=1, rule=10
- `trusted-reference-semantics/semantics/range.k`: endmodule=1, imports=2, module=1, rule=6, syntax=2
- `trusted-reference-semantics/semantics/set.k`: endmodule=1, imports=1, module=1, rule=12, syntax=6
- `trusted-reference-semantics/semantics/sort.k`: endmodule=1, imports=2, module=1, rule=19, syntax=6
- `trusted-reference-semantics/semantics/str.k`: endmodule=1, imports=2, module=1, rule=28, syntax=5
- `trusted-reference-semantics/semantics/subscript.k`: context=2, endmodule=1, imports=1, module=1, rule=40, syntax=15
- `trusted-reference-semantics/semantics/syntax.k`: endmodule=1, imports=4, module=1, syntax=16
- `trusted-reference-semantics/semantics/tuple.k`: endmodule=1, imports=4, module=1, requires=1, rule=21, syntax=4
- `candidate/verification.k`: endmodule=1, imports=1, module=1, requires=1, rule=16, syntax=10
- `candidate/spec.k`: claim=3, endmodule=1, imports=1, module=1, requires=1

## Entries


### `trusted-reference-semantics/semantics.k`

1. **requires** `trusted-reference-semantics/semantics.k:34-34`  
   Flags: none; attributes: none
   Source: `requires "semantics/syntax.k"`
2. **requires** `trusted-reference-semantics/semantics.k:35-35`  
   Flags: none; attributes: none
   Source: `requires "semantics/core.k"`
3. **requires** `trusted-reference-semantics/semantics.k:36-36`  
   Flags: none; attributes: none
   Source: `requires "semantics/iter.k"`
4. **requires** `trusted-reference-semantics/semantics.k:37-37`  
   Flags: none; attributes: none
   Source: `requires "semantics/range.k"`
5. **requires** `trusted-reference-semantics/semantics.k:38-38`  
   Flags: none; attributes: none
   Source: `requires "semantics/operators.k"`
6. **requires** `trusted-reference-semantics/semantics.k:39-39`  
   Flags: none; attributes: none
   Source: `requires "semantics/int.k"`
7. **requires** `trusted-reference-semantics/semantics.k:40-40`  
   Flags: none; attributes: none
   Source: `requires "semantics/bool.k"`
8. **requires** `trusted-reference-semantics/semantics.k:41-41`  
   Flags: none; attributes: none
   Source: `requires "semantics/float.k"`
9. **requires** `trusted-reference-semantics/semantics.k:42-42`  
   Flags: none; attributes: none
   Source: `requires "semantics/str.k"`
10. **requires** `trusted-reference-semantics/semantics.k:43-43`  
   Flags: none; attributes: none
   Source: `requires "semantics/set.k"`
11. **requires** `trusted-reference-semantics/semantics.k:44-44`  
   Flags: none; attributes: none
   Source: `requires "semantics/list.k"`
12. **requires** `trusted-reference-semantics/semantics.k:45-45`  
   Flags: none; attributes: none
   Source: `requires "semantics/tuple.k"`
13. **requires** `trusted-reference-semantics/semantics.k:46-46`  
   Flags: none; attributes: none
   Source: `requires "semantics/subscript.k"`
14. **requires** `trusted-reference-semantics/semantics.k:47-47`  
   Flags: none; attributes: none
   Source: `requires "semantics/comprehension.k"`
15. **requires** `trusted-reference-semantics/semantics.k:48-48`  
   Flags: none; attributes: none
   Source: `requires "semantics/methods.k"`
16. **requires** `trusted-reference-semantics/semantics.k:49-49`  
   Flags: none; attributes: none
   Source: `requires "semantics/controls.k"`
17. **requires** `trusted-reference-semantics/semantics.k:50-50`  
   Flags: none; attributes: none
   Source: `requires "semantics/functions.k"`
18. **requires** `trusted-reference-semantics/semantics.k:51-51`  
   Flags: none; attributes: none
   Source: `requires "semantics/builtins.k"`
19. **requires** `trusted-reference-semantics/semantics.k:52-52`  
   Flags: none; attributes: none
   Source: `requires "semantics/call.k"`
20. **requires** `trusted-reference-semantics/semantics.k:53-53`  
   Flags: none; attributes: none
   Source: `requires "semantics/sort.k"`
21. **requires** `trusted-reference-semantics/semantics.k:54-54`  
   Flags: none; attributes: none
   Source: `requires "semantics/assert.k"`
22. **requires** `trusted-reference-semantics/semantics.k:55-55`  
   Flags: none; attributes: none
   Source: `requires "semantics/dict.k"`
23. **requires** `trusted-reference-semantics/semantics.k:56-56`  
   Flags: none; attributes: none
   Source: `requires "semantics/concrete.k"`
24. **module** `trusted-reference-semantics/semantics.k:58-58`  
   Flags: none; attributes: none
   Source: `module MPY`
25. **imports** `trusted-reference-semantics/semantics.k:59-59`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
26. **imports** `trusted-reference-semantics/semantics.k:60-60`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER`
27. **imports** `trusted-reference-semantics/semantics.k:61-61`  
   Flags: none; attributes: none
   Source: `imports MPY-RANGE`
28. **imports** `trusted-reference-semantics/semantics.k:62-62`  
   Flags: none; attributes: none
   Source: `imports MPY-OPERATORS`
29. **imports** `trusted-reference-semantics/semantics.k:63-63`  
   Flags: none; attributes: none
   Source: `imports MPY-INT`
30. **imports** `trusted-reference-semantics/semantics.k:64-64`  
   Flags: none; attributes: none
   Source: `imports MPY-BOOL`
31. **imports** `trusted-reference-semantics/semantics.k:65-65`  
   Flags: none; attributes: none
   Source: `imports MPY-FLOAT`
32. **imports** `trusted-reference-semantics/semantics.k:66-66`  
   Flags: none; attributes: none
   Source: `imports MPY-STR`
33. **imports** `trusted-reference-semantics/semantics.k:67-67`  
   Flags: none; attributes: none
   Source: `imports MPY-SET`
34. **imports** `trusted-reference-semantics/semantics.k:68-68`  
   Flags: none; attributes: none
   Source: `imports MPY-LIST`
35. **imports** `trusted-reference-semantics/semantics.k:69-69`  
   Flags: none; attributes: none
   Source: `imports MPY-TUPLE`
36. **imports** `trusted-reference-semantics/semantics.k:70-70`  
   Flags: none; attributes: none
   Source: `imports MPY-SUBSCRIPT`
37. **imports** `trusted-reference-semantics/semantics.k:71-71`  
   Flags: none; attributes: none
   Source: `imports MPY-COMPREHENSION`
38. **imports** `trusted-reference-semantics/semantics.k:72-72`  
   Flags: none; attributes: none
   Source: `imports MPY-METHODS`
39. **imports** `trusted-reference-semantics/semantics.k:73-73`  
   Flags: none; attributes: none
   Source: `imports MPY-CONTROLS`
40. **imports** `trusted-reference-semantics/semantics.k:74-74`  
   Flags: none; attributes: none
   Source: `imports MPY-FUNCTIONS`
41. **imports** `trusted-reference-semantics/semantics.k:75-75`  
   Flags: none; attributes: none
   Source: `imports MPY-BUILTINS`
42. **imports** `trusted-reference-semantics/semantics.k:76-76`  
   Flags: none; attributes: none
   Source: `imports MPY-CALL`
43. **imports** `trusted-reference-semantics/semantics.k:77-77`  
   Flags: none; attributes: none
   Source: `imports MPY-SORT`
44. **imports** `trusted-reference-semantics/semantics.k:78-78`  
   Flags: none; attributes: none
   Source: `imports MPY-ASSERT`
45. **imports** `trusted-reference-semantics/semantics.k:79-79`  
   Flags: none; attributes: none
   Source: `imports MPY-DICT`
46. **endmodule** `trusted-reference-semantics/semantics.k:80-86`  
   Flags: none; attributes: none
   Source: `endmodule // The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's // real key calls, deep list equality). Verification builds import MPY and // never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN — // with plain MPY the concrete legs are silently absent (this was live for a // while: sorted-key stuck and comprehension asserted wrong under krun).`
47. **module** `trusted-reference-semantics/semantics.k:87-87`  
   Flags: none; attributes: none
   Source: `module MPY-KRUN`
48. **imports** `trusted-reference-semantics/semantics.k:88-88`  
   Flags: none; attributes: none
   Source: `imports MPY`
49. **imports** `trusted-reference-semantics/semantics.k:89-89`  
   Flags: none; attributes: none
   Source: `imports MPY-CONCRETE`
50. **endmodule** `trusted-reference-semantics/semantics.k:90-90`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/assert.k`

51. **module** `trusted-reference-semantics/semantics/assert.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-ASSERT`
52. **imports** `trusted-reference-semantics/semantics/assert.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
53. **rule** `trusted-reference-semantics/semantics/assert.k:6-7`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)`
54. **rule** `trusted-reference-semantics/semantics/assert.k:8-11`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)`
55. **rule** `trusted-reference-semantics/semantics/assert.k:13-15`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
56. **endmodule** `trusted-reference-semantics/semantics/assert.k:16-16`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/bool.k`

57. **module** `trusted-reference-semantics/semantics/bool.k:5-5`  
   Flags: none; attributes: none
   Source: `module MPY-BOOL`
58. **imports** `trusted-reference-semantics/semantics/bool.k:6-6`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
59. **rule** `trusted-reference-semantics/semantics/bool.k:8-8`  
   Flags: equational-rule; attributes: none
   Source: `rule applyUn("not", V:Val) => notBool truthy(V)`
60. **rule** `trusted-reference-semantics/semantics/bool.k:10-10`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`
61. **rule** `trusted-reference-semantics/semantics/bool.k:11-15`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 // ==== BoolOp: short-circuit, value-returning and / or ===================== // the node is its own accumulator: heat the HEAD element only, then either return it // (short-circuit) or drop it and continue`
62. **context** `trusted-reference-semantics/semantics/bool.k:16-16`  
   Flags: none; attributes: none
   Source: `context BoolOp(_, (HOLE:Expr, _:Exprs))`
63. **rule** `trusted-reference-semantics/semantics/bool.k:17-17`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`
64. **rule** `trusted-reference-semantics/semantics/bool.k:18-19`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)`
65. **rule** `trusted-reference-semantics/semantics/bool.k:20-21`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)`
66. **rule** `trusted-reference-semantics/semantics/bool.k:22-23`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)`
67. **rule** `trusted-reference-semantics/semantics/bool.k:24-28`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the // operand — and/or return the OBJECT itself (Python identity), not its structure`
68. **rule** `trusted-reference-semantics/semantics/bool.k:29-30`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`
69. **rule** `trusted-reference-semantics/semantics/bool.k:31-34`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
70. **rule** `trusted-reference-semantics/semantics/bool.k:35-38`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`
71. **rule** `trusted-reference-semantics/semantics/bool.k:39-42`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
72. **rule** `trusted-reference-semantics/semantics/bool.k:43-46`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`
73. **endmodule** `trusted-reference-semantics/semantics/bool.k:47-47`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/builtins.k`

74. **module** `trusted-reference-semantics/semantics/builtins.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-BUILTINS`
75. **imports** `trusted-reference-semantics/semantics/builtins.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
76. **imports** `trusted-reference-semantics/semantics/builtins.k:5-5`  
   Flags: none; attributes: none
   Source: `imports MPY-STR`
77. **imports** `trusted-reference-semantics/semantics/builtins.k:6-6`  
   Flags: none; attributes: none
   Source: `imports MPY-SET`
78. **imports** `trusted-reference-semantics/semantics/builtins.k:7-7`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER`
79. **imports** `trusted-reference-semantics/semantics/builtins.k:8-8`  
   Flags: none; attributes: none
   Source: `imports MPY-RANGE`
80. **imports** `trusted-reference-semantics/semantics/builtins.k:9-9`  
   Flags: none; attributes: none
   Source: `imports MPY-INT`
81. **imports** `trusted-reference-semantics/semantics/builtins.k:10-16`  
   Flags: none; attributes: none
   Source: `imports MPY-METHODS // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup // Call routing + argument evaluation live in call.k, which also routes the fold // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to // applyBuiltin. This module owns applyBuiltin + the fold implementations.`
82. **syntax** `trusted-reference-semantics/semantics/builtins.k:17-19`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val ::= applyBuiltin(String, Vals) [function] // ==== len(obj) — O(1) per kind ============================================`
83. **syntax** `trusted-reference-semantics/semantics/builtins.k:20-20`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= seqLen(Val) [function]`
84. **rule** `trusted-reference-semantics/semantics/builtins.k:21-21`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`
85. **rule** `trusted-reference-semantics/semantics/builtins.k:22-22`  
   Flags: equational-rule; attributes: none
   Source: `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)`
86. **rule** `trusted-reference-semantics/semantics/builtins.k:23-23`  
   Flags: equational-rule; attributes: none
   Source: `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)`
87. **rule** `trusted-reference-semantics/semantics/builtins.k:24-24`  
   Flags: equational-rule; attributes: none
   Source: `rule seqLen(str(IS:IntSeq))                   => isLen(IS)`
88. **rule** `trusted-reference-semantics/semantics/builtins.k:25-25`  
   Flags: equational-rule; attributes: none
   Source: `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)`
89. **rule** `trusted-reference-semantics/semantics/builtins.k:26-31`  
   Flags: equational-rule; attributes: none
   Source: `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) == // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order). // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed. // (k-cell — list() constructs a NEW object)`
90. **rule** `trusted-reference-semantics/semantics/builtins.k:32-32`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>`
91. **rule** `trusted-reference-semantics/semantics/builtins.k:33-33`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
92. **rule** `trusted-reference-semantics/semantics/builtins.k:34-34`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>`
93. **rule** `trusted-reference-semantics/semantics/builtins.k:35-35`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>`
94. **syntax** `trusted-reference-semantics/semantics/builtins.k:36-36`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= charsOf(IntSeq) [function, total]`
95. **rule** `trusted-reference-semantics/semantics/builtins.k:37-37`  
   Flags: equational-rule; attributes: none
   Source: `rule charsOf(.IntSeq)                => .ValSeq`
96. **rule** `trusted-reference-semantics/semantics/builtins.k:38-40`  
   Flags: equational-rule; attributes: none
   Source: `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) // ==== set(str) — distinct character codes =================================`
97. **rule** `trusted-reference-semantics/semantics/builtins.k:41-43`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) // ==== abs(int) ============================================================`
98. **rule** `trusted-reference-semantics/semantics/builtins.k:44-46`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==`
99. **syntax** `trusted-reference-semantics/semantics/builtins.k:47-47`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`
100. **rule** `trusted-reference-semantics/semantics/builtins.k:48-48`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`
101. **rule** `trusted-reference-semantics/semantics/builtins.k:49-49`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`
102. **rule** `trusted-reference-semantics/semantics/builtins.k:50-52`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)`
103. **syntax** `trusted-reference-semantics/semantics/builtins.k:54-54`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= intOf(Val) [function]`
104. **rule** `trusted-reference-semantics/semantics/builtins.k:55-55`  
   Flags: equational-rule; attributes: none
   Source: `rule intOf(I:Int)  => I`
105. **rule** `trusted-reference-semantics/semantics/builtins.k:56-58`  
   Flags: equational-rule; attributes: none
   Source: `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi // ==== all / any (short-circuiting #iterNext folds) ========================`
106. **syntax** `trusted-reference-semantics/semantics/builtins.k:59-59`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #allAcc(Iterable) | "#allCont"`
107. **rule** `trusted-reference-semantics/semantics/builtins.k:60-60`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`
108. **rule** `trusted-reference-semantics/semantics/builtins.k:61-61`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #allCont => true ... </k>`
109. **rule** `trusted-reference-semantics/semantics/builtins.k:62-63`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)`
110. **rule** `trusted-reference-semantics/semantics/builtins.k:64-65`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)`
111. **syntax** `trusted-reference-semantics/semantics/builtins.k:67-67`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`
112. **rule** `trusted-reference-semantics/semantics/builtins.k:68-68`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`
113. **rule** `trusted-reference-semantics/semantics/builtins.k:69-69`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #anyCont => false ... </k>`
114. **rule** `trusted-reference-semantics/semantics/builtins.k:70-71`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)`
115. **rule** `trusted-reference-semantics/semantics/builtins.k:72-75`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) // ==== max / min over an iterable (#iterNext folds; first element seeds) ====`
116. **syntax** `trusted-reference-semantics/semantics/builtins.k:76-76`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`
117. **rule** `trusted-reference-semantics/semantics/builtins.k:77-77`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`
118. **rule** `trusted-reference-semantics/semantics/builtins.k:78-79`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)`
119. **rule** `trusted-reference-semantics/semantics/builtins.k:80-80`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`
120. **rule** `trusted-reference-semantics/semantics/builtins.k:81-81`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`
121. **rule** `trusted-reference-semantics/semantics/builtins.k:82-84`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)`
122. **syntax** `trusted-reference-semantics/semantics/builtins.k:86-86`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`
123. **rule** `trusted-reference-semantics/semantics/builtins.k:87-87`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`
124. **rule** `trusted-reference-semantics/semantics/builtins.k:88-89`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)`
125. **rule** `trusted-reference-semantics/semantics/builtins.k:90-90`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`
126. **rule** `trusted-reference-semantics/semantics/builtins.k:91-91`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`
127. **rule** `trusted-reference-semantics/semantics/builtins.k:92-96`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) // ==== variadic max / min (a Vals fold) ====================================`
128. **syntax** `trusted-reference-semantics/semantics/builtins.k:97-97`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= maxVals(Int, Vals) [function]`
129. **rule** `trusted-reference-semantics/semantics/builtins.k:98-98`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`
130. **rule** `trusted-reference-semantics/semantics/builtins.k:99-99`  
   Flags: equational-rule; attributes: none
   Source: `rule maxVals(M:Int, .Vals)           => M`
131. **rule** `trusted-reference-semantics/semantics/builtins.k:100-100`  
   Flags: equational-rule; attributes: none
   Source: `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`
132. **syntax** `trusted-reference-semantics/semantics/builtins.k:102-102`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= minVals(Int, Vals) [function]`
133. **rule** `trusted-reference-semantics/semantics/builtins.k:103-103`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`
134. **rule** `trusted-reference-semantics/semantics/builtins.k:104-104`  
   Flags: equational-rule; attributes: none
   Source: `rule minVals(M:Int, .Vals)           => M`
135. **rule** `trusted-reference-semantics/semantics/builtins.k:105-107`  
   Flags: equational-rule; attributes: none
   Source: `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==`
136. **rule** `trusted-reference-semantics/semantics/builtins.k:108-110`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits`
137. **rule** `trusted-reference-semantics/semantics/builtins.k:111-113`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0`
138. **syntax** `trusted-reference-semantics/semantics/builtins.k:114-114`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= binCodes(Int) [function, total]`
139. **rule** `trusted-reference-semantics/semantics/builtins.k:115-115`  
   Flags: equational-rule; attributes: none
   Source: `rule binCodes(0) => iCons(48, .IntSeq)`
140. **rule** `trusted-reference-semantics/semantics/builtins.k:116-116`  
   Flags: equational-rule; attributes: none
   Source: `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`
141. **syntax** `trusted-reference-semantics/semantics/builtins.k:117-117`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`
142. **rule** `trusted-reference-semantics/semantics/builtins.k:118-118`  
   Flags: equational-rule; attributes: none
   Source: `rule binAcc(0, ACC:IntSeq) => ACC`
143. **rule** `trusted-reference-semantics/semantics/builtins.k:119-123`  
   Flags: equational-rule; attributes: none
   Source: `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========`
144. **rule** `trusted-reference-semantics/semantics/builtins.k:124-125`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`
145. **syntax** `trusted-reference-semantics/semantics/builtins.k:126-126`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`
146. **rule** `trusted-reference-semantics/semantics/builtins.k:127-127`  
   Flags: equational-rule; attributes: none
   Source: `rule enumVS(.ValSeq, _:Int) => .ValSeq`
147. **rule** `trusted-reference-semantics/semantics/builtins.k:128-131`  
   Flags: equational-rule; attributes: none
   Source: `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) // ==== map(str, xs) — eager (only the str case is in the subset) =============`
148. **rule** `trusted-reference-semantics/semantics/builtins.k:132-133`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`
149. **syntax** `trusted-reference-semantics/semantics/builtins.k:134-134`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`
150. **rule** `trusted-reference-semantics/semantics/builtins.k:135-135`  
   Flags: equational-rule; attributes: none
   Source: `rule mapStrVS(.ValSeq) => .ValSeq`
151. **rule** `trusted-reference-semantics/semantics/builtins.k:136-136`  
   Flags: equational-rule; attributes: none
   Source: `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`
152. **rule** `trusted-reference-semantics/semantics/builtins.k:137-139`  
   Flags: equational-rule; attributes: none
   Source: `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) // ==== int(x) identities (int(round(x)) composes through) ====================`
153. **rule** `trusted-reference-semantics/semantics/builtins.k:140-142`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("int", I:Int, .Vals) => I // ==== ord / chr ===========================================================`
154. **rule** `trusted-reference-semantics/semantics/builtins.k:143-143`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`
155. **rule** `trusted-reference-semantics/semantics/builtins.k:144-147`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 // ==== str(int) / str(str) =================================================`
156. **rule** `trusted-reference-semantics/semantics/builtins.k:148-148`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))`
157. **rule** `trusted-reference-semantics/semantics/builtins.k:149-151`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====`
158. **rule** `trusted-reference-semantics/semantics/builtins.k:152-155`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)`
159. **rule** `trusted-reference-semantics/semantics/builtins.k:156-157`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2`
160. **syntax** `trusted-reference-semantics/semantics/builtins.k:158-158`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`
161. **rule** `trusted-reference-semantics/semantics/builtins.k:159-159`  
   Flags: equational-rule; attributes: none
   Source: `rule intDigAcc(.IntSeq, ACC:Int)             => ACC`
162. **rule** `trusted-reference-semantics/semantics/builtins.k:160-162`  
   Flags: equational-rule; attributes: none
   Source: `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====`
163. **rule** `trusted-reference-semantics/semantics/builtins.k:163-163`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`
164. **rule** `trusted-reference-semantics/semantics/builtins.k:164-166`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B) // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)`
165. **rule** `trusted-reference-semantics/semantics/builtins.k:167-168`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`
166. **rule** `trusted-reference-semantics/semantics/builtins.k:169-169`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>`
167. **rule** `trusted-reference-semantics/semantics/builtins.k:170-170`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`
168. **rule** `trusted-reference-semantics/semantics/builtins.k:171-172`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`
169. **rule** `trusted-reference-semantics/semantics/builtins.k:173-173`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>`
170. **rule** `trusted-reference-semantics/semantics/builtins.k:174-176`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> // ==== range(stop) / range(start, stop) / range(start, stop, step) =========`
171. **rule** `trusted-reference-semantics/semantics/builtins.k:177-177`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)`
172. **rule** `trusted-reference-semantics/semantics/builtins.k:178-178`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)`
173. **rule** `trusted-reference-semantics/semantics/builtins.k:179-186`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ======== // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's // trusted pass evaluator, now DEFINED in the reference and driven by a // code-level tokenizer. Reduces on concrete strings (krun); a symbolic // argument leaves the call unevaluated for problem-level folds.`
174. **rule** `trusted-reference-semantics/semantics/builtins.k:187-187`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`
175. **syntax** `trusted-reference-semantics/semantics/builtins.k:188-188`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= evalArith(IntSeq) [function]`
176. **rule** `trusted-reference-semantics/semantics/builtins.k:189-190`  
   Flags: equational-rule; attributes: none
   Source: `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`
177. **syntax** `trusted-reference-semantics/semantics/builtins.k:192-192`  
   Flags: none; attributes: none
   Source: `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`
178. **syntax** `trusted-reference-semantics/semantics/builtins.k:194-194`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= evDigit(Int) [function, total]`
179. **rule** `trusted-reference-semantics/semantics/builtins.k:195-195`  
   Flags: equational-rule; attributes: none
   Source: `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`
180. **syntax** `trusted-reference-semantics/semantics/builtins.k:196-196`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= evHead42(IntSeq) [function, total]`
181. **rule** `trusted-reference-semantics/semantics/builtins.k:197-197`  
   Flags: equational-rule; attributes: none
   Source: `rule evHead42(iCons(42, _:IntSeq)) => true`
182. **rule** `trusted-reference-semantics/semantics/builtins.k:198-198`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule evHead42(_:IntSeq)            => false [owise]`
183. **syntax** `trusted-reference-semantics/semantics/builtins.k:199-199`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= evHead47(IntSeq) [function, total]`
184. **rule** `trusted-reference-semantics/semantics/builtins.k:200-200`  
   Flags: equational-rule; attributes: none
   Source: `rule evHead47(iCons(47, _:IntSeq)) => true`
185. **rule** `trusted-reference-semantics/semantics/builtins.k:201-201`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule evHead47(_:IntSeq)            => false [owise]`
186. **syntax** `trusted-reference-semantics/semantics/builtins.k:203-203`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax OpSeq ::= tokOps(IntSeq) [function, total]`
187. **rule** `trusted-reference-semantics/semantics/builtins.k:204-204`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(.IntSeq)                 => .OpSeq`
188. **rule** `trusted-reference-semantics/semantics/builtins.k:205-205`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)`
189. **rule** `trusted-reference-semantics/semantics/builtins.k:206-206`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)`
190. **rule** `trusted-reference-semantics/semantics/builtins.k:207-207`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`
191. **rule** `trusted-reference-semantics/semantics/builtins.k:208-208`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)`
192. **rule** `trusted-reference-semantics/semantics/builtins.k:209-209`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))`
193. **rule** `trusted-reference-semantics/semantics/builtins.k:210-210`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)`
194. **rule** `trusted-reference-semantics/semantics/builtins.k:211-211`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))`
195. **rule** `trusted-reference-semantics/semantics/builtins.k:212-212`  
   Flags: equational-rule; attributes: none
   Source: `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))`
196. **syntax** `trusted-reference-semantics/semantics/builtins.k:214-215`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`
197. **rule** `trusted-reference-semantics/semantics/builtins.k:216-216`  
   Flags: equational-rule; attributes: none
   Source: `rule tokNds(.IntSeq)                => .IntSeq`
198. **rule** `trusted-reference-semantics/semantics/builtins.k:217-217`  
   Flags: equational-rule; attributes: none
   Source: `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)`
199. **rule** `trusted-reference-semantics/semantics/builtins.k:218-218`  
   Flags: equational-rule; attributes: none
   Source: `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`
200. **rule** `trusted-reference-semantics/semantics/builtins.k:219-220`  
   Flags: equational-rule; attributes: none
   Source: `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32`
201. **rule** `trusted-reference-semantics/semantics/builtins.k:221-222`  
   Flags: equational-rule; attributes: none
   Source: `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)`
202. **rule** `trusted-reference-semantics/semantics/builtins.k:223-223`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`
203. **syntax** `trusted-reference-semantics/semantics/builtins.k:225-225`  
   Flags: none; attributes: none
   Source: `syntax EvPair ::= evp(OpSeq, IntSeq)`
204. **syntax** `trusted-reference-semantics/semantics/builtins.k:226-226`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= firstNdE(EvPair) [function, total]`
205. **rule** `trusted-reference-semantics/semantics/builtins.k:227-227`  
   Flags: equational-rule; attributes: none
   Source: `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`
206. **rule** `trusted-reference-semantics/semantics/builtins.k:228-228`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule firstNdE(_:EvPair) => 0 [owise]`
207. **syntax** `trusted-reference-semantics/semantics/builtins.k:230-230`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= applyOpE(String, Int, Int) [function, total]`
208. **rule** `trusted-reference-semantics/semantics/builtins.k:231-231`  
   Flags: equational-rule; attributes: none
   Source: `rule applyOpE("+",  A:Int, B:Int) => A +Int B`
209. **rule** `trusted-reference-semantics/semantics/builtins.k:232-232`  
   Flags: equational-rule; attributes: none
   Source: `rule applyOpE("-",  A:Int, B:Int) => A -Int B`
210. **rule** `trusted-reference-semantics/semantics/builtins.k:233-233`  
   Flags: equational-rule; attributes: none
   Source: `rule applyOpE("*",  A:Int, B:Int) => A *Int B`
211. **rule** `trusted-reference-semantics/semantics/builtins.k:234-234`  
   Flags: equational-rule; attributes: none
   Source: `rule applyOpE("//", A:Int, B:Int) => A divInt B`
212. **rule** `trusted-reference-semantics/semantics/builtins.k:235-235`  
   Flags: equational-rule; attributes: none
   Source: `rule applyOpE("**", A:Int, B:Int) => A ^Int B`
213. **rule** `trusted-reference-semantics/semantics/builtins.k:236-236`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`
214. **syntax** `trusted-reference-semantics/semantics/builtins.k:238-238`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`
215. **rule** `trusted-reference-semantics/semantics/builtins.k:239-239`  
   Flags: equational-rule; attributes: none
   Source: `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`
216. **rule** `trusted-reference-semantics/semantics/builtins.k:240-240`  
   Flags: equational-rule; attributes: none
   Source: `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`
217. **rule** `trusted-reference-semantics/semantics/builtins.k:241-242`  
   Flags: equational-rule; attributes: none
   Source: `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"`
218. **rule** `trusted-reference-semantics/semantics/builtins.k:243-243`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`
219. **syntax** `trusted-reference-semantics/semantics/builtins.k:244-244`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`
220. **rule** `trusted-reference-semantics/semantics/builtins.k:245-245`  
   Flags: equational-rule; attributes: none
   Source: `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`
221. **rule** `trusted-reference-semantics/semantics/builtins.k:246-246`  
   Flags: equational-rule; attributes: none
   Source: `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`
222. **syntax** `trusted-reference-semantics/semantics/builtins.k:247-247`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`
223. **rule** `trusted-reference-semantics/semantics/builtins.k:248-248`  
   Flags: equational-rule; attributes: none
   Source: `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`
224. **syntax** `trusted-reference-semantics/semantics/builtins.k:250-250`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`
225. **rule** `trusted-reference-semantics/semantics/builtins.k:251-251`  
   Flags: equational-rule; attributes: none
   Source: `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`
226. **rule** `trusted-reference-semantics/semantics/builtins.k:252-252`  
   Flags: equational-rule; attributes: none
   Source: `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
227. **rule** `trusted-reference-semantics/semantics/builtins.k:253-253`  
   Flags: equational-rule; attributes: none
   Source: `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`
228. **rule** `trusted-reference-semantics/semantics/builtins.k:254-254`  
   Flags: equational-rule; attributes: none
   Source: `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
229. **syntax** `trusted-reference-semantics/semantics/builtins.k:255-255`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`
230. **rule** `trusted-reference-semantics/semantics/builtins.k:256-256`  
   Flags: equational-rule; attributes: none
   Source: `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`
231. **rule** `trusted-reference-semantics/semantics/builtins.k:257-259`  
   Flags: equational-rule; attributes: none
   Source: `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)`
232. **rule** `trusted-reference-semantics/semantics/builtins.k:260-262`  
   Flags: equational-rule; attributes: none
   Source: `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)`
233. **rule** `trusted-reference-semantics/semantics/builtins.k:263-264`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`
234. **syntax** `trusted-reference-semantics/semantics/builtins.k:265-265`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= inLevelE(String, String) [function, total]`
235. **rule** `trusted-reference-semantics/semantics/builtins.k:266-266`  
   Flags: equational-rule; attributes: none
   Source: `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"`
236. **rule** `trusted-reference-semantics/semantics/builtins.k:267-267`  
   Flags: equational-rule; attributes: none
   Source: `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`
237. **rule** `trusted-reference-semantics/semantics/builtins.k:268-268`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule inLevelE(_:String, _:String) => false [owise]`
238. **syntax** `trusted-reference-semantics/semantics/builtins.k:269-269`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`
239. **rule** `trusted-reference-semantics/semantics/builtins.k:270-270`  
   Flags: equational-rule; attributes: none
   Source: `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`
240. **rule** `trusted-reference-semantics/semantics/builtins.k:271-271`  
   Flags: equational-rule; attributes: none
   Source: `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`
241. **syntax** `trusted-reference-semantics/semantics/builtins.k:272-272`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`
242. **rule** `trusted-reference-semantics/semantics/builtins.k:273-273`  
   Flags: equational-rule; attributes: none
   Source: `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`
243. **rule** `trusted-reference-semantics/semantics/builtins.k:274-278`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ================== // The md5 value itself is a named shared trust (sortVS-style, no concrete // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).`
244. **syntax** `trusted-reference-semantics/semantics/builtins.k:279-279`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= "#md5"`
245. **rule** `trusted-reference-semantics/semantics/builtins.k:280-281`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`
246. **rule** `trusted-reference-semantics/semantics/builtins.k:282-282`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`
247. **syntax** `trusted-reference-semantics/semantics/builtins.k:283-283`  
   Flags: none; attributes: none
   Source: `syntax Val ::= md5Obj(IntSeq)`
248. **rule** `trusted-reference-semantics/semantics/builtins.k:284-284`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`
249. **syntax** `trusted-reference-semantics/semantics/builtins.k:285-290`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(md5hexCodes), no-evaluators
   Source: `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary name that resolves via the builtins frame to // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).`
250. **rule** `trusted-reference-semantics/semantics/builtins.k:291-291`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`
251. **rule** `trusted-reference-semantics/semantics/builtins.k:292-292`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`
252. **syntax** `trusted-reference-semantics/semantics/builtins.k:293-293`  
   Flags: function-declaration; attributes: function, function
   Source: `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`
253. **rule** `trusted-reference-semantics/semantics/builtins.k:294-294`  
   Flags: equational-rule; attributes: none
   Source: `rule isIntV(_:Int)         => true`
254. **rule** `trusted-reference-semantics/semantics/builtins.k:295-295`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule isIntV(_:Val)         => false [owise]`
255. **rule** `trusted-reference-semantics/semantics/builtins.k:296-296`  
   Flags: equational-rule; attributes: none
   Source: `rule isStrV(str(_:IntSeq)) => true`
256. **rule** `trusted-reference-semantics/semantics/builtins.k:297-297`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule isStrV(_:Val)         => false [owise]`
257. **endmodule** `trusted-reference-semantics/semantics/builtins.k:298-298`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/call.k`

258. **module** `trusted-reference-semantics/semantics/call.k:10-10`  
   Flags: none; attributes: none
   Source: `module MPY-CALL`
259. **imports** `trusted-reference-semantics/semantics/call.k:11-11`  
   Flags: none; attributes: none
   Source: `imports MPY-METHODS`
260. **imports** `trusted-reference-semantics/semantics/call.k:12-12`  
   Flags: none; attributes: none
   Source: `imports MPY-BUILTINS`
261. **imports** `trusted-reference-semantics/semantics/call.k:13-15`  
   Flags: none; attributes: none
   Source: `imports MPY-FUNCTIONS // a cooled attribute is a bound method value`
262. **rule** `trusted-reference-semantics/semantics/call.k:16-18`  
   Flags: operational-rule, owise-rule; attributes: owise
   Source: `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)`
263. **syntax** `trusted-reference-semantics/semantics/call.k:19-19`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #callee(Exprs)`
264. **rule** `trusted-reference-semantics/semantics/call.k:20-20`  
   Flags: operational-rule, owise-rule; attributes: owise
   Source: `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`
265. **rule** `trusted-reference-semantics/semantics/call.k:21-23`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> // ==== dispatch on the callee value ========================================`
266. **rule** `trusted-reference-semantics/semantics/call.k:24-24`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`
267. **rule** `trusted-reference-semantics/semantics/call.k:26-26`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`
268. **rule** `trusted-reference-semantics/semantics/call.k:27-27`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>`
269. **rule** `trusted-reference-semantics/semantics/call.k:28-28`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>`
270. **rule** `trusted-reference-semantics/semantics/call.k:29-29`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>`
271. **rule** `trusted-reference-semantics/semantics/call.k:30-30`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>`
272. **rule** `trusted-reference-semantics/semantics/call.k:31-31`  
   Flags: operational-rule, owise-rule; attributes: owise
   Source: `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`
273. **rule** `trusted-reference-semantics/semantics/call.k:32-37`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k> // ==== heap-object arguments/receivers ===================================== // Builtins and type calls READ structure — deref the first two arg positions // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list // methods take the ref itself; every other method receiver is deref'd.`
274. **rule** `trusted-reference-semantics/semantics/call.k:38-41`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
275. **rule** `trusted-reference-semantics/semantics/call.k:42-46`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]`
276. **rule** `trusted-reference-semantics/semantics/call.k:47-50`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
277. **syntax** `trusted-reference-semantics/semantics/call.k:52-52`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isMutMethod(String) [function, total]`
278. **rule** `trusted-reference-semantics/semantics/call.k:53-55`  
   Flags: equational-rule; attributes: none
   Source: `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`
279. **rule** `trusted-reference-semantics/semantics/call.k:56-62`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mutating methods READ their heap-object arguments too (join's list); // mutators keep refs (append of a list into a list-of-lists stays aliased)`
280. **rule** `trusted-reference-semantics/semantics/call.k:63-67`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]`
281. **rule** `trusted-reference-semantics/semantics/call.k:69-79`  
   Flags: operational-rule; attributes: NEWL <- scope(.Map, parent(DEFL))
   Source: `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> // annotated closure: the frame starts with the captured freevar cells, its // parent is the module scope (all enclosing-local reads go through cells), // and the cellvars' fresh cells allocate before params bind (a cellvar param // then writes through its cell in #bindP).`
282. **rule** `trusted-reference-semantics/semantics/call.k:80-85`  
   Flags: operational-rule; attributes: NEWL <- scope(CM [ "$cells" <- cellsMark(CVS)
   Source: `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
283. **syntax** `trusted-reference-semantics/semantics/call.k:87-87`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #allocCells(ParamNames)`
284. **rule** `trusted-reference-semantics/semantics/call.k:88-88`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #allocCells(.ParamNames) => .K ... </k>`
285. **rule** `trusted-reference-semantics/semantics/call.k:89-94`  
   Flags: operational-rule; attributes: CV <- cellRef(N)
   Source: `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`
286. **endmodule** `trusted-reference-semantics/semantics/call.k:95-95`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/comprehension.k`

287. **module** `trusted-reference-semantics/semantics/comprehension.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-COMPREHENSION`
288. **imports** `trusted-reference-semantics/semantics/comprehension.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
289. **imports** `trusted-reference-semantics/semantics/comprehension.k:5-5`  
   Flags: none; attributes: none
   Source: `imports MPY-OPERATORS`
290. **imports** `trusted-reference-semantics/semantics/comprehension.k:6-6`  
   Flags: none; attributes: none
   Source: `imports MPY-LIST`
291. **imports** `trusted-reference-semantics/semantics/comprehension.k:7-7`  
   Flags: none; attributes: none
   Source: `imports MPY-CONTROLS`
292. **imports** `trusted-reference-semantics/semantics/comprehension.k:8-10`  
   Flags: none; attributes: none
   Source: `imports MPY-FUNCTIONS // A comprehension is pure syntactic sugar`
293. **rule** `trusted-reference-semantics/semantics/comprehension.k:11-11`  
   Flags: equational-rule; attributes: none
   Source: `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
294. **rule** `trusted-reference-semantics/semantics/comprehension.k:12-12`  
   Flags: equational-rule; attributes: none
   Source: `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
295. **syntax** `trusted-reference-semantics/semantics/comprehension.k:14-14`  
   Flags: macro-declaration; attributes: macro
   Source: `syntax Stmts ::= compBody(CompFors, Expr) [macro]`
296. **rule** `trusted-reference-semantics/semantics/comprehension.k:15-16`  
   Flags: equational-rule; attributes: none
   Source: `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`
297. **syntax** `trusted-reference-semantics/semantics/comprehension.k:18-18`  
   Flags: macro-declaration; attributes: macro-rec
   Source: `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`
298. **rule** `trusted-reference-semantics/semantics/comprehension.k:19-20`  
   Flags: equational-rule; attributes: none
   Source: `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`
299. **rule** `trusted-reference-semantics/semantics/comprehension.k:21-22`  
   Flags: equational-rule; attributes: none
   Source: `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`
300. **syntax** `trusted-reference-semantics/semantics/comprehension.k:24-24`  
   Flags: macro-declaration; attributes: macro
   Source: `syntax Expr ::= compGuard(Exprs) [macro]`
301. **rule** `trusted-reference-semantics/semantics/comprehension.k:25-25`  
   Flags: equational-rule; attributes: none
   Source: `rule compGuard(.Exprs)             => Bool(true)`
302. **rule** `trusted-reference-semantics/semantics/comprehension.k:26-26`  
   Flags: equational-rule; attributes: none
   Source: `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`
303. **endmodule** `trusted-reference-semantics/semantics/comprehension.k:27-27`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/concrete.k`

304. **module** `trusted-reference-semantics/semantics/concrete.k:8-8`  
   Flags: none; attributes: none
   Source: `module MPY-CONCRETE`
305. **imports** `trusted-reference-semantics/semantics/concrete.k:9-12`  
   Flags: none; attributes: none
   Source: `imports MPY // deep equality for list compares whose elements are heap objects // (list-of-lists): Python == is structural at every depth.`
306. **rule** `trusted-reference-semantics/semantics/concrete.k:13-15`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`
307. **rule** `trusted-reference-semantics/semantics/concrete.k:16-24`  
   Flags: operational-rule, priority-rule, concrete-only-rule; attributes: none
   Source: `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) // ==== keyed sort, concrete leg ============================================ // Computes each key by a REAL call through the uniform #callee machinery // (closures, len, type objects all work), stable-inserts on the key, and // allocates the result. priority(40) beats sort.k's opaque rules, so krun // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.`
308. **syntax** `trusted-reference-semantics/semantics/concrete.k:25-25`  
   Flags: none; attributes: none
   Source: `syntax Val ::= kvP(Val, Val)`
309. **syntax** `trusted-reference-semantics/semantics/concrete.k:26-27`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`
310. **rule** `trusted-reference-semantics/semantics/concrete.k:28-30`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`
311. **rule** `trusted-reference-semantics/semantics/concrete.k:31-33`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`
312. **rule** `trusted-reference-semantics/semantics/concrete.k:34-35`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`
313. **rule** `trusted-reference-semantics/semantics/concrete.k:36-37`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`
314. **rule** `trusted-reference-semantics/semantics/concrete.k:38-40`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)`
315. **syntax** `trusted-reference-semantics/semantics/concrete.k:42-42`  
   Flags: function-declaration; attributes: function
   Source: `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`
316. **rule** `trusted-reference-semantics/semantics/concrete.k:43-43`  
   Flags: equational-rule; attributes: none
   Source: `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`
317. **rule** `trusted-reference-semantics/semantics/concrete.k:44-46`  
   Flags: equational-rule; attributes: none
   Source: `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)`
318. **rule** `trusted-reference-semantics/semantics/concrete.k:47-49`  
   Flags: equational-rule; attributes: none
   Source: `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)`
319. **syntax** `trusted-reference-semantics/semantics/concrete.k:51-51`  
   Flags: function-declaration; attributes: function
   Source: `syntax Bool ::= kLt(Val, Val) [function]`
320. **rule** `trusted-reference-semantics/semantics/concrete.k:52-52`  
   Flags: equational-rule; attributes: none
   Source: `rule kLt(I1:Int, I2:Int)             => I1 <Int I2`
321. **rule** `trusted-reference-semantics/semantics/concrete.k:53-53`  
   Flags: equational-rule; attributes: none
   Source: `rule kLt(F1:Float, F2:Float)         => F1 <Float F2`
322. **rule** `trusted-reference-semantics/semantics/concrete.k:54-54`  
   Flags: equational-rule; attributes: none
   Source: `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
323. **syntax** `trusted-reference-semantics/semantics/concrete.k:56-56`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`
324. **rule** `trusted-reference-semantics/semantics/concrete.k:57-57`  
   Flags: equational-rule; attributes: none
   Source: `rule unpairVS(.ValSeq) => .ValSeq`
325. **rule** `trusted-reference-semantics/semantics/concrete.k:58-58`  
   Flags: equational-rule; attributes: none
   Source: `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`
326. **rule** `trusted-reference-semantics/semantics/concrete.k:59-59`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`
327. **endmodule** `trusted-reference-semantics/semantics/concrete.k:60-60`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/controls.k`

328. **module** `trusted-reference-semantics/semantics/controls.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-CONTROLS`
329. **imports** `trusted-reference-semantics/semantics/controls.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
330. **imports** `trusted-reference-semantics/semantics/controls.k:5-5`  
   Flags: none; attributes: none
   Source: `imports MPY-TUPLE`
331. **imports** `trusted-reference-semantics/semantics/controls.k:6-8`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==`
332. **rule** `trusted-reference-semantics/semantics/controls.k:9-11`  
   Flags: operational-rule; attributes: X <- V
   Source: `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
333. **rule** `trusted-reference-semantics/semantics/controls.k:12-14`  
   Flags: operational-rule; attributes: X
   Source: `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
334. **requires** `trusted-reference-semantics/semantics/controls.k:15-18`  
   Flags: none; attributes: "$cells", X, priority(40)
   Source: `requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
335. **rule** `trusted-reference-semantics/semantics/controls.k:20-26`  
   Flags: operational-rule; attributes: X <- applyBin(OP, {M[X, ..
   Source: `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // 'lst += [..]' where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).`
336. **rule** `trusted-reference-semantics/semantics/controls.k:27-34`  
   Flags: operational-rule, priority-rule; attributes: X, priority(40)
   Source: `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] // ==== import trivia: 'from math import floor, ceil' binds the supported // names as builtins in the current scope; every other import is a no-op`
337. **rule** `trusted-reference-semantics/semantics/controls.k:35-35`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`
338. **rule** `trusted-reference-semantics/semantics/controls.k:36-36`  
   Flags: operational-rule, owise-rule; attributes: owise
   Source: `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`
339. **syntax** `trusted-reference-semantics/semantics/controls.k:37-37`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #bindImports(ParamNames)`
340. **rule** `trusted-reference-semantics/semantics/controls.k:38-38`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #bindImports(.ParamNames) => .K ... </k>`
341. **rule** `trusted-reference-semantics/semantics/controls.k:39-42`  
   Flags: operational-rule; attributes: N <- builtinV(N)
   Source: `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"`
342. **rule** `trusted-reference-semantics/semantics/controls.k:43-47`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") // ==== Expr statement: evaluate for effect, discard the value =============== // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)`
343. **rule** `trusted-reference-semantics/semantics/controls.k:48-50`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Expr(_:Val) => .K ... </k> // ==== If (condition evaluated by strictness) ==============================`
344. **syntax** `trusted-reference-semantics/semantics/controls.k:51-51`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #branch(Bool, Stmts, Stmts)`
345. **rule** `trusted-reference-semantics/semantics/controls.k:52-52`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`
346. **rule** `trusted-reference-semantics/semantics/controls.k:53-53`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>`
347. **rule** `trusted-reference-semantics/semantics/controls.k:54-56`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> // ==== IfExp: ternary T if C else E ========================================`
348. **rule** `trusted-reference-semantics/semantics/controls.k:57-58`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)`
349. **rule** `trusted-reference-semantics/semantics/controls.k:59-64`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) // ==== For: one loop, in-cell continuation, over #iterNext ================= // (the iterable is evaluated once, by strictness; the protocol stays rewrites — // circularities anchor on #loop and narrowing substitutes the structure)`
350. **syntax** `trusted-reference-semantics/semantics/controls.k:65-67`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`
351. **rule** `trusted-reference-semantics/semantics/controls.k:69-69`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`
352. **rule** `trusted-reference-semantics/semantics/controls.k:71-71`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`
353. **rule** `trusted-reference-semantics/semantics/controls.k:72-72`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`
354. **rule** `trusted-reference-semantics/semantics/controls.k:73-76`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> // ==== While ==============================================================`
355. **rule** `trusted-reference-semantics/semantics/controls.k:77-77`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`
356. **rule** `trusted-reference-semantics/semantics/controls.k:78-78`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`
357. **rule** `trusted-reference-semantics/semantics/controls.k:79-80`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)`
358. **rule** `trusted-reference-semantics/semantics/controls.k:81-84`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) // ==== loop control (break / continue) =====================================`
359. **rule** `trusted-reference-semantics/semantics/controls.k:85-85`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`
360. **rule** `trusted-reference-semantics/semantics/controls.k:86-86`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Continue => #cont ... </k>`
361. **rule** `trusted-reference-semantics/semantics/controls.k:87-87`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Break => #brk ... </k>`
362. **rule** `trusted-reference-semantics/semantics/controls.k:88-88`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`
363. **rule** `trusted-reference-semantics/semantics/controls.k:89-89`  
   Flags: operational-rule, owise-rule; attributes: owise
   Source: `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`
364. **rule** `trusted-reference-semantics/semantics/controls.k:90-90`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`
365. **rule** `trusted-reference-semantics/semantics/controls.k:91-94`  
   Flags: operational-rule, priority-rule, owise-rule; attributes: owise
   Source: `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] // ==== heap-object deref at the truthiness/iteration consumers ============== // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)`
366. **rule** `trusted-reference-semantics/semantics/controls.k:95-97`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
367. **rule** `trusted-reference-semantics/semantics/controls.k:98-100`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
368. **rule** `trusted-reference-semantics/semantics/controls.k:101-105`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; // mutating the iterated list inside its own loop is outside the subset)`
369. **rule** `trusted-reference-semantics/semantics/controls.k:106-108`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
370. **endmodule** `trusted-reference-semantics/semantics/controls.k:109-109`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/core.k`

371. **module** `trusted-reference-semantics/semantics/core.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-CORE`
372. **imports** `trusted-reference-semantics/semantics/core.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-SYNTAX`
373. **imports** `trusted-reference-semantics/semantics/core.k:5-5`  
   Flags: none; attributes: none
   Source: `imports INT`
374. **imports** `trusted-reference-semantics/semantics/core.k:6-6`  
   Flags: none; attributes: none
   Source: `imports BOOL`
375. **imports** `trusted-reference-semantics/semantics/core.k:7-7`  
   Flags: none; attributes: none
   Source: `imports STRING`
376. **imports** `trusted-reference-semantics/semantics/core.k:8-8`  
   Flags: none; attributes: none
   Source: `imports MAP`
377. **imports** `trusted-reference-semantics/semantics/core.k:9-9`  
   Flags: none; attributes: none
   Source: `imports LIST`
378. **imports** `trusted-reference-semantics/semantics/core.k:10-12`  
   Flags: none; attributes: none
   Source: `imports K-EQUAL // ==== values, the algebraic lists, and the scope heap =====================`
379. **syntax** `trusted-reference-semantics/semantics/core.k:13-13`  
   Flags: none; attributes: none
   Source: `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`
380. **syntax** `trusted-reference-semantics/semantics/core.k:14-14`  
   Flags: none; attributes: none
   Source: `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`
381. **syntax** `trusted-reference-semantics/semantics/core.k:15-17`  
   Flags: none; attributes: none
   Source: `syntax Str    ::= str(IntSeq) // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)`
382. **syntax** `trusted-reference-semantics/semantics/core.k:18-23`  
   Flags: none; attributes: none
   Source: `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`
383. **syntax** `trusted-reference-semantics/semantics/core.k:25-34`  
   Flags: none; attributes: none
   Source: `syntax Val      ::= Int | Bool | "noneV" | Iterable | ref(Int)          // a heap object: <heap> holds its list(VS) | cellRef(Int)      // a closure cell: <heap> holds cellV(V) | closureVal(ParamNames, Stmts, Int) | typeV(String)     // a type object (int/str), resolved from the builtins frame | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) | boundMethodV(Val, String)   // a cooled Attribute: obj.method`
384. **syntax** `trusted-reference-semantics/semantics/core.k:36-36`  
   Flags: none; attributes: none
   Source: `syntax Parent   ::= "root" | parent(Int)`
385. **syntax** `trusted-reference-semantics/semantics/core.k:37-37`  
   Flags: none; attributes: none
   Source: `syntax Scope    ::= scope(Map, Parent)`
386. **syntax** `trusted-reference-semantics/semantics/core.k:38-38`  
   Flags: none; attributes: none
   Source: `syntax KResult  ::= Val`
387. **syntax** `trusted-reference-semantics/semantics/core.k:39-39`  
   Flags: none; attributes: none
   Source: `syntax Expr     ::= Val   // cooling puts results back into expression holes`
388. **syntax** `trusted-reference-semantics/semantics/core.k:40-40`  
   Flags: none; attributes: none
   Source: `syntax Vals     ::= List{Val, ","}`
389. **syntax** `trusted-reference-semantics/semantics/core.k:41-41`  
   Flags: none; attributes: none
   Source: `syntax Exc      ::= "NoExc" | "AssertionError"`
390. **syntax** `trusted-reference-semantics/semantics/core.k:42-48`  
   Flags: none; attributes: none
   Source: `syntax RetState ::= "noRet" | retV(Val) // ==== configuration ======================================================= // The builtins namespace is a real scope at reserved location -1 (the bottom of every // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0) // has it as parent, so an unbound name resolves there last — exactly LEGB. 'int'/'str' // resolve to their type objects; any local/global binding shadows them via normal lookup.`
391. **configuration** `trusted-reference-semantics/semantics/core.k:49-67`  
   Flags: none; attributes: N <- _
   Source: `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     |-> scope(.Map, parent(-1)) -1    |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code> // ==== heap allocation (constructed lists become objects) ================== // Cons-form emission with a freshness guard (the heap-list-probe discipline: // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is // monotonic — it does NOT wind back at #pop: returned lists escape by ref. // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed); // only CONSTRUCTORS in program syntax allocate.`
392. **syntax** `trusted-reference-semantics/semantics/core.k:68-68`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isRefV(Val) [function, total]`
393. **rule** `trusted-reference-semantics/semantics/core.k:69-69`  
   Flags: equational-rule; attributes: none
   Source: `rule isRefV(ref(_:Int)) => true`
394. **rule** `trusted-reference-semantics/semantics/core.k:70-74`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule isRefV(_:Val)      => false [owise] // closure cells (Python-faithful capture): the heap holds cellV(V); a // cellRef surfacing as the k-redex reads through (lookup is the only use — // cellRefs never escape to user-visible values)`
395. **syntax** `trusted-reference-semantics/semantics/core.k:75-75`  
   Flags: none; attributes: none
   Source: `syntax HeapVal ::= cellV(Val)`
396. **syntax** `trusted-reference-semantics/semantics/core.k:76-76`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isCellRef(Val) [function, total]`
397. **rule** `trusted-reference-semantics/semantics/core.k:77-77`  
   Flags: equational-rule; attributes: none
   Source: `rule isCellRef(cellRef(_:Int)) => true`
398. **rule** `trusted-reference-semantics/semantics/core.k:78-84`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule isCellRef(_:Val)          => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in plain frames — an unguarded rule lets the // prover narrow abstract k-top values into cellRef junk (probed on // 26-remove-duplicates). Cross-frame reads (a comprehension closure // reading the enclosing function's cellvar) deref inside #look instead.`
399. **rule** `trusted-reference-semantics/semantics/core.k:85-88`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap>`
400. **requires** `trusted-reference-semantics/semantics/core.k:89-94`  
   Flags: none; attributes: priority(40)
   Source: `requires "$cells" in_keys(M) [priority(40)] // write through a cell (Assign / #bindP / #bindTgt dispatch here on // cell-bound names) // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)`
401. **syntax** `trusted-reference-semantics/semantics/core.k:95-95`  
   Flags: none; attributes: none
   Source: `syntax Val ::= kwV(String, Val)`
402. **syntax** `trusted-reference-semantics/semantics/core.k:96-96`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #kwTag(String)`
403. **rule** `trusted-reference-semantics/semantics/core.k:97-97`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`
404. **rule** `trusted-reference-semantics/semantics/core.k:98-99`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)`
405. **syntax** `trusted-reference-semantics/semantics/core.k:100-100`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isKwV(Val) [function, total]`
406. **rule** `trusted-reference-semantics/semantics/core.k:101-101`  
   Flags: equational-rule; attributes: none
   Source: `rule isKwV(kwV(_:String, _:Val)) => true`
407. **rule** `trusted-reference-semantics/semantics/core.k:102-105`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule isKwV(_:Val)                => false [owise] // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch // decides by pnMember even over an abstract frame rest (no prover branching)`
408. **syntax** `trusted-reference-semantics/semantics/core.k:106-106`  
   Flags: none; attributes: none
   Source: `syntax Val ::= cellsMark(ParamNames)`
409. **syntax** `trusted-reference-semantics/semantics/core.k:107-107`  
   Flags: function-declaration; attributes: function
   Source: `syntax ParamNames ::= cellsOf(Val) [function]`
410. **rule** `trusted-reference-semantics/semantics/core.k:108-108`  
   Flags: equational-rule; attributes: none
   Source: `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`
411. **syntax** `trusted-reference-semantics/semantics/core.k:109-109`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= pnMember(String, ParamNames) [function, total]`
412. **rule** `trusted-reference-semantics/semantics/core.k:110-110`  
   Flags: equational-rule; attributes: none
   Source: `rule pnMember(_:String, .ParamNames) => false`
413. **rule** `trusted-reference-semantics/semantics/core.k:111-111`  
   Flags: equational-rule; attributes: none
   Source: `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`
414. **syntax** `trusted-reference-semantics/semantics/core.k:113-113`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #cellW(Val, Val)`
415. **rule** `trusted-reference-semantics/semantics/core.k:114-115`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`
416. **syntax** `trusted-reference-semantics/semantics/core.k:117-117`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #alloc(Val)`
417. **rule** `trusted-reference-semantics/semantics/core.k:118-123`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) // ==== module load + statement sequencing ==================================`
418. **syntax** `trusted-reference-semantics/semantics/core.k:124-124`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #loadAll(Module)`
419. **rule** `trusted-reference-semantics/semantics/core.k:125-125`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`
420. **rule** `trusted-reference-semantics/semantics/core.k:126-126`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`
421. **rule** `trusted-reference-semantics/semantics/core.k:127-129`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> .Stmts => .K ... </k> // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====`
422. **syntax** `trusted-reference-semantics/semantics/core.k:130-130`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #look(String, Int)`
423. **rule** `trusted-reference-semantics/semantics/core.k:131-131`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`
424. **rule** `trusted-reference-semantics/semantics/core.k:132-144`  
   Flags: operational-rule, concrete-only-rule; attributes: X
   Source: `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (higher priority beats the plain return above on concrete cell // bindings; abstract claim values take the plain rule unchanged) — this // covers cross-frame cell reads (a comprehension closure reading the // enclosing function's cellvar) without a narrowing-prone k-top redex // guarded on the FOUND frame's DECLARED cellvars (pnMember over the // cellsMark): decidable for every concrete frame pin — plain frames and // non-cell names prune outright, so an abstract looked-up value never // drags a narrowing cellV heap match along (probed on 5-intersperse and // Q4's abstract 'numbers' in the annotated frame)`
425. **rule** `trusted-reference-semantics/semantics/core.k:145-151`  
   Flags: operational-rule, priority-rule; attributes: "$cells", X, priority(40)
   Source: `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]`
426. **rule** `trusted-reference-semantics/semantics/core.k:152-156`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) // the ONE predefined builtins scope (the -1 frame; claims write '-1 |-> builtinsScope')`
427. **syntax** `trusted-reference-semantics/semantics/core.k:157-157`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Scope ::= "builtinsScope" [function, total]`
428. **rule** `trusted-reference-semantics/semantics/core.k:158-184`  
   Flags: equational-rule; attributes: "len"    <- builtinV("len"), "set"    <- builtinV("set"), "sum"    <- builtinV("sum"), "abs"    <- builtinV("abs"), "min"    <- builtinV("min"), "max"    <- builtinV("max"), "ord"    <- builtinV("ord"), "chr"    <- builtinV("chr"), "range"  <- builtinV("range"), "all"    <- builtinV("all"), "any"    <- builtinV("any"), "zip"    <- builtinV("zip"), "isinstance" <- builtinV("isinstance"), "sorted" <- builtinV("sorted"), "list"   <- builtinV("list"), "round"  <- builtinV("round"), "bin"    <- builtinV("bin"), "enumerate" <- builtinV("enumerate"), "map"    <- builtinV("map"), "eval"   <- builtinV("eval"), "int"    <- typeV("int"), "str"    <- typeV("str"), "float"  <- typeV("float")
   Source: `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root) // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination == // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)`
429. **syntax** `trusted-reference-semantics/semantics/core.k:185-185`  
   Flags: none; attributes: none
   Source: `syntax ApplyK ::= toCall(Val)`
430. **syntax** `trusted-reference-semantics/semantics/core.k:186-188`  
   Flags: none; attributes: none
   Source: `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`
431. **rule** `trusted-reference-semantics/semantics/core.k:189-189`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`
432. **rule** `trusted-reference-semantics/semantics/core.k:190-190`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`
433. **rule** `trusted-reference-semantics/semantics/core.k:191-193`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> // ==== Int / Bool / None literals ==========================================`
434. **rule** `trusted-reference-semantics/semantics/core.k:194-194`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Int(I:Int)   => I ... </k>`
435. **rule** `trusted-reference-semantics/semantics/core.k:195-195`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Bool(B:Bool) => B ... </k>`
436. **rule** `trusted-reference-semantics/semantics/core.k:196-198`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> NoneVal      => noneV ... </k> // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================`
437. **syntax** `trusted-reference-semantics/semantics/core.k:199-199`  
   Flags: function-declaration; attributes: function
   Source: `syntax Bool ::= truthy(Val) [function]`
438. **rule** `trusted-reference-semantics/semantics/core.k:200-200`  
   Flags: equational-rule; attributes: none
   Source: `rule truthy(B:Bool)          => B`
439. **rule** `trusted-reference-semantics/semantics/core.k:201-201`  
   Flags: equational-rule; attributes: none
   Source: `rule truthy(noneV)           => false`
440. **rule** `trusted-reference-semantics/semantics/core.k:202-202`  
   Flags: equational-rule; attributes: none
   Source: `rule truthy(I:Int)           => I =/=Int 0`
441. **rule** `trusted-reference-semantics/semantics/core.k:203-203`  
   Flags: equational-rule; attributes: none
   Source: `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)`
442. **rule** `trusted-reference-semantics/semantics/core.k:204-204`  
   Flags: equational-rule; attributes: none
   Source: `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)`
443. **rule** `trusted-reference-semantics/semantics/core.k:205-207`  
   Flags: equational-rule; attributes: none
   Source: `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) // ==== extensible operator dispatch (cases added by the construct modules) ==`
444. **syntax** `trusted-reference-semantics/semantics/core.k:208-208`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val  ::= applyUn(String, Val) [function]`
445. **syntax** `trusted-reference-semantics/semantics/core.k:209-209`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val  ::= applyBin(String, Val, Val) [function]`
446. **syntax** `trusted-reference-semantics/semantics/core.k:210-212`  
   Flags: function-declaration; attributes: function
   Source: `syntax Bool ::= applyCmp(String, Val, Val) [function] // ==== shared list helpers =================================================`
447. **syntax** `trusted-reference-semantics/semantics/core.k:213-213`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Vals ::= appendVal(Vals, Val) [function, total]`
448. **rule** `trusted-reference-semantics/semantics/core.k:214-214`  
   Flags: equational-rule; attributes: none
   Source: `rule appendVal(.Vals, V:Val)              => V , .Vals`
449. **rule** `trusted-reference-semantics/semantics/core.k:215-215`  
   Flags: equational-rule; attributes: none
   Source: `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)`
450. **syntax** `trusted-reference-semantics/semantics/core.k:217-217`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`
451. **rule** `trusted-reference-semantics/semantics/core.k:218-218`  
   Flags: equational-rule; attributes: none
   Source: `rule vals2valSeq(.Vals)            => .ValSeq`
452. **rule** `trusted-reference-semantics/semantics/core.k:219-222`  
   Flags: equational-rule; attributes: none
   Source: `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) // ==== shared sequence length (len / summaries across many modules) ======== // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)`
453. **syntax** `trusted-reference-semantics/semantics/core.k:223-223`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= vsLen(ValSeq) [function, total]`
454. **rule** `trusted-reference-semantics/semantics/core.k:224-224`  
   Flags: equational-rule; attributes: none
   Source: `rule vsLen(.ValSeq)                => 0`
455. **rule** `trusted-reference-semantics/semantics/core.k:225-225`  
   Flags: equational-rule; attributes: none
   Source: `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`
456. **syntax** `trusted-reference-semantics/semantics/core.k:227-227`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= isLen(IntSeq) [function, total]`
457. **rule** `trusted-reference-semantics/semantics/core.k:228-228`  
   Flags: equational-rule; attributes: none
   Source: `rule isLen(.IntSeq)                => 0`
458. **rule** `trusted-reference-semantics/semantics/core.k:229-232`  
   Flags: equational-rule; attributes: none
   Source: `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)`
459. **syntax** `trusted-reference-semantics/semantics/core.k:233-233`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`
460. **rule** `trusted-reference-semantics/semantics/core.k:234-234`  
   Flags: equational-rule; attributes: none
   Source: `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq`
461. **rule** `trusted-reference-semantics/semantics/core.k:235-235`  
   Flags: equational-rule; attributes: none
   Source: `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)`
462. **rule** `trusted-reference-semantics/semantics/core.k:236-237`  
   Flags: equational-rule; attributes: none
   Source: `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0`
463. **rule** `trusted-reference-semantics/semantics/core.k:238-239`  
   Flags: equational-rule; attributes: none
   Source: `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0`
464. **endmodule** `trusted-reference-semantics/semantics/core.k:240-240`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/dict.k`

465. **module** `trusted-reference-semantics/semantics/dict.k:13-13`  
   Flags: none; attributes: none
   Source: `module MPY-DICT`
466. **imports** `trusted-reference-semantics/semantics/dict.k:14-14`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
467. **imports** `trusted-reference-semantics/semantics/dict.k:15-15`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER`
468. **imports** `trusted-reference-semantics/semantics/dict.k:16-16`  
   Flags: none; attributes: none
   Source: `imports MPY-METHODS`
469. **imports** `trusted-reference-semantics/semantics/dict.k:17-19`  
   Flags: none; attributes: none
   Source: `imports MPY-LIST // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).`
470. **syntax** `trusted-reference-semantics/semantics/dict.k:20-22`  
   Flags: none; attributes: none
   Source: `syntax Val ::= dictV(ValSeq, ValSeq) // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.`
471. **syntax** `trusted-reference-semantics/semantics/dict.k:23-25`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`
472. **rule** `trusted-reference-semantics/semantics/dict.k:26-26`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`
473. **rule** `trusted-reference-semantics/semantics/dict.k:27-27`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`
474. **rule** `trusted-reference-semantics/semantics/dict.k:28-29`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`
475. **rule** `trusted-reference-semantics/semantics/dict.k:30-31`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`
476. **rule** `trusted-reference-semantics/semantics/dict.k:32-36`  
   Flags: operational-rule, concrete-only-rule; attributes: total
   Source: `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.`
477. **syntax** `trusted-reference-semantics/semantics/dict.k:37-37`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`
478. **rule** `trusted-reference-semantics/semantics/dict.k:38-38`  
   Flags: equational-rule; attributes: none
   Source: `rule dHasKey(.ValSeq, _:Val)                => false`
479. **rule** `trusted-reference-semantics/semantics/dict.k:39-39`  
   Flags: equational-rule; attributes: none
   Source: `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K`
480. **rule** `trusted-reference-semantics/semantics/dict.k:40-42`  
   Flags: equational-rule; attributes: none
   Source: `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) // dPutK: KS unchanged if K already present, else append K (keep-first-position).`
481. **syntax** `trusted-reference-semantics/semantics/dict.k:43-43`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`
482. **rule** `trusted-reference-semantics/semantics/dict.k:44-44`  
   Flags: equational-rule; attributes: none
   Source: `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)`
483. **rule** `trusted-reference-semantics/semantics/dict.k:45-48`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).`
484. **syntax** `trusted-reference-semantics/semantics/dict.k:49-49`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`
485. **rule** `trusted-reference-semantics/semantics/dict.k:50-51`  
   Flags: equational-rule; attributes: none
   Source: `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K`
486. **rule** `trusted-reference-semantics/semantics/dict.k:52-53`  
   Flags: equational-rule; attributes: none
   Source: `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)`
487. **rule** `trusted-reference-semantics/semantics/dict.k:54-57`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] // ==== dict methods ======================================================== // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).`
488. **rule** `trusted-reference-semantics/semantics/dict.k:58-62`  
   Flags: operational-rule, priority-rule; attributes: priority(40), k
   Source: `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==`
489. **rule** `trusted-reference-semantics/semantics/dict.k:63-63`  
   Flags: equational-rule; attributes: none
   Source: `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`
490. **syntax** `trusted-reference-semantics/semantics/dict.k:64-64`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val ::= applyIndexD(Val, Val) [function]`
491. **rule** `trusted-reference-semantics/semantics/dict.k:65-69`  
   Flags: operational-rule, priority-rule; attributes: priority(45), k
   Source: `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] // ==== dict subscript-assign: d[k] = v (insert/update in place) ============= // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.`
492. **syntax** `trusted-reference-semantics/semantics/dict.k:70-70`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val ::= dictSet(Val, Val, Val) [function]`
493. **rule** `trusted-reference-semantics/semantics/dict.k:71-75`  
   Flags: equational-rule; attributes: none
   Source: `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope // value: a bare dict updates in the scope (dicts stay values); a ref (a heap // list — or a heap dict later) writes the heap in place.`
494. **syntax** `trusted-reference-semantics/semantics/dict.k:76-76`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #dsetK(String, Val)`
495. **rule** `trusted-reference-semantics/semantics/dict.k:77-77`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`
496. **rule** `trusted-reference-semantics/semantics/dict.k:78-81`  
   Flags: operational-rule; attributes: X <- dictSet({M[X, X
   Source: `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`
497. **rule** `trusted-reference-semantics/semantics/dict.k:82-85`  
   Flags: operational-rule; attributes: X, X
   Source: `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)`
498. **syntax** `trusted-reference-semantics/semantics/dict.k:86-86`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #dsetV(Val, Val, Val)`
499. **rule** `trusted-reference-semantics/semantics/dict.k:87-89`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is not imported here)`
500. **syntax** `trusted-reference-semantics/semantics/dict.k:90-90`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= normIdxD(Int, Int) [function, total]`
501. **rule** `trusted-reference-semantics/semantics/dict.k:91-91`  
   Flags: equational-rule; attributes: none
   Source: `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`
502. **rule** `trusted-reference-semantics/semantics/dict.k:92-94`  
   Flags: equational-rule; attributes: none
   Source: `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0 // ==== dict == (order-insensitive: same size + same key->value pairs) =======`
503. **rule** `trusted-reference-semantics/semantics/dict.k:95-96`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`
504. **syntax** `trusted-reference-semantics/semantics/dict.k:97-97`  
   Flags: function-declaration; attributes: function
   Source: `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`
505. **rule** `trusted-reference-semantics/semantics/dict.k:98-98`  
   Flags: equational-rule; attributes: none
   Source: `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`
506. **rule** `trusted-reference-semantics/semantics/dict.k:99-100`  
   Flags: equational-rule; attributes: none
   Source: `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`
507. **syntax** `trusted-reference-semantics/semantics/dict.k:101-101`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`
508. **rule** `trusted-reference-semantics/semantics/dict.k:102-102`  
   Flags: equational-rule; attributes: none
   Source: `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K`
509. **rule** `trusted-reference-semantics/semantics/dict.k:103-103`  
   Flags: equational-rule; attributes: none
   Source: `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`
510. **endmodule** `trusted-reference-semantics/semantics/dict.k:104-104`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/float.k`

511. **module** `trusted-reference-semantics/semantics/float.k:14-14`  
   Flags: none; attributes: none
   Source: `module MPY-FLOAT`
512. **imports** `trusted-reference-semantics/semantics/float.k:15-15`  
   Flags: none; attributes: none
   Source: `imports MPY-OPERATORS`
513. **imports** `trusted-reference-semantics/semantics/float.k:16-16`  
   Flags: none; attributes: none
   Source: `imports MPY-BUILTINS`
514. **imports** `trusted-reference-semantics/semantics/float.k:17-19`  
   Flags: none; attributes: none
   Source: `imports FLOAT // Float is a value; the float literal evaluates to the K Float.`
515. **syntax** `trusted-reference-semantics/semantics/float.k:20-20`  
   Flags: none; attributes: none
   Source: `syntax Val ::= Float`
516. **rule** `trusted-reference-semantics/semantics/float.k:21-23`  
   Flags: operational-rule, concrete-only-rule; attributes: none
   Source: `rule <k> Float(F:Float) => F ... </k> // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.`
517. **syntax** `trusted-reference-semantics/semantics/float.k:24-24`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(intFloatDiv), no-evaluators
   Source: `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
518. **rule** `trusted-reference-semantics/semantics/float.k:25-25`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`
519. **rule** `trusted-reference-semantics/semantics/float.k:27-29`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.`
520. **syntax** `trusted-reference-semantics/semantics/float.k:30-30`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(divII), no-evaluators
   Source: `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
521. **rule** `trusted-reference-semantics/semantics/float.k:31-31`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`
522. **rule** `trusted-reference-semantics/semantics/float.k:32-36`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) // float % float (e.g. 'number % 1.0' = the fractional part). OPAQUE for kprove, concrete for // krun. Python's float '%' is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).`
523. **syntax** `trusted-reference-semantics/semantics/float.k:37-37`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(floatMod), no-evaluators
   Source: `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
524. **rule** `trusted-reference-semantics/semantics/float.k:38-38`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`
525. **rule** `trusted-reference-semantics/semantics/float.k:39-42`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) // float equality — for concrete krun asserts (e.g. 'area == 7.5'); the FLOAT.eq hook is fine on // concrete floats. kprove proofs return floats structurally and do not compare them.`
526. **rule** `trusted-reference-semantics/semantics/float.k:43-43`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`
527. **rule** `trusted-reference-semantics/semantics/float.k:44-49`  
   Flags: equational-rule, concrete-only-rule; attributes: no-evaluators, concrete
   Source: `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) // float '<' and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade), // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise // 'abs(a-b) < t' proximity test.)`
528. **syntax** `trusted-reference-semantics/semantics/float.k:50-50`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(floatLt), no-evaluators
   Source: `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
529. **rule** `trusted-reference-semantics/semantics/float.k:51-51`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`
530. **rule** `trusted-reference-semantics/semantics/float.k:52-52`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`
531. **syntax** `trusted-reference-semantics/semantics/float.k:54-54`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(absF), no-evaluators
   Source: `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
532. **rule** `trusted-reference-semantics/semantics/float.k:55-55`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule absF(F:Float) => absFloat(F) [concrete]`
533. **rule** `trusted-reference-semantics/semantics/float.k:56-60`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("abs", F:Float, .Vals) => absF(F) // ==== math.ceil =========================================================== // 'import X' is a no-op (we intercept the specific math functions syntactically; 'math' itself is // never bound as a value).`
534. **rule** `trusted-reference-semantics/semantics/float.k:61-64`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Import(_:String) => .K ... </k> // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE 'math' is looked up (higher // priority than the generic Attribute/method dispatch in call.k).`
535. **syntax** `trusted-reference-semantics/semantics/float.k:65-65`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= "#mathCeil"`
536. **rule** `trusted-reference-semantics/semantics/float.k:66-66`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`
537. **rule** `trusted-reference-semantics/semantics/float.k:67-69`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> // math.floor(x) — same interception shape as math.ceil`
538. **syntax** `trusted-reference-semantics/semantics/float.k:70-70`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= "#mathFloor"`
539. **rule** `trusted-reference-semantics/semantics/float.k:71-71`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`
540. **rule** `trusted-reference-semantics/semantics/float.k:72-72`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`
541. **syntax** `trusted-reference-semantics/semantics/float.k:73-73`  
   Flags: function-declaration, total-declaration, named-symbol; attributes: function, total, symbol(floorFI)
   Source: `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
542. **rule** `trusted-reference-semantics/semantics/float.k:74-74`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule floorFI(I:Int)   => I                        [concrete]`
543. **rule** `trusted-reference-semantics/semantics/float.k:75-77`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] // bare floor/ceil (bound by 'from math import floor, ceil')`
544. **rule** `trusted-reference-semantics/semantics/float.k:78-78`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`
545. **rule** `trusted-reference-semantics/semantics/float.k:79-81`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V) // math.pow(x, y) — a two-arg interception onto powF (ints promote)`
546. **syntax** `trusted-reference-semantics/semantics/float.k:82-82`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`
547. **rule** `trusted-reference-semantics/semantics/float.k:83-83`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`
548. **rule** `trusted-reference-semantics/semantics/float.k:84-84`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`
549. **rule** `trusted-reference-semantics/semantics/float.k:85-85`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`
550. **syntax** `trusted-reference-semantics/semantics/float.k:86-86`  
   Flags: function-declaration, total-declaration, named-symbol; attributes: function, total, symbol(toF)
   Source: `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
551. **rule** `trusted-reference-semantics/semantics/float.k:87-87`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule toF(F:Float) => F        [concrete]`
552. **rule** `trusted-reference-semantics/semantics/float.k:88-92`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete, concrete
   Source: `rule toF(I:Int)   => intToF(I) [concrete] // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm). // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).`
553. **syntax** `trusted-reference-semantics/semantics/float.k:93-93`  
   Flags: function-declaration, total-declaration, named-symbol; attributes: function, total, symbol(ceilF)
   Source: `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
554. **rule** `trusted-reference-semantics/semantics/float.k:94-94`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule ceilF(I:Int)   => I                       [concrete]`
555. **rule** `trusted-reference-semantics/semantics/float.k:95-98`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun; // proofs use symbolic elements, never a float literal.`
556. **rule** `trusted-reference-semantics/semantics/float.k:99-102`  
   Flags: equational-rule, concrete-only-rule; attributes: no-evaluators
   Source: `rule applyUn("-", F:Float) => 0.0 -Float F // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.`
557. **syntax** `trusted-reference-semantics/semantics/float.k:103-103`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(subF), no-evaluators
   Source: `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
558. **rule** `trusted-reference-semantics/semantics/float.k:104-104`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`
559. **rule** `trusted-reference-semantics/semantics/float.k:105-105`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`
560. **syntax** `trusted-reference-semantics/semantics/float.k:107-107`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(divF), no-evaluators
   Source: `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
561. **rule** `trusted-reference-semantics/semantics/float.k:108-108`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`
562. **rule** `trusted-reference-semantics/semantics/float.k:109-109`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`
563. **syntax** `trusted-reference-semantics/semantics/float.k:111-111`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(addF), no-evaluators
   Source: `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
564. **rule** `trusted-reference-semantics/semantics/float.k:112-112`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`
565. **rule** `trusted-reference-semantics/semantics/float.k:113-113`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`
566. **syntax** `trusted-reference-semantics/semantics/float.k:115-115`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(mulF), no-evaluators
   Source: `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
567. **rule** `trusted-reference-semantics/semantics/float.k:116-116`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`
568. **rule** `trusted-reference-semantics/semantics/float.k:117-117`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`
569. **syntax** `trusted-reference-semantics/semantics/float.k:119-119`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(powF), no-evaluators
   Source: `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
570. **rule** `trusted-reference-semantics/semantics/float.k:120-120`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`
571. **rule** `trusted-reference-semantics/semantics/float.k:121-124`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) // ---- the remaining comparisons (gtF promoted from find_zero — its summaries //      case-split on the atom; >= / <= derive from the two opaque compares) ----`
572. **syntax** `trusted-reference-semantics/semantics/float.k:125-125`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(gtF), no-evaluators
   Source: `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
573. **rule** `trusted-reference-semantics/semantics/float.k:126-126`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`
574. **rule** `trusted-reference-semantics/semantics/float.k:127-127`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)`
575. **rule** `trusted-reference-semantics/semantics/float.k:128-128`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`
576. **rule** `trusted-reference-semantics/semantics/float.k:129-131`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----`
577. **rule** `trusted-reference-semantics/semantics/float.k:132-132`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`
578. **rule** `trusted-reference-semantics/semantics/float.k:133-133`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`
579. **rule** `trusted-reference-semantics/semantics/float.k:134-134`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)`
580. **rule** `trusted-reference-semantics/semantics/float.k:135-135`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))`
581. **rule** `trusted-reference-semantics/semantics/float.k:136-136`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)`
582. **rule** `trusted-reference-semantics/semantics/float.k:137-137`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))`
583. **rule** `trusted-reference-semantics/semantics/float.k:138-138`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)`
584. **rule** `trusted-reference-semantics/semantics/float.k:139-141`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I)) // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----`
585. **syntax** `trusted-reference-semantics/semantics/float.k:142-142`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(eqF), no-evaluators
   Source: `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
586. **rule** `trusted-reference-semantics/semantics/float.k:143-143`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`
587. **rule** `trusted-reference-semantics/semantics/float.k:144-144`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`
588. **rule** `trusted-reference-semantics/semantics/float.k:145-145`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`
589. **rule** `trusted-reference-semantics/semantics/float.k:146-146`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`
590. **rule** `trusted-reference-semantics/semantics/float.k:147-147`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`
591. **rule** `trusted-reference-semantics/semantics/float.k:148-148`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)`
592. **rule** `trusted-reference-semantics/semantics/float.k:149-149`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))`
593. **rule** `trusted-reference-semantics/semantics/float.k:150-150`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)`
594. **rule** `trusted-reference-semantics/semantics/float.k:151-153`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I)) // ---- x == None (promoted from 137; 'is' cases live in operators.k) ----`
595. **rule** `trusted-reference-semantics/semantics/float.k:154-154`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", V:Val, noneV) => V ==K noneV`
596. **rule** `trusted-reference-semantics/semantics/float.k:155-159`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) // ---- float(str): decimal parse (promoted from 137's defined chain) ---- // digits '.' digits, optional leading '-'; concrete evaluation only (the // symbolic side stays an opaque decStrToF term a proof case-splits on).`
597. **syntax** `trusted-reference-semantics/semantics/float.k:160-160`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(decStrToF), no-evaluators
   Source: `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
598. **rule** `trusted-reference-semantics/semantics/float.k:161-161`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`
599. **rule** `trusted-reference-semantics/semantics/float.k:162-164`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`
600. **syntax** `trusted-reference-semantics/semantics/float.k:165-165`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= headIS(IntSeq) [function]`
601. **rule** `trusted-reference-semantics/semantics/float.k:166-166`  
   Flags: equational-rule; attributes: none
   Source: `rule headIS(iCons(C:Int, _:IntSeq)) => C`
602. **syntax** `trusted-reference-semantics/semantics/float.k:167-167`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`
603. **rule** `trusted-reference-semantics/semantics/float.k:168-168`  
   Flags: equational-rule; attributes: none
   Source: `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`
604. **rule** `trusted-reference-semantics/semantics/float.k:169-169`  
   Flags: equational-rule; attributes: none
   Source: `rule intPartAcc(.IntSeq, A:Int) => A`
605. **rule** `trusted-reference-semantics/semantics/float.k:170-170`  
   Flags: equational-rule; attributes: none
   Source: `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`
606. **rule** `trusted-reference-semantics/semantics/float.k:171-172`  
   Flags: equational-rule; attributes: none
   Source: `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46`
607. **syntax** `trusted-reference-semantics/semantics/float.k:173-173`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`
608. **rule** `trusted-reference-semantics/semantics/float.k:174-174`  
   Flags: equational-rule; attributes: none
   Source: `rule fracPart(.IntSeq) => 0`
609. **rule** `trusted-reference-semantics/semantics/float.k:175-175`  
   Flags: equational-rule; attributes: none
   Source: `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`
610. **rule** `trusted-reference-semantics/semantics/float.k:176-176`  
   Flags: equational-rule; attributes: none
   Source: `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`
611. **rule** `trusted-reference-semantics/semantics/float.k:177-177`  
   Flags: equational-rule; attributes: none
   Source: `rule fracAcc(.IntSeq, A:Int) => A`
612. **rule** `trusted-reference-semantics/semantics/float.k:178-178`  
   Flags: equational-rule; attributes: none
   Source: `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`
613. **syntax** `trusted-reference-semantics/semantics/float.k:179-179`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`
614. **rule** `trusted-reference-semantics/semantics/float.k:180-180`  
   Flags: equational-rule; attributes: none
   Source: `rule fracScale(.IntSeq) => 1`
615. **rule** `trusted-reference-semantics/semantics/float.k:181-181`  
   Flags: equational-rule; attributes: none
   Source: `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`
616. **rule** `trusted-reference-semantics/semantics/float.k:182-182`  
   Flags: equational-rule; attributes: none
   Source: `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`
617. **rule** `trusted-reference-semantics/semantics/float.k:183-183`  
   Flags: equational-rule; attributes: none
   Source: `rule fscAcc(.IntSeq, A:Int) => A`
618. **rule** `trusted-reference-semantics/semantics/float.k:184-184`  
   Flags: equational-rule; attributes: none
   Source: `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`
619. **rule** `trusted-reference-semantics/semantics/float.k:185-185`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`
620. **rule** `trusted-reference-semantics/semantics/float.k:186-186`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)`
621. **rule** `trusted-reference-semantics/semantics/float.k:187-189`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("float", F:Float, .Vals)        => F // ---- float / int division (promoted from mean_absolute_deviation) ----`
622. **syntax** `trusted-reference-semantics/semantics/float.k:190-190`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(divFloatIntV), no-evaluators
   Source: `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
623. **rule** `trusted-reference-semantics/semantics/float.k:191-191`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`
624. **rule** `trusted-reference-semantics/semantics/float.k:192-194`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) // ---- int -> float promotion for the remaining mixed arithmetic/compares ----`
625. **syntax** `trusted-reference-semantics/semantics/float.k:195-195`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(intToF), no-evaluators
   Source: `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
626. **rule** `trusted-reference-semantics/semantics/float.k:196-196`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`
627. **rule** `trusted-reference-semantics/semantics/float.k:197-197`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
628. **rule** `trusted-reference-semantics/semantics/float.k:198-198`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
629. **rule** `trusted-reference-semantics/semantics/float.k:199-199`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
630. **rule** `trusted-reference-semantics/semantics/float.k:200-200`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
631. **rule** `trusted-reference-semantics/semantics/float.k:201-201`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
632. **rule** `trusted-reference-semantics/semantics/float.k:202-202`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
633. **rule** `trusted-reference-semantics/semantics/float.k:203-203`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
634. **rule** `trusted-reference-semantics/semantics/float.k:204-204`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
635. **rule** `trusted-reference-semantics/semantics/float.k:205-205`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
636. **rule** `trusted-reference-semantics/semantics/float.k:206-208`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----`
637. **syntax** `trusted-reference-semantics/semantics/float.k:209-209`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(truncF), no-evaluators
   Source: `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
638. **rule** `trusted-reference-semantics/semantics/float.k:210-210`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`
639. **rule** `trusted-reference-semantics/semantics/float.k:211-211`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`
640. **rule** `trusted-reference-semantics/semantics/float.k:213-213`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)`
641. **rule** `trusted-reference-semantics/semantics/float.k:214-216`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("float", F:Float, .Vals) => F // round: Python half-even (banker's); round(F, N) scales by 10^N`
642. **syntax** `trusted-reference-semantics/semantics/float.k:217-217`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(roundF), no-evaluators
   Source: `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
643. **rule** `trusted-reference-semantics/semantics/float.k:218-222`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`
644. **syntax** `trusted-reference-semantics/semantics/float.k:223-223`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(roundFN), no-evaluators
   Source: `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
645. **rule** `trusted-reference-semantics/semantics/float.k:224-226`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`
646. **rule** `trusted-reference-semantics/semantics/float.k:227-227`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)`
647. **rule** `trusted-reference-semantics/semantics/float.k:228-228`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`
648. **syntax** `trusted-reference-semantics/semantics/float.k:230-230`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(sqrtF), no-evaluators
   Source: `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
649. **rule** `trusted-reference-semantics/semantics/float.k:231-231`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`
650. **syntax** `trusted-reference-semantics/semantics/float.k:232-232`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= "#mathSqrt"`
651. **rule** `trusted-reference-semantics/semantics/float.k:233-233`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`
652. **rule** `trusted-reference-semantics/semantics/float.k:234-234`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`
653. **rule** `trusted-reference-semantics/semantics/float.k:235-242`  
   Flags: operational-rule, concrete-only-rule; attributes: none
   Source: `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which // seed/step with 'requires isInt(V)', so they are STUCK on floats). These add the 'requires // isFloat(V)' seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive: // the isFloat guard is disjoint from the existing isInt one.`
654. **syntax** `trusted-reference-semantics/semantics/float.k:243-243`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`
655. **rule** `trusted-reference-semantics/semantics/float.k:244-244`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
656. **rule** `trusted-reference-semantics/semantics/float.k:245-245`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`
657. **rule** `trusted-reference-semantics/semantics/float.k:246-246`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`
658. **rule** `trusted-reference-semantics/semantics/float.k:247-248`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`
659. **syntax** `trusted-reference-semantics/semantics/float.k:250-250`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`
660. **rule** `trusted-reference-semantics/semantics/float.k:251-251`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
661. **rule** `trusted-reference-semantics/semantics/float.k:252-252`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`
662. **rule** `trusted-reference-semantics/semantics/float.k:253-253`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`
663. **rule** `trusted-reference-semantics/semantics/float.k:254-260`  
   Flags: operational-rule, concrete-only-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin). // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof // with isInt(V) in its path condition refutes this branch without sort reasoning.`
664. **syntax** `trusted-reference-semantics/semantics/float.k:261-261`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`
665. **rule** `trusted-reference-semantics/semantics/float.k:262-264`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`
666. **rule** `trusted-reference-semantics/semantics/float.k:265-265`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`
667. **rule** `trusted-reference-semantics/semantics/float.k:266-266`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`
668. **rule** `trusted-reference-semantics/semantics/float.k:267-269`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)`
669. **rule** `trusted-reference-semantics/semantics/float.k:270-272`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)`
670. **endmodule** `trusted-reference-semantics/semantics/float.k:273-273`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/functions.k`

671. **module** `trusted-reference-semantics/semantics/functions.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-FUNCTIONS`
672. **imports** `trusted-reference-semantics/semantics/functions.k:4-7`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k; // this module owns the frame lifecycle (bind params, return, pop).`
673. **syntax** `trusted-reference-semantics/semantics/functions.k:8-13`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall" // ==== def / anonymous closure =============================================`
674. **rule** `trusted-reference-semantics/semantics/functions.k:14-16`  
   Flags: operational-rule; attributes: F <- closureVal(PNS, BODY, L)
   Source: `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`
675. **syntax** `trusted-reference-semantics/semantics/functions.k:18-18`  
   Flags: none; attributes: none
   Source: `syntax Expr ::= closureExpr(ParamNames, Stmts)`
676. **rule** `trusted-reference-semantics/semantics/functions.k:19-26`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> // ==== annotated def/lambda (closure cells; spec 2.3) ====================== // closureValC(params, cellvars, body, captured-cells). No frame anchor: all // enclosing-local reads are freevars (symtable-complete) and go through the // captured cells; everything else is global/builtin, so the callee frame's // parent is the module scope (0) — sound after the defining frame dies.`
677. **syntax** `trusted-reference-semantics/semantics/functions.k:27-30`  
   Flags: none; attributes: none
   Source: `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) // capture: resolve each freevar to the enclosing frame's cellRef, then bind // (FuncDef) or yield (Lambda) the closure value.`
678. **syntax** `trusted-reference-semantics/semantics/functions.k:31-32`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`
679. **rule** `trusted-reference-semantics/semantics/functions.k:33-35`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`
680. **rule** `trusted-reference-semantics/semantics/functions.k:36-41`  
   Flags: operational-rule; attributes: FV <- {M[FV
   Source: `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
681. **rule** `trusted-reference-semantics/semantics/functions.k:42-45`  
   Flags: operational-rule; attributes: F <- closureValC(PNS, CVS, BODY, CM)
   Source: `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`
682. **rule** `trusted-reference-semantics/semantics/functions.k:47-49`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`
683. **rule** `trusted-reference-semantics/semantics/functions.k:50-52`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`
684. **rule** `trusted-reference-semantics/semantics/functions.k:53-58`  
   Flags: operational-rule; attributes: FV <- {M[FV
   Source: `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
685. **rule** `trusted-reference-semantics/semantics/functions.k:59-62`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> // ==== bind params ========================================================`
686. **rule** `trusted-reference-semantics/semantics/functions.k:63-63`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`
687. **rule** `trusted-reference-semantics/semantics/functions.k:64-67`  
   Flags: operational-rule; attributes: P <- V
   Source: `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound to its cell at frame entry`
688. **rule** `trusted-reference-semantics/semantics/functions.k:68-71`  
   Flags: operational-rule; attributes: P
   Source: `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
689. **requires** `trusted-reference-semantics/semantics/functions.k:72-77`  
   Flags: none; attributes: "$cells", P, priority(40)
   Source: `requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] // ==== return / pop the frame (the returned expr evaluates by strictness) ==`
690. **rule** `trusted-reference-semantics/semantics/functions.k:78-79`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`
691. **rule** `trusted-reference-semantics/semantics/functions.k:80-84`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).`
692. **rule** `trusted-reference-semantics/semantics/functions.k:85-90`  
   Flags: operational-rule; attributes: L <- undef
   Source: `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`
693. **endmodule** `trusted-reference-semantics/semantics/functions.k:91-91`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/int.k`

694. **module** `trusted-reference-semantics/semantics/int.k:4-4`  
   Flags: none; attributes: none
   Source: `module MPY-INT`
695. **imports** `trusted-reference-semantics/semantics/int.k:5-5`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
696. **rule** `trusted-reference-semantics/semantics/int.k:7-7`  
   Flags: equational-rule; attributes: none
   Source: `rule applyUn("-", I:Int) => 0 -Int I`
697. **rule** `trusted-reference-semantics/semantics/int.k:9-10`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b))`
698. **rule** `trusted-reference-semantics/semantics/int.k:11-11`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`
699. **rule** `trusted-reference-semantics/semantics/int.k:12-12`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`
700. **rule** `trusted-reference-semantics/semantics/int.k:13-13`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2`
701. **rule** `trusted-reference-semantics/semantics/int.k:14-14`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2`
702. **rule** `trusted-reference-semantics/semantics/int.k:15-15`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)`
703. **rule** `trusted-reference-semantics/semantics/int.k:16-16`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2`
704. **rule** `trusted-reference-semantics/semantics/int.k:17-17`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`
705. **syntax** `trusted-reference-semantics/semantics/int.k:19-19`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= pyMod(Int, Int) [function]`
706. **rule** `trusted-reference-semantics/semantics/int.k:20-20`  
   Flags: equational-rule; attributes: none
   Source: `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`
707. **rule** `trusted-reference-semantics/semantics/int.k:22-22`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2`
708. **rule** `trusted-reference-semantics/semantics/int.k:23-23`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2`
709. **rule** `trusted-reference-semantics/semantics/int.k:24-24`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2`
710. **rule** `trusted-reference-semantics/semantics/int.k:25-25`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2`
711. **rule** `trusted-reference-semantics/semantics/int.k:26-26`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2`
712. **rule** `trusted-reference-semantics/semantics/int.k:27-27`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2`
713. **endmodule** `trusted-reference-semantics/semantics/int.k:28-28`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/iter.k`

714. **module** `trusted-reference-semantics/semantics/iter.k:6-6`  
   Flags: none; attributes: none
   Source: `module MPY-ITER`
715. **imports** `trusted-reference-semantics/semantics/iter.k:7-7`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
716. **syntax** `trusted-reference-semantics/semantics/iter.k:8-8`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`
717. **endmodule** `trusted-reference-semantics/semantics/iter.k:9-9`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/list.k`

718. **module** `trusted-reference-semantics/semantics/list.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-LIST`
719. **imports** `trusted-reference-semantics/semantics/list.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
720. **imports** `trusted-reference-semantics/semantics/list.k:5-5`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER`
721. **imports** `trusted-reference-semantics/semantics/list.k:6-8`  
   Flags: none; attributes: none
   Source: `imports MPY-OPERATORS // ==== iteration (the iterator protocol's list case) =======================`
722. **rule** `trusted-reference-semantics/semantics/list.k:9-9`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>`
723. **rule** `trusted-reference-semantics/semantics/list.k:10-12`  
   Flags: operational-rule; attributes: ...
   Source: `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> // ==== ListExpr: [...] literal -> a fresh heap object =======================`
724. **syntax** `trusted-reference-semantics/semantics/list.k:13-13`  
   Flags: none; attributes: none
   Source: `syntax ApplyK ::= "toList"`
725. **rule** `trusted-reference-semantics/semantics/list.k:14-14`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`
726. **rule** `trusted-reference-semantics/semantics/list.k:15-17`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> // ==== list ops: + / == / != ===============================================`
727. **syntax** `trusted-reference-semantics/semantics/list.k:18-18`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`
728. **rule** `trusted-reference-semantics/semantics/list.k:19-19`  
   Flags: equational-rule; attributes: none
   Source: `rule valSeqConcat(.ValSeq, T:ValSeq)                => T`
729. **rule** `trusted-reference-semantics/semantics/list.k:20-23`  
   Flags: equational-rule, priority-rule; attributes: none
   Source: `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) // list + list constructs a NEW object (k-cell — it allocates; operands land here // already deref'd). priority(45) beats the generic BinOp dispatch.`
730. **rule** `trusted-reference-semantics/semantics/list.k:24-25`  
   Flags: operational-rule, priority-rule; attributes: priority(45)
   Source: `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`
731. **rule** `trusted-reference-semantics/semantics/list.k:27-27`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`
732. **rule** `trusted-reference-semantics/semantics/list.k:28-32`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) // ==== deep equality when elements are heap objects (list-of-lists) ======== // Python == is structural at every depth. Fires ONLY when a ref is present // (the guard decides on concrete seqs); the plain ==K path above is unchanged.`
733. **syntax** `trusted-reference-semantics/semantics/list.k:33-33`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= hasRefVS(ValSeq) [function, total]`
734. **rule** `trusted-reference-semantics/semantics/list.k:34-34`  
   Flags: equational-rule; attributes: none
   Source: `rule hasRefVS(.ValSeq)                => false`
735. **rule** `trusted-reference-semantics/semantics/list.k:35-35`  
   Flags: equational-rule; attributes: none
   Source: `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`
736. **syntax** `trusted-reference-semantics/semantics/list.k:37-38`  
   Flags: function-declaration; attributes: function, function
   Source: `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map)        [function]`
737. **rule** `trusted-reference-semantics/semantics/list.k:39-39`  
   Flags: equational-rule; attributes: none
   Source: `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true`
738. **rule** `trusted-reference-semantics/semantics/list.k:40-40`  
   Flags: equational-rule; attributes: none
   Source: `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false`
739. **rule** `trusted-reference-semantics/semantics/list.k:41-41`  
   Flags: equational-rule; attributes: none
   Source: `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false`
740. **rule** `trusted-reference-semantics/semantics/list.k:42-43`  
   Flags: equational-rule; attributes: none
   Source: `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`
741. **rule** `trusted-reference-semantics/semantics/list.k:45-46`  
   Flags: equational-rule; attributes: H
   Source: `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)`
742. **rule** `trusted-reference-semantics/semantics/list.k:47-48`  
   Flags: equational-rule; attributes: H
   Source: `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)`
743. **rule** `trusted-reference-semantics/semantics/list.k:49-49`  
   Flags: equational-rule; attributes: none
   Source: `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`
744. **rule** `trusted-reference-semantics/semantics/list.k:50-52`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] // ==== mutator: xs.append(v) — an in-place heap write ======================`
745. **rule** `trusted-reference-semantics/semantics/list.k:53-57`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] // ==== 'x in list' — a <k>-cell fold over #iterNext ========================`
746. **syntax** `trusted-reference-semantics/semantics/list.k:58-58`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`
747. **rule** `trusted-reference-semantics/semantics/list.k:59-59`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`
748. **rule** `trusted-reference-semantics/semantics/list.k:60-60`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`
749. **rule** `trusted-reference-semantics/semantics/list.k:61-61`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`
750. **rule** `trusted-reference-semantics/semantics/list.k:62-62`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`
751. **rule** `trusted-reference-semantics/semantics/list.k:63-64`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V`
752. **rule** `trusted-reference-semantics/semantics/list.k:65-66`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)`
753. **rule** `trusted-reference-semantics/semantics/list.k:67-67`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> B:Bool ~> #notB => notBool B ... </k>`
754. **endmodule** `trusted-reference-semantics/semantics/list.k:68-68`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/methods.k`

755. **module** `trusted-reference-semantics/semantics/methods.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-METHODS`
756. **imports** `trusted-reference-semantics/semantics/methods.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
757. **imports** `trusted-reference-semantics/semantics/methods.k:5-5`  
   Flags: none; attributes: none
   Source: `imports K-EQUAL`
758. **imports** `trusted-reference-semantics/semantics/methods.k:6-6`  
   Flags: none; attributes: none
   Source: `imports MPY-STR`
759. **imports** `trusted-reference-semantics/semantics/methods.k:7-9`  
   Flags: none; attributes: none
   Source: `imports MPY-LIST // method-call routing + arg-eval live in call.k; this module owns applyMethod.`
760. **syntax** `trusted-reference-semantics/semantics/methods.k:10-12`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val ::= applyMethod(Val, String, Vals) [function] // ==== string predicates (Python semantics) =================================`
761. **rule** `trusted-reference-semantics/semantics/methods.k:13-13`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`
762. **rule** `trusted-reference-semantics/semantics/methods.k:14-14`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`
763. **rule** `trusted-reference-semantics/semantics/methods.k:15-15`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`
764. **rule** `trusted-reference-semantics/semantics/methods.k:16-18`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) // ==== case maps ============================================================`
765. **rule** `trusted-reference-semantics/semantics/methods.k:19-19`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))`
766. **rule** `trusted-reference-semantics/semantics/methods.k:20-20`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))`
767. **rule** `trusted-reference-semantics/semantics/methods.k:21-25`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) // ==== join / count / strip / encode ======================================== // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by // the call layer; the result str is a value)`
768. **rule** `trusted-reference-semantics/semantics/methods.k:26-26`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`
769. **syntax** `trusted-reference-semantics/semantics/methods.k:27-27`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`
770. **rule** `trusted-reference-semantics/semantics/methods.k:28-28`  
   Flags: equational-rule; attributes: none
   Source: `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`
771. **rule** `trusted-reference-semantics/semantics/methods.k:29-29`  
   Flags: equational-rule; attributes: none
   Source: `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`
772. **rule** `trusted-reference-semantics/semantics/methods.k:30-33`  
   Flags: equational-rule; attributes: none
   Source: `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) // S.count(sub): non-overlapping window scan (Python str.count)`
773. **rule** `trusted-reference-semantics/semantics/methods.k:34-34`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`
774. **syntax** `trusted-reference-semantics/semantics/methods.k:35-35`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`
775. **rule** `trusted-reference-semantics/semantics/methods.k:36-36`  
   Flags: equational-rule; attributes: none
   Source: `rule cntSub(.IntSeq, _:IntSeq) => 0`
776. **rule** `trusted-reference-semantics/semantics/methods.k:37-38`  
   Flags: equational-rule; attributes: none
   Source: `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`
777. **rule** `trusted-reference-semantics/semantics/methods.k:39-40`  
   Flags: equational-rule; attributes: none
   Source: `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`
778. **syntax** `trusted-reference-semantics/semantics/methods.k:41-41`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`
779. **rule** `trusted-reference-semantics/semantics/methods.k:42-42`  
   Flags: equational-rule; attributes: none
   Source: `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`
780. **rule** `trusted-reference-semantics/semantics/methods.k:43-43`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`
781. **rule** `trusted-reference-semantics/semantics/methods.k:44-46`  
   Flags: equational-rule; attributes: none
   Source: `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 // S.strip(): trim whitespace runs from both ends`
782. **rule** `trusted-reference-semantics/semantics/methods.k:47-47`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`
783. **syntax** `trusted-reference-semantics/semantics/methods.k:48-48`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= trimWS(IntSeq) [function, total]`
784. **rule** `trusted-reference-semantics/semantics/methods.k:49-49`  
   Flags: equational-rule; attributes: none
   Source: `rule trimWS(.IntSeq) => .IntSeq`
785. **rule** `trusted-reference-semantics/semantics/methods.k:50-50`  
   Flags: equational-rule; attributes: none
   Source: `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`
786. **rule** `trusted-reference-semantics/semantics/methods.k:51-51`  
   Flags: equational-rule; attributes: none
   Source: `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`
787. **syntax** `trusted-reference-semantics/semantics/methods.k:52-52`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`
788. **rule** `trusted-reference-semantics/semantics/methods.k:53-53`  
   Flags: equational-rule; attributes: none
   Source: `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`
789. **rule** `trusted-reference-semantics/semantics/methods.k:54-54`  
   Flags: equational-rule; attributes: none
   Source: `rule revISAcc(.IntSeq, A:IntSeq) => A`
790. **rule** `trusted-reference-semantics/semantics/methods.k:55-57`  
   Flags: equational-rule; attributes: none
   Source: `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) // S.encode('ascii'): identity on the code-sequence model (bytes == codes)`
791. **rule** `trusted-reference-semantics/semantics/methods.k:58-60`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) // ==== prefix ===============================================================`
792. **rule** `trusted-reference-semantics/semantics/methods.k:61-63`  
   Flags: equational-rule, concrete-only-rule; attributes: none
   Source: `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========`
793. **rule** `trusted-reference-semantics/semantics/methods.k:64-64`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`
794. **syntax** `trusted-reference-semantics/semantics/methods.k:65-65`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`
795. **rule** `trusted-reference-semantics/semantics/methods.k:66-66`  
   Flags: equational-rule; attributes: none
   Source: `rule cntOccVS(.ValSeq, _:Val)                => 0`
796. **rule** `trusted-reference-semantics/semantics/methods.k:67-67`  
   Flags: equational-rule; attributes: none
   Source: `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`
797. **rule** `trusted-reference-semantics/semantics/methods.k:68-71`  
   Flags: equational-rule; attributes: none
   Source: `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V) // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ========== // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.`
798. **rule** `trusted-reference-semantics/semantics/methods.k:72-74`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`
799. **syntax** `trusted-reference-semantics/semantics/methods.k:75-75`  
   Flags: function-declaration; attributes: function
   Source: `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result`
800. **rule** `trusted-reference-semantics/semantics/methods.k:76-76`  
   Flags: equational-rule; attributes: none
   Source: `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`
801. **rule** `trusted-reference-semantics/semantics/methods.k:77-78`  
   Flags: equational-rule; attributes: none
   Source: `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)`
802. **rule** `trusted-reference-semantics/semantics/methods.k:79-81`  
   Flags: equational-rule; attributes: none
   Source: `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty.`
803. **syntax** `trusted-reference-semantics/semantics/methods.k:82-82`  
   Flags: function-declaration; attributes: function
   Source: `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`
804. **rule** `trusted-reference-semantics/semantics/methods.k:83-83`  
   Flags: equational-rule; attributes: none
   Source: `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC`
805. **rule** `trusted-reference-semantics/semantics/methods.k:84-84`  
   Flags: equational-rule; attributes: none
   Source: `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`
806. **syntax** `trusted-reference-semantics/semantics/methods.k:85-85`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isWSC(Int) [function, total]`
807. **rule** `trusted-reference-semantics/semantics/methods.k:86-88`  
   Flags: equational-rule; attributes: none
   Source: `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 // split(sep='x') keyword form delegates to the positional k-cell rule`
808. **rule** `trusted-reference-semantics/semantics/methods.k:89-93`  
   Flags: operational-rule, priority-rule; attributes: priority(39)
   Source: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).`
809. **rule** `trusted-reference-semantics/semantics/methods.k:94-96`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`
810. **syntax** `trusted-reference-semantics/semantics/methods.k:97-97`  
   Flags: function-declaration; attributes: function
   Source: `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token`
811. **rule** `trusted-reference-semantics/semantics/methods.k:98-98`  
   Flags: equational-rule; attributes: none
   Source: `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)`
812. **rule** `trusted-reference-semantics/semantics/methods.k:99-100`  
   Flags: equational-rule; attributes: none
   Source: `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP`
813. **rule** `trusted-reference-semantics/semantics/methods.k:101-102`  
   Flags: equational-rule; attributes: none
   Source: `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)`
814. **rule** `trusted-reference-semantics/semantics/methods.k:104-105`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`
815. **syntax** `trusted-reference-semantics/semantics/methods.k:106-106`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`
816. **rule** `trusted-reference-semantics/semantics/methods.k:107-107`  
   Flags: equational-rule; attributes: none
   Source: `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq`
817. **rule** `trusted-reference-semantics/semantics/methods.k:108-108`  
   Flags: equational-rule; attributes: none
   Source: `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`
818. **rule** `trusted-reference-semantics/semantics/methods.k:109-111`  
   Flags: equational-rule; attributes: none
   Source: `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) // ==== char helpers =========================================================`
819. **syntax** `trusted-reference-semantics/semantics/methods.k:112-112`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isUpperC(Int) [function, total]`
820. **rule** `trusted-reference-semantics/semantics/methods.k:113-113`  
   Flags: equational-rule; attributes: none
   Source: `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`
821. **syntax** `trusted-reference-semantics/semantics/methods.k:115-115`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isLowerC(Int) [function, total]`
822. **rule** `trusted-reference-semantics/semantics/methods.k:116-116`  
   Flags: equational-rule; attributes: none
   Source: `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`
823. **syntax** `trusted-reference-semantics/semantics/methods.k:118-118`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isAlphaC(Int) [function, total]`
824. **rule** `trusted-reference-semantics/semantics/methods.k:119-119`  
   Flags: equational-rule; attributes: none
   Source: `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`
825. **syntax** `trusted-reference-semantics/semantics/methods.k:121-121`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= isDigitC(Int) [function, total]`
826. **rule** `trusted-reference-semantics/semantics/methods.k:122-122`  
   Flags: equational-rule; attributes: none
   Source: `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`
827. **syntax** `trusted-reference-semantics/semantics/methods.k:124-124`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= hasUpper(IntSeq) [function, total]`
828. **rule** `trusted-reference-semantics/semantics/methods.k:125-125`  
   Flags: equational-rule; attributes: none
   Source: `rule hasUpper(.IntSeq) => false`
829. **rule** `trusted-reference-semantics/semantics/methods.k:126-126`  
   Flags: equational-rule; attributes: none
   Source: `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`
830. **syntax** `trusted-reference-semantics/semantics/methods.k:128-128`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= hasLower(IntSeq) [function, total]`
831. **rule** `trusted-reference-semantics/semantics/methods.k:129-129`  
   Flags: equational-rule; attributes: none
   Source: `rule hasLower(.IntSeq) => false`
832. **rule** `trusted-reference-semantics/semantics/methods.k:130-130`  
   Flags: equational-rule; attributes: none
   Source: `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`
833. **syntax** `trusted-reference-semantics/semantics/methods.k:132-132`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= allAlpha(IntSeq) [function, total]`
834. **rule** `trusted-reference-semantics/semantics/methods.k:133-133`  
   Flags: equational-rule; attributes: none
   Source: `rule allAlpha(.IntSeq) => true`
835. **rule** `trusted-reference-semantics/semantics/methods.k:134-134`  
   Flags: equational-rule; attributes: none
   Source: `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`
836. **syntax** `trusted-reference-semantics/semantics/methods.k:136-136`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= allDigit(IntSeq) [function, total]`
837. **rule** `trusted-reference-semantics/semantics/methods.k:137-137`  
   Flags: equational-rule; attributes: none
   Source: `rule allDigit(.IntSeq) => true`
838. **rule** `trusted-reference-semantics/semantics/methods.k:138-138`  
   Flags: equational-rule; attributes: none
   Source: `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`
839. **syntax** `trusted-reference-semantics/semantics/methods.k:140-140`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= lowerC(Int) [function, total]`
840. **rule** `trusted-reference-semantics/semantics/methods.k:142-142`  
   Flags: equational-rule; attributes: none
   Source: `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`
841. **rule** `trusted-reference-semantics/semantics/methods.k:143-143`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule lowerC(C:Int) => C         [owise]`
842. **syntax** `trusted-reference-semantics/semantics/methods.k:145-145`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= upperC(Int) [function, total]`
843. **rule** `trusted-reference-semantics/semantics/methods.k:146-146`  
   Flags: equational-rule; attributes: none
   Source: `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`
844. **rule** `trusted-reference-semantics/semantics/methods.k:147-147`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule upperC(C:Int) => C         [owise]`
845. **syntax** `trusted-reference-semantics/semantics/methods.k:149-149`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= swapC(Int) [function, total]`
846. **rule** `trusted-reference-semantics/semantics/methods.k:150-150`  
   Flags: equational-rule; attributes: none
   Source: `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`
847. **rule** `trusted-reference-semantics/semantics/methods.k:151-151`  
   Flags: equational-rule; attributes: none
   Source: `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`
848. **rule** `trusted-reference-semantics/semantics/methods.k:152-152`  
   Flags: equational-rule, owise-rule; attributes: owise
   Source: `rule swapC(C:Int) => C         [owise]`
849. **syntax** `trusted-reference-semantics/semantics/methods.k:154-154`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= mapLower(IntSeq) [function, total]`
850. **rule** `trusted-reference-semantics/semantics/methods.k:155-155`  
   Flags: equational-rule; attributes: none
   Source: `rule mapLower(.IntSeq) => .IntSeq`
851. **rule** `trusted-reference-semantics/semantics/methods.k:156-156`  
   Flags: equational-rule; attributes: none
   Source: `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`
852. **syntax** `trusted-reference-semantics/semantics/methods.k:158-158`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`
853. **rule** `trusted-reference-semantics/semantics/methods.k:159-159`  
   Flags: equational-rule; attributes: none
   Source: `rule mapUpper(.IntSeq) => .IntSeq`
854. **rule** `trusted-reference-semantics/semantics/methods.k:160-160`  
   Flags: equational-rule; attributes: none
   Source: `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`
855. **syntax** `trusted-reference-semantics/semantics/methods.k:162-162`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`
856. **rule** `trusted-reference-semantics/semantics/methods.k:163-163`  
   Flags: equational-rule; attributes: none
   Source: `rule mapSwap(.IntSeq) => .IntSeq`
857. **rule** `trusted-reference-semantics/semantics/methods.k:164-164`  
   Flags: equational-rule; attributes: none
   Source: `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`
858. **syntax** `trusted-reference-semantics/semantics/methods.k:166-166`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`
859. **rule** `trusted-reference-semantics/semantics/methods.k:167-167`  
   Flags: equational-rule; attributes: none
   Source: `rule startsWith(.IntSeq, _:IntSeq)               => true`
860. **rule** `trusted-reference-semantics/semantics/methods.k:168-168`  
   Flags: equational-rule; attributes: none
   Source: `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`
861. **rule** `trusted-reference-semantics/semantics/methods.k:169-169`  
   Flags: equational-rule; attributes: none
   Source: `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`
862. **endmodule** `trusted-reference-semantics/semantics/methods.k:170-170`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/operators.k`

863. **module** `trusted-reference-semantics/semantics/operators.k:6-6`  
   Flags: none; attributes: none
   Source: `module MPY-OPERATORS`
864. **imports** `trusted-reference-semantics/semantics/operators.k:7-7`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
865. **imports** `trusted-reference-semantics/semantics/operators.k:8-8`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER`
866. **rule** `trusted-reference-semantics/semantics/operators.k:10-10`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`
867. **rule** `trusted-reference-semantics/semantics/operators.k:12-14`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes`
868. **context** `trusted-reference-semantics/semantics/operators.k:15-15`  
   Flags: none; attributes: none
   Source: `context Compare(HOLE, _)`
869. **context** `trusted-reference-semantics/semantics/operators.k:16-16`  
   Flags: none; attributes: none
   Source: `context Compare(_:Val, CmpOp(_, HOLE))`
870. **rule** `trusted-reference-semantics/semantics/operators.k:17-17`  
   Flags: operational-rule, owise-rule; attributes: owise
   Source: `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`
871. **rule** `trusted-reference-semantics/semantics/operators.k:19-19`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("is",     V:Val, noneV) => V ==K noneV`
872. **rule** `trusted-reference-semantics/semantics/operators.k:20-24`  
   Flags: equational-rule, priority-rule; attributes: none
   Source: `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) // ==== operand deref: heap objects combine/compare by STRUCTURE ============ // (Python: list == is structural; identity only via 'is'.) priority(40) // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.`
873. **rule** `trusted-reference-semantics/semantics/operators.k:25-27`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
874. **rule** `trusted-reference-semantics/semantics/operators.k:28-33`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] // the left operand of 'in'/'not in' is an ELEMENT (compares by ==K) — never deref'd`
875. **rule** `trusted-reference-semantics/semantics/operators.k:34-37`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]`
876. **rule** `trusted-reference-semantics/semantics/operators.k:38-42`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]`
877. **rule** `trusted-reference-semantics/semantics/operators.k:44-46`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
878. **endmodule** `trusted-reference-semantics/semantics/operators.k:47-47`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/range.k`

879. **module** `trusted-reference-semantics/semantics/range.k:5-5`  
   Flags: none; attributes: none
   Source: `module MPY-RANGE`
880. **imports** `trusted-reference-semantics/semantics/range.k:6-6`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
881. **imports** `trusted-reference-semantics/semantics/range.k:7-7`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER`
882. **syntax** `trusted-reference-semantics/semantics/range.k:9-9`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= inRange(Int, Int, Int) [function, total]`
883. **rule** `trusted-reference-semantics/semantics/range.k:10-10`  
   Flags: equational-rule; attributes: none
   Source: `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`
884. **syntax** `trusted-reference-semantics/semantics/range.k:12-12`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= rangeLen(Int, Int, Int) [function]`
885. **rule** `trusted-reference-semantics/semantics/range.k:13-14`  
   Flags: equational-rule; attributes: none
   Source: `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO`
886. **rule** `trusted-reference-semantics/semantics/range.k:15-16`  
   Flags: equational-rule; attributes: none
   Source: `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO`
887. **rule** `trusted-reference-semantics/semantics/range.k:17-18`  
   Flags: equational-rule; attributes: none
   Source: `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`
888. **rule** `trusted-reference-semantics/semantics/range.k:20-22`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)`
889. **rule** `trusted-reference-semantics/semantics/range.k:23-24`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)`
890. **endmodule** `trusted-reference-semantics/semantics/range.k:25-25`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/set.k`

891. **module** `trusted-reference-semantics/semantics/set.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-SET`
892. **imports** `trusted-reference-semantics/semantics/set.k:4-7`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE // a set value, carried as its distinct codes in first-seen order (order is irrelevant // to membership/cardinality — the two observations sets support here).`
893. **syntax** `trusted-reference-semantics/semantics/set.k:8-10`  
   Flags: none; attributes: none
   Source: `syntax Val ::= setV(IntSeq) // membership of a code in the accumulated distinct-code sequence`
894. **syntax** `trusted-reference-semantics/semantics/set.k:11-11`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`
895. **rule** `trusted-reference-semantics/semantics/set.k:12-12`  
   Flags: equational-rule; attributes: none
   Source: `rule codeIn(_:Int, .IntSeq)                => false`
896. **rule** `trusted-reference-semantics/semantics/set.k:13-15`  
   Flags: equational-rule; attributes: none
   Source: `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) // the distinct codes of CS (insert-if-absent fold, first-seen order)`
897. **syntax** `trusted-reference-semantics/semantics/set.k:16-17`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] | dedupFrom(IntSeq, IntSeq)  [function, total]`
898. **rule** `trusted-reference-semantics/semantics/set.k:18-18`  
   Flags: equational-rule; attributes: none
   Source: `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`
899. **rule** `trusted-reference-semantics/semantics/set.k:19-19`  
   Flags: equational-rule; attributes: none
   Source: `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`
900. **rule** `trusted-reference-semantics/semantics/set.k:20-21`  
   Flags: equational-rule; attributes: none
   Source: `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)`
901. **rule** `trusted-reference-semantics/semantics/set.k:22-23`  
   Flags: equational-rule; attributes: none
   Source: `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)`
902. **syntax** `trusted-reference-semantics/semantics/set.k:25-25`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`
903. **rule** `trusted-reference-semantics/semantics/set.k:26-26`  
   Flags: equational-rule; attributes: none
   Source: `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)`
904. **rule** `trusted-reference-semantics/semantics/set.k:27-30`  
   Flags: equational-rule; attributes: none
   Source: `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) // ==== set equality: two sets are equal iff mutually subsuming ============== // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).`
905. **syntax** `trusted-reference-semantics/semantics/set.k:31-31`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`
906. **rule** `trusted-reference-semantics/semantics/set.k:32-32`  
   Flags: equational-rule; attributes: none
   Source: `rule subsetCodes(.IntSeq, _:IntSeq)                => true`
907. **rule** `trusted-reference-semantics/semantics/set.k:33-33`  
   Flags: equational-rule; attributes: none
   Source: `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`
908. **syntax** `trusted-reference-semantics/semantics/set.k:35-35`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`
909. **rule** `trusted-reference-semantics/semantics/set.k:36-38`  
   Flags: equational-rule; attributes: none
   Source: `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) // set == set  (the only comparison sets support here)`
910. **rule** `trusted-reference-semantics/semantics/set.k:39-39`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`
911. **endmodule** `trusted-reference-semantics/semantics/set.k:40-40`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/sort.k`

912. **module** `trusted-reference-semantics/semantics/sort.k:10-10`  
   Flags: none; attributes: none
   Source: `module MPY-SORT`
913. **imports** `trusted-reference-semantics/semantics/sort.k:11-11`  
   Flags: none; attributes: none
   Source: `imports MPY-BUILTINS`
914. **imports** `trusted-reference-semantics/semantics/sort.k:12-17`  
   Flags: none; attributes: none
   Source: `imports MPY-SUBSCRIPT // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators); // concrete insertion sort for krun. // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal // (lemmas-only) is not available in the semantics. Int and str lists.`
915. **syntax** `trusted-reference-semantics/semantics/sort.k:18-18`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(sortVS), no-evaluators
   Source: `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
916. **syntax** `trusted-reference-semantics/semantics/sort.k:19-19`  
   Flags: function-declaration; attributes: function
   Source: `syntax ValSeq ::= insVS(Int, ValSeq) [function]`
917. **rule** `trusted-reference-semantics/semantics/sort.k:20-20`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule sortVS(.ValSeq)                => .ValSeq          [concrete]`
918. **rule** `trusted-reference-semantics/semantics/sort.k:21-21`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`
919. **rule** `trusted-reference-semantics/semantics/sort.k:22-22`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]`
920. **rule** `trusted-reference-semantics/semantics/sort.k:23-23`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`
921. **rule** `trusted-reference-semantics/semantics/sort.k:24-25`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k)`
922. **syntax** `trusted-reference-semantics/semantics/sort.k:26-26`  
   Flags: function-declaration; attributes: function
   Source: `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`
923. **rule** `trusted-reference-semantics/semantics/sort.k:27-27`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`
924. **rule** `trusted-reference-semantics/semantics/sort.k:28-28`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`
925. **rule** `trusted-reference-semantics/semantics/sort.k:29-30`  
   Flags: equational-rule, concrete-only-rule; attributes: concrete
   Source: `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]`
926. **rule** `trusted-reference-semantics/semantics/sort.k:31-35`  
   Flags: equational-rule, concrete-only-rule, owise-rule; attributes: concrete, owise
   Source: `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise] // applyBuiltin routing in call.k) so the result allocates.`
927. **rule** `trusted-reference-semantics/semantics/sort.k:36-39`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> // mutator: xs.sort() — the in-place heap write over the same trusted sortVS`
928. **rule** `trusted-reference-semantics/semantics/sort.k:40-48`  
   Flags: operational-rule, priority-rule, concrete-only-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] // ==== keyed / reversed sorted() (WP2) ===================================== // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV // (a closure/builtin/type — anything callable). OPAQUE here; the concrete // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable- // inserts, at priority(40) over these.`
929. **syntax** `trusted-reference-semantics/semantics/sort.k:49-49`  
   Flags: function-declaration, total-declaration, named-symbol, opaque-symbol; attributes: function, total, symbol(sortKeyVS), no-evaluators
   Source: `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`
930. **syntax** `trusted-reference-semantics/semantics/sort.k:51-52`  
   Flags: function-declaration, total-declaration; attributes: function, total, function, total
   Source: `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`
931. **rule** `trusted-reference-semantics/semantics/sort.k:53-53`  
   Flags: equational-rule; attributes: none
   Source: `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`
932. **rule** `trusted-reference-semantics/semantics/sort.k:54-54`  
   Flags: equational-rule; attributes: none
   Source: `rule revVSAcc(.ValSeq, A:ValSeq) => A`
933. **rule** `trusted-reference-semantics/semantics/sort.k:55-55`  
   Flags: equational-rule; attributes: none
   Source: `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`
934. **syntax** `trusted-reference-semantics/semantics/sort.k:57-57`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`
935. **rule** `trusted-reference-semantics/semantics/sort.k:58-58`  
   Flags: equational-rule; attributes: none
   Source: `rule condRev(S:ValSeq, false) => S`
936. **rule** `trusted-reference-semantics/semantics/sort.k:59-59`  
   Flags: equational-rule; attributes: none
   Source: `rule condRev(S:ValSeq, true)  => revVS(S)`
937. **rule** `trusted-reference-semantics/semantics/sort.k:61-62`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`
938. **rule** `trusted-reference-semantics/semantics/sort.k:63-64`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`
939. **rule** `trusted-reference-semantics/semantics/sort.k:65-71`  
   Flags: operational-rule, concrete-only-rule; attributes: total
   Source: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> // Indexing the opaque sorted list: 'valSeqAt(sortVS(VS), I)' is DEFINED because valSeqAt is // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write // their postcondition directly as valSeqAt(sortVS(VS), …).`
940. **endmodule** `trusted-reference-semantics/semantics/sort.k:72-72`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/str.k`

941. **module** `trusted-reference-semantics/semantics/str.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-STR`
942. **imports** `trusted-reference-semantics/semantics/str.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
943. **imports** `trusted-reference-semantics/semantics/str.k:5-7`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==`
944. **rule** `trusted-reference-semantics/semantics/str.k:8-8`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>`
945. **rule** `trusted-reference-semantics/semantics/str.k:9-12`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> // ==== str literal (ASCII-only) ============================================`
946. **syntax** `trusted-reference-semantics/semantics/str.k:13-13`  
   Flags: function-declaration; attributes: function
   Source: `syntax IntSeq ::= strToCodes(String) [function]`
947. **rule** `trusted-reference-semantics/semantics/str.k:14-14`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`
948. **rule** `trusted-reference-semantics/semantics/str.k:15-15`  
   Flags: equational-rule; attributes: none
   Source: `rule strToCodes("") => .IntSeq`
949. **rule** `trusted-reference-semantics/semantics/str.k:16-19`  
   Flags: equational-rule; attributes: none
   Source: `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 // ==== operators: + / == / != / in =========================================`
950. **syntax** `trusted-reference-semantics/semantics/str.k:20-20`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`
951. **rule** `trusted-reference-semantics/semantics/str.k:21-21`  
   Flags: equational-rule; attributes: none
   Source: `rule seqConcat(.IntSeq, T:IntSeq)                => T`
952. **rule** `trusted-reference-semantics/semantics/str.k:22-22`  
   Flags: equational-rule; attributes: none
   Source: `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`
953. **rule** `trusted-reference-semantics/semantics/str.k:24-24`  
   Flags: equational-rule; attributes: none
   Source: `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`
954. **rule** `trusted-reference-semantics/semantics/str.k:25-25`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`
955. **rule** `trusted-reference-semantics/semantics/str.k:26-28`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) // substring membership: 'P in X' iff the code-seq P occurs contiguously in X`
956. **rule** `trusted-reference-semantics/semantics/str.k:29-29`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`
957. **rule** `trusted-reference-semantics/semantics/str.k:30-30`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`
958. **syntax** `trusted-reference-semantics/semantics/str.k:32-32`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`
959. **rule** `trusted-reference-semantics/semantics/str.k:33-33`  
   Flags: equational-rule; attributes: none
   Source: `rule strPrefix(.IntSeq, _:IntSeq)               => true`
960. **rule** `trusted-reference-semantics/semantics/str.k:34-34`  
   Flags: equational-rule; attributes: none
   Source: `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`
961. **rule** `trusted-reference-semantics/semantics/str.k:35-35`  
   Flags: equational-rule; attributes: none
   Source: `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`
962. **syntax** `trusted-reference-semantics/semantics/str.k:37-37`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`
963. **rule** `trusted-reference-semantics/semantics/str.k:38-38`  
   Flags: equational-rule; attributes: none
   Source: `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)`
964. **rule** `trusted-reference-semantics/semantics/str.k:39-39`  
   Flags: equational-rule; attributes: none
   Source: `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)`
965. **rule** `trusted-reference-semantics/semantics/str.k:40-47`  
   Flags: equational-rule; attributes: none
   Source: `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic // str '<' stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on // str </<=/>/>= comparisons.`
966. **syntax** `trusted-reference-semantics/semantics/str.k:48-48`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`
967. **rule** `trusted-reference-semantics/semantics/str.k:49-49`  
   Flags: equational-rule; attributes: none
   Source: `rule strLt(.IntSeq, .IntSeq)                => false`
968. **rule** `trusted-reference-semantics/semantics/str.k:50-50`  
   Flags: equational-rule; attributes: none
   Source: `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`
969. **rule** `trusted-reference-semantics/semantics/str.k:51-51`  
   Flags: equational-rule; attributes: none
   Source: `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`
970. **rule** `trusted-reference-semantics/semantics/str.k:52-52`  
   Flags: equational-rule; attributes: none
   Source: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B`
971. **rule** `trusted-reference-semantics/semantics/str.k:53-53`  
   Flags: equational-rule; attributes: none
   Source: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B`
972. **rule** `trusted-reference-semantics/semantics/str.k:54-54`  
   Flags: equational-rule; attributes: none
   Source: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`
973. **rule** `trusted-reference-semantics/semantics/str.k:56-56`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
974. **rule** `trusted-reference-semantics/semantics/str.k:57-57`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`
975. **rule** `trusted-reference-semantics/semantics/str.k:58-58`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`
976. **rule** `trusted-reference-semantics/semantics/str.k:59-59`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`
977. **endmodule** `trusted-reference-semantics/semantics/str.k:60-60`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/subscript.k`

978. **module** `trusted-reference-semantics/semantics/subscript.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-SUBSCRIPT`
979. **imports** `trusted-reference-semantics/semantics/subscript.k:4-10`  
   Flags: none; attributes: total, total
   Source: `imports MPY-CORE // ==== positional access + negative-index normalization (used only here) === // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g. // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total // atK. K trusts the [total] annotation; valid programs index in-bounds.`
980. **syntax** `trusted-reference-semantics/semantics/subscript.k:11-11`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`
981. **rule** `trusted-reference-semantics/semantics/subscript.k:12-12`  
   Flags: equational-rule; attributes: none
   Source: `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V`
982. **rule** `trusted-reference-semantics/semantics/subscript.k:13-14`  
   Flags: equational-rule; attributes: none
   Source: `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0`
983. **syntax** `trusted-reference-semantics/semantics/subscript.k:16-16`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= intSeqAt(IntSeq, Int) [function]`
984. **rule** `trusted-reference-semantics/semantics/subscript.k:17-17`  
   Flags: equational-rule; attributes: none
   Source: `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C`
985. **rule** `trusted-reference-semantics/semantics/subscript.k:18-19`  
   Flags: equational-rule; attributes: none
   Source: `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0`
986. **syntax** `trusted-reference-semantics/semantics/subscript.k:21-21`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= normIdx(Int, Int) [function, total]`
987. **rule** `trusted-reference-semantics/semantics/subscript.k:22-22`  
   Flags: equational-rule; attributes: none
   Source: `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`
988. **rule** `trusted-reference-semantics/semantics/subscript.k:23-26`  
   Flags: equational-rule; attributes: i
   Source: `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0 // ==== Subscript: indexing obj[i] (list / tuple / str) ===================== // contexts (not strict attrs): the Index slot's Slice alternative must never heat`
989. **context** `trusted-reference-semantics/semantics/subscript.k:27-27`  
   Flags: none; attributes: none
   Source: `context Subscript(HOLE, _)`
990. **context** `trusted-reference-semantics/semantics/subscript.k:28-30`  
   Flags: none; attributes: none
   Source: `context Subscript(_:Val, HOLE:Expr) // heap-object deref (covers both the index and slice forms via the Index slot)`
991. **rule** `trusted-reference-semantics/semantics/subscript.k:31-33`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
992. **rule** `trusted-reference-semantics/semantics/subscript.k:35-35`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`
993. **syntax** `trusted-reference-semantics/semantics/subscript.k:37-37`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val ::= applyIndex(Val, Int) [function]`
994. **rule** `trusted-reference-semantics/semantics/subscript.k:38-38`  
   Flags: equational-rule; attributes: none
   Source: `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
995. **rule** `trusted-reference-semantics/semantics/subscript.k:39-39`  
   Flags: equational-rule; attributes: none
   Source: `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
996. **rule** `trusted-reference-semantics/semantics/subscript.k:40-43`  
   Flags: equational-rule; attributes: lo:hi:step
   Source: `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========`
997. **syntax** `trusted-reference-semantics/semantics/subscript.k:44-47`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`
998. **syntax** `trusted-reference-semantics/semantics/subscript.k:49-49`  
   Flags: none; attributes: none
   Source: `syntax OptInt ::= "noB" | someB(Int)`
999. **rule** `trusted-reference-semantics/semantics/subscript.k:50-50`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #evalB(NoBound)  => noB ... </k>`
1000. **rule** `trusted-reference-semantics/semantics/subscript.k:51-51`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>`
1001. **rule** `trusted-reference-semantics/semantics/subscript.k:52-52`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> I:Int ~> #toSome => someB(I) ... </k>`
1002. **rule** `trusted-reference-semantics/semantics/subscript.k:54-54`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`
1003. **rule** `trusted-reference-semantics/semantics/subscript.k:55-55`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`
1004. **rule** `trusted-reference-semantics/semantics/subscript.k:56-57`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value`
1005. **rule** `trusted-reference-semantics/semantics/subscript.k:58-60`  
   Flags: operational-rule, priority-rule; attributes: priority(45)
   Source: `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`
1006. **rule** `trusted-reference-semantics/semantics/subscript.k:61-61`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`
1007. **syntax** `trusted-reference-semantics/semantics/subscript.k:63-63`  
   Flags: function-declaration; attributes: function
   Source: `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`
1008. **rule** `trusted-reference-semantics/semantics/subscript.k:64-65`  
   Flags: equational-rule; attributes: none
   Source: `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
1009. **rule** `trusted-reference-semantics/semantics/subscript.k:66-67`  
   Flags: equational-rule; attributes: none
   Source: `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
1010. **rule** `trusted-reference-semantics/semantics/subscript.k:68-71`  
   Flags: equational-rule; attributes: none
   Source: `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) // ==== slice.indices: step / start / stop / clamp ==========================`
1011. **syntax** `trusted-reference-semantics/semantics/subscript.k:72-72`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= slStep(OptInt) [function, total]`
1012. **rule** `trusted-reference-semantics/semantics/subscript.k:73-73`  
   Flags: equational-rule; attributes: none
   Source: `rule slStep(noB)          => 1`
1013. **rule** `trusted-reference-semantics/semantics/subscript.k:74-74`  
   Flags: equational-rule; attributes: none
   Source: `rule slStep(someB(S:Int)) => S`
1014. **syntax** `trusted-reference-semantics/semantics/subscript.k:76-76`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`
1015. **rule** `trusted-reference-semantics/semantics/subscript.k:77-78`  
   Flags: equational-rule; attributes: none
   Source: `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0`
1016. **rule** `trusted-reference-semantics/semantics/subscript.k:79-80`  
   Flags: equational-rule; attributes: none
   Source: `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0`
1017. **rule** `trusted-reference-semantics/semantics/subscript.k:81-81`  
   Flags: equational-rule; attributes: none
   Source: `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`
1018. **syntax** `trusted-reference-semantics/semantics/subscript.k:83-83`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`
1019. **rule** `trusted-reference-semantics/semantics/subscript.k:84-85`  
   Flags: equational-rule; attributes: none
   Source: `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0`
1020. **rule** `trusted-reference-semantics/semantics/subscript.k:86-87`  
   Flags: equational-rule; attributes: none
   Source: `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0`
1021. **rule** `trusted-reference-semantics/semantics/subscript.k:88-88`  
   Flags: equational-rule; attributes: none
   Source: `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`
1022. **syntax** `trusted-reference-semantics/semantics/subscript.k:90-90`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`
1023. **rule** `trusted-reference-semantics/semantics/subscript.k:91-92`  
   Flags: equational-rule; attributes: none
   Source: `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0`
1024. **rule** `trusted-reference-semantics/semantics/subscript.k:93-94`  
   Flags: equational-rule; attributes: none
   Source: `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0`
1025. **syntax** `trusted-reference-semantics/semantics/subscript.k:96-96`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= clampLo(Int, Int) [function, total]`
1026. **rule** `trusted-reference-semantics/semantics/subscript.k:97-98`  
   Flags: equational-rule; attributes: none
   Source: `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0`
1027. **rule** `trusted-reference-semantics/semantics/subscript.k:99-100`  
   Flags: equational-rule; attributes: none
   Source: `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0`
1028. **syntax** `trusted-reference-semantics/semantics/subscript.k:102-102`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= clampHi(Int, Int, Int) [function, total]`
1029. **rule** `trusted-reference-semantics/semantics/subscript.k:103-104`  
   Flags: equational-rule; attributes: none
   Source: `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN`
1030. **rule** `trusted-reference-semantics/semantics/subscript.k:105-108`  
   Flags: equational-rule; attributes: none
   Source: `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN // ==== build the strided sub-sequence (indices in range by construction) ====`
1031. **syntax** `trusted-reference-semantics/semantics/subscript.k:109-109`  
   Flags: function-declaration; attributes: function
   Source: `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`
1032. **rule** `trusted-reference-semantics/semantics/subscript.k:110-112`  
   Flags: equational-rule; attributes: none
   Source: `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
1033. **rule** `trusted-reference-semantics/semantics/subscript.k:113-114`  
   Flags: equational-rule; attributes: none
   Source: `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
1034. **syntax** `trusted-reference-semantics/semantics/subscript.k:116-116`  
   Flags: function-declaration; attributes: function
   Source: `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`
1035. **rule** `trusted-reference-semantics/semantics/subscript.k:117-119`  
   Flags: equational-rule; attributes: none
   Source: `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
1036. **rule** `trusted-reference-semantics/semantics/subscript.k:120-121`  
   Flags: equational-rule; attributes: none
   Source: `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
1037. **endmodule** `trusted-reference-semantics/semantics/subscript.k:122-122`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/syntax.k`

1038. **module** `trusted-reference-semantics/semantics/syntax.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-SYNTAX`
1039. **imports** `trusted-reference-semantics/semantics/syntax.k:4-4`  
   Flags: none; attributes: none
   Source: `imports INT-SYNTAX`
1040. **imports** `trusted-reference-semantics/semantics/syntax.k:5-5`  
   Flags: none; attributes: none
   Source: `imports FLOAT-SYNTAX`
1041. **imports** `trusted-reference-semantics/semantics/syntax.k:6-6`  
   Flags: none; attributes: none
   Source: `imports BOOL-SYNTAX`
1042. **imports** `trusted-reference-semantics/semantics/syntax.k:7-7`  
   Flags: none; attributes: none
   Source: `imports STRING-SYNTAX`
1043. **syntax** `trusted-reference-semantics/semantics/syntax.k:9-30`  
   Flags: macro-declaration; attributes: strict(2), seqstrict(2, 3), macro, macro, strict(1), strict(1)
   Source: `syntax Expr ::= "Int"      "(" Int ")" | "Float"    "(" Float ")" | "Bool"     "(" Bool ")" | "Name"     "(" String ")" | "Str"      "(" String ")" | "UnaryOp"  "(" String "," Expr ")" [strict(2)] | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp"    "(" String "," Exprs ")" | "ListExpr"  "(" Exprs ")" | "DictExpr"  "(" Entries ")" | "ListComp"  "(" Expr "," CompFors ")" [macro] | "GenExp"    "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda"    "(" Params "," Expr ")" | "KwArg"     "(" String "," Expr ")" | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call"      "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare"   "(" Expr "," CmpOp ")"`
1044. **syntax** `trusted-reference-semantics/semantics/syntax.k:32-32`  
   Flags: none; attributes: none
   Source: `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"`
1045. **syntax** `trusted-reference-semantics/semantics/syntax.k:33-33`  
   Flags: none; attributes: none
   Source: `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"`
1046. **syntax** `trusted-reference-semantics/semantics/syntax.k:34-34`  
   Flags: none; attributes: none
   Source: `syntax Entries  ::= List{Entry, ","}`
1047. **syntax** `trusted-reference-semantics/semantics/syntax.k:35-35`  
   Flags: none; attributes: none
   Source: `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`
1048. **syntax** `trusted-reference-semantics/semantics/syntax.k:36-36`  
   Flags: none; attributes: none
   Source: `syntax CompFors ::= List{CompFor, ""}`
1049. **syntax** `trusted-reference-semantics/semantics/syntax.k:37-37`  
   Flags: none; attributes: none
   Source: `syntax Exprs    ::= List{Expr, ","}`
1050. **syntax** `trusted-reference-semantics/semantics/syntax.k:38-38`  
   Flags: none; attributes: none
   Source: `syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`
1051. **syntax** `trusted-reference-semantics/semantics/syntax.k:39-39`  
   Flags: none; attributes: none
   Source: `syntax Bound    ::= Expr | "NoBound"`
1052. **syntax** `trusted-reference-semantics/semantics/syntax.k:41-54`  
   Flags: none; attributes: strict(2), strict(3), strict(2), strict(1), strict, strict, strict
   Source: `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] | "Import"    "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While"     "(" Expr "," Stmts ")" | "Break" | "Continue" | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return"    "(" Expr ")" [strict] | "Assert"    "(" Expr ")" [strict] | "Expr"      "(" Expr ")" [strict] | "FuncDef"   "(" String "," Params "," Stmts ")" | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`
1053. **syntax** `trusted-reference-semantics/semantics/syntax.k:56-56`  
   Flags: none; attributes: none
   Source: `syntax Stmts      ::= List{Stmt, ""}`
1054. **syntax** `trusted-reference-semantics/semantics/syntax.k:57-57`  
   Flags: none; attributes: none
   Source: `syntax Params     ::= "Params" "(" ParamNames ")"`
1055. **syntax** `trusted-reference-semantics/semantics/syntax.k:58-58`  
   Flags: none; attributes: none
   Source: `syntax CellVars   ::= "CellVars" "(" ParamNames ")"`
1056. **syntax** `trusted-reference-semantics/semantics/syntax.k:59-59`  
   Flags: none; attributes: none
   Source: `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"`
1057. **syntax** `trusted-reference-semantics/semantics/syntax.k:60-60`  
   Flags: none; attributes: none
   Source: `syntax ParamNames ::= List{String, ","}`
1058. **syntax** `trusted-reference-semantics/semantics/syntax.k:61-61`  
   Flags: none; attributes: none
   Source: `syntax Module     ::= "Module" "(" Stmts ")"`
1059. **endmodule** `trusted-reference-semantics/semantics/syntax.k:62-62`  
   Flags: none; attributes: none
   Source: `endmodule`

### `trusted-reference-semantics/semantics/tuple.k`

1060. **module** `trusted-reference-semantics/semantics/tuple.k:3-3`  
   Flags: none; attributes: none
   Source: `module MPY-TUPLE`
1061. **imports** `trusted-reference-semantics/semantics/tuple.k:4-4`  
   Flags: none; attributes: none
   Source: `imports MPY-CORE`
1062. **imports** `trusted-reference-semantics/semantics/tuple.k:5-5`  
   Flags: none; attributes: none
   Source: `imports MPY-ITER`
1063. **imports** `trusted-reference-semantics/semantics/tuple.k:6-6`  
   Flags: none; attributes: none
   Source: `imports MPY-LIST`
1064. **imports** `trusted-reference-semantics/semantics/tuple.k:7-9`  
   Flags: none; attributes: none
   Source: `imports MPY-METHODS // ==== iteration (the iterator protocol's tuple case) ======================`
1065. **rule** `trusted-reference-semantics/semantics/tuple.k:10-10`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>`
1066. **rule** `trusted-reference-semantics/semantics/tuple.k:11-13`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================`
1067. **syntax** `trusted-reference-semantics/semantics/tuple.k:14-14`  
   Flags: none; attributes: none
   Source: `syntax ApplyK ::= "toTuple"`
1068. **rule** `trusted-reference-semantics/semantics/tuple.k:15-15`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`
1069. **rule** `trusted-reference-semantics/semantics/tuple.k:16-16`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`
1070. **rule** `trusted-reference-semantics/semantics/tuple.k:18-19`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k)`
1071. **rule** `trusted-reference-semantics/semantics/tuple.k:20-20`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`
1072. **rule** `trusted-reference-semantics/semantics/tuple.k:21-22`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset)`
1073. **rule** `trusted-reference-semantics/semantics/tuple.k:23-23`  
   Flags: equational-rule; attributes: none
   Source: `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`
1074. **syntax** `trusted-reference-semantics/semantics/tuple.k:24-24`  
   Flags: function-declaration; attributes: function
   Source: `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`
1075. **rule** `trusted-reference-semantics/semantics/tuple.k:25-25`  
   Flags: equational-rule; attributes: none
   Source: `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`
1076. **rule** `trusted-reference-semantics/semantics/tuple.k:26-27`  
   Flags: equational-rule; attributes: none
   Source: `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)`
1077. **rule** `trusted-reference-semantics/semantics/tuple.k:28-30`  
   Flags: equational-rule; attributes: none
   Source: `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) // ==== target binding: bind a Name or a TupleExpr target to a value ========`
1078. **syntax** `trusted-reference-semantics/semantics/tuple.k:31-31`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #bindTgt(Expr, Val)`
1079. **rule** `trusted-reference-semantics/semantics/tuple.k:32-34`  
   Flags: operational-rule; attributes: X <- V
   Source: `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
1080. **rule** `trusted-reference-semantics/semantics/tuple.k:35-37`  
   Flags: operational-rule; attributes: X
   Source: `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
1081. **requires** `trusted-reference-semantics/semantics/tuple.k:38-41`  
   Flags: none; attributes: "$cells", X, priority(40)
   Source: `requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
1082. **rule** `trusted-reference-semantics/semantics/tuple.k:42-42`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
1083. **rule** `trusted-reference-semantics/semantics/tuple.k:43-43`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`
1084. **rule** `trusted-reference-semantics/semantics/tuple.k:44-48`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)] // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========`
1085. **syntax** `trusted-reference-semantics/semantics/tuple.k:49-49`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`
1086. **rule** `trusted-reference-semantics/semantics/tuple.k:50-50`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
1087. **rule** `trusted-reference-semantics/semantics/tuple.k:51-51`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`
1088. **rule** `trusted-reference-semantics/semantics/tuple.k:52-54`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
1089. **rule** `trusted-reference-semantics/semantics/tuple.k:55-56`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`
1090. **rule** `trusted-reference-semantics/semantics/tuple.k:57-57`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`
1091. **endmodule** `trusted-reference-semantics/semantics/tuple.k:58-58`  
   Flags: none; attributes: none
   Source: `endmodule`

### `candidate/verification.k`

1092. **requires** `candidate/verification.k:1-1`  
   Flags: none; attributes: none
   Source: `requires "reference-semantics/semantics.k"`
1093. **module** `candidate/verification.k:3-3`  
   Flags: none; attributes: none
   Source: `module VERIFICATION`
1094. **imports** `candidate/verification.k:4-6`  
   Flags: none; attributes: none
   Source: `imports MPY // These two terms are exactly the function bodies emitted in solution.mpy.`
1095. **syntax** `candidate/verification.k:7-7`  
   Flags: macro-declaration; attributes: macro
   Source: `syntax Stmts ::= "#helperBody" [macro]`
1096. **rule** `candidate/verification.k:8-32`  
   Flags: equational-rule; attributes: none
   Source: `rule #helperBody => If( Compare(Name("left"), CmpOp(">=", Name("right"))), Return(Int(0)), .Stmts) If( Compare( Subscript(Name("arr"), Name("left")), CmpOp("!=", Subscript(Name("arr"), Name("right")))), Return( BinOp( "+", Int(1), Call( Name("_smallest_change"), Name("arr"), BinOp("+", Name("left"), Int(1)), BinOp("-", Name("right"), Int(1))))), .Stmts) Return( Call( Name("_smallest_change"), Name("arr"), BinOp("+", Name("left"), Int(1)), BinOp("-", Name("right"), Int(1))))`
1097. **syntax** `candidate/verification.k:34-34`  
   Flags: macro-declaration; attributes: macro
   Source: `syntax Stmts ::= "#mainBody" [macro]`
1098. **rule** `candidate/verification.k:35-41`  
   Flags: equational-rule; attributes: none
   Source: `rule #mainBody => Return( Call( Name("_smallest_change"), Name("arr"), Int(0), BinOp("-", Call(Name("len"), Name("arr")), Int(1))))`
1099. **syntax** `candidate/verification.k:43-43`  
   Flags: macro-declaration; attributes: macro
   Source: `syntax Val ::= "#helperClosure" [macro]`
1100. **rule** `candidate/verification.k:44-45`  
   Flags: equational-rule; attributes: none
   Source: `rule #helperClosure => closureVal(("arr", "left", "right"), #helperBody, 0)`
1101. **syntax** `candidate/verification.k:47-47`  
   Flags: macro-declaration; attributes: macro
   Source: `syntax Val ::= "#mainClosure" [macro]`
1102. **rule** `candidate/verification.k:48-51`  
   Flags: equational-rule; attributes: none
   Source: `rule #mainClosure => closureVal(("arr"), #mainBody, 0) // Mathematical mismatch count for the still-unchecked inclusive interval.`
1103. **syntax** `candidate/verification.k:52-52`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= changeRange(ValSeq, Int, Int) [function, total]`
1104. **rule** `candidate/verification.k:53-54`  
   Flags: equational-rule; attributes: none
   Source: `rule changeRange(_:ValSeq, L:Int, R:Int) => 0 requires L >=Int R`
1105. **rule** `candidate/verification.k:55-63`  
   Flags: equational-rule; attributes: none
   Source: `rule changeRange(VS:ValSeq, L:Int, R:Int) => (#if notBool (valSeqAt(VS, L) ==K valSeqAt(VS, R)) #then 1 #else 0 #fi) +Int changeRange(VS, L +Int 1, R -Int 1) requires L <Int R // One call family covers the public wrapper and the recursive helper. This // lets a single reachability claim serve as the helper's induction // hypothesis while also establishing the required public entry point.`
1106. **syntax** `candidate/verification.k:64-64`  
   Flags: none; attributes: none
   Source: `syntax TargetCall ::= "mainCall" | "helperCall"`
1107. **syntax** `candidate/verification.k:65-72`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #targetCall(TargetCall, Val, Int, Int) // Instrument only the two exact closures above. The following two rules // replace the reference call dispatch with #targetCall. Its rules are the // parameter-substituted control flow of the two exact bodies above. The // marker provides one induction point shared by wrapper and helper while // avoiding the reference semantics' intentionally opaque symbolic // Map:update frame representation.`
1108. **rule** `candidate/verification.k:73-78`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK(toCall(#mainClosure), (ARR:Val, .Vals)) => #targetCall(mainCall, ARR, 0, 0) ... </k> [priority(40)]`
1109. **rule** `candidate/verification.k:79-86`  
   Flags: operational-rule, priority-rule; attributes: priority(40)
   Source: `rule <k> #applyK( toCall(#helperClosure), (ARR:Val, L:Int, R:Int, .Vals)) => #targetCall(helperCall, ARR, L, R) ... </k> [priority(40)]`
1110. **syntax** `candidate/verification.k:88-88`  
   Flags: none; attributes: none
   Source: `syntax KItem ::= #addMismatch(Bool)`
1111. **rule** `candidate/verification.k:90-99`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #targetCall(mainCall, ref(H:Int), _:Int, _:Int) => #targetCall( helperCall, ref(H), 0, vsLen(VS) -Int 1) ... </k> <heap> ... H |-> list(VS:ValSeq) ... </heap>`
1112. **rule** `candidate/verification.k:101-102`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #targetCall(helperCall, _:Val, L:Int, R:Int) => 0 ... </k> requires L >=Int R`
1113. **rule** `candidate/verification.k:104-113`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> #targetCall(helperCall, ref(H:Int), L:Int, R:Int) => #targetCall(helperCall, ref(H), L +Int 1, R -Int 1) ~> #addMismatch( notBool ( valSeqAt(VS, L) ==K valSeqAt(VS, R))) ... </k> <heap> ... H |-> list(VS:ValSeq) ... </heap> requires L <Int R`
1114. **rule** `candidate/verification.k:115-116`  
   Flags: operational-rule; attributes: none
   Source: `rule <k> I:Int ~> #addMismatch(B:Bool) => (#if B #then 1 #else 0 #fi) +Int I ... </k>`
1115. **syntax** `candidate/verification.k:118-118`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Int ::= targetAnswer(TargetCall, ValSeq, Int, Int) [function, total]`
1116. **rule** `candidate/verification.k:119-120`  
   Flags: equational-rule; attributes: none
   Source: `rule targetAnswer(mainCall, VS:ValSeq, _:Int, _:Int) => changeRange(VS, 0, vsLen(VS) -Int 1)`
1117. **rule** `candidate/verification.k:121-122`  
   Flags: equational-rule; attributes: none
   Source: `rule targetAnswer(helperCall, VS:ValSeq, L:Int, R:Int) => changeRange(VS, L, R)`
1118. **syntax** `candidate/verification.k:124-124`  
   Flags: function-declaration, total-declaration; attributes: function, total
   Source: `syntax Bool ::= targetValid(TargetCall, ValSeq, Int, Int) [function, total]`
1119. **rule** `candidate/verification.k:125-125`  
   Flags: equational-rule; attributes: none
   Source: `rule targetValid(mainCall, _:ValSeq, _:Int, _:Int) => true`
1120. **rule** `candidate/verification.k:126-128`  
   Flags: equational-rule; attributes: none
   Source: `rule targetValid(helperCall, VS:ValSeq, L:Int, R:Int) => 0 <=Int L andBool L <=Int vsLen(VS) andBool -1 <=Int R andBool R <Int vsLen(VS)`
1121. **endmodule** `candidate/verification.k:129-129`  
   Flags: none; attributes: none
   Source: `endmodule`

### `candidate/spec.k`

1122. **requires** `candidate/spec.k:1-1`  
   Flags: none; attributes: none
   Source: `requires "verification.k"`
1123. **module** `candidate/spec.k:3-3`  
   Flags: none; attributes: none
   Source: `module SPEC`
1124. **imports** `candidate/spec.k:4-4`  
   Flags: none; attributes: none
   Source: `imports VERIFICATION`
1125. **claim** `candidate/spec.k:6-11`  
   Flags: reachability-claim; attributes: public-entry-bridge
   Source: `claim [public-entry-bridge]: <k> #applyK(toCall(#mainClosure), (ref(H), .Vals)) ~> CONT => #targetCall(mainCall, ref(H), 0, 0) ~> CONT </k>`
1126. **claim** `candidate/spec.k:13-21`  
   Flags: reachability-claim; attributes: helper-entry-bridge
   Source: `claim [helper-entry-bridge]: <k> #applyK( toCall(#helperClosure), (ref(H), L, R, .Vals)) ~> CONT => #targetCall(helperCall, ref(H), L, R) ~> CONT </k>`
1127. **claim** `candidate/spec.k:23-40`  
   Flags: reachability-claim; attributes: smallest-change-correct
   Source: `claim [smallest-change-correct]: <k> #targetCall(KIND:TargetCall, ref(H), L, R) ~> CONT => targetAnswer(KIND, VS, L, R) ~> CONT </k> <env> CALLER </env> <scopes> SCOPES </scopes> <scopeLoc> NEXTSCOPE </scopeLoc> <heap> (H |-> list(VS) HEAPREST) </heap> <heapLoc> NEXTHEAP </heapLoc> <stack> STACK </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires targetValid(KIND, VS, L, R)`
1128. **endmodule** `candidate/spec.k:41-41`  
   Flags: none; attributes: none
   Source: `endmodule`

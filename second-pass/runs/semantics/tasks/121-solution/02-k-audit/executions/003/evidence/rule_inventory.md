# Exhaustive K source inventory

Sources: the trusted supplied semantics copied to clean scratch, plus the candidate `verification.k` and `spec.k`. One row is emitted for every top-level local declaration, context, configuration, rule, or claim.

## Counts

| Kind | Count |
|---|---:|
| claim | 2 |
| configuration | 1 |
| context | 5 |
| endmodule | 27 |
| imports | 88 |
| module | 27 |
| requires | 25 |
| rule | 708 |
| syntax | 233 |

| Attribute | Declaration/rule count |
|---|---:|
| `concrete` | 35 |
| `function` | 148 |
| `macro` | 6 |
| `macro-rec` | 1 |
| `no-evaluators` | 22 |
| `owise` | 26 |
| `priority` | 48 |
| `seqstrict` | 1 |
| `strict` | 2 |
| `symbol` | 25 |
| `total` | 109 |
| `functional` | 0 |
| `simplification` | 0 |

## Inventory

| Location | Kind | Attributes | Audit disposition | Complete compact source |
|---|---|---|---|---|
| `semantics.k:34` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/syntax.k"` |
| `semantics.k:35` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/core.k"` |
| `semantics.k:36` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/iter.k"` |
| `semantics.k:37` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/range.k"` |
| `semantics.k:38` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/operators.k"` |
| `semantics.k:39` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/int.k"` |
| `semantics.k:40` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/bool.k"` |
| `semantics.k:41` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/float.k"` |
| `semantics.k:42` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/str.k"` |
| `semantics.k:43` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/set.k"` |
| `semantics.k:44` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/list.k"` |
| `semantics.k:45` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/tuple.k"` |
| `semantics.k:46` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/subscript.k"` |
| `semantics.k:47` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/comprehension.k"` |
| `semantics.k:48` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/methods.k"` |
| `semantics.k:49` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/controls.k"` |
| `semantics.k:50` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/functions.k"` |
| `semantics.k:51` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/builtins.k"` |
| `semantics.k:52` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/call.k"` |
| `semantics.k:53` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/sort.k"` |
| `semantics.k:54` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/assert.k"` |
| `semantics.k:55` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/dict.k"` |
| `semantics.k:56` | requires | `-` | ASSEMBLY/IMPORT: no rewrite | `requires "semantics/concrete.k"` |
| `semantics.k:58` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY` |
| `semantics.k:59` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics.k:60` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics.k:61` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-RANGE` |
| `semantics.k:62` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-OPERATORS` |
| `semantics.k:63` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-INT` |
| `semantics.k:64` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-BOOL` |
| `semantics.k:65` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-FLOAT` |
| `semantics.k:66` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-STR` |
| `semantics.k:67` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-SET` |
| `semantics.k:68` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-LIST` |
| `semantics.k:69` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-TUPLE` |
| `semantics.k:70` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-SUBSCRIPT` |
| `semantics.k:71` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-COMPREHENSION` |
| `semantics.k:72` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-METHODS` |
| `semantics.k:73` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CONTROLS` |
| `semantics.k:74` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-FUNCTIONS` |
| `semantics.k:75` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-BUILTINS` |
| `semantics.k:76` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CALL` |
| `semantics.k:77` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-SORT` |
| `semantics.k:78` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ASSERT` |
| `semantics.k:79` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-DICT` |
| `semantics.k:80` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics.k:87` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-KRUN` |
| `semantics.k:88` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY` |
| `semantics.k:89` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CONCRETE` |
| `semantics.k:90` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/assert.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-ASSERT` |
| `semantics/assert.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/assert.k:6` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| `semantics/assert.k:8` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| `semantics/assert.k:13` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/assert.k:16` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/bool.k:5` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-BOOL` |
| `semantics/bool.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/bool.k:8` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| `semantics/bool.k:10` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| `semantics/bool.k:11` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| `semantics/bool.k:16` | context | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| `semantics/bool.k:17` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| `semantics/bool.k:18` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| `semantics/bool.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| `semantics/bool.k:22` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| `semantics/bool.k:24` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| `semantics/bool.k:29` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| `semantics/bool.k:31` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `semantics/bool.k:35` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `semantics/bool.k:39` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `semantics/bool.k:43` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `semantics/bool.k:47` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/builtins.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-BUILTINS` |
| `semantics/builtins.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/builtins.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-STR` |
| `semantics/builtins.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-SET` |
| `semantics/builtins.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/builtins.k:8` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-RANGE` |
| `semantics/builtins.k:9` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-INT` |
| `semantics/builtins.k:10` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-METHODS` |
| `semantics/builtins.k:17` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| `semantics/builtins.k:20` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= seqLen(Val) [function]` |
| `semantics/builtins.k:21` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| `semantics/builtins.k:22` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| `semantics/builtins.k:23` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| `semantics/builtins.k:24` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| `semantics/builtins.k:25` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| `semantics/builtins.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| `semantics/builtins.k:32` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| `semantics/builtins.k:33` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| `semantics/builtins.k:34` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| `semantics/builtins.k:35` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| `semantics/builtins.k:36` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| `semantics/builtins.k:37` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule charsOf(.IntSeq)                => .ValSeq` |
| `semantics/builtins.k:38` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| `semantics/builtins.k:41` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| `semantics/builtins.k:44` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| `semantics/builtins.k:47` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| `semantics/builtins.k:48` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| `semantics/builtins.k:49` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| `semantics/builtins.k:50` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| `semantics/builtins.k:54` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= intOf(Val) [function]` |
| `semantics/builtins.k:55` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intOf(I:Int)  => I` |
| `semantics/builtins.k:56` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| `semantics/builtins.k:59` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| `semantics/builtins.k:60` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| `semantics/builtins.k:61` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| `semantics/builtins.k:62` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| `semantics/builtins.k:64` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| `semantics/builtins.k:67` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| `semantics/builtins.k:68` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| `semantics/builtins.k:69` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| `semantics/builtins.k:70` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| `semantics/builtins.k:72` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| `semantics/builtins.k:76` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| `semantics/builtins.k:77` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| `semantics/builtins.k:78` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `semantics/builtins.k:80` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| `semantics/builtins.k:81` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| `semantics/builtins.k:82` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| `semantics/builtins.k:86` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| `semantics/builtins.k:87` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| `semantics/builtins.k:88` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `semantics/builtins.k:90` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| `semantics/builtins.k:91` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| `semantics/builtins.k:92` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| `semantics/builtins.k:97` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= maxVals(Int, Vals) [function]` |
| `semantics/builtins.k:98` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| `semantics/builtins.k:99` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule maxVals(M:Int, .Vals)           => M` |
| `semantics/builtins.k:100` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| `semantics/builtins.k:102` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= minVals(Int, Vals) [function]` |
| `semantics/builtins.k:103` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| `semantics/builtins.k:104` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule minVals(M:Int, .Vals)           => M` |
| `semantics/builtins.k:105` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| `semantics/builtins.k:108` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| `semantics/builtins.k:111` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| `semantics/builtins.k:114` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| `semantics/builtins.k:115` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule binCodes(0) => iCons(48, .IntSeq)` |
| `semantics/builtins.k:116` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| `semantics/builtins.k:117` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| `semantics/builtins.k:118` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule binAcc(0, ACC:IntSeq) => ACC` |
| `semantics/builtins.k:119` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| `semantics/builtins.k:124` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| `semantics/builtins.k:126` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| `semantics/builtins.k:127` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| `semantics/builtins.k:128` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| `semantics/builtins.k:132` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| `semantics/builtins.k:134` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| `semantics/builtins.k:135` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapStrVS(.ValSeq) => .ValSeq` |
| `semantics/builtins.k:136` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| `semantics/builtins.k:137` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| `semantics/builtins.k:140` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| `semantics/builtins.k:143` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| `semantics/builtins.k:144` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| `semantics/builtins.k:148` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| `semantics/builtins.k:149` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| `semantics/builtins.k:152` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| `semantics/builtins.k:156` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| `semantics/builtins.k:158` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| `semantics/builtins.k:159` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| `semantics/builtins.k:160` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| `semantics/builtins.k:163` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| `semantics/builtins.k:164` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| `semantics/builtins.k:167` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| `semantics/builtins.k:169` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| `semantics/builtins.k:170` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| `semantics/builtins.k:171` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| `semantics/builtins.k:173` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| `semantics/builtins.k:174` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| `semantics/builtins.k:177` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| `semantics/builtins.k:178` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| `semantics/builtins.k:179` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| `semantics/builtins.k:187` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| `semantics/builtins.k:188` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= evalArith(IntSeq) [function]` |
| `semantics/builtins.k:189` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| `semantics/builtins.k:192` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| `semantics/builtins.k:194` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= evDigit(Int) [function, total]` |
| `semantics/builtins.k:195` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `semantics/builtins.k:196` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| `semantics/builtins.k:197` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| `semantics/builtins.k:198` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule evHead42(_:IntSeq)            => false [owise]` |
| `semantics/builtins.k:199` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| `semantics/builtins.k:200` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| `semantics/builtins.k:201` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule evHead47(_:IntSeq)            => false [owise]` |
| `semantics/builtins.k:203` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| `semantics/builtins.k:204` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(.IntSeq)                 => .OpSeq` |
| `semantics/builtins.k:205` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| `semantics/builtins.k:206` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| `semantics/builtins.k:207` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| `semantics/builtins.k:208` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| `semantics/builtins.k:209` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| `semantics/builtins.k:210` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| `semantics/builtins.k:211` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| `semantics/builtins.k:212` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| `semantics/builtins.k:214` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| `semantics/builtins.k:216` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokNds(.IntSeq)                => .IntSeq` |
| `semantics/builtins.k:217` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| `semantics/builtins.k:218` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| `semantics/builtins.k:219` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| `semantics/builtins.k:221` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| `semantics/builtins.k:223` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| `semantics/builtins.k:225` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| `semantics/builtins.k:226` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| `semantics/builtins.k:227` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| `semantics/builtins.k:228` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule firstNdE(_:EvPair) => 0 [owise]` |
| `semantics/builtins.k:230` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| `semantics/builtins.k:231` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| `semantics/builtins.k:232` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| `semantics/builtins.k:233` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| `semantics/builtins.k:234` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| `semantics/builtins.k:235` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| `semantics/builtins.k:236` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| `semantics/builtins.k:238` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| `semantics/builtins.k:239` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| `semantics/builtins.k:240` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| `semantics/builtins.k:241` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| `semantics/builtins.k:243` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| `semantics/builtins.k:244` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| `semantics/builtins.k:245` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| `semantics/builtins.k:246` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| `semantics/builtins.k:247` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| `semantics/builtins.k:248` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| `semantics/builtins.k:250` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| `semantics/builtins.k:251` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `semantics/builtins.k:252` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `semantics/builtins.k:253` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `semantics/builtins.k:254` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `semantics/builtins.k:255` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| `semantics/builtins.k:256` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| `semantics/builtins.k:257` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| `semantics/builtins.k:260` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| `semantics/builtins.k:263` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| `semantics/builtins.k:265` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| `semantics/builtins.k:266` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| `semantics/builtins.k:267` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| `semantics/builtins.k:268` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule inLevelE(_:String, _:String) => false [owise]` |
| `semantics/builtins.k:269` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| `semantics/builtins.k:270` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| `semantics/builtins.k:271` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| `semantics/builtins.k:272` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| `semantics/builtins.k:273` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| `semantics/builtins.k:274` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| `semantics/builtins.k:279` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= "#md5"` |
| `semantics/builtins.k:280` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| `semantics/builtins.k:282` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| `semantics/builtins.k:283` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= md5Obj(IntSeq)` |
| `semantics/builtins.k:284` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| `semantics/builtins.k:285` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| `semantics/builtins.k:291` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| `semantics/builtins.k:292` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| `semantics/builtins.k:293` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| `semantics/builtins.k:294` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isIntV(_:Int)         => true` |
| `semantics/builtins.k:295` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isIntV(_:Val)         => false [owise]` |
| `semantics/builtins.k:296` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isStrV(str(_:IntSeq)) => true` |
| `semantics/builtins.k:297` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isStrV(_:Val)         => false [owise]` |
| `semantics/builtins.k:298` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/call.k:10` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-CALL` |
| `semantics/call.k:11` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-METHODS` |
| `semantics/call.k:12` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-BUILTINS` |
| `semantics/call.k:13` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-FUNCTIONS` |
| `semantics/call.k:16` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| `semantics/call.k:19` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= #callee(Exprs)` |
| `semantics/call.k:20` | rule | `owise` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| `semantics/call.k:21` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| `semantics/call.k:24` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| `semantics/call.k:26` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| `semantics/call.k:27` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| `semantics/call.k:28` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| `semantics/call.k:29` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| `semantics/call.k:30` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| `semantics/call.k:31` | rule | `owise` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| `semantics/call.k:32` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| `semantics/call.k:38` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/call.k:42` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| `semantics/call.k:47` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/call.k:52` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isMutMethod(String) [function, total]` |
| `semantics/call.k:53` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| `semantics/call.k:56` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| `semantics/call.k:63` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| `semantics/call.k:69` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| `semantics/call.k:80` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| `semantics/call.k:87` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #allocCells(ParamNames)` |
| `semantics/call.k:88` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| `semantics/call.k:89` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| `semantics/call.k:95` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/comprehension.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-COMPREHENSION` |
| `semantics/comprehension.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/comprehension.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-OPERATORS` |
| `semantics/comprehension.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-LIST` |
| `semantics/comprehension.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CONTROLS` |
| `semantics/comprehension.k:8` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-FUNCTIONS` |
| `semantics/comprehension.k:11` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `semantics/comprehension.k:12` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `semantics/comprehension.k:14` | syntax | `macro` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| `semantics/comprehension.k:15` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| `semantics/comprehension.k:18` | syntax | `macro-rec` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| `semantics/comprehension.k:19` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| `semantics/comprehension.k:21` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| `semantics/comprehension.k:24` | syntax | `macro` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Expr ::= compGuard(Exprs) [macro]` |
| `semantics/comprehension.k:25` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule compGuard(.Exprs)             => Bool(true)` |
| `semantics/comprehension.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| `semantics/comprehension.k:27` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/concrete.k:8` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-CONCRETE` |
| `semantics/concrete.k:9` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY` |
| `semantics/concrete.k:13` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| `semantics/concrete.k:16` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| `semantics/concrete.k:25` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= kvP(Val, Val)` |
| `semantics/concrete.k:26` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| `semantics/concrete.k:28` | rule | `priority` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| `semantics/concrete.k:31` | rule | `priority` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| `semantics/concrete.k:34` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| `semantics/concrete.k:36` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| `semantics/concrete.k:38` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| `semantics/concrete.k:42` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| `semantics/concrete.k:43` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| `semantics/concrete.k:44` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| `semantics/concrete.k:47` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| `semantics/concrete.k:51` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= kLt(Val, Val) [function]` |
| `semantics/concrete.k:52` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| `semantics/concrete.k:53` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| `semantics/concrete.k:54` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `semantics/concrete.k:56` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| `semantics/concrete.k:57` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule unpairVS(.ValSeq) => .ValSeq` |
| `semantics/concrete.k:58` | rule | `-` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| `semantics/concrete.k:59` | rule | `owise` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| `semantics/concrete.k:60` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/controls.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-CONTROLS` |
| `semantics/controls.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/controls.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-TUPLE` |
| `semantics/controls.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/controls.k:9` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `semantics/controls.k:12` | rule | `priority` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `semantics/controls.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| `semantics/controls.k:27` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` |
| `semantics/controls.k:35` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| `semantics/controls.k:36` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| `semantics/controls.k:37` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #bindImports(ParamNames)` |
| `semantics/controls.k:38` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| `semantics/controls.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| `semantics/controls.k:43` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| `semantics/controls.k:48` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Expr(_:Val) => .K ... </k>` |
| `semantics/controls.k:51` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| `semantics/controls.k:52` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| `semantics/controls.k:53` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| `semantics/controls.k:54` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| `semantics/controls.k:57` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| `semantics/controls.k:59` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| `semantics/controls.k:65` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| `semantics/controls.k:69` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| `semantics/controls.k:71` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| `semantics/controls.k:72` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| `semantics/controls.k:73` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| `semantics/controls.k:77` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| `semantics/controls.k:78` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| `semantics/controls.k:79` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| `semantics/controls.k:81` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| `semantics/controls.k:85` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `semantics/controls.k:86` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Continue => #cont ... </k>` |
| `semantics/controls.k:87` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Break => #brk ... </k>` |
| `semantics/controls.k:88` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `semantics/controls.k:89` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| `semantics/controls.k:90` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| `semantics/controls.k:91` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| `semantics/controls.k:95` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/controls.k:98` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/controls.k:101` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/controls.k:106` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/controls.k:109` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/core.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-CORE` |
| `semantics/core.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-SYNTAX` |
| `semantics/core.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports INT` |
| `semantics/core.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports BOOL` |
| `semantics/core.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports STRING` |
| `semantics/core.k:8` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MAP` |
| `semantics/core.k:9` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports LIST` |
| `semantics/core.k:10` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports K-EQUAL` |
| `semantics/core.k:13` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| `semantics/core.k:14` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| `semantics/core.k:15` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Str    ::= str(IntSeq)` |
| `semantics/core.k:18` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| `semantics/core.k:25` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int)          // a heap object: <heap> holds its list(VS) \| cellRef(Int)      // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String)     // a type object (int/str), resolved from the builtins frame \| builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String)   // a cooled Attribute: obj.method` |
| `semantics/core.k:36` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Parent   ::= "root" \| parent(Int)` |
| `semantics/core.k:37` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Scope    ::= scope(Map, Parent)` |
| `semantics/core.k:38` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KResult  ::= Val` |
| `semantics/core.k:39` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Expr     ::= Val   // cooling puts results back into expression holes` |
| `semantics/core.k:40` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Vals     ::= List{Val, ","}` |
| `semantics/core.k:41` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| `semantics/core.k:42` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax RetState ::= "noRet" \| retV(Val)` |
| `semantics/core.k:49` | configuration | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>` |
| `semantics/core.k:68` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isRefV(Val) [function, total]` |
| `semantics/core.k:69` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isRefV(ref(_:Int)) => true` |
| `semantics/core.k:70` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isRefV(_:Val)      => false [owise]` |
| `semantics/core.k:75` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax HeapVal ::= cellV(Val)` |
| `semantics/core.k:76` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isCellRef(Val) [function, total]` |
| `semantics/core.k:77` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isCellRef(cellRef(_:Int)) => true` |
| `semantics/core.k:78` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isCellRef(_:Val)          => false [owise]` |
| `semantics/core.k:85` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| `semantics/core.k:95` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= kwV(String, Val)` |
| `semantics/core.k:96` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #kwTag(String)` |
| `semantics/core.k:97` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| `semantics/core.k:98` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| `semantics/core.k:100` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isKwV(Val) [function, total]` |
| `semantics/core.k:101` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isKwV(kwV(_:String, _:Val)) => true` |
| `semantics/core.k:102` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isKwV(_:Val)                => false [owise]` |
| `semantics/core.k:106` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= cellsMark(ParamNames)` |
| `semantics/core.k:107` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ParamNames ::= cellsOf(Val) [function]` |
| `semantics/core.k:108` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| `semantics/core.k:109` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| `semantics/core.k:110` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule pnMember(_:String, .ParamNames) => false` |
| `semantics/core.k:111` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| `semantics/core.k:113` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #cellW(Val, Val)` |
| `semantics/core.k:114` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| `semantics/core.k:117` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= #alloc(Val)` |
| `semantics/core.k:118` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| `semantics/core.k:124` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #loadAll(Module)` |
| `semantics/core.k:125` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| `semantics/core.k:126` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| `semantics/core.k:127` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> .Stmts => .K ... </k>` |
| `semantics/core.k:130` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= #look(String, Int)` |
| `semantics/core.k:131` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| `semantics/core.k:132` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| `semantics/core.k:145` | rule | `priority` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| `semantics/core.k:152` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| `semantics/core.k:157` | syntax | `function,total` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Scope ::= "builtinsScope" [function, total]` |
| `semantics/core.k:158` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)` |
| `semantics/core.k:185` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax ApplyK ::= toCall(Val)` |
| `semantics/core.k:186` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| `semantics/core.k:189` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| `semantics/core.k:190` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| `semantics/core.k:191` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| `semantics/core.k:194` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Int(I:Int)   => I ... </k>` |
| `semantics/core.k:195` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Bool(B:Bool) => B ... </k>` |
| `semantics/core.k:196` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> NoneVal      => noneV ... </k>` |
| `semantics/core.k:199` | syntax | `function` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Bool ::= truthy(Val) [function]` |
| `semantics/core.k:200` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule truthy(B:Bool)          => B` |
| `semantics/core.k:201` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule truthy(noneV)           => false` |
| `semantics/core.k:202` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule truthy(I:Int)           => I =/=Int 0` |
| `semantics/core.k:203` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| `semantics/core.k:204` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| `semantics/core.k:205` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| `semantics/core.k:208` | syntax | `function` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Val  ::= applyUn(String, Val) [function]` |
| `semantics/core.k:209` | syntax | `function` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| `semantics/core.k:210` | syntax | `function` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| `semantics/core.k:213` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| `semantics/core.k:214` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| `semantics/core.k:215` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| `semantics/core.k:217` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| `semantics/core.k:218` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule vals2valSeq(.Vals)            => .ValSeq` |
| `semantics/core.k:219` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| `semantics/core.k:223` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| `semantics/core.k:224` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule vsLen(.ValSeq)                => 0` |
| `semantics/core.k:225` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| `semantics/core.k:227` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= isLen(IntSeq) [function, total]` |
| `semantics/core.k:228` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isLen(.IntSeq)                => 0` |
| `semantics/core.k:229` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| `semantics/core.k:233` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| `semantics/core.k:234` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| `semantics/core.k:235` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| `semantics/core.k:236` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| `semantics/core.k:238` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0` |
| `semantics/core.k:240` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/dict.k:13` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-DICT` |
| `semantics/dict.k:14` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/dict.k:15` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/dict.k:16` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-METHODS` |
| `semantics/dict.k:17` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-LIST` |
| `semantics/dict.k:20` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| `semantics/dict.k:23` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| `semantics/dict.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| `semantics/dict.k:27` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| `semantics/dict.k:28` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| `semantics/dict.k:30` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| `semantics/dict.k:32` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| `semantics/dict.k:37` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| `semantics/dict.k:38` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dHasKey(.ValSeq, _:Val)                => false` |
| `semantics/dict.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| `semantics/dict.k:40` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| `semantics/dict.k:43` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| `semantics/dict.k:44` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| `semantics/dict.k:45` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| `semantics/dict.k:49` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| `semantics/dict.k:50` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K` |
| `semantics/dict.k:52` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| `semantics/dict.k:54` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| `semantics/dict.k:58` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| `semantics/dict.k:63` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| `semantics/dict.k:64` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| `semantics/dict.k:65` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| `semantics/dict.k:70` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| `semantics/dict.k:71` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| `semantics/dict.k:76` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #dsetK(String, Val)` |
| `semantics/dict.k:77` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| `semantics/dict.k:78` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| `semantics/dict.k:82` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| `semantics/dict.k:86` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| `semantics/dict.k:87` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| `semantics/dict.k:90` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| `semantics/dict.k:91` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| `semantics/dict.k:92` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| `semantics/dict.k:95` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| `semantics/dict.k:97` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| `semantics/dict.k:98` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| `semantics/dict.k:99` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| `semantics/dict.k:101` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| `semantics/dict.k:102` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| `semantics/dict.k:103` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| `semantics/dict.k:104` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/float.k:14` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-FLOAT` |
| `semantics/float.k:15` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-OPERATORS` |
| `semantics/float.k:16` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-BUILTINS` |
| `semantics/float.k:17` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports FLOAT` |
| `semantics/float.k:20` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= Float` |
| `semantics/float.k:21` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Float(F:Float) => F ... </k>` |
| `semantics/float.k:24` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| `semantics/float.k:25` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| `semantics/float.k:27` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| `semantics/float.k:30` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| `semantics/float.k:31` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| `semantics/float.k:32` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| `semantics/float.k:37` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| `semantics/float.k:38` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| `semantics/float.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| `semantics/float.k:43` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| `semantics/float.k:44` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| `semantics/float.k:50` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| `semantics/float.k:51` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| `semantics/float.k:52` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| `semantics/float.k:54` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| `semantics/float.k:55` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule absF(F:Float) => absFloat(F) [concrete]` |
| `semantics/float.k:56` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| `semantics/float.k:61` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Import(_:String) => .K ... </k>` |
| `semantics/float.k:65` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= "#mathCeil"` |
| `semantics/float.k:66` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| `semantics/float.k:67` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| `semantics/float.k:70` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= "#mathFloor"` |
| `semantics/float.k:71` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| `semantics/float.k:72` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| `semantics/float.k:73` | syntax | `function,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| `semantics/float.k:74` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule floorFI(I:Int)   => I                        [concrete]` |
| `semantics/float.k:75` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| `semantics/float.k:78` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| `semantics/float.k:79` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| `semantics/float.k:82` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| `semantics/float.k:83` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| `semantics/float.k:84` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| `semantics/float.k:85` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| `semantics/float.k:86` | syntax | `function,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| `semantics/float.k:87` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule toF(F:Float) => F        [concrete]` |
| `semantics/float.k:88` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule toF(I:Int)   => intToF(I) [concrete]` |
| `semantics/float.k:93` | syntax | `function,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| `semantics/float.k:94` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule ceilF(I:Int)   => I                       [concrete]` |
| `semantics/float.k:95` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| `semantics/float.k:99` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| `semantics/float.k:103` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| `semantics/float.k:104` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| `semantics/float.k:105` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| `semantics/float.k:107` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| `semantics/float.k:108` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| `semantics/float.k:109` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| `semantics/float.k:111` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| `semantics/float.k:112` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| `semantics/float.k:113` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| `semantics/float.k:115` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| `semantics/float.k:116` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| `semantics/float.k:117` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| `semantics/float.k:119` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| `semantics/float.k:120` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| `semantics/float.k:121` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| `semantics/float.k:125` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| `semantics/float.k:126` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| `semantics/float.k:127` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| `semantics/float.k:128` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| `semantics/float.k:129` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| `semantics/float.k:132` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| `semantics/float.k:133` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| `semantics/float.k:134` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| `semantics/float.k:135` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| `semantics/float.k:136` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| `semantics/float.k:137` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| `semantics/float.k:138` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| `semantics/float.k:139` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| `semantics/float.k:142` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| `semantics/float.k:143` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| `semantics/float.k:144` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| `semantics/float.k:145` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| `semantics/float.k:146` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| `semantics/float.k:147` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| `semantics/float.k:148` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` |
| `semantics/float.k:149` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` |
| `semantics/float.k:150` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` |
| `semantics/float.k:151` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` |
| `semantics/float.k:154` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| `semantics/float.k:155` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| `semantics/float.k:160` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| `semantics/float.k:161` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| `semantics/float.k:162` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| `semantics/float.k:165` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= headIS(IntSeq) [function]` |
| `semantics/float.k:166` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| `semantics/float.k:167` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k:168` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| `semantics/float.k:169` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intPartAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k:170` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| `semantics/float.k:171` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| `semantics/float.k:173` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k:174` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracPart(.IntSeq) => 0` |
| `semantics/float.k:175` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| `semantics/float.k:176` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| `semantics/float.k:177` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k:178` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| `semantics/float.k:179` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k:180` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracScale(.IntSeq) => 1` |
| `semantics/float.k:181` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| `semantics/float.k:182` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| `semantics/float.k:183` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fscAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k:184` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| `semantics/float.k:185` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| `semantics/float.k:186` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| `semantics/float.k:187` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| `semantics/float.k:190` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| `semantics/float.k:191` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| `semantics/float.k:192` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| `semantics/float.k:195` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| `semantics/float.k:196` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| `semantics/float.k:197` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| `semantics/float.k:198` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| `semantics/float.k:199` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| `semantics/float.k:200` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| `semantics/float.k:201` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| `semantics/float.k:202` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| `semantics/float.k:203` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| `semantics/float.k:204` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| `semantics/float.k:205` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| `semantics/float.k:206` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| `semantics/float.k:209` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| `semantics/float.k:210` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| `semantics/float.k:211` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| `semantics/float.k:213` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| `semantics/float.k:214` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| `semantics/float.k:217` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| `semantics/float.k:218` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| `semantics/float.k:223` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| `semantics/float.k:224` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| `semantics/float.k:227` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| `semantics/float.k:228` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| `semantics/float.k:230` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| `semantics/float.k:231` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| `semantics/float.k:232` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= "#mathSqrt"` |
| `semantics/float.k:233` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| `semantics/float.k:234` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| `semantics/float.k:235` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| `semantics/float.k:243` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| `semantics/float.k:244` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `semantics/float.k:245` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| `semantics/float.k:246` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| `semantics/float.k:247` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| `semantics/float.k:250` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| `semantics/float.k:251` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `semantics/float.k:252` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| `semantics/float.k:253` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| `semantics/float.k:254` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| `semantics/float.k:261` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| `semantics/float.k:262` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| `semantics/float.k:265` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| `semantics/float.k:266` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| `semantics/float.k:267` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| `semantics/float.k:270` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| `semantics/float.k:273` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/functions.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-FUNCTIONS` |
| `semantics/functions.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/functions.k:8` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` |
| `semantics/functions.k:14` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| `semantics/functions.k:18` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| `semantics/functions.k:19` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| `semantics/functions.k:27` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| `semantics/functions.k:31` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| `semantics/functions.k:33` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| `semantics/functions.k:36` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `semantics/functions.k:42` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| `semantics/functions.k:47` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| `semantics/functions.k:50` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| `semantics/functions.k:53` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `semantics/functions.k:59` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| `semantics/functions.k:63` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| `semantics/functions.k:64` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| `semantics/functions.k:68` | rule | `priority` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` |
| `semantics/functions.k:78` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| `semantics/functions.k:80` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| `semantics/functions.k:85` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| `semantics/functions.k:91` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/int.k:4` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-INT` |
| `semantics/int.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/int.k:7` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyUn("-", I:Int) => 0 -Int I` |
| `semantics/int.k:9` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| `semantics/int.k:11` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| `semantics/int.k:12` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| `semantics/int.k:13` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| `semantics/int.k:14` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| `semantics/int.k:15` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| `semantics/int.k:16` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| `semantics/int.k:17` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| `semantics/int.k:19` | syntax | `function` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Int ::= pyMod(Int, Int) [function]` |
| `semantics/int.k:20` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| `semantics/int.k:22` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| `semantics/int.k:23` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| `semantics/int.k:24` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| `semantics/int.k:25` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| `semantics/int.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| `semantics/int.k:27` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |
| `semantics/int.k:28` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/iter.k:6` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-ITER` |
| `semantics/iter.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/iter.k:8` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| `semantics/iter.k:9` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/list.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-LIST` |
| `semantics/list.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/list.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/list.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-OPERATORS` |
| `semantics/list.k:9` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| `semantics/list.k:10` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| `semantics/list.k:13` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ApplyK ::= "toList"` |
| `semantics/list.k:14` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| `semantics/list.k:15` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| `semantics/list.k:18` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| `semantics/list.k:19` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| `semantics/list.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| `semantics/list.k:24` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| `semantics/list.k:27` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| `semantics/list.k:28` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| `semantics/list.k:33` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| `semantics/list.k:34` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule hasRefVS(.ValSeq)                => false` |
| `semantics/list.k:35` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| `semantics/list.k:37` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function]` |
| `semantics/list.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| `semantics/list.k:40` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| `semantics/list.k:41` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| `semantics/list.k:42` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| `semantics/list.k:45` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| `semantics/list.k:47` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| `semantics/list.k:49` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| `semantics/list.k:50` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| `semantics/list.k:53` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| `semantics/list.k:58` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| `semantics/list.k:59` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| `semantics/list.k:60` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| `semantics/list.k:61` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| `semantics/list.k:62` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| `semantics/list.k:63` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| `semantics/list.k:65` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| `semantics/list.k:67` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| `semantics/list.k:68` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/methods.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-METHODS` |
| `semantics/methods.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/methods.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports K-EQUAL` |
| `semantics/methods.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-STR` |
| `semantics/methods.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-LIST` |
| `semantics/methods.k:10` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| `semantics/methods.k:13` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| `semantics/methods.k:14` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| `semantics/methods.k:15` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| `semantics/methods.k:16` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| `semantics/methods.k:19` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| `semantics/methods.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| `semantics/methods.k:21` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| `semantics/methods.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| `semantics/methods.k:27` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| `semantics/methods.k:28` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| `semantics/methods.k:29` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| `semantics/methods.k:30` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| `semantics/methods.k:34` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| `semantics/methods.k:35` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| `semantics/methods.k:36` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| `semantics/methods.k:37` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| `semantics/methods.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| `semantics/methods.k:41` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| `semantics/methods.k:42` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| `semantics/methods.k:43` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| `semantics/methods.k:44` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| `semantics/methods.k:47` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| `semantics/methods.k:48` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| `semantics/methods.k:49` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule trimWS(.IntSeq) => .IntSeq` |
| `semantics/methods.k:50` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| `semantics/methods.k:51` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| `semantics/methods.k:52` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| `semantics/methods.k:53` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| `semantics/methods.k:54` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| `semantics/methods.k:55` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| `semantics/methods.k:58` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| `semantics/methods.k:61` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| `semantics/methods.k:64` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| `semantics/methods.k:65` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| `semantics/methods.k:66` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| `semantics/methods.k:67` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| `semantics/methods.k:68` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| `semantics/methods.k:72` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| `semantics/methods.k:75` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result` |
| `semantics/methods.k:76` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| `semantics/methods.k:77` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| `semantics/methods.k:79` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| `semantics/methods.k:82` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| `semantics/methods.k:83` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| `semantics/methods.k:84` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| `semantics/methods.k:85` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isWSC(Int) [function, total]` |
| `semantics/methods.k:86` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| `semantics/methods.k:89` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| `semantics/methods.k:94` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| `semantics/methods.k:97` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token` |
| `semantics/methods.k:98` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| `semantics/methods.k:99` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| `semantics/methods.k:101` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| `semantics/methods.k:104` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| `semantics/methods.k:106` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| `semantics/methods.k:107` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| `semantics/methods.k:108` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| `semantics/methods.k:109` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| `semantics/methods.k:112` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isUpperC(Int) [function, total]` |
| `semantics/methods.k:113` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| `semantics/methods.k:115` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isLowerC(Int) [function, total]` |
| `semantics/methods.k:116` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| `semantics/methods.k:118` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| `semantics/methods.k:119` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| `semantics/methods.k:121` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= isDigitC(Int) [function, total]` |
| `semantics/methods.k:122` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `semantics/methods.k:124` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| `semantics/methods.k:125` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule hasUpper(.IntSeq) => false` |
| `semantics/methods.k:126` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| `semantics/methods.k:128` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| `semantics/methods.k:129` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule hasLower(.IntSeq) => false` |
| `semantics/methods.k:130` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| `semantics/methods.k:132` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| `semantics/methods.k:133` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule allAlpha(.IntSeq) => true` |
| `semantics/methods.k:134` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| `semantics/methods.k:136` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| `semantics/methods.k:137` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule allDigit(.IntSeq) => true` |
| `semantics/methods.k:138` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| `semantics/methods.k:140` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= lowerC(Int) [function, total]` |
| `semantics/methods.k:142` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `semantics/methods.k:143` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule lowerC(C:Int) => C         [owise]` |
| `semantics/methods.k:145` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= upperC(Int) [function, total]` |
| `semantics/methods.k:146` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `semantics/methods.k:147` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule upperC(C:Int) => C         [owise]` |
| `semantics/methods.k:149` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= swapC(Int) [function, total]` |
| `semantics/methods.k:150` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `semantics/methods.k:151` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `semantics/methods.k:152` | rule | `owise` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule swapC(C:Int) => C         [owise]` |
| `semantics/methods.k:154` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| `semantics/methods.k:155` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapLower(.IntSeq) => .IntSeq` |
| `semantics/methods.k:156` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| `semantics/methods.k:158` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| `semantics/methods.k:159` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapUpper(.IntSeq) => .IntSeq` |
| `semantics/methods.k:160` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| `semantics/methods.k:162` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| `semantics/methods.k:163` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapSwap(.IntSeq) => .IntSeq` |
| `semantics/methods.k:164` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| `semantics/methods.k:166` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| `semantics/methods.k:167` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| `semantics/methods.k:168` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/methods.k:169` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| `semantics/methods.k:170` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/operators.k:6` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-OPERATORS` |
| `semantics/operators.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/operators.k:8` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/operators.k:10` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| `semantics/operators.k:12` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| `semantics/operators.k:15` | context | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `context Compare(HOLE, _)` |
| `semantics/operators.k:16` | context | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `context Compare(_:Val, CmpOp(_, HOLE))` |
| `semantics/operators.k:17` | rule | `owise` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| `semantics/operators.k:19` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| `semantics/operators.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| `semantics/operators.k:25` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/operators.k:28` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| `semantics/operators.k:34` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| `semantics/operators.k:38` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| `semantics/operators.k:44` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/operators.k:47` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/range.k:5` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-RANGE` |
| `semantics/range.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/range.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/range.k:9` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| `semantics/range.k:10` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| `semantics/range.k:12` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| `semantics/range.k:13` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| `semantics/range.k:15` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| `semantics/range.k:17` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| `semantics/range.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| `semantics/range.k:23` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| `semantics/range.k:25` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/set.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-SET` |
| `semantics/set.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/set.k:8` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= setV(IntSeq)` |
| `semantics/set.k:11` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| `semantics/set.k:12` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule codeIn(_:Int, .IntSeq)                => false` |
| `semantics/set.k:13` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| `semantics/set.k:16` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total]` |
| `semantics/set.k:18` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| `semantics/set.k:19` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| `semantics/set.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| `semantics/set.k:22` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| `semantics/set.k:25` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| `semantics/set.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| `semantics/set.k:27` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| `semantics/set.k:31` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| `semantics/set.k:32` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| `semantics/set.k:33` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| `semantics/set.k:35` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| `semantics/set.k:36` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| `semantics/set.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| `semantics/set.k:40` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/sort.k:10` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-SORT` |
| `semantics/sort.k:11` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-BUILTINS` |
| `semantics/sort.k:12` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-SUBSCRIPT` |
| `semantics/sort.k:18` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| `semantics/sort.k:19` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| `semantics/sort.k:20` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| `semantics/sort.k:21` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| `semantics/sort.k:22` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| `semantics/sort.k:23` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| `semantics/sort.k:24` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| `semantics/sort.k:26` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| `semantics/sort.k:27` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| `semantics/sort.k:28` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| `semantics/sort.k:29` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| `semantics/sort.k:31` | rule | `concrete` | FIXED-CONCRETE-ONLY: absent from Haskell proof definition | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| `semantics/sort.k:36` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| `semantics/sort.k:40` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| `semantics/sort.k:49` | syntax | `function,no-evaluators,symbol,total` | FIXED-OPAQUE-UNUSED: explicit trust boundary, unreachable here | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| `semantics/sort.k:51` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| `semantics/sort.k:53` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| `semantics/sort.k:54` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| `semantics/sort.k:55` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| `semantics/sort.k:57` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| `semantics/sort.k:58` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule condRev(S:ValSeq, false) => S` |
| `semantics/sort.k:59` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| `semantics/sort.k:61` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| `semantics/sort.k:63` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| `semantics/sort.k:65` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |
| `semantics/sort.k:72` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/str.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-STR` |
| `semantics/str.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/str.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/str.k:8` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| `semantics/str.k:9` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| `semantics/str.k:13` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= strToCodes(String) [function]` |
| `semantics/str.k:14` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| `semantics/str.k:15` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strToCodes("") => .IntSeq` |
| `semantics/str.k:16` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| `semantics/str.k:20` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:21` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| `semantics/str.k:22` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| `semantics/str.k:24` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| `semantics/str.k:25` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| `semantics/str.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| `semantics/str.k:29` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| `semantics/str.k:30` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| `semantics/str.k:32` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:33` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| `semantics/str.k:34` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/str.k:35` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| `semantics/str.k:37` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:38` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| `semantics/str.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| `semantics/str.k:40` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| `semantics/str.k:48` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:49` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strLt(.IntSeq, .IntSeq)                => false` |
| `semantics/str.k:50` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| `semantics/str.k:51` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/str.k:52` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| `semantics/str.k:53` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| `semantics/str.k:54` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| `semantics/str.k:56` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `semantics/str.k:57` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| `semantics/str.k:58` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| `semantics/str.k:59` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| `semantics/str.k:60` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/subscript.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-SUBSCRIPT` |
| `semantics/subscript.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/subscript.k:11` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| `semantics/subscript.k:12` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| `semantics/subscript.k:13` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| `semantics/subscript.k:16` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| `semantics/subscript.k:17` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| `semantics/subscript.k:18` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| `semantics/subscript.k:21` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| `semantics/subscript.k:22` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| `semantics/subscript.k:23` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| `semantics/subscript.k:27` | context | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `context Subscript(HOLE, _)` |
| `semantics/subscript.k:28` | context | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `context Subscript(_:Val, HOLE:Expr)` |
| `semantics/subscript.k:31` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/subscript.k:35` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| `semantics/subscript.k:37` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= applyIndex(Val, Int) [function]` |
| `semantics/subscript.k:38` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `semantics/subscript.k:39` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `semantics/subscript.k:40` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| `semantics/subscript.k:44` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| `semantics/subscript.k:49` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax OptInt ::= "noB" \| someB(Int)` |
| `semantics/subscript.k:50` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| `semantics/subscript.k:51` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| `semantics/subscript.k:52` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| `semantics/subscript.k:54` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| `semantics/subscript.k:55` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| `semantics/subscript.k:56` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| `semantics/subscript.k:58` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| `semantics/subscript.k:61` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| `semantics/subscript.k:63` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| `semantics/subscript.k:64` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `semantics/subscript.k:66` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `semantics/subscript.k:68` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| `semantics/subscript.k:72` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= slStep(OptInt) [function, total]` |
| `semantics/subscript.k:73` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStep(noB)          => 1` |
| `semantics/subscript.k:74` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStep(someB(S:Int)) => S` |
| `semantics/subscript.k:76` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| `semantics/subscript.k:77` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| `semantics/subscript.k:79` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0` |
| `semantics/subscript.k:81` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| `semantics/subscript.k:83` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| `semantics/subscript.k:84` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0` |
| `semantics/subscript.k:86` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| `semantics/subscript.k:88` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| `semantics/subscript.k:90` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| `semantics/subscript.k:91` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0` |
| `semantics/subscript.k:93` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| `semantics/subscript.k:96` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| `semantics/subscript.k:97` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| `semantics/subscript.k:99` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| `semantics/subscript.k:102` | syntax | `function,total` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| `semantics/subscript.k:103` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN` |
| `semantics/subscript.k:105` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| `semantics/subscript.k:109` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| `semantics/subscript.k:110` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `semantics/subscript.k:113` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `semantics/subscript.k:116` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| `semantics/subscript.k:117` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `semantics/subscript.k:120` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `semantics/subscript.k:122` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/syntax.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-SYNTAX` |
| `semantics/syntax.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports INT-SYNTAX` |
| `semantics/syntax.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports FLOAT-SYNTAX` |
| `semantics/syntax.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports BOOL-SYNTAX` |
| `semantics/syntax.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports STRING-SYNTAX` |
| `semantics/syntax.k:9` | syntax | `macro,seqstrict,strict` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp"    "(" String "," Exprs ")" \| "ListExpr"  "(" Exprs ")" \| "DictExpr"  "(" Entries ")" \| "ListComp"  "(" Expr "," CompFors ")" [macro] \| "GenExp"    "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda"    "(" Params "," Expr ")" \| "KwArg"     "(" String "," Expr ")" \| "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call"      "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare"   "(" Expr "," CmpOp ")"` |
| `semantics/syntax.k:32` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| `semantics/syntax.k:33` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| `semantics/syntax.k:34` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Entries  ::= List{Entry, ","}` |
| `semantics/syntax.k:35` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| `semantics/syntax.k:36` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax CompFors ::= List{CompFor, ""}` |
| `semantics/syntax.k:37` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Exprs    ::= List{Expr, ","}` |
| `semantics/syntax.k:38` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| `semantics/syntax.k:39` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Bound    ::= Expr \| "NoBound"` |
| `semantics/syntax.k:41` | syntax | `strict` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While"     "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return"    "(" Expr ")" [strict] \| "Assert"    "(" Expr ")" [strict] \| "Expr"      "(" Expr ")" [strict] \| "FuncDef"   "(" String "," Params "," Stmts ")" \| "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| `semantics/syntax.k:56` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Stmts      ::= List{Stmt, ""}` |
| `semantics/syntax.k:57` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| `semantics/syntax.k:58` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| `semantics/syntax.k:59` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| `semantics/syntax.k:60` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax ParamNames ::= List{String, ","}` |
| `semantics/syntax.k:61` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax Module     ::= "Module" "(" Stmts ")"` |
| `semantics/syntax.k:62` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `semantics/tuple.k:3` | module | `-` | ASSEMBLY/IMPORT: no rewrite | `module MPY-TUPLE` |
| `semantics/tuple.k:4` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-CORE` |
| `semantics/tuple.k:5` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-ITER` |
| `semantics/tuple.k:6` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-LIST` |
| `semantics/tuple.k:7` | imports | `-` | ASSEMBLY/IMPORT: no rewrite | `imports MPY-METHODS` |
| `semantics/tuple.k:10` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| `semantics/tuple.k:11` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| `semantics/tuple.k:14` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax ApplyK ::= "toTuple"` |
| `semantics/tuple.k:15` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| `semantics/tuple.k:16` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| `semantics/tuple.k:18` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| `semantics/tuple.k:20` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| `semantics/tuple.k:21` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| `semantics/tuple.k:23` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| `semantics/tuple.k:24` | syntax | `function` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| `semantics/tuple.k:25` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| `semantics/tuple.k:26` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| `semantics/tuple.k:28` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| `semantics/tuple.k:31` | syntax | `-` | FIXED-RELEVANT-DECLARATION: matches submitted constructs/evaluation order | `syntax KItem ::= #bindTgt(Expr, Val)` |
| `semantics/tuple.k:32` | rule | `-` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `semantics/tuple.k:35` | rule | `priority` | FIXED-RELEVANT-SOUND: faithful operational/mathematical step | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `semantics/tuple.k:42` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:43` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:44` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/tuple.k:49` | syntax | `-` | FIXED-UNUSED-DECLARATION: no rewrite contribution to this theorem | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| `semantics/tuple.k:50` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:51` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:52` | rule | `priority` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/tuple.k:55` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:57` | rule | `-` | FIXED-UNUSED-RULE: inspected; unreachable from submitted claim term | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| `semantics/tuple.k:58` | endmodule | `-` | ASSEMBLY/IMPORT: no rewrite | `endmodule` |
| `verification.k:1` | requires | `-` | PINNING-MACRO: exact expanded KAST equality checked | `requires "reference-semantics/semantics.k"` |
| `verification.k:3` | module | `-` | PINNING-MACRO: exact expanded KAST equality checked | `module VERIFICATION` |
| `verification.k:4` | imports | `-` | PINNING-MACRO: exact expanded KAST equality checked | `imports MPY` |
| `verification.k:7` | syntax | `macro` | PINNING-MACRO: exact expanded KAST equality checked | `syntax Stmts ::= "solutionLoopBody" [macro]` |
| `verification.k:8` | rule | `-` | PINNING-MACRO: exact expanded KAST equality checked | `rule solutionLoopBody => If( Name("even_position"), Assign( Name("total"), BinOp( "+", Name("total"), BinOp( "*", Name("value"), BinOp("%", Name("value"), Int(2))))) .Stmts, .Stmts) Assign( Name("even_position"), UnaryOp("not", Name("even_position"))) .Stmts` |
| `verification.k:27` | syntax | `macro` | PINNING-MACRO: exact expanded KAST equality checked | `syntax Stmts ::= "solutionBody" [macro]` |
| `verification.k:28` | rule | `-` | PINNING-MACRO: exact expanded KAST equality checked | `rule solutionBody => Assign(Name("total"), Int(0)) Assign(Name("even_position"), Bool(true)) Assign(Name("value"), Int(0)) For(Name("value"), Name("lst"), solutionLoopBody) Return(Name("total")) .Stmts` |
| `verification.k:36` | syntax | `macro` | PINNING-MACRO: exact expanded KAST equality checked | `syntax Val ::= "solutionClosure" [macro]` |
| `verification.k:37` | rule | `-` | PINNING-MACRO: exact expanded KAST equality checked | `rule solutionClosure => closureVal(("lst", .ParamNames), solutionBody, 0)` |
| `verification.k:42` | syntax | `function,total` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `syntax Bool ::= allInts(ValSeq) [function, total]` |
| `verification.k:43` | rule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `rule allInts(.ValSeq) => true` |
| `verification.k:44` | rule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)` |
| `verification.k:49` | syntax | `function,total` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `syntax Int ::= intProjection(Val) [function, total]` |
| `verification.k:50` | rule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `rule intProjection(I:Int) => I` |
| `verification.k:52` | rule | `priority` | PROOF-BRIDGE-SOUND: fixed-semantics Int-domain connection proved; guard is exact generated isInt predicate | `rule <k> BinOp("%", V:Val, I:Int) => pyMod(intProjection(V), I) ... </k> requires isInt(V) [priority(40)]` |
| `verification.k:55` | rule | `priority` | PROOF-BRIDGE-SOUND: fixed-semantics Int-domain connection proved; guard is exact generated isInt predicate | `rule <k> BinOp("+", I:Int, V:Val) => I +Int intProjection(V) ... </k> requires isInt(V) [priority(40)]` |
| `verification.k:58` | rule | `priority` | PROOF-BRIDGE-SOUND: fixed-semantics Int-domain connection proved; guard is exact generated isInt predicate | `rule <k> BinOp("*", V:Val, I:Int) => intProjection(V) *Int I ... </k> requires isInt(V) [priority(40)]` |
| `verification.k:62` | syntax | `function` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `syntax Int ::= oddAtEvenPositions(ValSeq, Bool) [function] \| oddAtEvenAcc(ValSeq, Bool, Int) [function]` |
| `verification.k:64` | rule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `rule oddAtEvenPositions(VS:ValSeq, B:Bool) => oddAtEvenAcc(VS, B, 0)` |
| `verification.k:66` | rule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `rule oddAtEvenAcc(.ValSeq, _:Bool, ACC:Int) => ACC` |
| `verification.k:67` | rule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `rule oddAtEvenAcc(vCons(V:Val, R:ValSeq), true, ACC:Int) => oddAtEvenAcc( R, false, ACC +Int intProjection(V) *Int pyMod(intProjection(V), 2))` |
| `verification.k:72` | rule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `rule oddAtEvenAcc(vCons(_:Val, R:ValSeq), false, ACC:Int) => oddAtEvenAcc(R, true, ACC)` |
| `verification.k:74` | endmodule | `-` | PROOF-DEFINITION-SOUND: structural/guarded equations; terminating on ValSeq | `endmodule` |
| `spec.k:1` | requires | `-` | SPEC-STRUCTURE | `requires "verification.k"` |
| `spec.k:3` | module | `-` | SPEC-STRUCTURE | `module SPEC` |
| `spec.k:4` | imports | `-` | SPEC-STRUCTURE | `imports VERIFICATION` |
| `spec.k:10` | claim | `-` | CLAIM-AUDITED: satisfiable, result-constraining, real-program pinned | `claim [loop-invariant]: <k> #loop(list(VS:ValSeq), Name("value"), solutionLoopBody) ~> KONT:K => KONT </k> <env> L:Int </env> <scopes> BASE:Map L \|-> scope( "lst" \|-> LIST:Val "total" \|-> TOTAL:Int "even_position" \|-> EVEN:Bool "value" \|-> OLD:Val, P:Parent) => BASE L \|-> scope( "lst" \|-> LIST "total" \|-> oddAtEvenAcc(VS, EVEN, TOTAL) "even_position" \|-> ?FINAL_EVEN:Bool "value" \|-> ?FINAL_VALUE:Val, P) </scopes> requires allInts(VS)` |
| `spec.k:37` | claim | `-` | CLAIM-AUDITED: satisfiable, result-constraining, real-program pinned | `claim [solution-correct]: <k> Call(solutionClosure, (list(VS:ValSeq), .Exprs)) => oddAtEvenPositions(VS, true) </k> <env> 0 </env> <scopes> 0  \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(VS)` |
| `spec.k:56` | endmodule | `-` | SPEC-STRUCTURE | `endmodule` |

# Exhaustive K-source inventory

Generated from the fresh scratch sources. The supplied tree is byte-identical to `/reference/reference-semantics`; proof-local means a candidate-authored K source outside that trusted tree.

Total records: 1073. Kind counts: `{'module': 33, 'rule': 731, 'endmodule': 33, 'context': 5, 'syntax': 233, 'configuration': 1, 'requires': 29, 'claim': 8}`.

Classification counts: `{'supplied': 1001, 'ordinary': 674, 'priority(40)': 45, 'evaluation-context': 5, 'function': 150, 'total': 111, 'concrete': 54, 'owise': 29, 'opaque/no-evaluators': 24, 'macro': 6, 'priority(45)': 4, 'priority(39)': 1, 'proof-local': 72, 'reachability-claim': 8, 'simplification': 3}`.

## Counts by file

| File | Kind | Count |
|---|---:|---:|
| `connection-mutation-spec.k` | claim | 1 |
| `connection-mutation-spec.k` | endmodule | 1 |
| `connection-mutation-spec.k` | module | 1 |
| `connection-mutation-spec.k` | requires | 1 |
| `connection-spec.k` | claim | 1 |
| `connection-spec.k` | endmodule | 1 |
| `connection-spec.k` | module | 1 |
| `connection-spec.k` | requires | 1 |
| `projection-spec.k` | claim | 2 |
| `projection-spec.k` | endmodule | 1 |
| `projection-spec.k` | module | 1 |
| `projection-spec.k` | requires | 1 |
| `reference-semantics/semantics.k` | endmodule | 2 |
| `reference-semantics/semantics.k` | module | 2 |
| `reference-semantics/semantics.k` | requires | 23 |
| `reference-semantics/semantics/assert.k` | endmodule | 1 |
| `reference-semantics/semantics/assert.k` | module | 1 |
| `reference-semantics/semantics/assert.k` | rule | 3 |
| `reference-semantics/semantics/bool.k` | context | 1 |
| `reference-semantics/semantics/bool.k` | endmodule | 1 |
| `reference-semantics/semantics/bool.k` | module | 1 |
| `reference-semantics/semantics/bool.k` | rule | 13 |
| `reference-semantics/semantics/builtins.k` | endmodule | 1 |
| `reference-semantics/semantics/builtins.k` | module | 1 |
| `reference-semantics/semantics/builtins.k` | rule | 137 |
| `reference-semantics/semantics/builtins.k` | syntax | 38 |
| `reference-semantics/semantics/call.k` | endmodule | 1 |
| `reference-semantics/semantics/call.k` | module | 1 |
| `reference-semantics/semantics/call.k` | rule | 21 |
| `reference-semantics/semantics/call.k` | syntax | 3 |
| `reference-semantics/semantics/comprehension.k` | endmodule | 1 |
| `reference-semantics/semantics/comprehension.k` | module | 1 |
| `reference-semantics/semantics/comprehension.k` | rule | 7 |
| `reference-semantics/semantics/comprehension.k` | syntax | 3 |
| `reference-semantics/semantics/concrete.k` | endmodule | 1 |
| `reference-semantics/semantics/concrete.k` | module | 1 |
| `reference-semantics/semantics/concrete.k` | rule | 16 |
| `reference-semantics/semantics/concrete.k` | syntax | 5 |
| `reference-semantics/semantics/controls.k` | endmodule | 1 |
| `reference-semantics/semantics/controls.k` | module | 1 |
| `reference-semantics/semantics/controls.k` | rule | 34 |
| `reference-semantics/semantics/controls.k` | syntax | 3 |
| `reference-semantics/semantics/core.k` | configuration | 1 |
| `reference-semantics/semantics/core.k` | endmodule | 1 |
| `reference-semantics/semantics/core.k` | module | 1 |
| `reference-semantics/semantics/core.k` | rule | 46 |
| `reference-semantics/semantics/core.k` | syntax | 37 |
| `reference-semantics/semantics/dict.k` | endmodule | 1 |
| `reference-semantics/semantics/dict.k` | module | 1 |
| `reference-semantics/semantics/dict.k` | rule | 28 |
| `reference-semantics/semantics/dict.k` | syntax | 12 |
| `reference-semantics/semantics/float.k` | endmodule | 1 |
| `reference-semantics/semantics/float.k` | module | 1 |
| `reference-semantics/semantics/float.k` | rule | 121 |
| `reference-semantics/semantics/float.k` | syntax | 34 |
| `reference-semantics/semantics/functions.k` | endmodule | 1 |
| `reference-semantics/semantics/functions.k` | module | 1 |
| `reference-semantics/semantics/functions.k` | rule | 15 |
| `reference-semantics/semantics/functions.k` | syntax | 4 |
| `reference-semantics/semantics/int.k` | endmodule | 1 |
| `reference-semantics/semantics/int.k` | module | 1 |
| `reference-semantics/semantics/int.k` | rule | 16 |
| `reference-semantics/semantics/int.k` | syntax | 1 |
| `reference-semantics/semantics/iter.k` | endmodule | 1 |
| `reference-semantics/semantics/iter.k` | module | 1 |
| `reference-semantics/semantics/iter.k` | syntax | 1 |
| `reference-semantics/semantics/list.k` | endmodule | 1 |
| `reference-semantics/semantics/list.k` | module | 1 |
| `reference-semantics/semantics/list.k` | rule | 27 |
| `reference-semantics/semantics/list.k` | syntax | 5 |
| `reference-semantics/semantics/methods.k` | endmodule | 1 |
| `reference-semantics/semantics/methods.k` | module | 1 |
| `reference-semantics/semantics/methods.k` | rule | 75 |
| `reference-semantics/semantics/methods.k` | syntax | 27 |
| `reference-semantics/semantics/operators.k` | context | 2 |
| `reference-semantics/semantics/operators.k` | endmodule | 1 |
| `reference-semantics/semantics/operators.k` | module | 1 |
| `reference-semantics/semantics/operators.k` | rule | 10 |
| `reference-semantics/semantics/range.k` | endmodule | 1 |
| `reference-semantics/semantics/range.k` | module | 1 |
| `reference-semantics/semantics/range.k` | rule | 6 |
| `reference-semantics/semantics/range.k` | syntax | 2 |
| `reference-semantics/semantics/set.k` | endmodule | 1 |
| `reference-semantics/semantics/set.k` | module | 1 |
| `reference-semantics/semantics/set.k` | rule | 12 |
| `reference-semantics/semantics/set.k` | syntax | 6 |
| `reference-semantics/semantics/sort.k` | endmodule | 1 |
| `reference-semantics/semantics/sort.k` | module | 1 |
| `reference-semantics/semantics/sort.k` | rule | 19 |
| `reference-semantics/semantics/sort.k` | syntax | 6 |
| `reference-semantics/semantics/str.k` | endmodule | 1 |
| `reference-semantics/semantics/str.k` | module | 1 |
| `reference-semantics/semantics/str.k` | rule | 28 |
| `reference-semantics/semantics/str.k` | syntax | 5 |
| `reference-semantics/semantics/subscript.k` | context | 2 |
| `reference-semantics/semantics/subscript.k` | endmodule | 1 |
| `reference-semantics/semantics/subscript.k` | module | 1 |
| `reference-semantics/semantics/subscript.k` | rule | 40 |
| `reference-semantics/semantics/subscript.k` | syntax | 15 |
| `reference-semantics/semantics/syntax.k` | endmodule | 1 |
| `reference-semantics/semantics/syntax.k` | module | 1 |
| `reference-semantics/semantics/syntax.k` | syntax | 16 |
| `reference-semantics/semantics/tuple.k` | endmodule | 1 |
| `reference-semantics/semantics/tuple.k` | module | 1 |
| `reference-semantics/semantics/tuple.k` | rule | 21 |
| `reference-semantics/semantics/tuple.k` | syntax | 4 |
| `spec-vacuity.k` | claim | 1 |
| `spec-vacuity.k` | endmodule | 1 |
| `spec-vacuity.k` | module | 1 |
| `spec-vacuity.k` | requires | 1 |
| `spec.k` | claim | 3 |
| `spec.k` | endmodule | 1 |
| `spec.k` | module | 1 |
| `spec.k` | requires | 1 |
| `verification.k` | endmodule | 3 |
| `verification.k` | module | 3 |
| `verification.k` | requires | 1 |
| `verification.k` | rule | 36 |
| `verification.k` | syntax | 6 |

## Every record

| ID | Location | Kind/class | Source record |
|---:|---|---|---|
| 1 | `reference-semantics/semantics/assert.k:3` | module; supplied | `module MPY-ASSERT imports MPY-CORE` |
| 2 | `reference-semantics/semantics/assert.k:6` | rule; supplied, ordinary | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 3 | `reference-semantics/semantics/assert.k:8` | rule; supplied, ordinary | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 4 | `reference-semantics/semantics/assert.k:13` | rule; supplied, ordinary, priority(40) | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 5 | `reference-semantics/semantics/assert.k:16` | endmodule; supplied | `endmodule` |
| 6 | `reference-semantics/semantics/bool.k:5` | module; supplied | `module MPY-BOOL imports MPY-CORE` |
| 7 | `reference-semantics/semantics/bool.k:8` | rule; supplied, ordinary | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 8 | `reference-semantics/semantics/bool.k:10` | rule; supplied, ordinary | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 9 | `reference-semantics/semantics/bool.k:11` | rule; supplied, ordinary | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 // ==== BoolOp: short-circuit, value-returning and / or ===================== // the node is its own accumulator: heat the HEAD element only, then either return it // (short-circuit) or drop it and continue` |
| 10 | `reference-semantics/semantics/bool.k:16` | context; supplied, evaluation-context | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 11 | `reference-semantics/semantics/bool.k:17` | rule; supplied, ordinary | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 12 | `reference-semantics/semantics/bool.k:18` | rule; supplied, ordinary | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 13 | `reference-semantics/semantics/bool.k:20` | rule; supplied, ordinary | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 14 | `reference-semantics/semantics/bool.k:22` | rule; supplied, ordinary | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 15 | `reference-semantics/semantics/bool.k:24` | rule; supplied, ordinary | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the // operand — and/or return the OBJECT itself (Python identity), not its structure` |
| 16 | `reference-semantics/semantics/bool.k:29` | rule; supplied, ordinary, priority(40) | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 17 | `reference-semantics/semantics/bool.k:31` | rule; supplied, ordinary, priority(40) | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 18 | `reference-semantics/semantics/bool.k:35` | rule; supplied, ordinary, priority(40) | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 19 | `reference-semantics/semantics/bool.k:39` | rule; supplied, ordinary, priority(40) | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 20 | `reference-semantics/semantics/bool.k:43` | rule; supplied, ordinary, priority(40) | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 21 | `reference-semantics/semantics/bool.k:47` | endmodule; supplied | `endmodule` |
| 22 | `reference-semantics/semantics/builtins.k:3` | module; supplied | `module MPY-BUILTINS imports MPY-CORE imports MPY-STR imports MPY-SET imports MPY-ITER imports MPY-RANGE imports MPY-INT imports MPY-METHODS // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup // Call routing + argument evaluation live in call.k, which also routes the fold // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to // applyBuiltin. This module owns applyBuiltin + the fold implementations.` |
| 23 | `reference-semantics/semantics/builtins.k:17` | syntax; supplied, function | `syntax Val ::= applyBuiltin(String, Vals) [function] // ==== len(obj) — O(1) per kind ============================================` |
| 24 | `reference-semantics/semantics/builtins.k:20` | syntax; supplied, function | `syntax Int ::= seqLen(Val) [function]` |
| 25 | `reference-semantics/semantics/builtins.k:21` | rule; supplied, ordinary | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 26 | `reference-semantics/semantics/builtins.k:22` | rule; supplied, ordinary | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| 27 | `reference-semantics/semantics/builtins.k:23` | rule; supplied, ordinary | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| 28 | `reference-semantics/semantics/builtins.k:24` | rule; supplied, ordinary | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| 29 | `reference-semantics/semantics/builtins.k:25` | rule; supplied, ordinary | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| 30 | `reference-semantics/semantics/builtins.k:26` | rule; supplied, ordinary | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) == // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order). // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed. // (k-cell — list() constructs a NEW object)` |
| 31 | `reference-semantics/semantics/builtins.k:32` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 32 | `reference-semantics/semantics/builtins.k:33` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 33 | `reference-semantics/semantics/builtins.k:34` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| 34 | `reference-semantics/semantics/builtins.k:35` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| 35 | `reference-semantics/semantics/builtins.k:36` | syntax; supplied, function, total | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 36 | `reference-semantics/semantics/builtins.k:37` | rule; supplied, ordinary | `rule charsOf(.IntSeq) => .ValSeq` |
| 37 | `reference-semantics/semantics/builtins.k:38` | rule; supplied, ordinary | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) // ==== set(str) — distinct character codes =================================` |
| 38 | `reference-semantics/semantics/builtins.k:41` | rule; supplied, ordinary | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) // ==== abs(int) ============================================================` |
| 39 | `reference-semantics/semantics/builtins.k:44` | rule; supplied, ordinary | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==` |
| 40 | `reference-semantics/semantics/builtins.k:47` | syntax; supplied | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 41 | `reference-semantics/semantics/builtins.k:48` | rule; supplied, ordinary | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 42 | `reference-semantics/semantics/builtins.k:49` | rule; supplied, ordinary | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 43 | `reference-semantics/semantics/builtins.k:50` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 44 | `reference-semantics/semantics/builtins.k:54` | syntax; supplied, function | `syntax Int ::= intOf(Val) [function]` |
| 45 | `reference-semantics/semantics/builtins.k:55` | rule; supplied, ordinary | `rule intOf(I:Int) => I` |
| 46 | `reference-semantics/semantics/builtins.k:56` | rule; supplied, ordinary | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi // ==== all / any (short-circuiting #iterNext folds) ========================` |
| 47 | `reference-semantics/semantics/builtins.k:59` | syntax; supplied | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 48 | `reference-semantics/semantics/builtins.k:60` | rule; supplied, ordinary | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 49 | `reference-semantics/semantics/builtins.k:61` | rule; supplied, ordinary | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 50 | `reference-semantics/semantics/builtins.k:62` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 51 | `reference-semantics/semantics/builtins.k:64` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 52 | `reference-semantics/semantics/builtins.k:67` | syntax; supplied | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 53 | `reference-semantics/semantics/builtins.k:68` | rule; supplied, ordinary | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 54 | `reference-semantics/semantics/builtins.k:69` | rule; supplied, ordinary | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 55 | `reference-semantics/semantics/builtins.k:70` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 56 | `reference-semantics/semantics/builtins.k:72` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) // ==== max / min over an iterable (#iterNext folds; first element seeds) ====` |
| 57 | `reference-semantics/semantics/builtins.k:76` | syntax; supplied | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 58 | `reference-semantics/semantics/builtins.k:77` | rule; supplied, ordinary | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 59 | `reference-semantics/semantics/builtins.k:78` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 60 | `reference-semantics/semantics/builtins.k:80` | rule; supplied, ordinary | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 61 | `reference-semantics/semantics/builtins.k:81` | rule; supplied, ordinary | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 62 | `reference-semantics/semantics/builtins.k:82` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 63 | `reference-semantics/semantics/builtins.k:86` | syntax; supplied | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 64 | `reference-semantics/semantics/builtins.k:87` | rule; supplied, ordinary | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 65 | `reference-semantics/semantics/builtins.k:88` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 66 | `reference-semantics/semantics/builtins.k:90` | rule; supplied, ordinary | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 67 | `reference-semantics/semantics/builtins.k:91` | rule; supplied, ordinary | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 68 | `reference-semantics/semantics/builtins.k:92` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) // ==== variadic max / min (a Vals fold) ====================================` |
| 69 | `reference-semantics/semantics/builtins.k:97` | syntax; supplied, function | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 70 | `reference-semantics/semantics/builtins.k:98` | rule; supplied, ordinary | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 71 | `reference-semantics/semantics/builtins.k:99` | rule; supplied, ordinary | `rule maxVals(M:Int, .Vals) => M` |
| 72 | `reference-semantics/semantics/builtins.k:100` | rule; supplied, ordinary | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 73 | `reference-semantics/semantics/builtins.k:102` | syntax; supplied, function | `syntax Int ::= minVals(Int, Vals) [function]` |
| 74 | `reference-semantics/semantics/builtins.k:103` | rule; supplied, ordinary | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 75 | `reference-semantics/semantics/builtins.k:104` | rule; supplied, ordinary | `rule minVals(M:Int, .Vals) => M` |
| 76 | `reference-semantics/semantics/builtins.k:105` | rule; supplied, ordinary | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==` |
| 77 | `reference-semantics/semantics/builtins.k:108` | rule; supplied, ordinary | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits` |
| 78 | `reference-semantics/semantics/builtins.k:111` | rule; supplied, ordinary | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 79 | `reference-semantics/semantics/builtins.k:114` | syntax; supplied, function, total | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 80 | `reference-semantics/semantics/builtins.k:115` | rule; supplied, ordinary | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 81 | `reference-semantics/semantics/builtins.k:116` | rule; supplied, ordinary | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 82 | `reference-semantics/semantics/builtins.k:117` | syntax; supplied, function, total | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 83 | `reference-semantics/semantics/builtins.k:118` | rule; supplied, ordinary | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 84 | `reference-semantics/semantics/builtins.k:119` | rule; supplied, ordinary | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========` |
| 85 | `reference-semantics/semantics/builtins.k:124` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 86 | `reference-semantics/semantics/builtins.k:126` | syntax; supplied, function, total | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 87 | `reference-semantics/semantics/builtins.k:127` | rule; supplied, ordinary | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 88 | `reference-semantics/semantics/builtins.k:128` | rule; supplied, ordinary | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) // ==== map(str, xs) — eager (only the str case is in the subset) =============` |
| 89 | `reference-semantics/semantics/builtins.k:132` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 90 | `reference-semantics/semantics/builtins.k:134` | syntax; supplied, function, total | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 91 | `reference-semantics/semantics/builtins.k:135` | rule; supplied, ordinary | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 92 | `reference-semantics/semantics/builtins.k:136` | rule; supplied, ordinary | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 93 | `reference-semantics/semantics/builtins.k:137` | rule; supplied, ordinary | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) // ==== int(x) identities (int(round(x)) composes through) ====================` |
| 94 | `reference-semantics/semantics/builtins.k:140` | rule; supplied, ordinary | `rule applyBuiltin("int", I:Int, .Vals) => I // ==== ord / chr ===========================================================` |
| 95 | `reference-semantics/semantics/builtins.k:143` | rule; supplied, ordinary | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 96 | `reference-semantics/semantics/builtins.k:144` | rule; supplied, ordinary | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 // ==== str(int) / str(str) =================================================` |
| 97 | `reference-semantics/semantics/builtins.k:148` | rule; supplied, ordinary | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| 98 | `reference-semantics/semantics/builtins.k:149` | rule; supplied, ordinary | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====` |
| 99 | `reference-semantics/semantics/builtins.k:152` | rule; supplied, ordinary | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)` |
| 100 | `reference-semantics/semantics/builtins.k:156` | rule; supplied, ordinary | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 101 | `reference-semantics/semantics/builtins.k:158` | syntax; supplied, function, total | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 102 | `reference-semantics/semantics/builtins.k:159` | rule; supplied, ordinary | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| 103 | `reference-semantics/semantics/builtins.k:160` | rule; supplied, ordinary | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====` |
| 104 | `reference-semantics/semantics/builtins.k:163` | rule; supplied, ordinary | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 105 | `reference-semantics/semantics/builtins.k:164` | rule; supplied, ordinary | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)` |
| 106 | `reference-semantics/semantics/builtins.k:167` | rule; supplied, ordinary | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 107 | `reference-semantics/semantics/builtins.k:169` | rule; supplied, ordinary | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| 108 | `reference-semantics/semantics/builtins.k:170` | rule; supplied, ordinary | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 109 | `reference-semantics/semantics/builtins.k:171` | rule; supplied, ordinary | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 110 | `reference-semantics/semantics/builtins.k:173` | rule; supplied, ordinary | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| 111 | `reference-semantics/semantics/builtins.k:174` | rule; supplied, ordinary | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> // ==== range(stop) / range(start, stop) / range(start, stop, step) =========` |
| 112 | `reference-semantics/semantics/builtins.k:177` | rule; supplied, ordinary | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| 113 | `reference-semantics/semantics/builtins.k:178` | rule; supplied, ordinary | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| 114 | `reference-semantics/semantics/builtins.k:179` | rule; supplied, concrete | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ======== // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's // trusted pass evaluator, now DEFINED in the reference and driven by a // code-level tokenizer. Reduces on concrete strings (krun); a symbolic // argument leaves the call unevaluated for problem-level folds.` |
| 115 | `reference-semantics/semantics/builtins.k:187` | rule; supplied, ordinary | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 116 | `reference-semantics/semantics/builtins.k:188` | syntax; supplied, function | `syntax Int ::= evalArith(IntSeq) [function]` |
| 117 | `reference-semantics/semantics/builtins.k:189` | rule; supplied, ordinary | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 118 | `reference-semantics/semantics/builtins.k:192` | syntax; supplied | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 119 | `reference-semantics/semantics/builtins.k:194` | syntax; supplied, function, total | `syntax Bool ::= evDigit(Int) [function, total]` |
| 120 | `reference-semantics/semantics/builtins.k:195` | rule; supplied, ordinary | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 121 | `reference-semantics/semantics/builtins.k:196` | syntax; supplied, function, total | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 122 | `reference-semantics/semantics/builtins.k:197` | rule; supplied, ordinary | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 123 | `reference-semantics/semantics/builtins.k:198` | rule; supplied, ordinary, owise | `rule evHead42(_:IntSeq) => false [owise]` |
| 124 | `reference-semantics/semantics/builtins.k:199` | syntax; supplied, function, total | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 125 | `reference-semantics/semantics/builtins.k:200` | rule; supplied, ordinary | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 126 | `reference-semantics/semantics/builtins.k:201` | rule; supplied, ordinary, owise | `rule evHead47(_:IntSeq) => false [owise]` |
| 127 | `reference-semantics/semantics/builtins.k:203` | syntax; supplied, function, total | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 128 | `reference-semantics/semantics/builtins.k:204` | rule; supplied, ordinary | `rule tokOps(.IntSeq) => .OpSeq` |
| 129 | `reference-semantics/semantics/builtins.k:205` | rule; supplied, ordinary | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| 130 | `reference-semantics/semantics/builtins.k:206` | rule; supplied, ordinary | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| 131 | `reference-semantics/semantics/builtins.k:207` | rule; supplied, ordinary | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 132 | `reference-semantics/semantics/builtins.k:208` | rule; supplied, ordinary | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 133 | `reference-semantics/semantics/builtins.k:209` | rule; supplied, ordinary | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 134 | `reference-semantics/semantics/builtins.k:210` | rule; supplied, ordinary | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 135 | `reference-semantics/semantics/builtins.k:211` | rule; supplied, ordinary | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| 136 | `reference-semantics/semantics/builtins.k:212` | rule; supplied, ordinary | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` |
| 137 | `reference-semantics/semantics/builtins.k:214` | syntax; supplied, function, total | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 138 | `reference-semantics/semantics/builtins.k:216` | rule; supplied, ordinary | `rule tokNds(.IntSeq) => .IntSeq` |
| 139 | `reference-semantics/semantics/builtins.k:217` | rule; supplied, ordinary | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| 140 | `reference-semantics/semantics/builtins.k:218` | rule; supplied, ordinary | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 141 | `reference-semantics/semantics/builtins.k:219` | rule; supplied, ordinary | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 142 | `reference-semantics/semantics/builtins.k:221` | rule; supplied, ordinary | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 143 | `reference-semantics/semantics/builtins.k:223` | rule; supplied, ordinary, owise | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 144 | `reference-semantics/semantics/builtins.k:225` | syntax; supplied | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 145 | `reference-semantics/semantics/builtins.k:226` | syntax; supplied, function, total | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 146 | `reference-semantics/semantics/builtins.k:227` | rule; supplied, ordinary | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 147 | `reference-semantics/semantics/builtins.k:228` | rule; supplied, ordinary, owise | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 148 | `reference-semantics/semantics/builtins.k:230` | syntax; supplied, function, total | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 149 | `reference-semantics/semantics/builtins.k:231` | rule; supplied, ordinary | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| 150 | `reference-semantics/semantics/builtins.k:232` | rule; supplied, ordinary | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| 151 | `reference-semantics/semantics/builtins.k:233` | rule; supplied, ordinary | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| 152 | `reference-semantics/semantics/builtins.k:234` | rule; supplied, ordinary | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 153 | `reference-semantics/semantics/builtins.k:235` | rule; supplied, ordinary | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 154 | `reference-semantics/semantics/builtins.k:236` | rule; supplied, ordinary, owise | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 155 | `reference-semantics/semantics/builtins.k:238` | syntax; supplied, function, total | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 156 | `reference-semantics/semantics/builtins.k:239` | rule; supplied, ordinary | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 157 | `reference-semantics/semantics/builtins.k:240` | rule; supplied, ordinary | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 158 | `reference-semantics/semantics/builtins.k:241` | rule; supplied, ordinary | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 159 | `reference-semantics/semantics/builtins.k:243` | rule; supplied, ordinary, owise | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 160 | `reference-semantics/semantics/builtins.k:244` | syntax; supplied, function, total | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 161 | `reference-semantics/semantics/builtins.k:245` | rule; supplied, ordinary | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 162 | `reference-semantics/semantics/builtins.k:246` | rule; supplied, ordinary | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 163 | `reference-semantics/semantics/builtins.k:247` | syntax; supplied, function, total | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 164 | `reference-semantics/semantics/builtins.k:248` | rule; supplied, ordinary | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 165 | `reference-semantics/semantics/builtins.k:250` | syntax; supplied, function, total | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 166 | `reference-semantics/semantics/builtins.k:251` | rule; supplied, ordinary | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 167 | `reference-semantics/semantics/builtins.k:252` | rule; supplied, ordinary | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 168 | `reference-semantics/semantics/builtins.k:253` | rule; supplied, ordinary | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 169 | `reference-semantics/semantics/builtins.k:254` | rule; supplied, ordinary | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 170 | `reference-semantics/semantics/builtins.k:255` | syntax; supplied, function, total | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 171 | `reference-semantics/semantics/builtins.k:256` | rule; supplied, ordinary | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 172 | `reference-semantics/semantics/builtins.k:257` | rule; supplied, ordinary | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 173 | `reference-semantics/semantics/builtins.k:260` | rule; supplied, ordinary | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 174 | `reference-semantics/semantics/builtins.k:263` | rule; supplied, ordinary, owise | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 175 | `reference-semantics/semantics/builtins.k:265` | syntax; supplied, function, total | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 176 | `reference-semantics/semantics/builtins.k:266` | rule; supplied, ordinary | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 177 | `reference-semantics/semantics/builtins.k:267` | rule; supplied, ordinary | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 178 | `reference-semantics/semantics/builtins.k:268` | rule; supplied, ordinary, owise | `rule inLevelE(_:String, _:String) => false [owise]` |
| 179 | `reference-semantics/semantics/builtins.k:269` | syntax; supplied, function, total | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 180 | `reference-semantics/semantics/builtins.k:270` | rule; supplied, ordinary | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 181 | `reference-semantics/semantics/builtins.k:271` | rule; supplied, ordinary | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 182 | `reference-semantics/semantics/builtins.k:272` | syntax; supplied, function, total | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 183 | `reference-semantics/semantics/builtins.k:273` | rule; supplied, ordinary | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 184 | `reference-semantics/semantics/builtins.k:274` | rule; supplied, concrete | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ================== // The md5 value itself is a named shared trust (sortVS-style, no concrete // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).` |
| 185 | `reference-semantics/semantics/builtins.k:279` | syntax; supplied | `syntax KItem ::= "#md5"` |
| 186 | `reference-semantics/semantics/builtins.k:280` | rule; supplied, ordinary, priority(40) | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 187 | `reference-semantics/semantics/builtins.k:282` | rule; supplied, ordinary | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 188 | `reference-semantics/semantics/builtins.k:283` | syntax; supplied | `syntax Val ::= md5Obj(IntSeq)` |
| 189 | `reference-semantics/semantics/builtins.k:284` | rule; supplied, ordinary | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 190 | `reference-semantics/semantics/builtins.k:285` | syntax; supplied, function, total, opaque/no-evaluators | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int\|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary name that resolves via the builtins frame to // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).` |
| 191 | `reference-semantics/semantics/builtins.k:291` | rule; supplied, ordinary | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 192 | `reference-semantics/semantics/builtins.k:292` | rule; supplied, ordinary | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 193 | `reference-semantics/semantics/builtins.k:293` | syntax; supplied, function | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 194 | `reference-semantics/semantics/builtins.k:294` | rule; supplied, ordinary | `rule isIntV(_:Int) => true` |
| 195 | `reference-semantics/semantics/builtins.k:295` | rule; supplied, ordinary, owise | `rule isIntV(_:Val) => false [owise]` |
| 196 | `reference-semantics/semantics/builtins.k:296` | rule; supplied, ordinary | `rule isStrV(str(_:IntSeq)) => true` |
| 197 | `reference-semantics/semantics/builtins.k:297` | rule; supplied, ordinary, owise | `rule isStrV(_:Val) => false [owise]` |
| 198 | `reference-semantics/semantics/builtins.k:298` | endmodule; supplied | `endmodule` |
| 199 | `reference-semantics/semantics/call.k:10` | module; supplied | `module MPY-CALL imports MPY-METHODS imports MPY-BUILTINS imports MPY-FUNCTIONS // a cooled attribute is a bound method value` |
| 200 | `reference-semantics/semantics/call.k:16` | rule; supplied, ordinary, owise | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)` |
| 201 | `reference-semantics/semantics/call.k:19` | syntax; supplied | `syntax KItem ::= #callee(Exprs)` |
| 202 | `reference-semantics/semantics/call.k:20` | rule; supplied, ordinary, owise | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 203 | `reference-semantics/semantics/call.k:21` | rule; supplied, ordinary | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> // ==== dispatch on the callee value ========================================` |
| 204 | `reference-semantics/semantics/call.k:24` | rule; supplied, ordinary | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 205 | `reference-semantics/semantics/call.k:26` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 206 | `reference-semantics/semantics/call.k:27` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| 207 | `reference-semantics/semantics/call.k:28` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| 208 | `reference-semantics/semantics/call.k:29` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| 209 | `reference-semantics/semantics/call.k:30` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| 210 | `reference-semantics/semantics/call.k:31` | rule; supplied, ordinary, owise | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 211 | `reference-semantics/semantics/call.k:32` | rule; supplied, ordinary | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> // ==== heap-object arguments/receivers ===================================== // Builtins and type calls READ structure — deref the first two arg positions // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list // methods take the ref itself; every other method receiver is deref'd.` |
| 212 | `reference-semantics/semantics/call.k:38` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 213 | `reference-semantics/semantics/call.k:42` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 214 | `reference-semantics/semantics/call.k:47` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 215 | `reference-semantics/semantics/call.k:52` | syntax; supplied, function, total | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 216 | `reference-semantics/semantics/call.k:53` | rule; supplied, ordinary | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 217 | `reference-semantics/semantics/call.k:56` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mutating methods READ their heap-object arguments too (join's list); // mutators keep refs (append of a list into a list-of-lists stays aliased)` |
| 218 | `reference-semantics/semantics/call.k:63` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| 219 | `reference-semantics/semantics/call.k:69` | rule; supplied, ordinary | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> // annotated closure: the frame starts with the captured freevar cells, its // parent is the module scope (all enclosing-local reads go through cells), // and the cellvars' fresh cells allocate before params bind (a cellvar param // then writes through its cell in #bindP).` |
| 220 | `reference-semantics/semantics/call.k:80` | rule; supplied, ordinary | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 221 | `reference-semantics/semantics/call.k:87` | syntax; supplied | `syntax KItem ::= #allocCells(ParamNames)` |
| 222 | `reference-semantics/semantics/call.k:88` | rule; supplied, ordinary | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 223 | `reference-semantics/semantics/call.k:89` | rule; supplied, ordinary | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 224 | `reference-semantics/semantics/call.k:95` | endmodule; supplied | `endmodule` |
| 225 | `reference-semantics/semantics/comprehension.k:3` | module; supplied | `module MPY-COMPREHENSION imports MPY-CORE imports MPY-OPERATORS imports MPY-LIST imports MPY-CONTROLS imports MPY-FUNCTIONS // A comprehension is pure syntactic sugar` |
| 226 | `reference-semantics/semantics/comprehension.k:11` | rule; supplied, ordinary | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 227 | `reference-semantics/semantics/comprehension.k:12` | rule; supplied, ordinary | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 228 | `reference-semantics/semantics/comprehension.k:14` | syntax; supplied, macro | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 229 | `reference-semantics/semantics/comprehension.k:15` | rule; supplied, ordinary | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 230 | `reference-semantics/semantics/comprehension.k:18` | syntax; supplied, macro | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 231 | `reference-semantics/semantics/comprehension.k:19` | rule; supplied, ordinary | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 232 | `reference-semantics/semantics/comprehension.k:21` | rule; supplied, ordinary | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 233 | `reference-semantics/semantics/comprehension.k:24` | syntax; supplied, macro | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 234 | `reference-semantics/semantics/comprehension.k:25` | rule; supplied, ordinary | `rule compGuard(.Exprs) => Bool(true)` |
| 235 | `reference-semantics/semantics/comprehension.k:26` | rule; supplied, ordinary | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 236 | `reference-semantics/semantics/comprehension.k:27` | endmodule; supplied | `endmodule` |
| 237 | `reference-semantics/semantics/concrete.k:8` | module; supplied | `module MPY-CONCRETE imports MPY // deep equality for list compares whose elements are heap objects // (list-of-lists): Python == is structural at every depth.` |
| 238 | `reference-semantics/semantics/concrete.k:13` | rule; supplied, ordinary | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 239 | `reference-semantics/semantics/concrete.k:16` | rule; supplied, concrete, priority(40) | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) // ==== keyed sort, concrete leg ============================================ // Computes each key by a REAL call through the uniform #callee machinery // (closures, len, type objects all work), stable-inserts on the key, and // allocates the result. priority(40) beats sort.k's opaque rules, so krun // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.` |
| 240 | `reference-semantics/semantics/concrete.k:25` | syntax; supplied | `syntax Val ::= kvP(Val, Val)` |
| 241 | `reference-semantics/semantics/concrete.k:26` | syntax; supplied | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 242 | `reference-semantics/semantics/concrete.k:28` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 243 | `reference-semantics/semantics/concrete.k:31` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 244 | `reference-semantics/semantics/concrete.k:34` | rule; supplied, ordinary | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 245 | `reference-semantics/semantics/concrete.k:36` | rule; supplied, ordinary | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 246 | `reference-semantics/semantics/concrete.k:38` | rule; supplied, ordinary | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 247 | `reference-semantics/semantics/concrete.k:42` | syntax; supplied, function | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 248 | `reference-semantics/semantics/concrete.k:43` | rule; supplied, ordinary | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 249 | `reference-semantics/semantics/concrete.k:44` | rule; supplied, ordinary | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 250 | `reference-semantics/semantics/concrete.k:47` | rule; supplied, ordinary | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 251 | `reference-semantics/semantics/concrete.k:51` | syntax; supplied, function | `syntax Bool ::= kLt(Val, Val) [function]` |
| 252 | `reference-semantics/semantics/concrete.k:52` | rule; supplied, ordinary | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| 253 | `reference-semantics/semantics/concrete.k:53` | rule; supplied, ordinary | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| 254 | `reference-semantics/semantics/concrete.k:54` | rule; supplied, ordinary | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 255 | `reference-semantics/semantics/concrete.k:56` | syntax; supplied, function, total | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 256 | `reference-semantics/semantics/concrete.k:57` | rule; supplied, ordinary | `rule unpairVS(.ValSeq) => .ValSeq` |
| 257 | `reference-semantics/semantics/concrete.k:58` | rule; supplied, ordinary | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 258 | `reference-semantics/semantics/concrete.k:59` | rule; supplied, ordinary, owise | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 259 | `reference-semantics/semantics/concrete.k:60` | endmodule; supplied | `endmodule` |
| 260 | `reference-semantics/semantics/controls.k:3` | module; supplied | `module MPY-CONTROLS imports MPY-CORE imports MPY-TUPLE imports MPY-ITER // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==` |
| 261 | `reference-semantics/semantics/controls.k:9` | rule; supplied, ordinary | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 262 | `reference-semantics/semantics/controls.k:12` | rule; supplied, ordinary, priority(40) | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 263 | `reference-semantics/semantics/controls.k:20` | rule; supplied, ordinary | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // \`lst += [..]\` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).` |
| 264 | `reference-semantics/semantics/controls.k:27` | rule; supplied, ordinary, priority(40) | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] // ==== import trivia: \`from math import floor, ceil\` binds the supported // names as builtins in the current scope; every other import is a no-op` |
| 265 | `reference-semantics/semantics/controls.k:35` | rule; supplied, ordinary | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 266 | `reference-semantics/semantics/controls.k:36` | rule; supplied, ordinary, owise | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 267 | `reference-semantics/semantics/controls.k:37` | syntax; supplied | `syntax KItem ::= #bindImports(ParamNames)` |
| 268 | `reference-semantics/semantics/controls.k:38` | rule; supplied, ordinary | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 269 | `reference-semantics/semantics/controls.k:39` | rule; supplied, ordinary | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| 270 | `reference-semantics/semantics/controls.k:43` | rule; supplied, ordinary | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") // ==== Expr statement: evaluate for effect, discard the value =============== // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)` |
| 271 | `reference-semantics/semantics/controls.k:48` | rule; supplied, ordinary | `rule <k> Expr(_:Val) => .K ... </k> // ==== If (condition evaluated by strictness) ==============================` |
| 272 | `reference-semantics/semantics/controls.k:51` | syntax; supplied | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 273 | `reference-semantics/semantics/controls.k:52` | rule; supplied, ordinary | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 274 | `reference-semantics/semantics/controls.k:53` | rule; supplied, ordinary | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| 275 | `reference-semantics/semantics/controls.k:54` | rule; supplied, ordinary | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> // ==== IfExp: ternary T if C else E ========================================` |
| 276 | `reference-semantics/semantics/controls.k:57` | rule; supplied, ordinary | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 277 | `reference-semantics/semantics/controls.k:59` | rule; supplied, ordinary | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) // ==== For: one loop, in-cell continuation, over #iterNext ================= // (the iterable is evaluated once, by strictness; the protocol stays rewrites — // circularities anchor on #loop and narrowing substitutes the structure)` |
| 278 | `reference-semantics/semantics/controls.k:65` | syntax; supplied | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| 279 | `reference-semantics/semantics/controls.k:69` | rule; supplied, ordinary | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 280 | `reference-semantics/semantics/controls.k:71` | rule; supplied, ordinary | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 281 | `reference-semantics/semantics/controls.k:72` | rule; supplied, ordinary | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 282 | `reference-semantics/semantics/controls.k:73` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> // ==== While ==============================================================` |
| 283 | `reference-semantics/semantics/controls.k:77` | rule; supplied, ordinary | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 284 | `reference-semantics/semantics/controls.k:78` | rule; supplied, ordinary | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 285 | `reference-semantics/semantics/controls.k:79` | rule; supplied, ordinary | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 286 | `reference-semantics/semantics/controls.k:81` | rule; supplied, ordinary | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) // ==== loop control (break / continue) =====================================` |
| 287 | `reference-semantics/semantics/controls.k:85` | rule; supplied, ordinary | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 288 | `reference-semantics/semantics/controls.k:86` | rule; supplied, ordinary | `rule <k> Continue => #cont ... </k>` |
| 289 | `reference-semantics/semantics/controls.k:87` | rule; supplied, ordinary | `rule <k> Break => #brk ... </k>` |
| 290 | `reference-semantics/semantics/controls.k:88` | rule; supplied, ordinary | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 291 | `reference-semantics/semantics/controls.k:89` | rule; supplied, ordinary, owise | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 292 | `reference-semantics/semantics/controls.k:90` | rule; supplied, ordinary | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 293 | `reference-semantics/semantics/controls.k:91` | rule; supplied, ordinary, priority(40), owise | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] // ==== heap-object deref at the truthiness/iteration consumers ============== // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)` |
| 294 | `reference-semantics/semantics/controls.k:95` | rule; supplied, ordinary, priority(40) | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 295 | `reference-semantics/semantics/controls.k:98` | rule; supplied, ordinary, priority(40) | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 296 | `reference-semantics/semantics/controls.k:101` | rule; supplied, ordinary, priority(40) | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; // mutating the iterated list inside its own loop is outside the subset)` |
| 297 | `reference-semantics/semantics/controls.k:106` | rule; supplied, ordinary, priority(40) | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 298 | `reference-semantics/semantics/controls.k:109` | endmodule; supplied | `endmodule` |
| 299 | `reference-semantics/semantics/core.k:3` | module; supplied | `module MPY-CORE imports MPY-SYNTAX imports INT imports BOOL imports STRING imports MAP imports LIST imports K-EQUAL // ==== values, the algebraic lists, and the scope heap =====================` |
| 300 | `reference-semantics/semantics/core.k:13` | syntax; supplied | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 301 | `reference-semantics/semantics/core.k:14` | syntax; supplied | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 302 | `reference-semantics/semantics/core.k:15` | syntax; supplied | `syntax Str ::= str(IntSeq) // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)` |
| 303 | `reference-semantics/semantics/core.k:18` | syntax; supplied | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| 304 | `reference-semantics/semantics/core.k:25` | syntax; supplied, function | `syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) // a type object (int/str), resolved from the builtins frame \| builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String) // a cooled Attribute: obj.method` |
| 305 | `reference-semantics/semantics/core.k:36` | syntax; supplied | `syntax Parent ::= "root" \| parent(Int)` |
| 306 | `reference-semantics/semantics/core.k:37` | syntax; supplied | `syntax Scope ::= scope(Map, Parent)` |
| 307 | `reference-semantics/semantics/core.k:38` | syntax; supplied | `syntax KResult ::= Val` |
| 308 | `reference-semantics/semantics/core.k:39` | syntax; supplied | `syntax Expr ::= Val // cooling puts results back into expression holes` |
| 309 | `reference-semantics/semantics/core.k:40` | syntax; supplied | `syntax Vals ::= List{Val, ","}` |
| 310 | `reference-semantics/semantics/core.k:41` | syntax; supplied | `syntax Exc ::= "NoExc" \| "AssertionError"` |
| 311 | `reference-semantics/semantics/core.k:42` | syntax; supplied | `syntax RetState ::= "noRet" \| retV(Val) // ==== configuration ======================================================= // The builtins namespace is a real scope at reserved location -1 (the bottom of every // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0) // has it as parent, so an unbound name resolves there last — exactly LEGB. \`int\`/\`str\` // resolve to their type objects; any local/global binding shadows them via normal lookup.` |
| 312 | `reference-semantics/semantics/core.k:49` | configuration; supplied | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code> // ==== heap allocation (constructed lists become objects) ================== // Cons-form emission with a freshness guard (the heap-list-probe discipline: // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is // monotonic — it does NOT wind back at #pop: returned lists escape by ref. // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed); // only CONSTRUCTORS in program syntax allocate.` |
| 313 | `reference-semantics/semantics/core.k:68` | syntax; supplied, function, total | `syntax Bool ::= isRefV(Val) [function, total]` |
| 314 | `reference-semantics/semantics/core.k:69` | rule; supplied, ordinary | `rule isRefV(ref(_:Int)) => true` |
| 315 | `reference-semantics/semantics/core.k:70` | rule; supplied, ordinary, owise | `rule isRefV(_:Val) => false [owise] // closure cells (Python-faithful capture): the heap holds cellV(V); a // cellRef surfacing as the k-redex reads through (lookup is the only use — // cellRefs never escape to user-visible values)` |
| 316 | `reference-semantics/semantics/core.k:75` | syntax; supplied | `syntax HeapVal ::= cellV(Val)` |
| 317 | `reference-semantics/semantics/core.k:76` | syntax; supplied, function, total | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 318 | `reference-semantics/semantics/core.k:77` | rule; supplied, ordinary | `rule isCellRef(cellRef(_:Int)) => true` |
| 319 | `reference-semantics/semantics/core.k:78` | rule; supplied, ordinary, owise | `rule isCellRef(_:Val) => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in plain frames — an unguarded rule lets the // prover narrow abstract k-top values into cellRef junk (probed on // 26-remove-duplicates). Cross-frame reads (a comprehension closure // reading the enclosing function's cellvar) deref inside #look instead.` |
| 320 | `reference-semantics/semantics/core.k:85` | rule; supplied, ordinary, priority(40) | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] // write through a cell (Assign / #bindP / #bindTgt dispatch here on // cell-bound names) // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)` |
| 321 | `reference-semantics/semantics/core.k:95` | syntax; supplied | `syntax Val ::= kwV(String, Val)` |
| 322 | `reference-semantics/semantics/core.k:96` | syntax; supplied | `syntax KItem ::= #kwTag(String)` |
| 323 | `reference-semantics/semantics/core.k:97` | rule; supplied, ordinary | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 324 | `reference-semantics/semantics/core.k:98` | rule; supplied, ordinary | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 325 | `reference-semantics/semantics/core.k:100` | syntax; supplied, function, total | `syntax Bool ::= isKwV(Val) [function, total]` |
| 326 | `reference-semantics/semantics/core.k:101` | rule; supplied, ordinary | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 327 | `reference-semantics/semantics/core.k:102` | rule; supplied, ordinary, owise | `rule isKwV(_:Val) => false [owise] // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch // decides by pnMember even over an abstract frame rest (no prover branching)` |
| 328 | `reference-semantics/semantics/core.k:106` | syntax; supplied | `syntax Val ::= cellsMark(ParamNames)` |
| 329 | `reference-semantics/semantics/core.k:107` | syntax; supplied, function | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 330 | `reference-semantics/semantics/core.k:108` | rule; supplied, ordinary | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 331 | `reference-semantics/semantics/core.k:109` | syntax; supplied, function, total | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 332 | `reference-semantics/semantics/core.k:110` | rule; supplied, ordinary | `rule pnMember(_:String, .ParamNames) => false` |
| 333 | `reference-semantics/semantics/core.k:111` | rule; supplied, ordinary | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 334 | `reference-semantics/semantics/core.k:113` | syntax; supplied | `syntax KItem ::= #cellW(Val, Val)` |
| 335 | `reference-semantics/semantics/core.k:114` | rule; supplied, ordinary | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| 336 | `reference-semantics/semantics/core.k:117` | syntax; supplied | `syntax KItem ::= #alloc(Val)` |
| 337 | `reference-semantics/semantics/core.k:118` | rule; supplied, ordinary | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) // ==== module load + statement sequencing ==================================` |
| 338 | `reference-semantics/semantics/core.k:124` | syntax; supplied | `syntax KItem ::= #loadAll(Module)` |
| 339 | `reference-semantics/semantics/core.k:125` | rule; supplied, ordinary | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 340 | `reference-semantics/semantics/core.k:126` | rule; supplied, ordinary | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 341 | `reference-semantics/semantics/core.k:127` | rule; supplied, ordinary | `rule <k> .Stmts => .K ... </k> // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====` |
| 342 | `reference-semantics/semantics/core.k:130` | syntax; supplied | `syntax KItem ::= #look(String, Int)` |
| 343 | `reference-semantics/semantics/core.k:131` | rule; supplied, ordinary | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 344 | `reference-semantics/semantics/core.k:132` | rule; supplied, concrete | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (higher priority beats the plain return above on concrete cell // bindings; abstract claim values take the plain rule unchanged) — this // covers cross-frame cell reads (a comprehension closure reading the // enclosing function's cellvar) without a narrowing-prone k-top redex // guarded on the FOUND frame's DECLARED cellvars (pnMember over the // cellsMark): decidable for every concrete frame pin — plain frames and // non-cell names prune outright, so an abstract looked-up value never // drags a narrowing cellV heap match along (probed on 5-intersperse and // Q4's abstract \`numbers\` in the annotated frame)` |
| 345 | `reference-semantics/semantics/core.k:145` | rule; supplied, ordinary, priority(40) | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| 346 | `reference-semantics/semantics/core.k:152` | rule; supplied, ordinary | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) // the ONE predefined builtins scope (the -1 frame; claims write \`-1 \|-> builtinsScope\`)` |
| 347 | `reference-semantics/semantics/core.k:157` | syntax; supplied, function, total | `syntax Scope ::= "builtinsScope" [function, total]` |
| 348 | `reference-semantics/semantics/core.k:158` | rule; supplied, ordinary | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root) // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination == // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)` |
| 349 | `reference-semantics/semantics/core.k:185` | syntax; supplied | `syntax ApplyK ::= toCall(Val)` |
| 350 | `reference-semantics/semantics/core.k:186` | syntax; supplied | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 351 | `reference-semantics/semantics/core.k:189` | rule; supplied, ordinary | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 352 | `reference-semantics/semantics/core.k:190` | rule; supplied, ordinary | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 353 | `reference-semantics/semantics/core.k:191` | rule; supplied, ordinary | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> // ==== Int / Bool / None literals ==========================================` |
| 354 | `reference-semantics/semantics/core.k:194` | rule; supplied, ordinary | `rule <k> Int(I:Int) => I ... </k>` |
| 355 | `reference-semantics/semantics/core.k:195` | rule; supplied, ordinary | `rule <k> Bool(B:Bool) => B ... </k>` |
| 356 | `reference-semantics/semantics/core.k:196` | rule; supplied, ordinary | `rule <k> NoneVal => noneV ... </k> // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================` |
| 357 | `reference-semantics/semantics/core.k:199` | syntax; supplied, function | `syntax Bool ::= truthy(Val) [function]` |
| 358 | `reference-semantics/semantics/core.k:200` | rule; supplied, ordinary | `rule truthy(B:Bool) => B` |
| 359 | `reference-semantics/semantics/core.k:201` | rule; supplied, ordinary | `rule truthy(noneV) => false` |
| 360 | `reference-semantics/semantics/core.k:202` | rule; supplied, ordinary | `rule truthy(I:Int) => I =/=Int 0` |
| 361 | `reference-semantics/semantics/core.k:203` | rule; supplied, ordinary | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| 362 | `reference-semantics/semantics/core.k:204` | rule; supplied, ordinary | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 363 | `reference-semantics/semantics/core.k:205` | rule; supplied, ordinary | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) // ==== extensible operator dispatch (cases added by the construct modules) ==` |
| 364 | `reference-semantics/semantics/core.k:208` | syntax; supplied, function | `syntax Val ::= applyUn(String, Val) [function]` |
| 365 | `reference-semantics/semantics/core.k:209` | syntax; supplied, function | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| 366 | `reference-semantics/semantics/core.k:210` | syntax; supplied, function | `syntax Bool ::= applyCmp(String, Val, Val) [function] // ==== shared list helpers =================================================` |
| 367 | `reference-semantics/semantics/core.k:213` | syntax; supplied, function, total | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 368 | `reference-semantics/semantics/core.k:214` | rule; supplied, ordinary | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| 369 | `reference-semantics/semantics/core.k:215` | rule; supplied, ordinary | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` |
| 370 | `reference-semantics/semantics/core.k:217` | syntax; supplied, function, total | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 371 | `reference-semantics/semantics/core.k:218` | rule; supplied, ordinary | `rule vals2valSeq(.Vals) => .ValSeq` |
| 372 | `reference-semantics/semantics/core.k:219` | rule; supplied, ordinary | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) // ==== shared sequence length (len / summaries across many modules) ======== // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)` |
| 373 | `reference-semantics/semantics/core.k:223` | syntax; supplied, function, total | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 374 | `reference-semantics/semantics/core.k:224` | rule; supplied, ordinary | `rule vsLen(.ValSeq) => 0` |
| 375 | `reference-semantics/semantics/core.k:225` | rule; supplied, ordinary | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 376 | `reference-semantics/semantics/core.k:227` | syntax; supplied, function, total | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 377 | `reference-semantics/semantics/core.k:228` | rule; supplied, ordinary | `rule isLen(.IntSeq) => 0` |
| 378 | `reference-semantics/semantics/core.k:229` | rule; supplied, ordinary | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)` |
| 379 | `reference-semantics/semantics/core.k:233` | syntax; supplied, function, total | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 380 | `reference-semantics/semantics/core.k:234` | rule; supplied, ordinary | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| 381 | `reference-semantics/semantics/core.k:235` | rule; supplied, ordinary | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| 382 | `reference-semantics/semantics/core.k:236` | rule; supplied, ordinary | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 383 | `reference-semantics/semantics/core.k:238` | rule; supplied, ordinary | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` |
| 384 | `reference-semantics/semantics/core.k:240` | endmodule; supplied | `endmodule` |
| 385 | `reference-semantics/semantics/dict.k:13` | module; supplied | `module MPY-DICT imports MPY-CORE imports MPY-ITER imports MPY-METHODS imports MPY-LIST // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).` |
| 386 | `reference-semantics/semantics/dict.k:20` | syntax; supplied | `syntax Val ::= dictV(ValSeq, ValSeq) // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.` |
| 387 | `reference-semantics/semantics/dict.k:23` | syntax; supplied | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 388 | `reference-semantics/semantics/dict.k:26` | rule; supplied, ordinary | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 389 | `reference-semantics/semantics/dict.k:27` | rule; supplied, ordinary | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 390 | `reference-semantics/semantics/dict.k:28` | rule; supplied, ordinary | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 391 | `reference-semantics/semantics/dict.k:30` | rule; supplied, ordinary | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 392 | `reference-semantics/semantics/dict.k:32` | rule; supplied, concrete | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.` |
| 393 | `reference-semantics/semantics/dict.k:37` | syntax; supplied, function, total | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 394 | `reference-semantics/semantics/dict.k:38` | rule; supplied, ordinary | `rule dHasKey(.ValSeq, _:Val) => false` |
| 395 | `reference-semantics/semantics/dict.k:39` | rule; supplied, ordinary | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| 396 | `reference-semantics/semantics/dict.k:40` | rule; supplied, ordinary | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) // dPutK: KS unchanged if K already present, else append K (keep-first-position).` |
| 397 | `reference-semantics/semantics/dict.k:43` | syntax; supplied, function, total | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 398 | `reference-semantics/semantics/dict.k:44` | rule; supplied, ordinary | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| 399 | `reference-semantics/semantics/dict.k:45` | rule; supplied, ordinary, owise | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).` |
| 400 | `reference-semantics/semantics/dict.k:49` | syntax; supplied, function, total | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 401 | `reference-semantics/semantics/dict.k:50` | rule; supplied, ordinary | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` |
| 402 | `reference-semantics/semantics/dict.k:52` | rule; supplied, ordinary | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 403 | `reference-semantics/semantics/dict.k:54` | rule; supplied, ordinary, owise | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] // ==== dict methods ======================================================== // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).` |
| 404 | `reference-semantics/semantics/dict.k:58` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==` |
| 405 | `reference-semantics/semantics/dict.k:63` | rule; supplied, ordinary | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 406 | `reference-semantics/semantics/dict.k:64` | syntax; supplied, function | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 407 | `reference-semantics/semantics/dict.k:65` | rule; supplied, ordinary, priority(45) | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] // ==== dict subscript-assign: d[k] = v (insert/update in place) ============= // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.` |
| 408 | `reference-semantics/semantics/dict.k:70` | syntax; supplied, function | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 409 | `reference-semantics/semantics/dict.k:71` | rule; supplied, ordinary | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope // value: a bare dict updates in the scope (dicts stay values); a ref (a heap // list — or a heap dict later) writes the heap in place.` |
| 410 | `reference-semantics/semantics/dict.k:76` | syntax; supplied | `syntax KItem ::= #dsetK(String, Val)` |
| 411 | `reference-semantics/semantics/dict.k:77` | rule; supplied, ordinary | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 412 | `reference-semantics/semantics/dict.k:78` | rule; supplied, ordinary | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| 413 | `reference-semantics/semantics/dict.k:82` | rule; supplied, ordinary | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 414 | `reference-semantics/semantics/dict.k:86` | syntax; supplied | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 415 | `reference-semantics/semantics/dict.k:87` | rule; supplied, ordinary | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is not imported here)` |
| 416 | `reference-semantics/semantics/dict.k:90` | syntax; supplied, function, total | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 417 | `reference-semantics/semantics/dict.k:91` | rule; supplied, ordinary | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 418 | `reference-semantics/semantics/dict.k:92` | rule; supplied, ordinary | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 // ==== dict == (order-insensitive: same size + same key->value pairs) =======` |
| 419 | `reference-semantics/semantics/dict.k:95` | rule; supplied, ordinary | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 420 | `reference-semantics/semantics/dict.k:97` | syntax; supplied, function | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 421 | `reference-semantics/semantics/dict.k:98` | rule; supplied, ordinary | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 422 | `reference-semantics/semantics/dict.k:99` | rule; supplied, ordinary | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 423 | `reference-semantics/semantics/dict.k:101` | syntax; supplied, function | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 424 | `reference-semantics/semantics/dict.k:102` | rule; supplied, ordinary | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| 425 | `reference-semantics/semantics/dict.k:103` | rule; supplied, ordinary | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 426 | `reference-semantics/semantics/dict.k:104` | endmodule; supplied | `endmodule` |
| 427 | `reference-semantics/semantics/float.k:14` | module; supplied | `module MPY-FLOAT imports MPY-OPERATORS imports MPY-BUILTINS imports FLOAT // Float is a value; the float literal evaluates to the K Float.` |
| 428 | `reference-semantics/semantics/float.k:20` | syntax; supplied | `syntax Val ::= Float` |
| 429 | `reference-semantics/semantics/float.k:21` | rule; supplied, concrete | `rule <k> Float(F:Float) => F ... </k> // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.` |
| 430 | `reference-semantics/semantics/float.k:24` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 431 | `reference-semantics/semantics/float.k:25` | rule; supplied, concrete | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 432 | `reference-semantics/semantics/float.k:27` | rule; supplied, concrete | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.` |
| 433 | `reference-semantics/semantics/float.k:30` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 434 | `reference-semantics/semantics/float.k:31` | rule; supplied, concrete | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 435 | `reference-semantics/semantics/float.k:32` | rule; supplied, concrete | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) // float % float (e.g. \`number % 1.0\` = the fractional part). OPAQUE for kprove, concrete for // krun. Python's float \`%\` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).` |
| 436 | `reference-semantics/semantics/float.k:37` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 437 | `reference-semantics/semantics/float.k:38` | rule; supplied, concrete | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 438 | `reference-semantics/semantics/float.k:39` | rule; supplied, concrete | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) // float equality — for concrete krun asserts (e.g. \`area == 7.5\`); the FLOAT.eq hook is fine on // concrete floats. kprove proofs return floats structurally and do not compare them.` |
| 439 | `reference-semantics/semantics/float.k:43` | rule; supplied, ordinary | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 440 | `reference-semantics/semantics/float.k:44` | rule; supplied, concrete | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) // float \`<\` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade), // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise // \`abs(a-b) < t\` proximity test.)` |
| 441 | `reference-semantics/semantics/float.k:50` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 442 | `reference-semantics/semantics/float.k:51` | rule; supplied, concrete | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 443 | `reference-semantics/semantics/float.k:52` | rule; supplied, ordinary | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 444 | `reference-semantics/semantics/float.k:54` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 445 | `reference-semantics/semantics/float.k:55` | rule; supplied, concrete | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 446 | `reference-semantics/semantics/float.k:56` | rule; supplied, ordinary | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F) // ==== math.ceil =========================================================== // \`import X\` is a no-op (we intercept the specific math functions syntactically; \`math\` itself is // never bound as a value).` |
| 447 | `reference-semantics/semantics/float.k:61` | rule; supplied, ordinary | `rule <k> Import(_:String) => .K ... </k> // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE \`math\` is looked up (higher // priority than the generic Attribute/method dispatch in call.k).` |
| 448 | `reference-semantics/semantics/float.k:65` | syntax; supplied | `syntax KItem ::= "#mathCeil"` |
| 449 | `reference-semantics/semantics/float.k:66` | rule; supplied, ordinary, priority(40) | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 450 | `reference-semantics/semantics/float.k:67` | rule; supplied, ordinary | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> // math.floor(x) — same interception shape as math.ceil` |
| 451 | `reference-semantics/semantics/float.k:70` | syntax; supplied | `syntax KItem ::= "#mathFloor"` |
| 452 | `reference-semantics/semantics/float.k:71` | rule; supplied, ordinary, priority(40) | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 453 | `reference-semantics/semantics/float.k:72` | rule; supplied, ordinary | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 454 | `reference-semantics/semantics/float.k:73` | syntax; supplied, function, total | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 455 | `reference-semantics/semantics/float.k:74` | rule; supplied, concrete | `rule floorFI(I:Int) => I [concrete]` |
| 456 | `reference-semantics/semantics/float.k:75` | rule; supplied, concrete | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] // bare floor/ceil (bound by \`from math import floor, ceil\`)` |
| 457 | `reference-semantics/semantics/float.k:78` | rule; supplied, ordinary | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 458 | `reference-semantics/semantics/float.k:79` | rule; supplied, ordinary | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) // math.pow(x, y) — a two-arg interception onto powF (ints promote)` |
| 459 | `reference-semantics/semantics/float.k:82` | syntax; supplied | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 460 | `reference-semantics/semantics/float.k:83` | rule; supplied, ordinary, priority(40) | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 461 | `reference-semantics/semantics/float.k:84` | rule; supplied, ordinary | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 462 | `reference-semantics/semantics/float.k:85` | rule; supplied, ordinary | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 463 | `reference-semantics/semantics/float.k:86` | syntax; supplied, function, total | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 464 | `reference-semantics/semantics/float.k:87` | rule; supplied, concrete | `rule toF(F:Float) => F [concrete]` |
| 465 | `reference-semantics/semantics/float.k:88` | rule; supplied, concrete | `rule toF(I:Int) => intToF(I) [concrete] // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm). // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).` |
| 466 | `reference-semantics/semantics/float.k:93` | syntax; supplied, function, total | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 467 | `reference-semantics/semantics/float.k:94` | rule; supplied, concrete | `rule ceilF(I:Int) => I [concrete]` |
| 468 | `reference-semantics/semantics/float.k:95` | rule; supplied, concrete | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun; // proofs use symbolic elements, never a float literal.` |
| 469 | `reference-semantics/semantics/float.k:99` | rule; supplied, concrete | `rule applyUn("-", F:Float) => 0.0 -Float F // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.` |
| 470 | `reference-semantics/semantics/float.k:103` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 471 | `reference-semantics/semantics/float.k:104` | rule; supplied, concrete | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 472 | `reference-semantics/semantics/float.k:105` | rule; supplied, ordinary | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 473 | `reference-semantics/semantics/float.k:107` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 474 | `reference-semantics/semantics/float.k:108` | rule; supplied, concrete | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 475 | `reference-semantics/semantics/float.k:109` | rule; supplied, ordinary | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 476 | `reference-semantics/semantics/float.k:111` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 477 | `reference-semantics/semantics/float.k:112` | rule; supplied, concrete | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 478 | `reference-semantics/semantics/float.k:113` | rule; supplied, ordinary | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 479 | `reference-semantics/semantics/float.k:115` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 480 | `reference-semantics/semantics/float.k:116` | rule; supplied, concrete | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 481 | `reference-semantics/semantics/float.k:117` | rule; supplied, ordinary | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 482 | `reference-semantics/semantics/float.k:119` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 483 | `reference-semantics/semantics/float.k:120` | rule; supplied, concrete | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 484 | `reference-semantics/semantics/float.k:121` | rule; supplied, ordinary | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) // ---- the remaining comparisons (gtF promoted from find_zero — its summaries // case-split on the atom; >= / <= derive from the two opaque compares) ----` |
| 485 | `reference-semantics/semantics/float.k:125` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 486 | `reference-semantics/semantics/float.k:126` | rule; supplied, concrete | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 487 | `reference-semantics/semantics/float.k:127` | rule; supplied, ordinary | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| 488 | `reference-semantics/semantics/float.k:128` | rule; supplied, ordinary | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 489 | `reference-semantics/semantics/float.k:129` | rule; supplied, ordinary | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----` |
| 490 | `reference-semantics/semantics/float.k:132` | rule; supplied, ordinary | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 491 | `reference-semantics/semantics/float.k:133` | rule; supplied, ordinary | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 492 | `reference-semantics/semantics/float.k:134` | rule; supplied, ordinary | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 493 | `reference-semantics/semantics/float.k:135` | rule; supplied, ordinary | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 494 | `reference-semantics/semantics/float.k:136` | rule; supplied, ordinary | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 495 | `reference-semantics/semantics/float.k:137` | rule; supplied, ordinary | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 496 | `reference-semantics/semantics/float.k:138` | rule; supplied, ordinary | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 497 | `reference-semantics/semantics/float.k:139` | rule; supplied, concrete | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----` |
| 498 | `reference-semantics/semantics/float.k:142` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 499 | `reference-semantics/semantics/float.k:143` | rule; supplied, concrete | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 500 | `reference-semantics/semantics/float.k:144` | rule; supplied, ordinary | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 501 | `reference-semantics/semantics/float.k:145` | rule; supplied, ordinary | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 502 | `reference-semantics/semantics/float.k:146` | rule; supplied, ordinary | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 503 | `reference-semantics/semantics/float.k:147` | rule; supplied, ordinary | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 504 | `reference-semantics/semantics/float.k:148` | rule; supplied, ordinary | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 505 | `reference-semantics/semantics/float.k:149` | rule; supplied, ordinary | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 506 | `reference-semantics/semantics/float.k:150` | rule; supplied, ordinary | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 507 | `reference-semantics/semantics/float.k:151` | rule; supplied, ordinary | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- x == None (promoted from 137; \`is\` cases live in operators.k) ----` |
| 508 | `reference-semantics/semantics/float.k:154` | rule; supplied, ordinary | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 509 | `reference-semantics/semantics/float.k:155` | rule; supplied, concrete | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) // ---- float(str): decimal parse (promoted from 137's defined chain) ---- // digits '.' digits, optional leading '-'; concrete evaluation only (the // symbolic side stays an opaque decStrToF term a proof case-splits on).` |
| 510 | `reference-semantics/semantics/float.k:160` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 511 | `reference-semantics/semantics/float.k:161` | rule; supplied, concrete | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 512 | `reference-semantics/semantics/float.k:162` | rule; supplied, concrete | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 513 | `reference-semantics/semantics/float.k:165` | syntax; supplied, function | `syntax Int ::= headIS(IntSeq) [function]` |
| 514 | `reference-semantics/semantics/float.k:166` | rule; supplied, ordinary | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 515 | `reference-semantics/semantics/float.k:167` | syntax; supplied, function, total | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 516 | `reference-semantics/semantics/float.k:168` | rule; supplied, ordinary | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 517 | `reference-semantics/semantics/float.k:169` | rule; supplied, ordinary | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 518 | `reference-semantics/semantics/float.k:170` | rule; supplied, ordinary | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 519 | `reference-semantics/semantics/float.k:171` | rule; supplied, ordinary | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 520 | `reference-semantics/semantics/float.k:173` | syntax; supplied, function, total | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 521 | `reference-semantics/semantics/float.k:174` | rule; supplied, ordinary | `rule fracPart(.IntSeq) => 0` |
| 522 | `reference-semantics/semantics/float.k:175` | rule; supplied, ordinary | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 523 | `reference-semantics/semantics/float.k:176` | rule; supplied, ordinary | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 524 | `reference-semantics/semantics/float.k:177` | rule; supplied, ordinary | `rule fracAcc(.IntSeq, A:Int) => A` |
| 525 | `reference-semantics/semantics/float.k:178` | rule; supplied, ordinary | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 526 | `reference-semantics/semantics/float.k:179` | syntax; supplied, function, total | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 527 | `reference-semantics/semantics/float.k:180` | rule; supplied, ordinary | `rule fracScale(.IntSeq) => 1` |
| 528 | `reference-semantics/semantics/float.k:181` | rule; supplied, ordinary | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 529 | `reference-semantics/semantics/float.k:182` | rule; supplied, ordinary | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 530 | `reference-semantics/semantics/float.k:183` | rule; supplied, ordinary | `rule fscAcc(.IntSeq, A:Int) => A` |
| 531 | `reference-semantics/semantics/float.k:184` | rule; supplied, ordinary | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 532 | `reference-semantics/semantics/float.k:185` | rule; supplied, ordinary | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 533 | `reference-semantics/semantics/float.k:186` | rule; supplied, ordinary | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 534 | `reference-semantics/semantics/float.k:187` | rule; supplied, ordinary | `rule applyBuiltin("float", F:Float, .Vals) => F // ---- float / int division (promoted from mean_absolute_deviation) ----` |
| 535 | `reference-semantics/semantics/float.k:190` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 536 | `reference-semantics/semantics/float.k:191` | rule; supplied, concrete | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 537 | `reference-semantics/semantics/float.k:192` | rule; supplied, ordinary | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) // ---- int -> float promotion for the remaining mixed arithmetic/compares ----` |
| 538 | `reference-semantics/semantics/float.k:195` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 539 | `reference-semantics/semantics/float.k:196` | rule; supplied, concrete | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 540 | `reference-semantics/semantics/float.k:197` | rule; supplied, ordinary | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 541 | `reference-semantics/semantics/float.k:198` | rule; supplied, ordinary | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 542 | `reference-semantics/semantics/float.k:199` | rule; supplied, ordinary | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 543 | `reference-semantics/semantics/float.k:200` | rule; supplied, ordinary | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 544 | `reference-semantics/semantics/float.k:201` | rule; supplied, ordinary | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 545 | `reference-semantics/semantics/float.k:202` | rule; supplied, ordinary | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 546 | `reference-semantics/semantics/float.k:203` | rule; supplied, ordinary | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 547 | `reference-semantics/semantics/float.k:204` | rule; supplied, ordinary | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 548 | `reference-semantics/semantics/float.k:205` | rule; supplied, ordinary | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 549 | `reference-semantics/semantics/float.k:206` | rule; supplied, ordinary | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----` |
| 550 | `reference-semantics/semantics/float.k:209` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 551 | `reference-semantics/semantics/float.k:210` | rule; supplied, concrete | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 552 | `reference-semantics/semantics/float.k:211` | rule; supplied, ordinary | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 553 | `reference-semantics/semantics/float.k:213` | rule; supplied, ordinary | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 554 | `reference-semantics/semantics/float.k:214` | rule; supplied, ordinary | `rule applyBuiltin("float", F:Float, .Vals) => F // round: Python half-even (banker's); round(F, N) scales by 10^N` |
| 555 | `reference-semantics/semantics/float.k:217` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 556 | `reference-semantics/semantics/float.k:218` | rule; supplied, concrete | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| 557 | `reference-semantics/semantics/float.k:223` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 558 | `reference-semantics/semantics/float.k:224` | rule; supplied, concrete | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 559 | `reference-semantics/semantics/float.k:227` | rule; supplied, ordinary | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| 560 | `reference-semantics/semantics/float.k:228` | rule; supplied, ordinary | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 561 | `reference-semantics/semantics/float.k:230` | syntax; supplied, function, total, opaque/no-evaluators | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 562 | `reference-semantics/semantics/float.k:231` | rule; supplied, concrete | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 563 | `reference-semantics/semantics/float.k:232` | syntax; supplied | `syntax KItem ::= "#mathSqrt"` |
| 564 | `reference-semantics/semantics/float.k:233` | rule; supplied, ordinary, priority(40) | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 565 | `reference-semantics/semantics/float.k:234` | rule; supplied, ordinary | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 566 | `reference-semantics/semantics/float.k:235` | rule; supplied, concrete | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which // seed/step with \`requires isInt(V)\`, so they are STUCK on floats). These add the \`requires // isFloat(V)\` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive: // the isFloat guard is disjoint from the existing isInt one.` |
| 567 | `reference-semantics/semantics/float.k:243` | syntax; supplied | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 568 | `reference-semantics/semantics/float.k:244` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 569 | `reference-semantics/semantics/float.k:245` | rule; supplied, ordinary | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 570 | `reference-semantics/semantics/float.k:246` | rule; supplied, ordinary | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 571 | `reference-semantics/semantics/float.k:247` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 572 | `reference-semantics/semantics/float.k:250` | syntax; supplied | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 573 | `reference-semantics/semantics/float.k:251` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 574 | `reference-semantics/semantics/float.k:252` | rule; supplied, ordinary | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 575 | `reference-semantics/semantics/float.k:253` | rule; supplied, ordinary | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 576 | `reference-semantics/semantics/float.k:254` | rule; supplied, concrete | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin). // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof // with isInt(V) in its path condition refutes this branch without sort reasoning.` |
| 577 | `reference-semantics/semantics/float.k:261` | syntax; supplied | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 578 | `reference-semantics/semantics/float.k:262` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 579 | `reference-semantics/semantics/float.k:265` | rule; supplied, ordinary | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 580 | `reference-semantics/semantics/float.k:266` | rule; supplied, ordinary | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 581 | `reference-semantics/semantics/float.k:267` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 582 | `reference-semantics/semantics/float.k:270` | rule; supplied, ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| 583 | `reference-semantics/semantics/float.k:273` | endmodule; supplied | `endmodule` |
| 584 | `reference-semantics/semantics/functions.k:3` | module; supplied | `module MPY-FUNCTIONS imports MPY-CORE // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k; // this module owns the frame lifecycle (bind params, return, pop).` |
| 585 | `reference-semantics/semantics/functions.k:8` | syntax; supplied | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" // ==== def / anonymous closure =============================================` |
| 586 | `reference-semantics/semantics/functions.k:14` | rule; supplied, ordinary | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 587 | `reference-semantics/semantics/functions.k:18` | syntax; supplied | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 588 | `reference-semantics/semantics/functions.k:19` | rule; supplied, ordinary | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> // ==== annotated def/lambda (closure cells; spec 2.3) ====================== // closureValC(params, cellvars, body, captured-cells). No frame anchor: all // enclosing-local reads are freevars (symtable-complete) and go through the // captured cells; everything else is global/builtin, so the callee frame's // parent is the module scope (0) — sound after the defining frame dies.` |
| 589 | `reference-semantics/semantics/functions.k:27` | syntax; supplied | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) // capture: resolve each freevar to the enclosing frame's cellRef, then bind // (FuncDef) or yield (Lambda) the closure value.` |
| 590 | `reference-semantics/semantics/functions.k:31` | syntax; supplied | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 591 | `reference-semantics/semantics/functions.k:33` | rule; supplied, ordinary | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 592 | `reference-semantics/semantics/functions.k:36` | rule; supplied, ordinary | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 593 | `reference-semantics/semantics/functions.k:42` | rule; supplied, ordinary | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| 594 | `reference-semantics/semantics/functions.k:47` | rule; supplied, ordinary | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 595 | `reference-semantics/semantics/functions.k:50` | rule; supplied, ordinary | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 596 | `reference-semantics/semantics/functions.k:53` | rule; supplied, ordinary | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 597 | `reference-semantics/semantics/functions.k:59` | rule; supplied, ordinary | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> // ==== bind params ========================================================` |
| 598 | `reference-semantics/semantics/functions.k:63` | rule; supplied, ordinary | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 599 | `reference-semantics/semantics/functions.k:64` | rule; supplied, ordinary | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound to its cell at frame entry` |
| 600 | `reference-semantics/semantics/functions.k:68` | rule; supplied, ordinary, priority(40) | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] // ==== return / pop the frame (the returned expr evaluates by strictness) ==` |
| 601 | `reference-semantics/semantics/functions.k:78` | rule; supplied, ordinary | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 602 | `reference-semantics/semantics/functions.k:80` | rule; supplied, ordinary | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).` |
| 603 | `reference-semantics/semantics/functions.k:85` | rule; supplied, ordinary | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| 604 | `reference-semantics/semantics/functions.k:91` | endmodule; supplied | `endmodule` |
| 605 | `reference-semantics/semantics/int.k:4` | module; supplied | `module MPY-INT imports MPY-CORE` |
| 606 | `reference-semantics/semantics/int.k:7` | rule; supplied, ordinary | `rule applyUn("-", I:Int) => 0 -Int I` |
| 607 | `reference-semantics/semantics/int.k:9` | rule; supplied, ordinary | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b))` |
| 608 | `reference-semantics/semantics/int.k:11` | rule; supplied, ordinary | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 609 | `reference-semantics/semantics/int.k:12` | rule; supplied, ordinary | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 610 | `reference-semantics/semantics/int.k:13` | rule; supplied, ordinary | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| 611 | `reference-semantics/semantics/int.k:14` | rule; supplied, ordinary | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| 612 | `reference-semantics/semantics/int.k:15` | rule; supplied, ordinary | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| 613 | `reference-semantics/semantics/int.k:16` | rule; supplied, ordinary | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 614 | `reference-semantics/semantics/int.k:17` | rule; supplied, ordinary | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 615 | `reference-semantics/semantics/int.k:19` | syntax; supplied, function | `syntax Int ::= pyMod(Int, Int) [function]` |
| 616 | `reference-semantics/semantics/int.k:20` | rule; supplied, ordinary | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 617 | `reference-semantics/semantics/int.k:22` | rule; supplied, ordinary | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| 618 | `reference-semantics/semantics/int.k:23` | rule; supplied, ordinary | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| 619 | `reference-semantics/semantics/int.k:24` | rule; supplied, ordinary | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| 620 | `reference-semantics/semantics/int.k:25` | rule; supplied, ordinary | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| 621 | `reference-semantics/semantics/int.k:26` | rule; supplied, ordinary | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| 622 | `reference-semantics/semantics/int.k:27` | rule; supplied, ordinary | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |
| 623 | `reference-semantics/semantics/int.k:28` | endmodule; supplied | `endmodule` |
| 624 | `reference-semantics/semantics/iter.k:6` | module; supplied | `module MPY-ITER imports MPY-CORE` |
| 625 | `reference-semantics/semantics/iter.k:8` | syntax; supplied | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| 626 | `reference-semantics/semantics/iter.k:9` | endmodule; supplied | `endmodule` |
| 627 | `reference-semantics/semantics/list.k:3` | module; supplied | `module MPY-LIST imports MPY-CORE imports MPY-ITER imports MPY-OPERATORS // ==== iteration (the iterator protocol's list case) =======================` |
| 628 | `reference-semantics/semantics/list.k:9` | rule; supplied, ordinary | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| 629 | `reference-semantics/semantics/list.k:10` | rule; supplied, ordinary | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> // ==== ListExpr: [...] literal -> a fresh heap object =======================` |
| 630 | `reference-semantics/semantics/list.k:13` | syntax; supplied | `syntax ApplyK ::= "toList"` |
| 631 | `reference-semantics/semantics/list.k:14` | rule; supplied, ordinary | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 632 | `reference-semantics/semantics/list.k:15` | rule; supplied, ordinary | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> // ==== list ops: + / == / != ===============================================` |
| 633 | `reference-semantics/semantics/list.k:18` | syntax; supplied, function, total | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 634 | `reference-semantics/semantics/list.k:19` | rule; supplied, ordinary | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| 635 | `reference-semantics/semantics/list.k:20` | rule; supplied, ordinary, priority(45) | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) // list + list constructs a NEW object (k-cell — it allocates; operands land here // already deref'd). priority(45) beats the generic BinOp dispatch.` |
| 636 | `reference-semantics/semantics/list.k:24` | rule; supplied, ordinary, priority(45) | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 637 | `reference-semantics/semantics/list.k:27` | rule; supplied, ordinary | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 638 | `reference-semantics/semantics/list.k:28` | rule; supplied, concrete | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) // ==== deep equality when elements are heap objects (list-of-lists) ======== // Python == is structural at every depth. Fires ONLY when a ref is present // (the guard decides on concrete seqs); the plain ==K path above is unchanged.` |
| 639 | `reference-semantics/semantics/list.k:33` | syntax; supplied, function, total | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 640 | `reference-semantics/semantics/list.k:34` | rule; supplied, ordinary | `rule hasRefVS(.ValSeq) => false` |
| 641 | `reference-semantics/semantics/list.k:35` | rule; supplied, ordinary | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 642 | `reference-semantics/semantics/list.k:37` | syntax; supplied, function | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function]` |
| 643 | `reference-semantics/semantics/list.k:39` | rule; supplied, ordinary | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| 644 | `reference-semantics/semantics/list.k:40` | rule; supplied, ordinary | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| 645 | `reference-semantics/semantics/list.k:41` | rule; supplied, ordinary | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| 646 | `reference-semantics/semantics/list.k:42` | rule; supplied, ordinary | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 647 | `reference-semantics/semantics/list.k:45` | rule; supplied, ordinary | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 648 | `reference-semantics/semantics/list.k:47` | rule; supplied, ordinary | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 649 | `reference-semantics/semantics/list.k:49` | rule; supplied, ordinary | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 650 | `reference-semantics/semantics/list.k:50` | rule; supplied, ordinary, owise | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] // ==== mutator: xs.append(v) — an in-place heap write ======================` |
| 651 | `reference-semantics/semantics/list.k:53` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] // ==== \`x in list\` — a <k>-cell fold over #iterNext ========================` |
| 652 | `reference-semantics/semantics/list.k:58` | syntax; supplied | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 653 | `reference-semantics/semantics/list.k:59` | rule; supplied, ordinary | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 654 | `reference-semantics/semantics/list.k:60` | rule; supplied, ordinary | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 655 | `reference-semantics/semantics/list.k:61` | rule; supplied, ordinary | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 656 | `reference-semantics/semantics/list.k:62` | rule; supplied, ordinary | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 657 | `reference-semantics/semantics/list.k:63` | rule; supplied, ordinary | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 658 | `reference-semantics/semantics/list.k:65` | rule; supplied, ordinary | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 659 | `reference-semantics/semantics/list.k:67` | rule; supplied, ordinary | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 660 | `reference-semantics/semantics/list.k:68` | endmodule; supplied | `endmodule` |
| 661 | `reference-semantics/semantics/methods.k:3` | module; supplied | `module MPY-METHODS imports MPY-CORE imports K-EQUAL imports MPY-STR imports MPY-LIST // method-call routing + arg-eval live in call.k; this module owns applyMethod.` |
| 662 | `reference-semantics/semantics/methods.k:10` | syntax; supplied, function | `syntax Val ::= applyMethod(Val, String, Vals) [function] // ==== string predicates (Python semantics) =================================` |
| 663 | `reference-semantics/semantics/methods.k:13` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 664 | `reference-semantics/semantics/methods.k:14` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 665 | `reference-semantics/semantics/methods.k:15` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 666 | `reference-semantics/semantics/methods.k:16` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) // ==== case maps ============================================================` |
| 667 | `reference-semantics/semantics/methods.k:19` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| 668 | `reference-semantics/semantics/methods.k:20` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| 669 | `reference-semantics/semantics/methods.k:21` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) // ==== join / count / strip / encode ======================================== // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by // the call layer; the result str is a value)` |
| 670 | `reference-semantics/semantics/methods.k:26` | rule; supplied, ordinary | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 671 | `reference-semantics/semantics/methods.k:27` | syntax; supplied, function, total | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 672 | `reference-semantics/semantics/methods.k:28` | rule; supplied, ordinary | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 673 | `reference-semantics/semantics/methods.k:29` | rule; supplied, ordinary | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 674 | `reference-semantics/semantics/methods.k:30` | rule; supplied, ordinary | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) // S.count(sub): non-overlapping window scan (Python str.count)` |
| 675 | `reference-semantics/semantics/methods.k:34` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 676 | `reference-semantics/semantics/methods.k:35` | syntax; supplied, function | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 677 | `reference-semantics/semantics/methods.k:36` | rule; supplied, ordinary | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 678 | `reference-semantics/semantics/methods.k:37` | rule; supplied, ordinary | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 679 | `reference-semantics/semantics/methods.k:39` | rule; supplied, ordinary | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 680 | `reference-semantics/semantics/methods.k:41` | syntax; supplied, function, total | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 681 | `reference-semantics/semantics/methods.k:42` | rule; supplied, ordinary | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 682 | `reference-semantics/semantics/methods.k:43` | rule; supplied, ordinary, owise | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 683 | `reference-semantics/semantics/methods.k:44` | rule; supplied, ordinary | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 // S.strip(): trim whitespace runs from both ends` |
| 684 | `reference-semantics/semantics/methods.k:47` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 685 | `reference-semantics/semantics/methods.k:48` | syntax; supplied, function, total | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 686 | `reference-semantics/semantics/methods.k:49` | rule; supplied, ordinary | `rule trimWS(.IntSeq) => .IntSeq` |
| 687 | `reference-semantics/semantics/methods.k:50` | rule; supplied, ordinary | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 688 | `reference-semantics/semantics/methods.k:51` | rule; supplied, ordinary | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 689 | `reference-semantics/semantics/methods.k:52` | syntax; supplied, function, total | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 690 | `reference-semantics/semantics/methods.k:53` | rule; supplied, ordinary | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 691 | `reference-semantics/semantics/methods.k:54` | rule; supplied, ordinary | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 692 | `reference-semantics/semantics/methods.k:55` | rule; supplied, ordinary | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) // S.encode('ascii'): identity on the code-sequence model (bytes == codes)` |
| 693 | `reference-semantics/semantics/methods.k:58` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) // ==== prefix ===============================================================` |
| 694 | `reference-semantics/semantics/methods.k:61` | rule; supplied, concrete | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========` |
| 695 | `reference-semantics/semantics/methods.k:64` | rule; supplied, ordinary | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 696 | `reference-semantics/semantics/methods.k:65` | syntax; supplied, function, total | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 697 | `reference-semantics/semantics/methods.k:66` | rule; supplied, ordinary | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| 698 | `reference-semantics/semantics/methods.k:67` | rule; supplied, ordinary | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 699 | `reference-semantics/semantics/methods.k:68` | rule; supplied, ordinary | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ========== // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.` |
| 700 | `reference-semantics/semantics/methods.k:72` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 701 | `reference-semantics/semantics/methods.k:75` | syntax; supplied, function | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` |
| 702 | `reference-semantics/semantics/methods.k:76` | rule; supplied, ordinary | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 703 | `reference-semantics/semantics/methods.k:77` | rule; supplied, ordinary | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 704 | `reference-semantics/semantics/methods.k:79` | rule; supplied, ordinary | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty.` |
| 705 | `reference-semantics/semantics/methods.k:82` | syntax; supplied, function | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 706 | `reference-semantics/semantics/methods.k:83` | rule; supplied, ordinary | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| 707 | `reference-semantics/semantics/methods.k:84` | rule; supplied, ordinary | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 708 | `reference-semantics/semantics/methods.k:85` | syntax; supplied, function, total | `syntax Bool ::= isWSC(Int) [function, total]` |
| 709 | `reference-semantics/semantics/methods.k:86` | rule; supplied, ordinary | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 // split(sep='x') keyword form delegates to the positional k-cell rule` |
| 710 | `reference-semantics/semantics/methods.k:89` | rule; supplied, ordinary, priority(39) | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).` |
| 711 | `reference-semantics/semantics/methods.k:94` | rule; supplied, ordinary, priority(40) | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 712 | `reference-semantics/semantics/methods.k:97` | syntax; supplied, function | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` |
| 713 | `reference-semantics/semantics/methods.k:98` | rule; supplied, ordinary | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| 714 | `reference-semantics/semantics/methods.k:99` | rule; supplied, ordinary | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 715 | `reference-semantics/semantics/methods.k:101` | rule; supplied, ordinary | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 716 | `reference-semantics/semantics/methods.k:104` | rule; supplied, ordinary | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 717 | `reference-semantics/semantics/methods.k:106` | syntax; supplied, function, total | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 718 | `reference-semantics/semantics/methods.k:107` | rule; supplied, ordinary | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| 719 | `reference-semantics/semantics/methods.k:108` | rule; supplied, ordinary | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 720 | `reference-semantics/semantics/methods.k:109` | rule; supplied, ordinary | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) // ==== char helpers =========================================================` |
| 721 | `reference-semantics/semantics/methods.k:112` | syntax; supplied, function, total | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 722 | `reference-semantics/semantics/methods.k:113` | rule; supplied, ordinary | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 723 | `reference-semantics/semantics/methods.k:115` | syntax; supplied, function, total | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 724 | `reference-semantics/semantics/methods.k:116` | rule; supplied, ordinary | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 725 | `reference-semantics/semantics/methods.k:118` | syntax; supplied, function, total | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 726 | `reference-semantics/semantics/methods.k:119` | rule; supplied, ordinary | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 727 | `reference-semantics/semantics/methods.k:121` | syntax; supplied, function, total | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 728 | `reference-semantics/semantics/methods.k:122` | rule; supplied, ordinary | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 729 | `reference-semantics/semantics/methods.k:124` | syntax; supplied, function, total | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 730 | `reference-semantics/semantics/methods.k:125` | rule; supplied, ordinary | `rule hasUpper(.IntSeq) => false` |
| 731 | `reference-semantics/semantics/methods.k:126` | rule; supplied, ordinary | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 732 | `reference-semantics/semantics/methods.k:128` | syntax; supplied, function, total | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 733 | `reference-semantics/semantics/methods.k:129` | rule; supplied, ordinary | `rule hasLower(.IntSeq) => false` |
| 734 | `reference-semantics/semantics/methods.k:130` | rule; supplied, ordinary | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 735 | `reference-semantics/semantics/methods.k:132` | syntax; supplied, function, total | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 736 | `reference-semantics/semantics/methods.k:133` | rule; supplied, ordinary | `rule allAlpha(.IntSeq) => true` |
| 737 | `reference-semantics/semantics/methods.k:134` | rule; supplied, ordinary | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 738 | `reference-semantics/semantics/methods.k:136` | syntax; supplied, function, total | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 739 | `reference-semantics/semantics/methods.k:137` | rule; supplied, ordinary | `rule allDigit(.IntSeq) => true` |
| 740 | `reference-semantics/semantics/methods.k:138` | rule; supplied, ordinary | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 741 | `reference-semantics/semantics/methods.k:140` | syntax; supplied, function, total | `syntax Int ::= lowerC(Int) [function, total]` |
| 742 | `reference-semantics/semantics/methods.k:142` | rule; supplied, ordinary | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 743 | `reference-semantics/semantics/methods.k:143` | rule; supplied, ordinary, owise | `rule lowerC(C:Int) => C [owise]` |
| 744 | `reference-semantics/semantics/methods.k:145` | syntax; supplied, function, total | `syntax Int ::= upperC(Int) [function, total]` |
| 745 | `reference-semantics/semantics/methods.k:146` | rule; supplied, ordinary | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 746 | `reference-semantics/semantics/methods.k:147` | rule; supplied, ordinary, owise | `rule upperC(C:Int) => C [owise]` |
| 747 | `reference-semantics/semantics/methods.k:149` | syntax; supplied, function, total | `syntax Int ::= swapC(Int) [function, total]` |
| 748 | `reference-semantics/semantics/methods.k:150` | rule; supplied, ordinary | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 749 | `reference-semantics/semantics/methods.k:151` | rule; supplied, ordinary | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 750 | `reference-semantics/semantics/methods.k:152` | rule; supplied, ordinary, owise | `rule swapC(C:Int) => C [owise]` |
| 751 | `reference-semantics/semantics/methods.k:154` | syntax; supplied, function, total | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 752 | `reference-semantics/semantics/methods.k:155` | rule; supplied, ordinary | `rule mapLower(.IntSeq) => .IntSeq` |
| 753 | `reference-semantics/semantics/methods.k:156` | rule; supplied, ordinary | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 754 | `reference-semantics/semantics/methods.k:158` | syntax; supplied, function, total | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 755 | `reference-semantics/semantics/methods.k:159` | rule; supplied, ordinary | `rule mapUpper(.IntSeq) => .IntSeq` |
| 756 | `reference-semantics/semantics/methods.k:160` | rule; supplied, ordinary | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 757 | `reference-semantics/semantics/methods.k:162` | syntax; supplied, function, total | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 758 | `reference-semantics/semantics/methods.k:163` | rule; supplied, ordinary | `rule mapSwap(.IntSeq) => .IntSeq` |
| 759 | `reference-semantics/semantics/methods.k:164` | rule; supplied, ordinary | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 760 | `reference-semantics/semantics/methods.k:166` | syntax; supplied, function, total | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 761 | `reference-semantics/semantics/methods.k:167` | rule; supplied, ordinary | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| 762 | `reference-semantics/semantics/methods.k:168` | rule; supplied, ordinary | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 763 | `reference-semantics/semantics/methods.k:169` | rule; supplied, ordinary | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 764 | `reference-semantics/semantics/methods.k:170` | endmodule; supplied | `endmodule` |
| 765 | `reference-semantics/semantics/operators.k:6` | module; supplied | `module MPY-OPERATORS imports MPY-CORE imports MPY-ITER` |
| 766 | `reference-semantics/semantics/operators.k:10` | rule; supplied, ordinary | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 767 | `reference-semantics/semantics/operators.k:12` | rule; supplied, ordinary | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes` |
| 768 | `reference-semantics/semantics/operators.k:15` | context; supplied, evaluation-context | `context Compare(HOLE, _)` |
| 769 | `reference-semantics/semantics/operators.k:16` | context; supplied, evaluation-context | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 770 | `reference-semantics/semantics/operators.k:17` | rule; supplied, ordinary, owise | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 771 | `reference-semantics/semantics/operators.k:19` | rule; supplied, ordinary | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| 772 | `reference-semantics/semantics/operators.k:20` | rule; supplied, ordinary, priority(40) | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) // ==== operand deref: heap objects combine/compare by STRUCTURE ============ // (Python: list == is structural; identity only via \`is\`.) priority(40) // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.` |
| 773 | `reference-semantics/semantics/operators.k:25` | rule; supplied, ordinary, priority(40) | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 774 | `reference-semantics/semantics/operators.k:28` | rule; supplied, ordinary, priority(40) | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] // the left operand of \`in\`/\`not in\` is an ELEMENT (compares by ==K) — never deref'd` |
| 775 | `reference-semantics/semantics/operators.k:34` | rule; supplied, ordinary, priority(40) | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 776 | `reference-semantics/semantics/operators.k:38` | rule; supplied, ordinary, priority(40) | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| 777 | `reference-semantics/semantics/operators.k:44` | rule; supplied, ordinary, priority(40) | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 778 | `reference-semantics/semantics/operators.k:47` | endmodule; supplied | `endmodule` |
| 779 | `reference-semantics/semantics/range.k:5` | module; supplied | `module MPY-RANGE imports MPY-CORE imports MPY-ITER` |
| 780 | `reference-semantics/semantics/range.k:9` | syntax; supplied, function, total | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 781 | `reference-semantics/semantics/range.k:10` | rule; supplied, ordinary | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 782 | `reference-semantics/semantics/range.k:12` | syntax; supplied, function | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 783 | `reference-semantics/semantics/range.k:13` | rule; supplied, ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 784 | `reference-semantics/semantics/range.k:15` | rule; supplied, ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 785 | `reference-semantics/semantics/range.k:17` | rule; supplied, ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 786 | `reference-semantics/semantics/range.k:20` | rule; supplied, ordinary | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 787 | `reference-semantics/semantics/range.k:23` | rule; supplied, ordinary | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| 788 | `reference-semantics/semantics/range.k:25` | endmodule; supplied | `endmodule` |
| 789 | `reference-semantics/semantics/set.k:3` | module; supplied | `module MPY-SET imports MPY-CORE // a set value, carried as its distinct codes in first-seen order (order is irrelevant // to membership/cardinality — the two observations sets support here).` |
| 790 | `reference-semantics/semantics/set.k:8` | syntax; supplied | `syntax Val ::= setV(IntSeq) // membership of a code in the accumulated distinct-code sequence` |
| 791 | `reference-semantics/semantics/set.k:11` | syntax; supplied, function, total | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 792 | `reference-semantics/semantics/set.k:12` | rule; supplied, ordinary | `rule codeIn(_:Int, .IntSeq) => false` |
| 793 | `reference-semantics/semantics/set.k:13` | rule; supplied, ordinary | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) // the distinct codes of CS (insert-if-absent fold, first-seen order)` |
| 794 | `reference-semantics/semantics/set.k:16` | syntax; supplied, function, total | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total]` |
| 795 | `reference-semantics/semantics/set.k:18` | rule; supplied, ordinary | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 796 | `reference-semantics/semantics/set.k:19` | rule; supplied, ordinary | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 797 | `reference-semantics/semantics/set.k:20` | rule; supplied, ordinary | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 798 | `reference-semantics/semantics/set.k:22` | rule; supplied, ordinary | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 799 | `reference-semantics/semantics/set.k:25` | syntax; supplied, function, total | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 800 | `reference-semantics/semantics/set.k:26` | rule; supplied, ordinary | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| 801 | `reference-semantics/semantics/set.k:27` | rule; supplied, ordinary | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) // ==== set equality: two sets are equal iff mutually subsuming ============== // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).` |
| 802 | `reference-semantics/semantics/set.k:31` | syntax; supplied, function, total | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 803 | `reference-semantics/semantics/set.k:32` | rule; supplied, ordinary | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| 804 | `reference-semantics/semantics/set.k:33` | rule; supplied, ordinary | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 805 | `reference-semantics/semantics/set.k:35` | syntax; supplied, function, total | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 806 | `reference-semantics/semantics/set.k:36` | rule; supplied, ordinary | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) // set == set (the only comparison sets support here)` |
| 807 | `reference-semantics/semantics/set.k:39` | rule; supplied, ordinary | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 808 | `reference-semantics/semantics/set.k:40` | endmodule; supplied | `endmodule` |
| 809 | `reference-semantics/semantics/sort.k:10` | module; supplied | `module MPY-SORT imports MPY-BUILTINS imports MPY-SUBSCRIPT // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators); // concrete insertion sort for krun. // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal // (lemmas-only) is not available in the semantics. Int and str lists.` |
| 810 | `reference-semantics/semantics/sort.k:18` | syntax; supplied, function, total, opaque/no-evaluators | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 811 | `reference-semantics/semantics/sort.k:19` | syntax; supplied, function | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 812 | `reference-semantics/semantics/sort.k:20` | rule; supplied, concrete | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| 813 | `reference-semantics/semantics/sort.k:21` | rule; supplied, concrete | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 814 | `reference-semantics/semantics/sort.k:22` | rule; supplied, concrete | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| 815 | `reference-semantics/semantics/sort.k:23` | rule; supplied, concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 816 | `reference-semantics/semantics/sort.k:24` | rule; supplied, concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k)` |
| 817 | `reference-semantics/semantics/sort.k:26` | syntax; supplied, function | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 818 | `reference-semantics/semantics/sort.k:27` | rule; supplied, concrete | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 819 | `reference-semantics/semantics/sort.k:28` | rule; supplied, concrete | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 820 | `reference-semantics/semantics/sort.k:29` | rule; supplied, concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 821 | `reference-semantics/semantics/sort.k:31` | rule; supplied, concrete, owise | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise] // applyBuiltin routing in call.k) so the result allocates.` |
| 822 | `reference-semantics/semantics/sort.k:36` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> // mutator: xs.sort() — the in-place heap write over the same trusted sortVS` |
| 823 | `reference-semantics/semantics/sort.k:40` | rule; supplied, concrete, priority(40) | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] // ==== keyed / reversed sorted() (WP2) ===================================== // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV // (a closure/builtin/type — anything callable). OPAQUE here; the concrete // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable- // inserts, at priority(40) over these.` |
| 824 | `reference-semantics/semantics/sort.k:49` | syntax; supplied, function, total, opaque/no-evaluators | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 825 | `reference-semantics/semantics/sort.k:51` | syntax; supplied, function, total | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 826 | `reference-semantics/semantics/sort.k:53` | rule; supplied, ordinary | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 827 | `reference-semantics/semantics/sort.k:54` | rule; supplied, ordinary | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 828 | `reference-semantics/semantics/sort.k:55` | rule; supplied, ordinary | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 829 | `reference-semantics/semantics/sort.k:57` | syntax; supplied, function, total | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 830 | `reference-semantics/semantics/sort.k:58` | rule; supplied, ordinary | `rule condRev(S:ValSeq, false) => S` |
| 831 | `reference-semantics/semantics/sort.k:59` | rule; supplied, ordinary | `rule condRev(S:ValSeq, true) => revVS(S)` |
| 832 | `reference-semantics/semantics/sort.k:61` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 833 | `reference-semantics/semantics/sort.k:63` | rule; supplied, ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 834 | `reference-semantics/semantics/sort.k:65` | rule; supplied, concrete | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> // Indexing the opaque sorted list: \`valSeqAt(sortVS(VS), I)\` is DEFINED because valSeqAt is // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write // their postcondition directly as valSeqAt(sortVS(VS), …).` |
| 835 | `reference-semantics/semantics/sort.k:72` | endmodule; supplied | `endmodule` |
| 836 | `reference-semantics/semantics/str.k:3` | module; supplied | `module MPY-STR imports MPY-CORE imports MPY-ITER // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==` |
| 837 | `reference-semantics/semantics/str.k:8` | rule; supplied, ordinary | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| 838 | `reference-semantics/semantics/str.k:9` | rule; supplied, ordinary | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> // ==== str literal (ASCII-only) ============================================` |
| 839 | `reference-semantics/semantics/str.k:13` | syntax; supplied, function | `syntax IntSeq ::= strToCodes(String) [function]` |
| 840 | `reference-semantics/semantics/str.k:14` | rule; supplied, ordinary | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 841 | `reference-semantics/semantics/str.k:15` | rule; supplied, ordinary | `rule strToCodes("") => .IntSeq` |
| 842 | `reference-semantics/semantics/str.k:16` | rule; supplied, ordinary | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 // ==== operators: + / == / != / in =========================================` |
| 843 | `reference-semantics/semantics/str.k:20` | syntax; supplied, function, total | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 844 | `reference-semantics/semantics/str.k:21` | rule; supplied, ordinary | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| 845 | `reference-semantics/semantics/str.k:22` | rule; supplied, ordinary | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 846 | `reference-semantics/semantics/str.k:24` | rule; supplied, ordinary | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 847 | `reference-semantics/semantics/str.k:25` | rule; supplied, ordinary | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 848 | `reference-semantics/semantics/str.k:26` | rule; supplied, ordinary | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) // substring membership: \`P in X\` iff the code-seq P occurs contiguously in X` |
| 849 | `reference-semantics/semantics/str.k:29` | rule; supplied, ordinary | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 850 | `reference-semantics/semantics/str.k:30` | rule; supplied, ordinary | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 851 | `reference-semantics/semantics/str.k:32` | syntax; supplied, function, total | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 852 | `reference-semantics/semantics/str.k:33` | rule; supplied, ordinary | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| 853 | `reference-semantics/semantics/str.k:34` | rule; supplied, ordinary | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 854 | `reference-semantics/semantics/str.k:35` | rule; supplied, ordinary | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 855 | `reference-semantics/semantics/str.k:37` | syntax; supplied, function, total | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 856 | `reference-semantics/semantics/str.k:38` | rule; supplied, ordinary | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| 857 | `reference-semantics/semantics/str.k:39` | rule; supplied, ordinary | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| 858 | `reference-semantics/semantics/str.k:40` | rule; supplied, ordinary | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic // str \`<\` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on // str </<=/>/>= comparisons.` |
| 859 | `reference-semantics/semantics/str.k:48` | syntax; supplied, function, total | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 860 | `reference-semantics/semantics/str.k:49` | rule; supplied, ordinary | `rule strLt(.IntSeq, .IntSeq) => false` |
| 861 | `reference-semantics/semantics/str.k:50` | rule; supplied, ordinary | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 862 | `reference-semantics/semantics/str.k:51` | rule; supplied, ordinary | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 863 | `reference-semantics/semantics/str.k:52` | rule; supplied, ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| 864 | `reference-semantics/semantics/str.k:53` | rule; supplied, ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| 865 | `reference-semantics/semantics/str.k:54` | rule; supplied, ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 866 | `reference-semantics/semantics/str.k:56` | rule; supplied, ordinary | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 867 | `reference-semantics/semantics/str.k:57` | rule; supplied, ordinary | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 868 | `reference-semantics/semantics/str.k:58` | rule; supplied, ordinary | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 869 | `reference-semantics/semantics/str.k:59` | rule; supplied, ordinary | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 870 | `reference-semantics/semantics/str.k:60` | endmodule; supplied | `endmodule` |
| 871 | `reference-semantics/semantics/subscript.k:3` | module; supplied | `module MPY-SUBSCRIPT imports MPY-CORE // ==== positional access + negative-index normalization (used only here) === // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g. // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total // atK. K trusts the [total] annotation; valid programs index in-bounds.` |
| 872 | `reference-semantics/semantics/subscript.k:11` | syntax; supplied, function, total | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 873 | `reference-semantics/semantics/subscript.k:12` | rule; supplied, ordinary | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| 874 | `reference-semantics/semantics/subscript.k:13` | rule; supplied, ordinary | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 875 | `reference-semantics/semantics/subscript.k:16` | syntax; supplied, function | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 876 | `reference-semantics/semantics/subscript.k:17` | rule; supplied, ordinary | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| 877 | `reference-semantics/semantics/subscript.k:18` | rule; supplied, ordinary | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 878 | `reference-semantics/semantics/subscript.k:21` | syntax; supplied, function, total | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 879 | `reference-semantics/semantics/subscript.k:22` | rule; supplied, ordinary | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 880 | `reference-semantics/semantics/subscript.k:23` | rule; supplied, ordinary | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0 // ==== Subscript: indexing obj[i] (list / tuple / str) ===================== // contexts (not strict attrs): the Index slot's Slice alternative must never heat` |
| 881 | `reference-semantics/semantics/subscript.k:27` | context; supplied, evaluation-context | `context Subscript(HOLE, _)` |
| 882 | `reference-semantics/semantics/subscript.k:28` | context; supplied, evaluation-context | `context Subscript(_:Val, HOLE:Expr) // heap-object deref (covers both the index and slice forms via the Index slot)` |
| 883 | `reference-semantics/semantics/subscript.k:31` | rule; supplied, ordinary, priority(40) | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 884 | `reference-semantics/semantics/subscript.k:35` | rule; supplied, ordinary | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 885 | `reference-semantics/semantics/subscript.k:37` | syntax; supplied, function | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 886 | `reference-semantics/semantics/subscript.k:38` | rule; supplied, ordinary | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 887 | `reference-semantics/semantics/subscript.k:39` | rule; supplied, ordinary | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 888 | `reference-semantics/semantics/subscript.k:40` | rule; supplied, ordinary | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========` |
| 889 | `reference-semantics/semantics/subscript.k:44` | syntax; supplied | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| 890 | `reference-semantics/semantics/subscript.k:49` | syntax; supplied | `syntax OptInt ::= "noB" \| someB(Int)` |
| 891 | `reference-semantics/semantics/subscript.k:50` | rule; supplied, ordinary | `rule <k> #evalB(NoBound) => noB ... </k>` |
| 892 | `reference-semantics/semantics/subscript.k:51` | rule; supplied, ordinary | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| 893 | `reference-semantics/semantics/subscript.k:52` | rule; supplied, ordinary | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 894 | `reference-semantics/semantics/subscript.k:54` | rule; supplied, ordinary | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 895 | `reference-semantics/semantics/subscript.k:55` | rule; supplied, ordinary | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 896 | `reference-semantics/semantics/subscript.k:56` | rule; supplied, ordinary | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value` |
| 897 | `reference-semantics/semantics/subscript.k:58` | rule; supplied, ordinary, priority(45) | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 898 | `reference-semantics/semantics/subscript.k:61` | rule; supplied, ordinary | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 899 | `reference-semantics/semantics/subscript.k:63` | syntax; supplied, function | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 900 | `reference-semantics/semantics/subscript.k:64` | rule; supplied, ordinary | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 901 | `reference-semantics/semantics/subscript.k:66` | rule; supplied, ordinary | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 902 | `reference-semantics/semantics/subscript.k:68` | rule; supplied, ordinary | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) // ==== slice.indices: step / start / stop / clamp ==========================` |
| 903 | `reference-semantics/semantics/subscript.k:72` | syntax; supplied, function, total | `syntax Int ::= slStep(OptInt) [function, total]` |
| 904 | `reference-semantics/semantics/subscript.k:73` | rule; supplied, ordinary | `rule slStep(noB) => 1` |
| 905 | `reference-semantics/semantics/subscript.k:74` | rule; supplied, ordinary | `rule slStep(someB(S:Int)) => S` |
| 906 | `reference-semantics/semantics/subscript.k:76` | syntax; supplied, function | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 907 | `reference-semantics/semantics/subscript.k:77` | rule; supplied, ordinary | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 908 | `reference-semantics/semantics/subscript.k:79` | rule; supplied, ordinary | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` |
| 909 | `reference-semantics/semantics/subscript.k:81` | rule; supplied, ordinary | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 910 | `reference-semantics/semantics/subscript.k:83` | syntax; supplied, function | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 911 | `reference-semantics/semantics/subscript.k:84` | rule; supplied, ordinary | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` |
| 912 | `reference-semantics/semantics/subscript.k:86` | rule; supplied, ordinary | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 913 | `reference-semantics/semantics/subscript.k:88` | rule; supplied, ordinary | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 914 | `reference-semantics/semantics/subscript.k:90` | syntax; supplied, function, total | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 915 | `reference-semantics/semantics/subscript.k:91` | rule; supplied, ordinary | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` |
| 916 | `reference-semantics/semantics/subscript.k:93` | rule; supplied, ordinary | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 917 | `reference-semantics/semantics/subscript.k:96` | syntax; supplied, function, total | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 918 | `reference-semantics/semantics/subscript.k:97` | rule; supplied, ordinary | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 919 | `reference-semantics/semantics/subscript.k:99` | rule; supplied, ordinary | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 920 | `reference-semantics/semantics/subscript.k:102` | syntax; supplied, function, total | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 921 | `reference-semantics/semantics/subscript.k:103` | rule; supplied, ordinary | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` |
| 922 | `reference-semantics/semantics/subscript.k:105` | rule; supplied, ordinary | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN // ==== build the strided sub-sequence (indices in range by construction) ====` |
| 923 | `reference-semantics/semantics/subscript.k:109` | syntax; supplied, function | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 924 | `reference-semantics/semantics/subscript.k:110` | rule; supplied, ordinary | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 925 | `reference-semantics/semantics/subscript.k:113` | rule; supplied, ordinary | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 926 | `reference-semantics/semantics/subscript.k:116` | syntax; supplied, function | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 927 | `reference-semantics/semantics/subscript.k:117` | rule; supplied, ordinary | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 928 | `reference-semantics/semantics/subscript.k:120` | rule; supplied, ordinary | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 929 | `reference-semantics/semantics/subscript.k:122` | endmodule; supplied | `endmodule` |
| 930 | `reference-semantics/semantics/syntax.k:3` | module; supplied | `module MPY-SYNTAX imports INT-SYNTAX imports FLOAT-SYNTAX imports BOOL-SYNTAX imports STRING-SYNTAX` |
| 931 | `reference-semantics/semantics/syntax.k:9` | syntax; supplied, macro | `syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda" "(" Params "," Expr ")" \| "KwArg" "(" String "," Expr ")" \| "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call" "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare" "(" Expr "," CmpOp ")"` |
| 932 | `reference-semantics/semantics/syntax.k:32` | syntax; supplied | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| 933 | `reference-semantics/semantics/syntax.k:33` | syntax; supplied | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| 934 | `reference-semantics/semantics/syntax.k:34` | syntax; supplied | `syntax Entries ::= List{Entry, ","}` |
| 935 | `reference-semantics/semantics/syntax.k:35` | syntax; supplied | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 936 | `reference-semantics/semantics/syntax.k:36` | syntax; supplied | `syntax CompFors ::= List{CompFor, ""}` |
| 937 | `reference-semantics/semantics/syntax.k:37` | syntax; supplied | `syntax Exprs ::= List{Expr, ","}` |
| 938 | `reference-semantics/semantics/syntax.k:38` | syntax; supplied | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 939 | `reference-semantics/semantics/syntax.k:39` | syntax; supplied | `syntax Bound ::= Expr \| "NoBound"` |
| 940 | `reference-semantics/semantics/syntax.k:41` | syntax; supplied | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [strict] \| "Expr" "(" Expr ")" [strict] \| "FuncDef" "(" String "," Params "," Stmts ")" \| "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| 941 | `reference-semantics/semantics/syntax.k:56` | syntax; supplied | `syntax Stmts ::= List{Stmt, ""}` |
| 942 | `reference-semantics/semantics/syntax.k:57` | syntax; supplied | `syntax Params ::= "Params" "(" ParamNames ")"` |
| 943 | `reference-semantics/semantics/syntax.k:58` | syntax; supplied | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| 944 | `reference-semantics/semantics/syntax.k:59` | syntax; supplied | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| 945 | `reference-semantics/semantics/syntax.k:60` | syntax; supplied | `syntax ParamNames ::= List{String, ","}` |
| 946 | `reference-semantics/semantics/syntax.k:61` | syntax; supplied | `syntax Module ::= "Module" "(" Stmts ")"` |
| 947 | `reference-semantics/semantics/syntax.k:62` | endmodule; supplied | `endmodule` |
| 948 | `reference-semantics/semantics/tuple.k:3` | module; supplied | `module MPY-TUPLE imports MPY-CORE imports MPY-ITER imports MPY-LIST imports MPY-METHODS // ==== iteration (the iterator protocol's tuple case) ======================` |
| 949 | `reference-semantics/semantics/tuple.k:10` | rule; supplied, ordinary | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| 950 | `reference-semantics/semantics/tuple.k:11` | rule; supplied, ordinary | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================` |
| 951 | `reference-semantics/semantics/tuple.k:14` | syntax; supplied | `syntax ApplyK ::= "toTuple"` |
| 952 | `reference-semantics/semantics/tuple.k:15` | rule; supplied, ordinary | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 953 | `reference-semantics/semantics/tuple.k:16` | rule; supplied, ordinary | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 954 | `reference-semantics/semantics/tuple.k:18` | rule; supplied, ordinary | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k)` |
| 955 | `reference-semantics/semantics/tuple.k:20` | rule; supplied, ordinary | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 956 | `reference-semantics/semantics/tuple.k:21` | rule; supplied, ordinary | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset)` |
| 957 | `reference-semantics/semantics/tuple.k:23` | rule; supplied, ordinary | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 958 | `reference-semantics/semantics/tuple.k:24` | syntax; supplied, function | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 959 | `reference-semantics/semantics/tuple.k:25` | rule; supplied, ordinary | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 960 | `reference-semantics/semantics/tuple.k:26` | rule; supplied, ordinary | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 961 | `reference-semantics/semantics/tuple.k:28` | rule; supplied, ordinary | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) // ==== target binding: bind a Name or a TupleExpr target to a value ========` |
| 962 | `reference-semantics/semantics/tuple.k:31` | syntax; supplied | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 963 | `reference-semantics/semantics/tuple.k:32` | rule; supplied, ordinary | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 964 | `reference-semantics/semantics/tuple.k:35` | rule; supplied, ordinary, priority(40) | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 965 | `reference-semantics/semantics/tuple.k:42` | rule; supplied, ordinary | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 966 | `reference-semantics/semantics/tuple.k:43` | rule; supplied, ordinary | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 967 | `reference-semantics/semantics/tuple.k:44` | rule; supplied, ordinary, priority(40) | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // ==== unpacking: a, b = <tuple\|list> (RHS evaluated by strictness) ========` |
| 968 | `reference-semantics/semantics/tuple.k:49` | syntax; supplied | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 969 | `reference-semantics/semantics/tuple.k:50` | rule; supplied, ordinary | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 970 | `reference-semantics/semantics/tuple.k:51` | rule; supplied, ordinary | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 971 | `reference-semantics/semantics/tuple.k:52` | rule; supplied, ordinary, priority(40) | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 972 | `reference-semantics/semantics/tuple.k:55` | rule; supplied, ordinary | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 973 | `reference-semantics/semantics/tuple.k:57` | rule; supplied, ordinary | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| 974 | `reference-semantics/semantics/tuple.k:58` | endmodule; supplied | `endmodule` |
| 975 | `reference-semantics/semantics.k:34` | requires; supplied | `requires "semantics/syntax.k"` |
| 976 | `reference-semantics/semantics.k:35` | requires; supplied | `requires "semantics/core.k"` |
| 977 | `reference-semantics/semantics.k:36` | requires; supplied | `requires "semantics/iter.k"` |
| 978 | `reference-semantics/semantics.k:37` | requires; supplied | `requires "semantics/range.k"` |
| 979 | `reference-semantics/semantics.k:38` | requires; supplied | `requires "semantics/operators.k"` |
| 980 | `reference-semantics/semantics.k:39` | requires; supplied | `requires "semantics/int.k"` |
| 981 | `reference-semantics/semantics.k:40` | requires; supplied | `requires "semantics/bool.k"` |
| 982 | `reference-semantics/semantics.k:41` | requires; supplied | `requires "semantics/float.k"` |
| 983 | `reference-semantics/semantics.k:42` | requires; supplied | `requires "semantics/str.k"` |
| 984 | `reference-semantics/semantics.k:43` | requires; supplied | `requires "semantics/set.k"` |
| 985 | `reference-semantics/semantics.k:44` | requires; supplied | `requires "semantics/list.k"` |
| 986 | `reference-semantics/semantics.k:45` | requires; supplied | `requires "semantics/tuple.k"` |
| 987 | `reference-semantics/semantics.k:46` | requires; supplied | `requires "semantics/subscript.k"` |
| 988 | `reference-semantics/semantics.k:47` | requires; supplied | `requires "semantics/comprehension.k"` |
| 989 | `reference-semantics/semantics.k:48` | requires; supplied | `requires "semantics/methods.k"` |
| 990 | `reference-semantics/semantics.k:49` | requires; supplied | `requires "semantics/controls.k"` |
| 991 | `reference-semantics/semantics.k:50` | requires; supplied | `requires "semantics/functions.k"` |
| 992 | `reference-semantics/semantics.k:51` | requires; supplied | `requires "semantics/builtins.k"` |
| 993 | `reference-semantics/semantics.k:52` | requires; supplied | `requires "semantics/call.k"` |
| 994 | `reference-semantics/semantics.k:53` | requires; supplied | `requires "semantics/sort.k"` |
| 995 | `reference-semantics/semantics.k:54` | requires; supplied | `requires "semantics/assert.k"` |
| 996 | `reference-semantics/semantics.k:55` | requires; supplied | `requires "semantics/dict.k"` |
| 997 | `reference-semantics/semantics.k:56` | requires; supplied | `requires "semantics/concrete.k"` |
| 998 | `reference-semantics/semantics.k:58` | module; supplied | `module MPY imports MPY-CORE imports MPY-ITER imports MPY-RANGE imports MPY-OPERATORS imports MPY-INT imports MPY-BOOL imports MPY-FLOAT imports MPY-STR imports MPY-SET imports MPY-LIST imports MPY-TUPLE imports MPY-SUBSCRIPT imports MPY-COMPREHENSION imports MPY-METHODS imports MPY-CONTROLS imports MPY-FUNCTIONS imports MPY-BUILTINS imports MPY-CALL imports MPY-SORT imports MPY-ASSERT imports MPY-DICT` |
| 999 | `reference-semantics/semantics.k:80` | endmodule; supplied | `endmodule // The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's // real key calls, deep list equality). Verification builds import MPY and // never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN — // with plain MPY the concrete legs are silently absent (this was live for a // while: sorted-key stuck and comprehension asserted wrong under krun).` |
| 1000 | `reference-semantics/semantics.k:87` | module; supplied | `module MPY-KRUN imports MPY imports MPY-CONCRETE` |
| 1001 | `reference-semantics/semantics.k:90` | endmodule; supplied | `endmodule` |
| 1002 | `connection-mutation-spec.k:1` | requires; proof-local | `requires "verification.k"` |
| 1003 | `connection-mutation-spec.k:3` | module; proof-local | `module CONNECTION-MUTATION-SPEC imports VERIFICATION-BASE` |
| 1004 | `connection-mutation-spec.k:6` | claim; proof-local, reachability-claim | `claim [empty-inner-body-must-not-summarize]: <k> #loop(list(REST:ValSeq), Name("item2"), .Stmts) => .K ... </k> <env> 1 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope( "find_closest_elements" \|-> closureVal( ("numbers", .ParamNames), findBody, 0), parent(-1)) 1 \|-> scope( "numbers" \|-> _NUMBERS:Val "items" \|-> _ITEMSREF:Val "item1" \|-> ITEM1:Val "item2" \|-> (OLD2:Val => lastItem(REST, OLD2)) "closest" \|-> ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq))) => tuple( vCons( innerFirst(ITEM1, REST, A, B), vCons( innerSecond(ITEM1, REST, A, B), .ValSeq))) ), parent(0)) </scopes> requires ITEM1 ==K tuple( vCons( itemIndex(ITEM1), vCons(itemFloat(ITEM1), .ValSeq))) andBool allFloatItems(REST)` |
| 1005 | `connection-mutation-spec.k:45` | endmodule; proof-local | `endmodule` |
| 1006 | `connection-spec.k:1` | requires; proof-local | `requires "verification.k"` |
| 1007 | `connection-spec.k:3` | module; proof-local | `module CONNECTION-SPEC imports VERIFICATION-BASE` |
| 1008 | `connection-spec.k:6` | claim; proof-local, reachability-claim | `claim [inner-loop-connection]: <k> #loop(list(REST:ValSeq), Name("item2"), innerBody) => .K ... </k> <env> 1 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope( "find_closest_elements" \|-> closureVal( ("numbers", .ParamNames), findBody, 0), parent(-1)) 1 \|-> scope( "numbers" \|-> _NUMBERS:Val "items" \|-> _ITEMSREF:Val "item1" \|-> ITEM1:Val "item2" \|-> (OLD2:Val => lastItem(REST, OLD2)) "closest" \|-> ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq))) => tuple( vCons( innerFirst(ITEM1, REST, A, B), vCons( innerSecond(ITEM1, REST, A, B), .ValSeq))) ), parent(0)) </scopes> requires ITEM1 ==K tuple( vCons( itemIndex(ITEM1), vCons(itemFloat(ITEM1), .ValSeq))) andBool allFloatItems(REST)` |
| 1009 | `connection-spec.k:45` | endmodule; proof-local | `endmodule` |
| 1010 | `projection-spec.k:1` | requires; proof-local | `requires "reference-semantics/semantics.k"` |
| 1011 | `projection-spec.k:3` | module; proof-local | `module PROJECTION-SPEC imports MPY` |
| 1012 | `projection-spec.k:6` | claim; proof-local, reachability-claim | `claim [index-zero-fixed]: <k> applyIndex( tuple(vCons(I:Int, vCons(F:Float, .ValSeq))), 0) => I ... </k>` |
| 1013 | `projection-spec.k:16` | claim; proof-local, reachability-claim | `claim [index-one-fixed]: <k> applyIndex( tuple(vCons(I:Int, vCons(F:Float, .ValSeq))), 1) => F ... </k>` |
| 1014 | `projection-spec.k:25` | endmodule; proof-local | `endmodule` |
| 1015 | `spec-vacuity.k:1` | requires; proof-local | `requires "verification.k"` |
| 1016 | `spec-vacuity.k:3` | module; proof-local | `module SPEC-VACUITY imports VERIFICATION` |
| 1017 | `spec-vacuity.k:6` | claim; proof-local, reachability-claim | `claim [false-result-shape]: <k> #loadAll(solutionModule) ~> Call( Name("find_closest_elements"), (list(vCons(F0:Float, vCons(F1:Float, .ValSeq))), .Exprs)) => tuple( vCons( orderedFirst(F0, F1), vCons( orderedSecond(F0, F1), vCons(noneV, .ValSeq)))) </k> <env> 0 </env> <scopes> ( 0 \|-> scope(.Map, parent(-1)) => 0 \|-> scope( "find_closest_elements" \|-> closureVal( ("numbers", .ParamNames), findBody, 0), parent(-1)) ) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map => 0 \|-> list( vCons( tuple(vCons(0, vCons(F0, .ValSeq))), vCons( tuple(vCons(1, vCons(F1, .ValSeq))), .ValSeq))) 1 \|-> list( vCons( tuple(vCons(0, vCons(F0, .ValSeq))), vCons( tuple(vCons(1, vCons(F1, .ValSeq))), .ValSeq))) </heap> <heapLoc> 0 => 2 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>` |
| 1018 | `spec-vacuity.k:55` | endmodule; proof-local | `endmodule` |
| 1019 | `spec.k:1` | requires; proof-local | `requires "verification.k"` |
| 1020 | `spec.k:3` | module; proof-local | `module SPEC imports VERIFICATION` |
| 1021 | `spec.k:6` | claim; proof-local, reachability-claim | `claim [inner-loop]: <k> #loop(list(REST:ValSeq), Name("item2"), innerBody) => .K ... </k> <env> 1 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope( "find_closest_elements" \|-> closureVal( ("numbers", .ParamNames), findBody, 0), parent(-1)) 1 \|-> scope( "numbers" \|-> NUMBERS:Val "items" \|-> ITEMSREF:Val "item1" \|-> ITEM1:Val "item2" \|-> (OLD2:Val => lastItem(REST, OLD2)) "closest" \|-> ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq))) => tuple( vCons( innerFirst(ITEM1, REST, A, B), vCons( innerSecond(ITEM1, REST, A, B), .ValSeq))) ), parent(0)) </scopes> requires ITEM1 ==K tuple( vCons( itemIndex(ITEM1), vCons(itemFloat(ITEM1), .ValSeq))) andBool allFloatItems(REST)` |
| 1022 | `spec.k:46` | claim; proof-local, reachability-claim | `claim [outer-loop]: <k> #loop(list(REST:ValSeq), Name("item1"), outerBody) => .K ... </k> <env> 1 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope( "find_closest_elements" \|-> closureVal( ("numbers", .ParamNames), findBody, 0), parent(-1)) 1 \|-> scope( "numbers" \|-> NUMBERS:Val "items" \|-> ref(H:Int) "item1" \|-> (OLD1:Val => ?FINAL1:Val) "item2" \|-> (OLD2:Val => ?FINAL2:Val) "closest" \|-> ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq))) => tuple( vCons( outerFirst(REST, ALL:ValSeq, A, B), vCons( outerSecond(REST, ALL, A, B), .ValSeq))) ), parent(0)) </scopes> <heap> H \|-> list(ALL) ... </heap> requires allFloatItems(REST) andBool allFloatItems(ALL)` |
| 1023 | `spec.k:83` | claim; proof-local, reachability-claim | `claim [find-closest]: <k> #loadAll(solutionModule) ~> Call( Name("find_closest_elements"), (list(vCons(F0:Float, vCons(F1:Float, REST:ValSeq))), .Exprs)) => tuple( vCons( outerFirst( enumVS(vCons(F0, vCons(F1, REST)), 0), enumVS(vCons(F0, vCons(F1, REST)), 0), orderedFirst(F0, F1), orderedSecond(F0, F1)), vCons( outerSecond( enumVS(vCons(F0, vCons(F1, REST)), 0), enumVS(vCons(F0, vCons(F1, REST)), 0), orderedFirst(F0, F1), orderedSecond(F0, F1)), .ValSeq))) </k> <env> 0 </env> <scopes> ( 0 \|-> scope(.Map, parent(-1)) => 0 \|-> scope( "find_closest_elements" \|-> closureVal( ("numbers", .ParamNames), findBody, 0), parent(-1)) ) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map => 0 \|-> list(enumVS(vCons(F0, vCons(F1, REST)), 0)) 1 \|-> list(enumVS(vCons(F0, vCons(F1, REST)), 0)) </heap> <heapLoc> 0 => 2 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allFloatVS(REST)` |
| 1024 | `spec.k:131` | endmodule; proof-local | `endmodule` |
| 1025 | `verification.k:1` | requires; proof-local | `requires "reference-semantics/semantics.k"` |
| 1026 | `verification.k:3` | module; proof-local | `module VERIFICATION-SYNTAX imports MPY-SYNTAX imports FLOAT-SYNTAX` |
| 1027 | `verification.k:7` | syntax; proof-local, macro | `syntax Stmts ::= "innerBody" [macro] \| "outerBody" [macro] \| "findBody" [macro]` |
| 1028 | `verification.k:10` | syntax; proof-local, macro | `syntax Module ::= "solutionModule" [macro]` |
| 1029 | `verification.k:12` | endmodule; proof-local | `endmodule` |
| 1030 | `verification.k:14` | module; proof-local | `module VERIFICATION-BASE imports MPY imports VERIFICATION-SYNTAX` |
| 1031 | `verification.k:18` | syntax; proof-local, function, total | `syntax Bool ::= allFloatVS(ValSeq) [function, total] \| allFloatItems(ValSeq) [function, total] \| candidateWins(Val, Val, Float, Float) [function, total]` |
| 1032 | `verification.k:21` | syntax; proof-local, function, total, opaque/no-evaluators | `syntax Float ::= floatProjection(Val) [function, total, no-evaluators] \| itemFloat(Val) [function, total, no-evaluators] \| orderedFirst(Float, Float) [function, total] \| orderedSecond(Float, Float) [function, total] \| stepFirst(Val, Val, Float, Float) [function, total] \| stepSecond(Val, Val, Float, Float) [function, total] \| innerFirst(Val, ValSeq, Float, Float) [function, total] \| innerSecond(Val, ValSeq, Float, Float) [function, total] \| outerFirst(ValSeq, ValSeq, Float, Float) [function, total] \| outerSecond(ValSeq, ValSeq, Float, Float) [function, total]` |
| 1033 | `verification.k:31` | syntax; proof-local, function, total, opaque/no-evaluators | `syntax Int ::= itemIndex(Val) [function, total, no-evaluators]` |
| 1034 | `verification.k:32` | syntax; proof-local, function, total | `syntax Val ::= lastItem(ValSeq, Val) [function, total]` |
| 1035 | `verification.k:34` | rule; proof-local, ordinary | `rule innerBody => If( Compare( Subscript(Name("item1"), Int(0)), CmpOp("<", Subscript(Name("item2"), Int(0)))), If( Compare( Call( Name("abs"), (BinOp( "-", Subscript(Name("item2"), Int(1)), Subscript(Name("item1"), Int(1))), .Exprs)), CmpOp( "<", Call( Name("abs"), (BinOp( "-", Subscript(Name("closest"), Int(1)), Subscript(Name("closest"), Int(0))), .Exprs)))), If( Compare( Subscript(Name("item1"), Int(1)), CmpOp("<", Subscript(Name("item2"), Int(1)))), (Assign( Name("closest"), TupleExpr( (Subscript(Name("item1"), Int(1)), Subscript(Name("item2"), Int(1)), .Exprs))) .Stmts), (Assign( Name("closest"), TupleExpr( (Subscript(Name("item2"), Int(1)), Subscript(Name("item1"), Int(1)), .Exprs))) .Stmts)), .Stmts), .Stmts)` |
| 1036 | `verification.k:78` | rule; proof-local, ordinary | `rule outerBody => (For(Name("item2"), Name("items"), innerBody) .Stmts)` |
| 1037 | `verification.k:81` | rule; proof-local, ordinary | `rule findBody => If( Compare( Subscript(Name("numbers"), Int(0)), CmpOp("<", Subscript(Name("numbers"), Int(1)))), (Assign( Name("closest"), TupleExpr( (Subscript(Name("numbers"), Int(0)), Subscript(Name("numbers"), Int(1)), .Exprs))) .Stmts), (Assign( Name("closest"), TupleExpr( (Subscript(Name("numbers"), Int(1)), Subscript(Name("numbers"), Int(0)), .Exprs))) .Stmts)) Assign( Name("items"), Call( Name("list"), (Call(Name("enumerate"), (Name("numbers"), .Exprs)), .Exprs))) Assign(Name("item1"), Subscript(Name("items"), Int(0))) Assign(Name("item2"), Subscript(Name("items"), Int(0))) For(Name("item1"), Name("items"), outerBody) Return(Name("closest")) .Stmts` |
| 1038 | `verification.k:111` | rule; proof-local, ordinary | `rule solutionModule => Module( ImportFrom("typing", ("List", "Tuple", .ParamNames)) FuncDef( "find_closest_elements", Params(("numbers", .ParamNames)), findBody) .Stmts)` |
| 1039 | `verification.k:120` | rule; proof-local, ordinary | `rule allFloatVS(.ValSeq) => true` |
| 1040 | `verification.k:121` | rule; proof-local, ordinary | `rule allFloatVS(vCons(V:Val, REST:ValSeq)) => (V ==K floatProjection(V)) andBool allFloatVS(REST)` |
| 1041 | `verification.k:123` | rule; proof-local, ordinary | `rule floatProjection(F:Float) => F` |
| 1042 | `verification.k:125` | rule; proof-local, ordinary | `rule allFloatItems(.ValSeq) => true` |
| 1043 | `verification.k:126` | rule; proof-local, ordinary | `rule allFloatItems(vCons(V:Val, REST:ValSeq)) => ( V ==K tuple( vCons( itemIndex(V), vCons(itemFloat(V), .ValSeq))) ) andBool allFloatItems(REST)` |
| 1044 | `verification.k:134` | rule; proof-local, ordinary | `rule itemIndex( tuple(vCons(I:Int, vCons(_:Float, .ValSeq)))) => I` |
| 1045 | `verification.k:137` | rule; proof-local, ordinary | `rule itemFloat( tuple(vCons(_:Int, vCons(F:Float, .ValSeq)))) => F` |
| 1046 | `verification.k:141` | rule; proof-local, simplification | `rule applyIndex(V:Val, 0) => itemIndex(V) requires V ==K tuple( vCons( itemIndex(V), vCons(itemFloat(V), .ValSeq))) [simplification]` |
| 1047 | `verification.k:148` | rule; proof-local, simplification | `rule applyIndex(V:Val, 1) => itemFloat(V) requires V ==K tuple( vCons( itemIndex(V), vCons(itemFloat(V), .ValSeq))) [simplification]` |
| 1048 | `verification.k:156` | rule; proof-local, simplification | `rule allFloatItems(enumVS(VS:ValSeq, _:Int)) => true requires allFloatVS(VS) [simplification]` |
| 1049 | `verification.k:161` | rule; proof-local, ordinary | `rule orderedFirst(X:Float, Y:Float) => X requires floatLt(X, Y)` |
| 1050 | `verification.k:163` | rule; proof-local, ordinary | `rule orderedFirst(X:Float, Y:Float) => Y requires notBool floatLt(X, Y)` |
| 1051 | `verification.k:165` | rule; proof-local, ordinary | `rule orderedSecond(X:Float, Y:Float) => Y requires floatLt(X, Y)` |
| 1052 | `verification.k:167` | rule; proof-local, ordinary | `rule orderedSecond(X:Float, Y:Float) => X requires notBool floatLt(X, Y)` |
| 1053 | `verification.k:169` | rule; proof-local, ordinary | `rule candidateWins(ITEM1:Val, ITEM2:Val, A:Float, B:Float) => itemIndex(ITEM1) <Int itemIndex(ITEM2) andBool floatLt( absF(subF(itemFloat(ITEM2), itemFloat(ITEM1))), absF(subF(B, A)))` |
| 1054 | `verification.k:175` | rule; proof-local, ordinary | `rule stepFirst(ITEM1:Val, ITEM2:Val, A:Float, B:Float) => A requires notBool candidateWins(ITEM1, ITEM2, A, B)` |
| 1055 | `verification.k:178` | rule; proof-local, ordinary | `rule stepFirst(ITEM1:Val, ITEM2:Val, A:Float, B:Float) => itemFloat(ITEM1) requires candidateWins(ITEM1, ITEM2, A, B) andBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))` |
| 1056 | `verification.k:182` | rule; proof-local, ordinary | `rule stepFirst(ITEM1:Val, ITEM2:Val, A:Float, B:Float) => itemFloat(ITEM2) requires candidateWins(ITEM1, ITEM2, A, B) andBool notBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))` |
| 1057 | `verification.k:187` | rule; proof-local, ordinary | `rule stepSecond(ITEM1:Val, ITEM2:Val, A:Float, B:Float) => B requires notBool candidateWins(ITEM1, ITEM2, A, B)` |
| 1058 | `verification.k:190` | rule; proof-local, ordinary | `rule stepSecond(ITEM1:Val, ITEM2:Val, A:Float, B:Float) => itemFloat(ITEM2) requires candidateWins(ITEM1, ITEM2, A, B) andBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))` |
| 1059 | `verification.k:194` | rule; proof-local, ordinary | `rule stepSecond(ITEM1:Val, ITEM2:Val, A:Float, B:Float) => itemFloat(ITEM1) requires candidateWins(ITEM1, ITEM2, A, B) andBool notBool floatLt(itemFloat(ITEM1), itemFloat(ITEM2))` |
| 1060 | `verification.k:199` | rule; proof-local, ordinary | `rule innerFirst(_ITEM1:Val, .ValSeq, A:Float, _B:Float) => A` |
| 1061 | `verification.k:200` | rule; proof-local, ordinary | `rule innerFirst( ITEM1:Val, vCons(ITEM2:Val, REST:ValSeq), A:Float, B:Float) => innerFirst( ITEM1, REST, stepFirst(ITEM1, ITEM2, A, B), stepSecond(ITEM1, ITEM2, A, B))` |
| 1062 | `verification.k:211` | rule; proof-local, ordinary | `rule innerSecond(_ITEM1:Val, .ValSeq, _A:Float, B:Float) => B` |
| 1063 | `verification.k:212` | rule; proof-local, ordinary | `rule innerSecond( ITEM1:Val, vCons(ITEM2:Val, REST:ValSeq), A:Float, B:Float) => innerSecond( ITEM1, REST, stepFirst(ITEM1, ITEM2, A, B), stepSecond(ITEM1, ITEM2, A, B))` |
| 1064 | `verification.k:223` | rule; proof-local, ordinary | `rule outerFirst(.ValSeq, _ALL:ValSeq, A:Float, _B:Float) => A` |
| 1065 | `verification.k:224` | rule; proof-local, ordinary | `rule outerFirst( vCons(ITEM1:Val, REST:ValSeq), ALL:ValSeq, A:Float, B:Float) => outerFirst( REST, ALL, innerFirst(ITEM1, ALL, A, B), innerSecond(ITEM1, ALL, A, B))` |
| 1066 | `verification.k:235` | rule; proof-local, ordinary | `rule outerSecond(.ValSeq, _ALL:ValSeq, _A:Float, B:Float) => B` |
| 1067 | `verification.k:236` | rule; proof-local, ordinary | `rule outerSecond( vCons(ITEM1:Val, REST:ValSeq), ALL:ValSeq, A:Float, B:Float) => outerSecond( REST, ALL, innerFirst(ITEM1, ALL, A, B), innerSecond(ITEM1, ALL, A, B))` |
| 1068 | `verification.k:247` | rule; proof-local, ordinary | `rule lastItem(.ValSeq, OLD:Val) => OLD` |
| 1069 | `verification.k:248` | rule; proof-local, ordinary | `rule lastItem(vCons(V:Val, REST:ValSeq), _OLD:Val) => lastItem(REST, V)` |
| 1070 | `verification.k:250` | endmodule; proof-local | `endmodule` |
| 1071 | `verification.k:252` | module; proof-local | `module VERIFICATION imports VERIFICATION-BASE` |
| 1072 | `verification.k:255` | rule; proof-local, ordinary, priority(40) | `rule <k> #loop(list(REST:ValSeq), Name("item2"), innerBody) => .K ... </k> <env> 1 </env> <scopes> -1 \|-> scope( "len" \|-> builtinV("len") "set" \|-> builtinV("set") "sum" \|-> builtinV("sum") "abs" \|-> builtinV("abs") "min" \|-> builtinV("min") "max" \|-> builtinV("max") "ord" \|-> builtinV("ord") "chr" \|-> builtinV("chr") "range" \|-> builtinV("range") "all" \|-> builtinV("all") "any" \|-> builtinV("any") "zip" \|-> builtinV("zip") "isinstance" \|-> builtinV("isinstance") "sorted" \|-> builtinV("sorted") "list" \|-> builtinV("list") "round" \|-> builtinV("round") "bin" \|-> builtinV("bin") "enumerate" \|-> builtinV("enumerate") "map" \|-> builtinV("map") "eval" \|-> builtinV("eval") "int" \|-> typeV("int") "str" \|-> typeV("str") "float" \|-> typeV("float"), root) 0 \|-> scope( "find_closest_elements" \|-> closureVal( ("numbers", .ParamNames), findBody, 0), parent(-1)) 1 \|-> scope( "numbers" \|-> _NUMBERS:Val "items" \|-> _ITEMSREF:Val "item1" \|-> ITEM1:Val "item2" \|-> (OLD2:Val => lastItem(REST, OLD2)) "closest" \|-> ( tuple(vCons(A:Float, vCons(B:Float, .ValSeq))) => tuple( vCons( innerFirst(ITEM1, REST, A, B), vCons( innerSecond(ITEM1, REST, A, B), .ValSeq))) ), parent(0)) </scopes> requires ITEM1 ==K tuple( vCons( itemIndex(ITEM1), vCons(itemFloat(ITEM1), .ValSeq))) andBool allFloatItems(REST) [priority(40)]` |
| 1073 | `verification.k:317` | endmodule; proof-local | `endmodule` |

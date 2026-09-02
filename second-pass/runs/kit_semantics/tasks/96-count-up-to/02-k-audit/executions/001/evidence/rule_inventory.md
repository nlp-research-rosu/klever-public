# Exhaustive source-level K inventory

Generated from the fresh scratch copy. Each source directive beginning with `requires`, `module`, `imports`, `endmodule`, `syntax`, `configuration`, `context`, `rule`, `claim`, or `alias` is listed once.

- Total entries: 1125
- Kind counts: {'claim': 3, 'configuration': 1, 'context': 5, 'endmodule': 28, 'imports': 94, 'module': 28, 'requires': 25, 'rule': 711, 'syntax': 230}
- Attribute counts: {'concrete': 36, 'function': 149, 'macro': 5, 'macro-rec': 1, 'no-evaluators': 22, 'owise': 26, 'priority': 45, 'seqstrict': 1, 'simplification': 2, 'strict': 2, 'symbol': 25, 'total': 109}
- Decision counts: {'CANDIDATE_DERIVED_LIST_LEMMA_SOUND': 2, 'CANDIDATE_MACRO_EXPANSION_SOUND': 4, 'CANDIDATE_MACRO_OR_SUMMARY_DECL_SOUND': 3, 'CANDIDATE_STRUCTURE_OK': 12, 'CANDIDATE_SUMMARY_EQUATION_SOUND': 10, 'FIXED_CONCRETE_TEST_PATH_REVIEWED': 5, 'FIXED_MATERIAL_CONFIGURATION_REVIEWED': 1, 'FIXED_MATERIAL_EXECUTION_REVIEWED': 104, 'FIXED_MATERIAL_STRUCTURE_REVIEWED': 90, 'FIXED_MATERIAL_SYNTAX_REVIEWED': 46, 'FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE': 816, 'FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE': 25, 'POSITIVE_CLAIM_FRESHLY_MACHINE_CHECKED': 3, 'SPEC_STRUCTURE_OK': 4}

Decision codes distinguish the fixed supplied baseline from candidate-authored proof extensions. `FIXED_UNUSED...` means the entry is present in the selected fixed semantics but no constructor, symbol, or continuation on this program's reachable proof path invokes it; it is retained in the trust ledger rather than asserted to be a universal model of all Python.

| Source | Line | Module | Kind | Attributes | Decision | Declaration/rule |
|---|---:|---|---|---|---|---|
| reference-semantics/semantics/assert.k | 3 | MPY-ASSERT | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-ASSERT |
| reference-semantics/semantics/assert.k | 4 | MPY-ASSERT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/assert.k | 6 | MPY-ASSERT | rule | - | FIXED_CONCRETE_TEST_PATH_REVIEWED | rule <k> Assert(V:Val) => .K ... </k> requires truthy(V) |
| reference-semantics/semantics/assert.k | 8 | MPY-ASSERT | rule | - | FIXED_CONCRETE_TEST_PATH_REVIEWED | rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V) |
| reference-semantics/semantics/assert.k | 13 | MPY-ASSERT | rule | priority | FIXED_CONCRETE_TEST_PATH_REVIEWED | rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/assert.k | 16 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/bool.k | 5 | MPY-BOOL | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-BOOL |
| reference-semantics/semantics/bool.k | 6 | MPY-BOOL | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/bool.k | 8 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyUn("not", V:Val) => notBool truthy(V) |
| reference-semantics/semantics/bool.k | 10 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2 |
| reference-semantics/semantics/bool.k | 11 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 |
| reference-semantics/semantics/bool.k | 16 | MPY-BOOL | context | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | context BoolOp(_, (HOLE:Expr, _:Exprs)) |
| reference-semantics/semantics/bool.k | 17 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k> |
| reference-semantics/semantics/bool.k | 18 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V) |
| reference-semantics/semantics/bool.k | 20 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V) |
| reference-semantics/semantics/bool.k | 22 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V) |
| reference-semantics/semantics/bool.k | 24 | MPY-BOOL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) |
| reference-semantics/semantics/bool.k | 29 | MPY-BOOL | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)] |
| reference-semantics/semantics/bool.k | 31 | MPY-BOOL | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| reference-semantics/semantics/bool.k | 35 | MPY-BOOL | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| reference-semantics/semantics/bool.k | 39 | MPY-BOOL | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| reference-semantics/semantics/bool.k | 43 | MPY-BOOL | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| reference-semantics/semantics/bool.k | 47 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/builtins.k | 3 | MPY-BUILTINS | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-BUILTINS |
| reference-semantics/semantics/builtins.k | 4 | MPY-BUILTINS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/builtins.k | 5 | MPY-BUILTINS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-STR |
| reference-semantics/semantics/builtins.k | 6 | MPY-BUILTINS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-SET |
| reference-semantics/semantics/builtins.k | 7 | MPY-BUILTINS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-ITER |
| reference-semantics/semantics/builtins.k | 8 | MPY-BUILTINS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-RANGE |
| reference-semantics/semantics/builtins.k | 9 | MPY-BUILTINS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-INT |
| reference-semantics/semantics/builtins.k | 10 | MPY-BUILTINS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-METHODS |
| reference-semantics/semantics/builtins.k | 17 | MPY-BUILTINS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= applyBuiltin(String, Vals) [function] |
| reference-semantics/semantics/builtins.k | 20 | MPY-BUILTINS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= seqLen(Val) [function] |
| reference-semantics/semantics/builtins.k | 21 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ) |
| reference-semantics/semantics/builtins.k | 22 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule seqLen(list(VS:ValSeq)) => vsLen(VS) |
| reference-semantics/semantics/builtins.k | 23 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule seqLen(tuple(VS:ValSeq)) => vsLen(VS) |
| reference-semantics/semantics/builtins.k | 24 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule seqLen(str(IS:IntSeq)) => isLen(IS) |
| reference-semantics/semantics/builtins.k | 25 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule seqLen(setV(DS:IntSeq)) => isLen(DS) |
| reference-semantics/semantics/builtins.k | 26 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) |
| reference-semantics/semantics/builtins.k | 32 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k> |
| reference-semantics/semantics/builtins.k | 33 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k> |
| reference-semantics/semantics/builtins.k | 34 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k> |
| reference-semantics/semantics/builtins.k | 35 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k> |
| reference-semantics/semantics/builtins.k | 36 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= charsOf(IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 37 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule charsOf(.IntSeq) => .ValSeq |
| reference-semantics/semantics/builtins.k | 38 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) |
| reference-semantics/semantics/builtins.k | 41 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) |
| reference-semantics/semantics/builtins.k | 44 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) |
| reference-semantics/semantics/builtins.k | 47 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int) |
| reference-semantics/semantics/builtins.k | 48 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k> |
| reference-semantics/semantics/builtins.k | 49 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k> |
| reference-semantics/semantics/builtins.k | 50 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V) |
| reference-semantics/semantics/builtins.k | 54 | MPY-BUILTINS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= intOf(Val) [function] |
| reference-semantics/semantics/builtins.k | 55 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intOf(I:Int) => I |
| reference-semantics/semantics/builtins.k | 56 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intOf(B:Bool) => #if B #then 1 #else 0 #fi |
| reference-semantics/semantics/builtins.k | 59 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #allAcc(Iterable) \| "#allCont" |
| reference-semantics/semantics/builtins.k | 60 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k> |
| reference-semantics/semantics/builtins.k | 61 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #allCont => true ... </k> |
| reference-semantics/semantics/builtins.k | 62 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V) |
| reference-semantics/semantics/builtins.k | 64 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V) |
| reference-semantics/semantics/builtins.k | 67 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #anyAcc(Iterable) \| "#anyCont" |
| reference-semantics/semantics/builtins.k | 68 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k> |
| reference-semantics/semantics/builtins.k | 69 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #anyCont => false ... </k> |
| reference-semantics/semantics/builtins.k | 70 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V) |
| reference-semantics/semantics/builtins.k | 72 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) |
| reference-semantics/semantics/builtins.k | 76 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int) |
| reference-semantics/semantics/builtins.k | 77 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k> |
| reference-semantics/semantics/builtins.k | 78 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| reference-semantics/semantics/builtins.k | 80 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k> |
| reference-semantics/semantics/builtins.k | 81 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k> |
| reference-semantics/semantics/builtins.k | 82 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| reference-semantics/semantics/builtins.k | 86 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int) |
| reference-semantics/semantics/builtins.k | 87 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k> |
| reference-semantics/semantics/builtins.k | 88 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| reference-semantics/semantics/builtins.k | 90 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k> |
| reference-semantics/semantics/builtins.k | 91 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #minCont(M:Int) => M ... </k> |
| reference-semantics/semantics/builtins.k | 92 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| reference-semantics/semantics/builtins.k | 97 | MPY-BUILTINS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= maxVals(Int, Vals) [function] |
| reference-semantics/semantics/builtins.k | 98 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST) |
| reference-semantics/semantics/builtins.k | 99 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule maxVals(M:Int, .Vals) => M |
| reference-semantics/semantics/builtins.k | 100 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R) |
| reference-semantics/semantics/builtins.k | 102 | MPY-BUILTINS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= minVals(Int, Vals) [function] |
| reference-semantics/semantics/builtins.k | 103 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST) |
| reference-semantics/semantics/builtins.k | 104 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule minVals(M:Int, .Vals) => M |
| reference-semantics/semantics/builtins.k | 105 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) |
| reference-semantics/semantics/builtins.k | 108 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 |
| reference-semantics/semantics/builtins.k | 111 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0 |
| reference-semantics/semantics/builtins.k | 114 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= binCodes(Int) [function, total] |
| reference-semantics/semantics/builtins.k | 115 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule binCodes(0) => iCons(48, .IntSeq) |
| reference-semantics/semantics/builtins.k | 116 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0 |
| reference-semantics/semantics/builtins.k | 117 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= binAcc(Int, IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 118 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule binAcc(0, ACC:IntSeq) => ACC |
| reference-semantics/semantics/builtins.k | 119 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 |
| reference-semantics/semantics/builtins.k | 124 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k> |
| reference-semantics/semantics/builtins.k | 126 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= enumVS(ValSeq, Int) [function, total] |
| reference-semantics/semantics/builtins.k | 127 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule enumVS(.ValSeq, _:Int) => .ValSeq |
| reference-semantics/semantics/builtins.k | 128 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) |
| reference-semantics/semantics/builtins.k | 132 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k> |
| reference-semantics/semantics/builtins.k | 134 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= mapStrVS(ValSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 135 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapStrVS(.ValSeq) => .ValSeq |
| reference-semantics/semantics/builtins.k | 136 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R)) |
| reference-semantics/semantics/builtins.k | 137 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) |
| reference-semantics/semantics/builtins.k | 140 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("int", I:Int, .Vals) => I |
| reference-semantics/semantics/builtins.k | 143 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C |
| reference-semantics/semantics/builtins.k | 144 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 |
| reference-semantics/semantics/builtins.k | 148 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I))) |
| reference-semantics/semantics/builtins.k | 149 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) |
| reference-semantics/semantics/builtins.k | 152 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 |
| reference-semantics/semantics/builtins.k | 156 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2 |
| reference-semantics/semantics/builtins.k | 158 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= intDigAcc(IntSeq, Int) [function, total] |
| reference-semantics/semantics/builtins.k | 159 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intDigAcc(.IntSeq, ACC:Int) => ACC |
| reference-semantics/semantics/builtins.k | 160 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) |
| reference-semantics/semantics/builtins.k | 163 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B) |
| reference-semantics/semantics/builtins.k | 164 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) |
| reference-semantics/semantics/builtins.k | 167 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k> |
| reference-semantics/semantics/builtins.k | 169 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k> |
| reference-semantics/semantics/builtins.k | 170 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k> |
| reference-semantics/semantics/builtins.k | 171 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k> |
| reference-semantics/semantics/builtins.k | 173 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k> |
| reference-semantics/semantics/builtins.k | 174 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> |
| reference-semantics/semantics/builtins.k | 177 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1) |
| reference-semantics/semantics/builtins.k | 178 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1) |
| reference-semantics/semantics/builtins.k | 179 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 |
| reference-semantics/semantics/builtins.k | 187 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS) |
| reference-semantics/semantics/builtins.k | 188 | MPY-BUILTINS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= evalArith(IntSeq) [function] |
| reference-semantics/semantics/builtins.k | 189 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS))))) |
| reference-semantics/semantics/builtins.k | 192 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq) |
| reference-semantics/semantics/builtins.k | 194 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= evDigit(Int) [function, total] |
| reference-semantics/semantics/builtins.k | 195 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57 |
| reference-semantics/semantics/builtins.k | 196 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= evHead42(IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 197 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule evHead42(iCons(42, _:IntSeq)) => true |
| reference-semantics/semantics/builtins.k | 198 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule evHead42(_:IntSeq) => false [owise] |
| reference-semantics/semantics/builtins.k | 199 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= evHead47(IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 200 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule evHead47(iCons(47, _:IntSeq)) => true |
| reference-semantics/semantics/builtins.k | 201 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule evHead47(_:IntSeq) => false [owise] |
| reference-semantics/semantics/builtins.k | 203 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax OpSeq ::= tokOps(IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 204 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(.IntSeq) => .OpSeq |
| reference-semantics/semantics/builtins.k | 205 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(32, R:IntSeq)) => tokOps(R) |
| reference-semantics/semantics/builtins.k | 206 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C) |
| reference-semantics/semantics/builtins.k | 207 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R)) |
| reference-semantics/semantics/builtins.k | 208 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R) |
| reference-semantics/semantics/builtins.k | 209 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R)) |
| reference-semantics/semantics/builtins.k | 210 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R) |
| reference-semantics/semantics/builtins.k | 211 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R)) |
| reference-semantics/semantics/builtins.k | 212 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R)) |
| reference-semantics/semantics/builtins.k | 214 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 216 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokNds(.IntSeq) => .IntSeq |
| reference-semantics/semantics/builtins.k | 217 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokNds(iCons(32, R:IntSeq)) => tokNds(R) |
| reference-semantics/semantics/builtins.k | 218 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C) |
| reference-semantics/semantics/builtins.k | 219 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32 |
| reference-semantics/semantics/builtins.k | 221 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C) |
| reference-semantics/semantics/builtins.k | 223 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise] |
| reference-semantics/semantics/builtins.k | 225 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax EvPair ::= evp(OpSeq, IntSeq) |
| reference-semantics/semantics/builtins.k | 226 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= firstNdE(EvPair) [function, total] |
| reference-semantics/semantics/builtins.k | 227 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N |
| reference-semantics/semantics/builtins.k | 228 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule firstNdE(_:EvPair) => 0 [owise] |
| reference-semantics/semantics/builtins.k | 230 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= applyOpE(String, Int, Int) [function, total] |
| reference-semantics/semantics/builtins.k | 231 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyOpE("+", A:Int, B:Int) => A +Int B |
| reference-semantics/semantics/builtins.k | 232 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyOpE("-", A:Int, B:Int) => A -Int B |
| reference-semantics/semantics/builtins.k | 233 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyOpE("*", A:Int, B:Int) => A *Int B |
| reference-semantics/semantics/builtins.k | 234 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyOpE("//", A:Int, B:Int) => A divInt B |
| reference-semantics/semantics/builtins.k | 235 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyOpE("**", A:Int, B:Int) => A ^Int B |
| reference-semantics/semantics/builtins.k | 236 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyOpE(_:String, A:Int, _:Int) => A [owise] |
| reference-semantics/semantics/builtins.k | 238 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 239 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS) |
| reference-semantics/semantics/builtins.k | 240 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS)) |
| reference-semantics/semantics/builtins.k | 241 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**" |
| reference-semantics/semantics/builtins.k | 243 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise] |
| reference-semantics/semantics/builtins.k | 244 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax EvPair ::= powCombE(Int, EvPair) [function, total] |
| reference-semantics/semantics/builtins.k | 245 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST)) |
| reference-semantics/semantics/builtins.k | 246 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq)) |
| reference-semantics/semantics/builtins.k | 247 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total] |
| reference-semantics/semantics/builtins.k | 248 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS)) |
| reference-semantics/semantics/builtins.k | 250 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total] |
| reference-semantics/semantics/builtins.k | 251 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq) |
| reference-semantics/semantics/builtins.k | 252 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| reference-semantics/semantics/builtins.k | 253 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq) |
| reference-semantics/semantics/builtins.k | 254 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| reference-semantics/semantics/builtins.k | 255 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total] |
| reference-semantics/semantics/builtins.k | 256 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) |
| reference-semantics/semantics/builtins.k | 257 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O) |
| reference-semantics/semantics/builtins.k | 260 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O) |
| reference-semantics/semantics/builtins.k | 263 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise] |
| reference-semantics/semantics/builtins.k | 265 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= inLevelE(String, String) [function, total] |
| reference-semantics/semantics/builtins.k | 266 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/" |
| reference-semantics/semantics/builtins.k | 267 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-" |
| reference-semantics/semantics/builtins.k | 268 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule inLevelE(_:String, _:String) => false [owise] |
| reference-semantics/semantics/builtins.k | 269 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax OpSeq ::= appendOpE(OpSeq, String) [function, total] |
| reference-semantics/semantics/builtins.k | 270 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq) |
| reference-semantics/semantics/builtins.k | 271 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O)) |
| reference-semantics/semantics/builtins.k | 272 | MPY-BUILTINS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= appendIE(IntSeq, Int) [function, total] |
| reference-semantics/semantics/builtins.k | 273 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq) |
| reference-semantics/semantics/builtins.k | 274 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) |
| reference-semantics/semantics/builtins.k | 279 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= "#md5" |
| reference-semantics/semantics/builtins.k | 280 | MPY-BUILTINS | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)] |
| reference-semantics/semantics/builtins.k | 282 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k> |
| reference-semantics/semantics/builtins.k | 283 | MPY-BUILTINS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= md5Obj(IntSeq) |
| reference-semantics/semantics/builtins.k | 284 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS)) |
| reference-semantics/semantics/builtins.k | 285 | MPY-BUILTINS | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] |
| reference-semantics/semantics/builtins.k | 291 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V) |
| reference-semantics/semantics/builtins.k | 292 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V) |
| reference-semantics/semantics/builtins.k | 293 | MPY-BUILTINS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function] |
| reference-semantics/semantics/builtins.k | 294 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isIntV(_:Int) => true |
| reference-semantics/semantics/builtins.k | 295 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isIntV(_:Val) => false [owise] |
| reference-semantics/semantics/builtins.k | 296 | MPY-BUILTINS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isStrV(str(_:IntSeq)) => true |
| reference-semantics/semantics/builtins.k | 297 | MPY-BUILTINS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isStrV(_:Val) => false [owise] |
| reference-semantics/semantics/builtins.k | 298 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/call.k | 10 | MPY-CALL | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-CALL |
| reference-semantics/semantics/call.k | 11 | MPY-CALL | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-METHODS |
| reference-semantics/semantics/call.k | 12 | MPY-CALL | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-BUILTINS |
| reference-semantics/semantics/call.k | 13 | MPY-CALL | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-FUNCTIONS |
| reference-semantics/semantics/call.k | 16 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> |
| reference-semantics/semantics/call.k | 19 | MPY-CALL | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= #callee(Exprs) |
| reference-semantics/semantics/call.k | 20 | MPY-CALL | rule | owise | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise] |
| reference-semantics/semantics/call.k | 21 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> |
| reference-semantics/semantics/call.k | 24 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k> |
| reference-semantics/semantics/call.k | 26 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k> |
| reference-semantics/semantics/call.k | 27 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k> |
| reference-semantics/semantics/call.k | 28 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k> |
| reference-semantics/semantics/call.k | 29 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k> |
| reference-semantics/semantics/call.k | 30 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k> |
| reference-semantics/semantics/call.k | 31 | MPY-CALL | rule | owise | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise] |
| reference-semantics/semantics/call.k | 32 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> |
| reference-semantics/semantics/call.k | 38 | MPY-CALL | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/call.k | 42 | MPY-CALL | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)] |
| reference-semantics/semantics/call.k | 47 | MPY-CALL | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/call.k | 52 | MPY-CALL | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Bool ::= isMutMethod(String) [function, total] |
| reference-semantics/semantics/call.k | 53 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove" |
| reference-semantics/semantics/call.k | 56 | MPY-CALL | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] |
| reference-semantics/semantics/call.k | 63 | MPY-CALL | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)] |
| reference-semantics/semantics/call.k | 69 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> |
| reference-semantics/semantics/call.k | 80 | MPY-CALL | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack… |
| reference-semantics/semantics/call.k | 87 | MPY-CALL | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #allocCells(ParamNames) |
| reference-semantics/semantics/call.k | 88 | MPY-CALL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #allocCells(.ParamNames) => .K ... </k> |
| reference-semantics/semantics/call.k | 89 | MPY-CALL | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| reference-semantics/semantics/call.k | 95 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/comprehension.k | 3 | MPY-COMPREHENSION | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-COMPREHENSION |
| reference-semantics/semantics/comprehension.k | 4 | MPY-COMPREHENSION | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/comprehension.k | 5 | MPY-COMPREHENSION | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-OPERATORS |
| reference-semantics/semantics/comprehension.k | 6 | MPY-COMPREHENSION | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-LIST |
| reference-semantics/semantics/comprehension.k | 7 | MPY-COMPREHENSION | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CONTROLS |
| reference-semantics/semantics/comprehension.k | 8 | MPY-COMPREHENSION | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-FUNCTIONS |
| reference-semantics/semantics/comprehension.k | 11 | MPY-COMPREHENSION | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| reference-semantics/semantics/comprehension.k | 12 | MPY-COMPREHENSION | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| reference-semantics/semantics/comprehension.k | 14 | MPY-COMPREHENSION | syntax | macro | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Stmts ::= compBody(CompFors, Expr) [macro] |
| reference-semantics/semantics/comprehension.k | 15 | MPY-COMPREHENSION | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc")) |
| reference-semantics/semantics/comprehension.k | 18 | MPY-COMPREHENSION | syntax | macro,macro-rec | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Stmt ::= compNest(CompFors, Expr) [macro-rec] |
| reference-semantics/semantics/comprehension.k | 19 | MPY-COMPREHENSION | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT))) |
| reference-semantics/semantics/comprehension.k | 21 | MPY-COMPREHENSION | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts)) |
| reference-semantics/semantics/comprehension.k | 24 | MPY-COMPREHENSION | syntax | macro | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Expr ::= compGuard(Exprs) [macro] |
| reference-semantics/semantics/comprehension.k | 25 | MPY-COMPREHENSION | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule compGuard(.Exprs) => Bool(true) |
| reference-semantics/semantics/comprehension.k | 26 | MPY-COMPREHENSION | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs)) |
| reference-semantics/semantics/comprehension.k | 27 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/concrete.k | 8 | MPY-CONCRETE | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-CONCRETE |
| reference-semantics/semantics/concrete.k | 9 | MPY-CONCRETE | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY |
| reference-semantics/semantics/concrete.k | 13 | MPY-CONCRETE | rule | - | FIXED_CONCRETE_TEST_PATH_REVIEWED | rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| reference-semantics/semantics/concrete.k | 16 | MPY-CONCRETE | rule | - | FIXED_CONCRETE_TEST_PATH_REVIEWED | rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| reference-semantics/semantics/concrete.k | 25 | MPY-CONCRETE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= kvP(Val, Val) |
| reference-semantics/semantics/concrete.k | 26 | MPY-CONCRETE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool) |
| reference-semantics/semantics/concrete.k | 28 | MPY-CONCRETE | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)] |
| reference-semantics/semantics/concrete.k | 31 | MPY-CONCRETE | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)] |
| reference-semantics/semantics/concrete.k | 34 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k> |
| reference-semantics/semantics/concrete.k | 36 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k> |
| reference-semantics/semantics/concrete.k | 38 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K) |
| reference-semantics/semantics/concrete.k | 42 | MPY-CONCRETE | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= insPair(ValSeq, Val, Val) [function] |
| reference-semantics/semantics/concrete.k | 43 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq) |
| reference-semantics/semantics/concrete.k | 44 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2) |
| reference-semantics/semantics/concrete.k | 47 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2) |
| reference-semantics/semantics/concrete.k | 51 | MPY-CONCRETE | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= kLt(Val, Val) [function] |
| reference-semantics/semantics/concrete.k | 52 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule kLt(I1:Int, I2:Int) => I1 <Int I2 |
| reference-semantics/semantics/concrete.k | 53 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule kLt(F1:Float, F2:Float) => F1 <Float F2 |
| reference-semantics/semantics/concrete.k | 54 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| reference-semantics/semantics/concrete.k | 56 | MPY-CONCRETE | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= unpairVS(ValSeq) [function, total] |
| reference-semantics/semantics/concrete.k | 57 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule unpairVS(.ValSeq) => .ValSeq |
| reference-semantics/semantics/concrete.k | 58 | MPY-CONCRETE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R)) |
| reference-semantics/semantics/concrete.k | 59 | MPY-CONCRETE | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise] |
| reference-semantics/semantics/concrete.k | 60 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/controls.k | 3 | MPY-CONTROLS | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-CONTROLS |
| reference-semantics/semantics/controls.k | 4 | MPY-CONTROLS | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CORE |
| reference-semantics/semantics/controls.k | 5 | MPY-CONTROLS | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-TUPLE |
| reference-semantics/semantics/controls.k | 6 | MPY-CONTROLS | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-ITER |
| reference-semantics/semantics/controls.k | 9 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| reference-semantics/semantics/controls.k | 12 | MPY-CONTROLS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| reference-semantics/semantics/controls.k | 20 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) |
| reference-semantics/semantics/controls.k | 27 | MPY-CONTROLS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] |
| reference-semantics/semantics/controls.k | 35 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k> |
| reference-semantics/semantics/controls.k | 36 | MPY-CONTROLS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise] |
| reference-semantics/semantics/controls.k | 37 | MPY-CONTROLS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #bindImports(ParamNames) |
| reference-semantics/semantics/controls.k | 38 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindImports(.ParamNames) => .K ... </k> |
| reference-semantics/semantics/controls.k | 39 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil" |
| reference-semantics/semantics/controls.k | 43 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") |
| reference-semantics/semantics/controls.k | 48 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Expr(_:Val) => .K ... </k> |
| reference-semantics/semantics/controls.k | 51 | MPY-CONTROLS | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= #branch(Bool, Stmts, Stmts) |
| reference-semantics/semantics/controls.k | 52 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k> |
| reference-semantics/semantics/controls.k | 53 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k> |
| reference-semantics/semantics/controls.k | 54 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> |
| reference-semantics/semantics/controls.k | 57 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V) |
| reference-semantics/semantics/controls.k | 59 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) |
| reference-semantics/semantics/controls.k | 65 | MPY-CONTROLS | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk" |
| reference-semantics/semantics/controls.k | 69 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k> |
| reference-semantics/semantics/controls.k | 71 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k> |
| reference-semantics/semantics/controls.k | 72 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k> |
| reference-semantics/semantics/controls.k | 73 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> |
| reference-semantics/semantics/controls.k | 77 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k> |
| reference-semantics/semantics/controls.k | 78 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k> |
| reference-semantics/semantics/controls.k | 79 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V) |
| reference-semantics/semantics/controls.k | 81 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) |
| reference-semantics/semantics/controls.k | 85 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #loopLbl(NEXT:K) => NEXT ... </k> |
| reference-semantics/semantics/controls.k | 86 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Continue => #cont ... </k> |
| reference-semantics/semantics/controls.k | 87 | MPY-CONTROLS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Break => #brk ... </k> |
| reference-semantics/semantics/controls.k | 88 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k> |
| reference-semantics/semantics/controls.k | 89 | MPY-CONTROLS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #cont ~> (_:KItem => .K) ... </k> [owise] |
| reference-semantics/semantics/controls.k | 90 | MPY-CONTROLS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #brk ~> #loopLbl(_:K) => .K ... </k> |
| reference-semantics/semantics/controls.k | 91 | MPY-CONTROLS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] |
| reference-semantics/semantics/controls.k | 95 | MPY-CONTROLS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/controls.k | 98 | MPY-CONTROLS | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/controls.k | 101 | MPY-CONTROLS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/controls.k | 106 | MPY-CONTROLS | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/controls.k | 109 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/core.k | 3 | MPY-CORE | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-CORE |
| reference-semantics/semantics/core.k | 4 | MPY-CORE | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-SYNTAX |
| reference-semantics/semantics/core.k | 5 | MPY-CORE | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports INT |
| reference-semantics/semantics/core.k | 6 | MPY-CORE | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports BOOL |
| reference-semantics/semantics/core.k | 7 | MPY-CORE | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports STRING |
| reference-semantics/semantics/core.k | 8 | MPY-CORE | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MAP |
| reference-semantics/semantics/core.k | 9 | MPY-CORE | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports LIST |
| reference-semantics/semantics/core.k | 10 | MPY-CORE | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports K-EQUAL |
| reference-semantics/semantics/core.k | 13 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq) |
| reference-semantics/semantics/core.k | 14 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq) |
| reference-semantics/semantics/core.k | 15 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Str ::= str(IntSeq) |
| reference-semantics/semantics/core.k | 18 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq) |
| reference-semantics/semantics/core.k | 25 | MPY-CORE | syntax | function | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) // a type object (int/str), resolved from the builtins frame \| builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String) // a cooled Attribute: obj.… |
| reference-semantics/semantics/core.k | 36 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Parent ::= "root" \| parent(Int) |
| reference-semantics/semantics/core.k | 37 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Scope ::= scope(Map, Parent) |
| reference-semantics/semantics/core.k | 38 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KResult ::= Val |
| reference-semantics/semantics/core.k | 39 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Expr ::= Val // cooling puts results back into expression holes |
| reference-semantics/semantics/core.k | 40 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Vals ::= List{Val, ","} |
| reference-semantics/semantics/core.k | 41 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Exc ::= "NoExc" \| "AssertionError" |
| reference-semantics/semantics/core.k | 42 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax RetState ::= "noRet" \| retV(Val) |
| reference-semantics/semantics/core.k | 49 | MPY-CORE | configuration | - | FIXED_MATERIAL_CONFIGURATION_REVIEWED | configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code> |
| reference-semantics/semantics/core.k | 68 | MPY-CORE | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Bool ::= isRefV(Val) [function, total] |
| reference-semantics/semantics/core.k | 69 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule isRefV(ref(_:Int)) => true |
| reference-semantics/semantics/core.k | 70 | MPY-CORE | rule | owise | FIXED_MATERIAL_EXECUTION_REVIEWED | rule isRefV(_:Val) => false [owise] |
| reference-semantics/semantics/core.k | 75 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax HeapVal ::= cellV(Val) |
| reference-semantics/semantics/core.k | 76 | MPY-CORE | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isCellRef(Val) [function, total] |
| reference-semantics/semantics/core.k | 77 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isCellRef(cellRef(_:Int)) => true |
| reference-semantics/semantics/core.k | 78 | MPY-CORE | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isCellRef(_:Val) => false [owise] |
| reference-semantics/semantics/core.k | 85 | MPY-CORE | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] |
| reference-semantics/semantics/core.k | 95 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= kwV(String, Val) |
| reference-semantics/semantics/core.k | 96 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #kwTag(String) |
| reference-semantics/semantics/core.k | 97 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k> |
| reference-semantics/semantics/core.k | 98 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V) |
| reference-semantics/semantics/core.k | 100 | MPY-CORE | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isKwV(Val) [function, total] |
| reference-semantics/semantics/core.k | 101 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isKwV(kwV(_:String, _:Val)) => true |
| reference-semantics/semantics/core.k | 102 | MPY-CORE | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isKwV(_:Val) => false [owise] |
| reference-semantics/semantics/core.k | 106 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= cellsMark(ParamNames) |
| reference-semantics/semantics/core.k | 107 | MPY-CORE | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ParamNames ::= cellsOf(Val) [function] |
| reference-semantics/semantics/core.k | 108 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule cellsOf(cellsMark(CVS:ParamNames)) => CVS |
| reference-semantics/semantics/core.k | 109 | MPY-CORE | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= pnMember(String, ParamNames) [function, total] |
| reference-semantics/semantics/core.k | 110 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule pnMember(_:String, .ParamNames) => false |
| reference-semantics/semantics/core.k | 111 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R) |
| reference-semantics/semantics/core.k | 113 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #cellW(Val, Val) |
| reference-semantics/semantics/core.k | 114 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap> |
| reference-semantics/semantics/core.k | 117 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= #alloc(Val) |
| reference-semantics/semantics/core.k | 118 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| reference-semantics/semantics/core.k | 124 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= #loadAll(Module) |
| reference-semantics/semantics/core.k | 125 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k> |
| reference-semantics/semantics/core.k | 126 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k> |
| reference-semantics/semantics/core.k | 127 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> .Stmts => .K ... </k> |
| reference-semantics/semantics/core.k | 130 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= #look(String, Int) |
| reference-semantics/semantics/core.k | 131 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env> |
| reference-semantics/semantics/core.k | 132 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) |
| reference-semantics/semantics/core.k | 145 | MPY-CORE | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)] |
| reference-semantics/semantics/core.k | 152 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) |
| reference-semantics/semantics/core.k | 157 | MPY-CORE | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Scope ::= "builtinsScope" [function, total] |
| reference-semantics/semantics/core.k | 158 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinsta… |
| reference-semantics/semantics/core.k | 185 | MPY-CORE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ApplyK ::= toCall(Val) |
| reference-semantics/semantics/core.k | 186 | MPY-CORE | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals) |
| reference-semantics/semantics/core.k | 189 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k> |
| reference-semantics/semantics/core.k | 190 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k> |
| reference-semantics/semantics/core.k | 191 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> |
| reference-semantics/semantics/core.k | 194 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Int(I:Int) => I ... </k> |
| reference-semantics/semantics/core.k | 195 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Bool(B:Bool) => B ... </k> |
| reference-semantics/semantics/core.k | 196 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> NoneVal => noneV ... </k> |
| reference-semantics/semantics/core.k | 199 | MPY-CORE | syntax | function | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Bool ::= truthy(Val) [function] |
| reference-semantics/semantics/core.k | 200 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule truthy(B:Bool) => B |
| reference-semantics/semantics/core.k | 201 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule truthy(noneV) => false |
| reference-semantics/semantics/core.k | 202 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule truthy(I:Int) => I =/=Int 0 |
| reference-semantics/semantics/core.k | 203 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq) |
| reference-semantics/semantics/core.k | 204 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq) |
| reference-semantics/semantics/core.k | 205 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) |
| reference-semantics/semantics/core.k | 208 | MPY-CORE | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= applyUn(String, Val) [function] |
| reference-semantics/semantics/core.k | 209 | MPY-CORE | syntax | function | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Val ::= applyBin(String, Val, Val) [function] |
| reference-semantics/semantics/core.k | 210 | MPY-CORE | syntax | function | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Bool ::= applyCmp(String, Val, Val) [function] |
| reference-semantics/semantics/core.k | 213 | MPY-CORE | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Vals ::= appendVal(Vals, Val) [function, total] |
| reference-semantics/semantics/core.k | 214 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule appendVal(.Vals, V:Val) => V , .Vals |
| reference-semantics/semantics/core.k | 215 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V) |
| reference-semantics/semantics/core.k | 217 | MPY-CORE | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax ValSeq ::= vals2valSeq(Vals) [function, total] |
| reference-semantics/semantics/core.k | 218 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule vals2valSeq(.Vals) => .ValSeq |
| reference-semantics/semantics/core.k | 219 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) |
| reference-semantics/semantics/core.k | 223 | MPY-CORE | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Int ::= vsLen(ValSeq) [function, total] |
| reference-semantics/semantics/core.k | 224 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule vsLen(.ValSeq) => 0 |
| reference-semantics/semantics/core.k | 225 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S) |
| reference-semantics/semantics/core.k | 227 | MPY-CORE | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= isLen(IntSeq) [function, total] |
| reference-semantics/semantics/core.k | 228 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isLen(.IntSeq) => 0 |
| reference-semantics/semantics/core.k | 229 | MPY-CORE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) |
| reference-semantics/semantics/core.k | 233 | MPY-CORE | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total] |
| reference-semantics/semantics/core.k | 234 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq |
| reference-semantics/semantics/core.k | 235 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S) |
| reference-semantics/semantics/core.k | 236 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0 |
| reference-semantics/semantics/core.k | 238 | MPY-CORE | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0 |
| reference-semantics/semantics/core.k | 240 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/dict.k | 13 | MPY-DICT | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-DICT |
| reference-semantics/semantics/dict.k | 14 | MPY-DICT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/dict.k | 15 | MPY-DICT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-ITER |
| reference-semantics/semantics/dict.k | 16 | MPY-DICT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-METHODS |
| reference-semantics/semantics/dict.k | 17 | MPY-DICT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-LIST |
| reference-semantics/semantics/dict.k | 20 | MPY-DICT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= dictV(ValSeq, ValSeq) |
| reference-semantics/semantics/dict.k | 23 | MPY-DICT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq) |
| reference-semantics/semantics/dict.k | 26 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k> |
| reference-semantics/semantics/dict.k | 27 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k> |
| reference-semantics/semantics/dict.k | 28 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k> |
| reference-semantics/semantics/dict.k | 30 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k> |
| reference-semantics/semantics/dict.k | 32 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> |
| reference-semantics/semantics/dict.k | 37 | MPY-DICT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= dHasKey(ValSeq, Val) [function, total] |
| reference-semantics/semantics/dict.k | 38 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dHasKey(.ValSeq, _:Val) => false |
| reference-semantics/semantics/dict.k | 39 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K |
| reference-semantics/semantics/dict.k | 40 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) |
| reference-semantics/semantics/dict.k | 43 | MPY-DICT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= dPutK(ValSeq, Val) [function, total] |
| reference-semantics/semantics/dict.k | 44 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K) |
| reference-semantics/semantics/dict.k | 45 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) |
| reference-semantics/semantics/dict.k | 49 | MPY-DICT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total] |
| reference-semantics/semantics/dict.k | 50 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K |
| reference-semantics/semantics/dict.k | 52 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K) |
| reference-semantics/semantics/dict.k | 54 | MPY-DICT | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] |
| reference-semantics/semantics/dict.k | 58 | MPY-DICT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] |
| reference-semantics/semantics/dict.k | 63 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K) |
| reference-semantics/semantics/dict.k | 64 | MPY-DICT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= applyIndexD(Val, Val) [function] |
| reference-semantics/semantics/dict.k | 65 | MPY-DICT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] |
| reference-semantics/semantics/dict.k | 70 | MPY-DICT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= dictSet(Val, Val, Val) [function] |
| reference-semantics/semantics/dict.k | 71 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) |
| reference-semantics/semantics/dict.k | 76 | MPY-DICT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #dsetK(String, Val) |
| reference-semantics/semantics/dict.k | 77 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k> |
| reference-semantics/semantics/dict.k | 78 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val) |
| reference-semantics/semantics/dict.k | 82 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) |
| reference-semantics/semantics/dict.k | 86 | MPY-DICT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #dsetV(Val, Val, Val) |
| reference-semantics/semantics/dict.k | 87 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> |
| reference-semantics/semantics/dict.k | 90 | MPY-DICT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= normIdxD(Int, Int) [function, total] |
| reference-semantics/semantics/dict.k | 91 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0 |
| reference-semantics/semantics/dict.k | 92 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 |
| reference-semantics/semantics/dict.k | 95 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2) |
| reference-semantics/semantics/dict.k | 97 | MPY-DICT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function] |
| reference-semantics/semantics/dict.k | 98 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true |
| reference-semantics/semantics/dict.k | 99 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2) |
| reference-semantics/semantics/dict.k | 101 | MPY-DICT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= dGet(ValSeq, ValSeq, Val) [function] |
| reference-semantics/semantics/dict.k | 102 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K |
| reference-semantics/semantics/dict.k | 103 | MPY-DICT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K) |
| reference-semantics/semantics/dict.k | 104 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/float.k | 14 | MPY-FLOAT | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-FLOAT |
| reference-semantics/semantics/float.k | 15 | MPY-FLOAT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-OPERATORS |
| reference-semantics/semantics/float.k | 16 | MPY-FLOAT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-BUILTINS |
| reference-semantics/semantics/float.k | 17 | MPY-FLOAT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports FLOAT |
| reference-semantics/semantics/float.k | 20 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= Float |
| reference-semantics/semantics/float.k | 21 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Float(F:Float) => F ... </k> |
| reference-semantics/semantics/float.k | 24 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators] |
| reference-semantics/semantics/float.k | 25 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete] |
| reference-semantics/semantics/float.k | 27 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) |
| reference-semantics/semantics/float.k | 30 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators] |
| reference-semantics/semantics/float.k | 31 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete] |
| reference-semantics/semantics/float.k | 32 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) |
| reference-semantics/semantics/float.k | 37 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators] |
| reference-semantics/semantics/float.k | 38 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete] |
| reference-semantics/semantics/float.k | 39 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) |
| reference-semantics/semantics/float.k | 43 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2 |
| reference-semantics/semantics/float.k | 44 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) |
| reference-semantics/semantics/float.k | 50 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators] |
| reference-semantics/semantics/float.k | 51 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete] |
| reference-semantics/semantics/float.k | 52 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2) |
| reference-semantics/semantics/float.k | 54 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators] |
| reference-semantics/semantics/float.k | 55 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule absF(F:Float) => absFloat(F) [concrete] |
| reference-semantics/semantics/float.k | 56 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("abs", F:Float, .Vals) => absF(F) |
| reference-semantics/semantics/float.k | 61 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Import(_:String) => .K ... </k> |
| reference-semantics/semantics/float.k | 65 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= "#mathCeil" |
| reference-semantics/semantics/float.k | 66 | MPY-FLOAT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)] |
| reference-semantics/semantics/float.k | 67 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> |
| reference-semantics/semantics/float.k | 70 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= "#mathFloor" |
| reference-semantics/semantics/float.k | 71 | MPY-FLOAT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)] |
| reference-semantics/semantics/float.k | 72 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k> |
| reference-semantics/semantics/float.k | 73 | MPY-FLOAT | syntax | function,total,symbol | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)] |
| reference-semantics/semantics/float.k | 74 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule floorFI(I:Int) => I [concrete] |
| reference-semantics/semantics/float.k | 75 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] |
| reference-semantics/semantics/float.k | 78 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V) |
| reference-semantics/semantics/float.k | 79 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) |
| reference-semantics/semantics/float.k | 82 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val) |
| reference-semantics/semantics/float.k | 83 | MPY-FLOAT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)] |
| reference-semantics/semantics/float.k | 84 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k> |
| reference-semantics/semantics/float.k | 85 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k> |
| reference-semantics/semantics/float.k | 86 | MPY-FLOAT | syntax | function,total,symbol | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= toF(Val) [function, total, symbol(toF)] |
| reference-semantics/semantics/float.k | 87 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule toF(F:Float) => F [concrete] |
| reference-semantics/semantics/float.k | 88 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule toF(I:Int) => intToF(I) [concrete] |
| reference-semantics/semantics/float.k | 93 | MPY-FLOAT | syntax | function,total,symbol | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)] |
| reference-semantics/semantics/float.k | 94 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule ceilF(I:Int) => I [concrete] |
| reference-semantics/semantics/float.k | 95 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] |
| reference-semantics/semantics/float.k | 99 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyUn("-", F:Float) => 0.0 -Float F |
| reference-semantics/semantics/float.k | 103 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators] |
| reference-semantics/semantics/float.k | 104 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete] |
| reference-semantics/semantics/float.k | 105 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2) |
| reference-semantics/semantics/float.k | 107 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators] |
| reference-semantics/semantics/float.k | 108 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete] |
| reference-semantics/semantics/float.k | 109 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2) |
| reference-semantics/semantics/float.k | 111 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators] |
| reference-semantics/semantics/float.k | 112 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete] |
| reference-semantics/semantics/float.k | 113 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2) |
| reference-semantics/semantics/float.k | 115 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators] |
| reference-semantics/semantics/float.k | 116 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete] |
| reference-semantics/semantics/float.k | 117 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2) |
| reference-semantics/semantics/float.k | 119 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators] |
| reference-semantics/semantics/float.k | 120 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete] |
| reference-semantics/semantics/float.k | 121 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) |
| reference-semantics/semantics/float.k | 125 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators] |
| reference-semantics/semantics/float.k | 126 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete] |
| reference-semantics/semantics/float.k | 127 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2) |
| reference-semantics/semantics/float.k | 128 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2) |
| reference-semantics/semantics/float.k | 129 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) |
| reference-semantics/semantics/float.k | 132 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F) |
| reference-semantics/semantics/float.k | 133 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 134 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F) |
| reference-semantics/semantics/float.k | 135 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 136 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F) |
| reference-semantics/semantics/float.k | 137 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 138 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F) |
| reference-semantics/semantics/float.k | 139 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 142 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators] |
| reference-semantics/semantics/float.k | 143 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete] |
| reference-semantics/semantics/float.k | 144 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F) |
| reference-semantics/semantics/float.k | 145 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 146 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F) |
| reference-semantics/semantics/float.k | 147 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 148 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F) |
| reference-semantics/semantics/float.k | 149 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I)) |
| reference-semantics/semantics/float.k | 150 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F) |
| reference-semantics/semantics/float.k | 151 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 154 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", V:Val, noneV) => V ==K noneV |
| reference-semantics/semantics/float.k | 155 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) |
| reference-semantics/semantics/float.k | 160 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators] |
| reference-semantics/semantics/float.k | 161 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete] |
| reference-semantics/semantics/float.k | 162 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete] |
| reference-semantics/semantics/float.k | 165 | MPY-FLOAT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= headIS(IntSeq) [function] |
| reference-semantics/semantics/float.k | 166 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule headIS(iCons(C:Int, _:IntSeq)) => C |
| reference-semantics/semantics/float.k | 167 | MPY-FLOAT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total] |
| reference-semantics/semantics/float.k | 168 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intPart(CS:IntSeq) => intPartAcc(CS, 0) |
| reference-semantics/semantics/float.k | 169 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intPartAcc(.IntSeq, A:Int) => A |
| reference-semantics/semantics/float.k | 170 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A |
| reference-semantics/semantics/float.k | 171 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46 |
| reference-semantics/semantics/float.k | 173 | MPY-FLOAT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total] |
| reference-semantics/semantics/float.k | 174 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracPart(.IntSeq) => 0 |
| reference-semantics/semantics/float.k | 175 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0) |
| reference-semantics/semantics/float.k | 176 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46 |
| reference-semantics/semantics/float.k | 177 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracAcc(.IntSeq, A:Int) => A |
| reference-semantics/semantics/float.k | 178 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48)) |
| reference-semantics/semantics/float.k | 179 | MPY-FLOAT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total] |
| reference-semantics/semantics/float.k | 180 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracScale(.IntSeq) => 1 |
| reference-semantics/semantics/float.k | 181 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1) |
| reference-semantics/semantics/float.k | 182 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46 |
| reference-semantics/semantics/float.k | 183 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fscAcc(.IntSeq, A:Int) => A |
| reference-semantics/semantics/float.k | 184 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10) |
| reference-semantics/semantics/float.k | 185 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS) |
| reference-semantics/semantics/float.k | 186 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("float", I:Int, .Vals) => intToF(I) |
| reference-semantics/semantics/float.k | 187 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("float", F:Float, .Vals) => F |
| reference-semantics/semantics/float.k | 190 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators] |
| reference-semantics/semantics/float.k | 191 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete] |
| reference-semantics/semantics/float.k | 192 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) |
| reference-semantics/semantics/float.k | 195 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators] |
| reference-semantics/semantics/float.k | 196 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete] |
| reference-semantics/semantics/float.k | 197 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F) |
| reference-semantics/semantics/float.k | 198 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 199 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F) |
| reference-semantics/semantics/float.k | 200 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 201 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F) |
| reference-semantics/semantics/float.k | 202 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 203 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F) |
| reference-semantics/semantics/float.k | 204 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I)) |
| reference-semantics/semantics/float.k | 205 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F) |
| reference-semantics/semantics/float.k | 206 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) |
| reference-semantics/semantics/float.k | 209 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators] |
| reference-semantics/semantics/float.k | 210 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete] |
| reference-semantics/semantics/float.k | 211 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("int", F:Float, .Vals) => truncF(F) |
| reference-semantics/semantics/float.k | 213 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("float", I:Int, .Vals) => intToF(I) |
| reference-semantics/semantics/float.k | 214 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("float", F:Float, .Vals) => F |
| reference-semantics/semantics/float.k | 217 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators] |
| reference-semantics/semantics/float.k | 218 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete] |
| reference-semantics/semantics/float.k | 223 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators] |
| reference-semantics/semantics/float.k | 224 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete] |
| reference-semantics/semantics/float.k | 227 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("round", F:Float, .Vals) => roundF(F) |
| reference-semantics/semantics/float.k | 228 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N) |
| reference-semantics/semantics/float.k | 230 | MPY-FLOAT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators] |
| reference-semantics/semantics/float.k | 231 | MPY-FLOAT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule sqrtF(F:Float) => sqrtFloat(F) [concrete] |
| reference-semantics/semantics/float.k | 232 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= "#mathSqrt" |
| reference-semantics/semantics/float.k | 233 | MPY-FLOAT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)] |
| reference-semantics/semantics/float.k | 234 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k> |
| reference-semantics/semantics/float.k | 235 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> |
| reference-semantics/semantics/float.k | 243 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float) |
| reference-semantics/semantics/float.k | 244 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| reference-semantics/semantics/float.k | 245 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k> |
| reference-semantics/semantics/float.k | 246 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k> |
| reference-semantics/semantics/float.k | 247 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| reference-semantics/semantics/float.k | 250 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float) |
| reference-semantics/semantics/float.k | 251 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| reference-semantics/semantics/float.k | 252 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k> |
| reference-semantics/semantics/float.k | 253 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #minContF(M:Float) => M ... </k> |
| reference-semantics/semantics/float.k | 254 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| reference-semantics/semantics/float.k | 261 | MPY-FLOAT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float) |
| reference-semantics/semantics/float.k | 262 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V)) |
| reference-semantics/semantics/float.k | 265 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k> |
| reference-semantics/semantics/float.k | 266 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k> |
| reference-semantics/semantics/float.k | 267 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V) |
| reference-semantics/semantics/float.k | 270 | MPY-FLOAT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V) |
| reference-semantics/semantics/float.k | 273 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/functions.k | 3 | MPY-FUNCTIONS | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-FUNCTIONS |
| reference-semantics/semantics/functions.k | 4 | MPY-FUNCTIONS | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CORE |
| reference-semantics/semantics/functions.k | 8 | MPY-FUNCTIONS | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" |
| reference-semantics/semantics/functions.k | 14 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes> |
| reference-semantics/semantics/functions.k | 18 | MPY-FUNCTIONS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Expr ::= closureExpr(ParamNames, Stmts) |
| reference-semantics/semantics/functions.k | 19 | MPY-FUNCTIONS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> |
| reference-semantics/semantics/functions.k | 27 | MPY-FUNCTIONS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) |
| reference-semantics/semantics/functions.k | 31 | MPY-FUNCTIONS | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map) |
| reference-semantics/semantics/functions.k | 33 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k> |
| reference-semantics/semantics/functions.k | 36 | MPY-FUNCTIONS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| reference-semantics/semantics/functions.k | 42 | MPY-FUNCTIONS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes> |
| reference-semantics/semantics/functions.k | 47 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env> |
| reference-semantics/semantics/functions.k | 50 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k> |
| reference-semantics/semantics/functions.k | 53 | MPY-FUNCTIONS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| reference-semantics/semantics/functions.k | 59 | MPY-FUNCTIONS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> |
| reference-semantics/semantics/functions.k | 63 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #bindP(.ParamNames, .Vals) => .K ... </k> |
| reference-semantics/semantics/functions.k | 64 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> |
| reference-semantics/semantics/functions.k | 68 | MPY-FUNCTIONS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] |
| reference-semantics/semantics/functions.k | 78 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret> |
| reference-semantics/semantics/functions.k | 80 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> |
| reference-semantics/semantics/functions.k | 85 | MPY-FUNCTIONS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc> |
| reference-semantics/semantics/functions.k | 91 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/int.k | 4 | MPY-INT | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-INT |
| reference-semantics/semantics/int.k | 5 | MPY-INT | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CORE |
| reference-semantics/semantics/int.k | 7 | MPY-INT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyUn("-", I:Int) => 0 -Int I |
| reference-semantics/semantics/int.k | 9 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 |
| reference-semantics/semantics/int.k | 11 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi |
| reference-semantics/semantics/int.k | 12 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I |
| reference-semantics/semantics/int.k | 13 | MPY-INT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2 |
| reference-semantics/semantics/int.k | 14 | MPY-INT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2 |
| reference-semantics/semantics/int.k | 15 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2) |
| reference-semantics/semantics/int.k | 16 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2 |
| reference-semantics/semantics/int.k | 17 | MPY-INT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0 |
| reference-semantics/semantics/int.k | 19 | MPY-INT | syntax | function | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Int ::= pyMod(Int, Int) [function] |
| reference-semantics/semantics/int.k | 20 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2 |
| reference-semantics/semantics/int.k | 22 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2 |
| reference-semantics/semantics/int.k | 23 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2 |
| reference-semantics/semantics/int.k | 24 | MPY-INT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2 |
| reference-semantics/semantics/int.k | 25 | MPY-INT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2 |
| reference-semantics/semantics/int.k | 26 | MPY-INT | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2 |
| reference-semantics/semantics/int.k | 27 | MPY-INT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2 |
| reference-semantics/semantics/int.k | 28 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/iter.k | 6 | MPY-ITER | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-ITER |
| reference-semantics/semantics/iter.k | 7 | MPY-ITER | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/iter.k | 8 | MPY-ITER | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable) |
| reference-semantics/semantics/iter.k | 9 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/list.k | 3 | MPY-LIST | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-LIST |
| reference-semantics/semantics/list.k | 4 | MPY-LIST | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CORE |
| reference-semantics/semantics/list.k | 5 | MPY-LIST | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-ITER |
| reference-semantics/semantics/list.k | 6 | MPY-LIST | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-OPERATORS |
| reference-semantics/semantics/list.k | 9 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k> |
| reference-semantics/semantics/list.k | 10 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> |
| reference-semantics/semantics/list.k | 13 | MPY-LIST | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax ApplyK ::= "toList" |
| reference-semantics/semantics/list.k | 14 | MPY-LIST | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k> |
| reference-semantics/semantics/list.k | 15 | MPY-LIST | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> |
| reference-semantics/semantics/list.k | 18 | MPY-LIST | syntax | function,total | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total] |
| reference-semantics/semantics/list.k | 19 | MPY-LIST | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule valSeqConcat(.ValSeq, T:ValSeq) => T |
| reference-semantics/semantics/list.k | 20 | MPY-LIST | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) |
| reference-semantics/semantics/list.k | 24 | MPY-LIST | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)] |
| reference-semantics/semantics/list.k | 27 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B |
| reference-semantics/semantics/list.k | 28 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) |
| reference-semantics/semantics/list.k | 33 | MPY-LIST | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= hasRefVS(ValSeq) [function, total] |
| reference-semantics/semantics/list.k | 34 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule hasRefVS(.ValSeq) => false |
| reference-semantics/semantics/list.k | 35 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R) |
| reference-semantics/semantics/list.k | 37 | MPY-LIST | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function] |
| reference-semantics/semantics/list.k | 39 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true |
| reference-semantics/semantics/list.k | 40 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false |
| reference-semantics/semantics/list.k | 41 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false |
| reference-semantics/semantics/list.k | 42 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP) |
| reference-semantics/semantics/list.k | 45 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP) |
| reference-semantics/semantics/list.k | 47 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP) |
| reference-semantics/semantics/list.k | 49 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP) |
| reference-semantics/semantics/list.k | 50 | MPY-LIST | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] |
| reference-semantics/semantics/list.k | 53 | MPY-LIST | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] |
| reference-semantics/semantics/list.k | 58 | MPY-LIST | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB" |
| reference-semantics/semantics/list.k | 59 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k> |
| reference-semantics/semantics/list.k | 60 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k> |
| reference-semantics/semantics/list.k | 61 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k> |
| reference-semantics/semantics/list.k | 62 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k> |
| reference-semantics/semantics/list.k | 63 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V |
| reference-semantics/semantics/list.k | 65 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V) |
| reference-semantics/semantics/list.k | 67 | MPY-LIST | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> B:Bool ~> #notB => notBool B ... </k> |
| reference-semantics/semantics/list.k | 68 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/methods.k | 3 | MPY-METHODS | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-METHODS |
| reference-semantics/semantics/methods.k | 4 | MPY-METHODS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/methods.k | 5 | MPY-METHODS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports K-EQUAL |
| reference-semantics/semantics/methods.k | 6 | MPY-METHODS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-STR |
| reference-semantics/semantics/methods.k | 7 | MPY-METHODS | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-LIST |
| reference-semantics/semantics/methods.k | 10 | MPY-METHODS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= applyMethod(Val, String, Vals) [function] |
| reference-semantics/semantics/methods.k | 13 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS) |
| reference-semantics/semantics/methods.k | 14 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS) |
| reference-semantics/semantics/methods.k | 15 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS) |
| reference-semantics/semantics/methods.k | 16 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) |
| reference-semantics/semantics/methods.k | 19 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS)) |
| reference-semantics/semantics/methods.k | 20 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS)) |
| reference-semantics/semantics/methods.k | 21 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) |
| reference-semantics/semantics/methods.k | 26 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS)) |
| reference-semantics/semantics/methods.k | 27 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total] |
| reference-semantics/semantics/methods.k | 28 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq |
| reference-semantics/semantics/methods.k | 29 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS |
| reference-semantics/semantics/methods.k | 30 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) |
| reference-semantics/semantics/methods.k | 34 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC) |
| reference-semantics/semantics/methods.k | 35 | MPY-METHODS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= cntSub(IntSeq, IntSeq) [function] |
| reference-semantics/semantics/methods.k | 36 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule cntSub(.IntSeq, _:IntSeq) => 0 |
| reference-semantics/semantics/methods.k | 37 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0 |
| reference-semantics/semantics/methods.k | 39 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0 |
| reference-semantics/semantics/methods.k | 41 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= dropIS(IntSeq, Int) [function, total] |
| reference-semantics/semantics/methods.k | 42 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0 |
| reference-semantics/semantics/methods.k | 43 | MPY-METHODS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dropIS(.IntSeq, _:Int) => .IntSeq [owise] |
| reference-semantics/semantics/methods.k | 44 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 |
| reference-semantics/semantics/methods.k | 47 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS))))) |
| reference-semantics/semantics/methods.k | 48 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= trimWS(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 49 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule trimWS(.IntSeq) => .IntSeq |
| reference-semantics/semantics/methods.k | 50 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C) |
| reference-semantics/semantics/methods.k | 51 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C) |
| reference-semantics/semantics/methods.k | 52 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 53 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule revIS(S:IntSeq) => revISAcc(S, .IntSeq) |
| reference-semantics/semantics/methods.k | 54 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule revISAcc(.IntSeq, A:IntSeq) => A |
| reference-semantics/semantics/methods.k | 55 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) |
| reference-semantics/semantics/methods.k | 58 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) |
| reference-semantics/semantics/methods.k | 61 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) |
| reference-semantics/semantics/methods.k | 64 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V) |
| reference-semantics/semantics/methods.k | 65 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= cntOccVS(ValSeq, Val) [function, total] |
| reference-semantics/semantics/methods.k | 66 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule cntOccVS(.ValSeq, _:Val) => 0 |
| reference-semantics/semantics/methods.k | 67 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V |
| reference-semantics/semantics/methods.k | 68 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) |
| reference-semantics/semantics/methods.k | 72 | MPY-METHODS | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)] |
| reference-semantics/semantics/methods.k | 75 | MPY-METHODS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result |
| reference-semantics/semantics/methods.k | 76 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR) |
| reference-semantics/semantics/methods.k | 77 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C) |
| reference-semantics/semantics/methods.k | 79 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) |
| reference-semantics/semantics/methods.k | 82 | MPY-METHODS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function] |
| reference-semantics/semantics/methods.k | 83 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule flushTok(ACC:ValSeq, .IntSeq) => ACC |
| reference-semantics/semantics/methods.k | 84 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq)) |
| reference-semantics/semantics/methods.k | 85 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isWSC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 86 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 |
| reference-semantics/semantics/methods.k | 89 | MPY-METHODS | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] |
| reference-semantics/semantics/methods.k | 94 | MPY-METHODS | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)] |
| reference-semantics/semantics/methods.k | 97 | MPY-METHODS | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token |
| reference-semantics/semantics/methods.k | 98 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq) |
| reference-semantics/semantics/methods.k | 99 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP |
| reference-semantics/semantics/methods.k | 101 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP) |
| reference-semantics/semantics/methods.k | 104 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B)) |
| reference-semantics/semantics/methods.k | 106 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total] |
| reference-semantics/semantics/methods.k | 107 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq |
| reference-semantics/semantics/methods.k | 108 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A |
| reference-semantics/semantics/methods.k | 109 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) |
| reference-semantics/semantics/methods.k | 112 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isUpperC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 113 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90 |
| reference-semantics/semantics/methods.k | 115 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isLowerC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 116 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122 |
| reference-semantics/semantics/methods.k | 118 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isAlphaC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 119 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C) |
| reference-semantics/semantics/methods.k | 121 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= isDigitC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 122 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57 |
| reference-semantics/semantics/methods.k | 124 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= hasUpper(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 125 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule hasUpper(.IntSeq) => false |
| reference-semantics/semantics/methods.k | 126 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S) |
| reference-semantics/semantics/methods.k | 128 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= hasLower(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 129 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule hasLower(.IntSeq) => false |
| reference-semantics/semantics/methods.k | 130 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S) |
| reference-semantics/semantics/methods.k | 132 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= allAlpha(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 133 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule allAlpha(.IntSeq) => true |
| reference-semantics/semantics/methods.k | 134 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S) |
| reference-semantics/semantics/methods.k | 136 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= allDigit(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 137 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule allDigit(.IntSeq) => true |
| reference-semantics/semantics/methods.k | 138 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S) |
| reference-semantics/semantics/methods.k | 140 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= lowerC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 142 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule lowerC(C:Int) => C +Int 32 requires isUpperC(C) |
| reference-semantics/semantics/methods.k | 143 | MPY-METHODS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule lowerC(C:Int) => C [owise] |
| reference-semantics/semantics/methods.k | 145 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= upperC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 146 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule upperC(C:Int) => C -Int 32 requires isLowerC(C) |
| reference-semantics/semantics/methods.k | 147 | MPY-METHODS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule upperC(C:Int) => C [owise] |
| reference-semantics/semantics/methods.k | 149 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= swapC(Int) [function, total] |
| reference-semantics/semantics/methods.k | 150 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule swapC(C:Int) => C +Int 32 requires isUpperC(C) |
| reference-semantics/semantics/methods.k | 151 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule swapC(C:Int) => C -Int 32 requires isLowerC(C) |
| reference-semantics/semantics/methods.k | 152 | MPY-METHODS | rule | owise | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule swapC(C:Int) => C [owise] |
| reference-semantics/semantics/methods.k | 154 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= mapLower(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 155 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapLower(.IntSeq) => .IntSeq |
| reference-semantics/semantics/methods.k | 156 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S)) |
| reference-semantics/semantics/methods.k | 158 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= mapUpper(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 159 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapUpper(.IntSeq) => .IntSeq |
| reference-semantics/semantics/methods.k | 160 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S)) |
| reference-semantics/semantics/methods.k | 162 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= mapSwap(IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 163 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapSwap(.IntSeq) => .IntSeq |
| reference-semantics/semantics/methods.k | 164 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S)) |
| reference-semantics/semantics/methods.k | 166 | MPY-METHODS | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/methods.k | 167 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule startsWith(.IntSeq, _:IntSeq) => true |
| reference-semantics/semantics/methods.k | 168 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| reference-semantics/semantics/methods.k | 169 | MPY-METHODS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs) |
| reference-semantics/semantics/methods.k | 170 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/operators.k | 6 | MPY-OPERATORS | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-OPERATORS |
| reference-semantics/semantics/operators.k | 7 | MPY-OPERATORS | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CORE |
| reference-semantics/semantics/operators.k | 8 | MPY-OPERATORS | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-ITER |
| reference-semantics/semantics/operators.k | 10 | MPY-OPERATORS | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k> |
| reference-semantics/semantics/operators.k | 12 | MPY-OPERATORS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> |
| reference-semantics/semantics/operators.k | 15 | MPY-OPERATORS | context | - | FIXED_MATERIAL_EXECUTION_REVIEWED | context Compare(HOLE, _) |
| reference-semantics/semantics/operators.k | 16 | MPY-OPERATORS | context | - | FIXED_MATERIAL_EXECUTION_REVIEWED | context Compare(_:Val, CmpOp(_, HOLE)) |
| reference-semantics/semantics/operators.k | 17 | MPY-OPERATORS | rule | owise | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise] |
| reference-semantics/semantics/operators.k | 19 | MPY-OPERATORS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyCmp("is", V:Val, noneV) => V ==K noneV |
| reference-semantics/semantics/operators.k | 20 | MPY-OPERATORS | rule | - | FIXED_MATERIAL_EXECUTION_REVIEWED | rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) |
| reference-semantics/semantics/operators.k | 25 | MPY-OPERATORS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/operators.k | 28 | MPY-OPERATORS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] |
| reference-semantics/semantics/operators.k | 34 | MPY-OPERATORS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)] |
| reference-semantics/semantics/operators.k | 38 | MPY-OPERATORS | rule | priority | FIXED_MATERIAL_EXECUTION_REVIEWED | rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)] |
| reference-semantics/semantics/operators.k | 44 | MPY-OPERATORS | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/operators.k | 47 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/range.k | 5 | MPY-RANGE | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-RANGE |
| reference-semantics/semantics/range.k | 6 | MPY-RANGE | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/range.k | 7 | MPY-RANGE | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-ITER |
| reference-semantics/semantics/range.k | 9 | MPY-RANGE | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= inRange(Int, Int, Int) [function, total] |
| reference-semantics/semantics/range.k | 10 | MPY-RANGE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI) |
| reference-semantics/semantics/range.k | 12 | MPY-RANGE | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= rangeLen(Int, Int, Int) [function] |
| reference-semantics/semantics/range.k | 13 | MPY-RANGE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO |
| reference-semantics/semantics/range.k | 15 | MPY-RANGE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO |
| reference-semantics/semantics/range.k | 17 | MPY-RANGE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO) |
| reference-semantics/semantics/range.k | 20 | MPY-RANGE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST) |
| reference-semantics/semantics/range.k | 23 | MPY-RANGE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST) |
| reference-semantics/semantics/range.k | 25 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/set.k | 3 | MPY-SET | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-SET |
| reference-semantics/semantics/set.k | 4 | MPY-SET | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/set.k | 8 | MPY-SET | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= setV(IntSeq) |
| reference-semantics/semantics/set.k | 11 | MPY-SET | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= codeIn(Int, IntSeq) [function, total] |
| reference-semantics/semantics/set.k | 12 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule codeIn(_:Int, .IntSeq) => false |
| reference-semantics/semantics/set.k | 13 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) |
| reference-semantics/semantics/set.k | 16 | MPY-SET | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/set.k | 18 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq) |
| reference-semantics/semantics/set.k | 19 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC |
| reference-semantics/semantics/set.k | 20 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC) |
| reference-semantics/semantics/set.k | 22 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC) |
| reference-semantics/semantics/set.k | 25 | MPY-SET | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= snocCode(IntSeq, Int) [function, total] |
| reference-semantics/semantics/set.k | 26 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq) |
| reference-semantics/semantics/set.k | 27 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) |
| reference-semantics/semantics/set.k | 31 | MPY-SET | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/set.k | 32 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule subsetCodes(.IntSeq, _:IntSeq) => true |
| reference-semantics/semantics/set.k | 33 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B) |
| reference-semantics/semantics/set.k | 35 | MPY-SET | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/set.k | 36 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) |
| reference-semantics/semantics/set.k | 39 | MPY-SET | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B) |
| reference-semantics/semantics/set.k | 40 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/sort.k | 10 | MPY-SORT | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-SORT |
| reference-semantics/semantics/sort.k | 11 | MPY-SORT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-BUILTINS |
| reference-semantics/semantics/sort.k | 12 | MPY-SORT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-SUBSCRIPT |
| reference-semantics/semantics/sort.k | 18 | MPY-SORT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators] |
| reference-semantics/semantics/sort.k | 19 | MPY-SORT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= insVS(Int, ValSeq) [function] |
| reference-semantics/semantics/sort.k | 20 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule sortVS(.ValSeq) => .ValSeq [concrete] |
| reference-semantics/semantics/sort.k | 21 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete] |
| reference-semantics/semantics/sort.k | 22 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete] |
| reference-semantics/semantics/sort.k | 23 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete] |
| reference-semantics/semantics/sort.k | 24 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] |
| reference-semantics/semantics/sort.k | 26 | MPY-SORT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function] |
| reference-semantics/semantics/sort.k | 27 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete] |
| reference-semantics/semantics/sort.k | 28 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete] |
| reference-semantics/semantics/sort.k | 29 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete] |
| reference-semantics/semantics/sort.k | 31 | MPY-SORT | rule | concrete | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] |
| reference-semantics/semantics/sort.k | 36 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> |
| reference-semantics/semantics/sort.k | 40 | MPY-SORT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] |
| reference-semantics/semantics/sort.k | 49 | MPY-SORT | syntax | function,total,symbol,no-evaluators | FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE | syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators] |
| reference-semantics/semantics/sort.k | 51 | MPY-SORT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total] |
| reference-semantics/semantics/sort.k | 53 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq) |
| reference-semantics/semantics/sort.k | 54 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule revVSAcc(.ValSeq, A:ValSeq) => A |
| reference-semantics/semantics/sort.k | 55 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A)) |
| reference-semantics/semantics/sort.k | 57 | MPY-SORT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= condRev(ValSeq, Bool) [function, total] |
| reference-semantics/semantics/sort.k | 58 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule condRev(S:ValSeq, false) => S |
| reference-semantics/semantics/sort.k | 59 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule condRev(S:ValSeq, true) => revVS(S) |
| reference-semantics/semantics/sort.k | 61 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k> |
| reference-semantics/semantics/sort.k | 63 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k> |
| reference-semantics/semantics/sort.k | 65 | MPY-SORT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> |
| reference-semantics/semantics/sort.k | 72 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/str.k | 3 | MPY-STR | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-STR |
| reference-semantics/semantics/str.k | 4 | MPY-STR | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/str.k | 5 | MPY-STR | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-ITER |
| reference-semantics/semantics/str.k | 8 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k> |
| reference-semantics/semantics/str.k | 9 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> |
| reference-semantics/semantics/str.k | 13 | MPY-STR | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= strToCodes(String) [function] |
| reference-semantics/semantics/str.k | 14 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Str(S:String) => str(strToCodes(S)) ... </k> |
| reference-semantics/semantics/str.k | 15 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strToCodes("") => .IntSeq |
| reference-semantics/semantics/str.k | 16 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 |
| reference-semantics/semantics/str.k | 20 | MPY-STR | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/str.k | 21 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule seqConcat(.IntSeq, T:IntSeq) => T |
| reference-semantics/semantics/str.k | 22 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T)) |
| reference-semantics/semantics/str.k | 24 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B)) |
| reference-semantics/semantics/str.k | 25 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B |
| reference-semantics/semantics/str.k | 26 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) |
| reference-semantics/semantics/str.k | 29 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X) |
| reference-semantics/semantics/str.k | 30 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X) |
| reference-semantics/semantics/str.k | 32 | MPY-STR | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/str.k | 33 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strPrefix(.IntSeq, _:IntSeq) => true |
| reference-semantics/semantics/str.k | 34 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| reference-semantics/semantics/str.k | 35 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs) |
| reference-semantics/semantics/str.k | 37 | MPY-STR | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= strContains(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/str.k | 38 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X) |
| reference-semantics/semantics/str.k | 39 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq) |
| reference-semantics/semantics/str.k | 40 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) |
| reference-semantics/semantics/str.k | 48 | MPY-STR | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Bool ::= strLt(IntSeq, IntSeq) [function, total] |
| reference-semantics/semantics/str.k | 49 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strLt(.IntSeq, .IntSeq) => false |
| reference-semantics/semantics/str.k | 50 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true |
| reference-semantics/semantics/str.k | 51 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| reference-semantics/semantics/str.k | 52 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B |
| reference-semantics/semantics/str.k | 53 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B |
| reference-semantics/semantics/str.k | 54 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B |
| reference-semantics/semantics/str.k | 56 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| reference-semantics/semantics/str.k | 57 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A) |
| reference-semantics/semantics/str.k | 58 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A) |
| reference-semantics/semantics/str.k | 59 | MPY-STR | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B) |
| reference-semantics/semantics/str.k | 60 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/subscript.k | 3 | MPY-SUBSCRIPT | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-SUBSCRIPT |
| reference-semantics/semantics/subscript.k | 4 | MPY-SUBSCRIPT | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/subscript.k | 11 | MPY-SUBSCRIPT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= valSeqAt(ValSeq, Int) [function, total] |
| reference-semantics/semantics/subscript.k | 12 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V |
| reference-semantics/semantics/subscript.k | 13 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0 |
| reference-semantics/semantics/subscript.k | 16 | MPY-SUBSCRIPT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= intSeqAt(IntSeq, Int) [function] |
| reference-semantics/semantics/subscript.k | 17 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C |
| reference-semantics/semantics/subscript.k | 18 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0 |
| reference-semantics/semantics/subscript.k | 21 | MPY-SUBSCRIPT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= normIdx(Int, Int) [function, total] |
| reference-semantics/semantics/subscript.k | 22 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0 |
| reference-semantics/semantics/subscript.k | 23 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule normIdx(I:Int, _:Int) => I requires I >=Int 0 |
| reference-semantics/semantics/subscript.k | 27 | MPY-SUBSCRIPT | context | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | context Subscript(HOLE, _) |
| reference-semantics/semantics/subscript.k | 28 | MPY-SUBSCRIPT | context | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | context Subscript(_:Val, HOLE:Expr) |
| reference-semantics/semantics/subscript.k | 31 | MPY-SUBSCRIPT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/subscript.k | 35 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k> |
| reference-semantics/semantics/subscript.k | 37 | MPY-SUBSCRIPT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= applyIndex(Val, Int) [function] |
| reference-semantics/semantics/subscript.k | 38 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| reference-semantics/semantics/subscript.k | 39 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| reference-semantics/semantics/subscript.k | 40 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) |
| reference-semantics/semantics/subscript.k | 44 | MPY-SUBSCRIPT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt) |
| reference-semantics/semantics/subscript.k | 49 | MPY-SUBSCRIPT | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax OptInt ::= "noB" \| someB(Int) |
| reference-semantics/semantics/subscript.k | 50 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #evalB(NoBound) => noB ... </k> |
| reference-semantics/semantics/subscript.k | 51 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #evalB(E:Expr) => E ~> #toSome ... </k> |
| reference-semantics/semantics/subscript.k | 52 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> I:Int ~> #toSome => someB(I) ... </k> |
| reference-semantics/semantics/subscript.k | 54 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k> |
| reference-semantics/semantics/subscript.k | 55 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k> |
| reference-semantics/semantics/subscript.k | 56 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> |
| reference-semantics/semantics/subscript.k | 58 | MPY-SUBSCRIPT | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)] |
| reference-semantics/semantics/subscript.k | 61 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k> |
| reference-semantics/semantics/subscript.k | 63 | MPY-SUBSCRIPT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function] |
| reference-semantics/semantics/subscript.k | 64 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| reference-semantics/semantics/subscript.k | 66 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| reference-semantics/semantics/subscript.k | 68 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) |
| reference-semantics/semantics/subscript.k | 72 | MPY-SUBSCRIPT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= slStep(OptInt) [function, total] |
| reference-semantics/semantics/subscript.k | 73 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStep(noB) => 1 |
| reference-semantics/semantics/subscript.k | 74 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStep(someB(S:Int)) => S |
| reference-semantics/semantics/subscript.k | 76 | MPY-SUBSCRIPT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= slStart(OptInt, OptInt, Int) [function] |
| reference-semantics/semantics/subscript.k | 77 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0 |
| reference-semantics/semantics/subscript.k | 79 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0 |
| reference-semantics/semantics/subscript.k | 81 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST)) |
| reference-semantics/semantics/subscript.k | 83 | MPY-SUBSCRIPT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= slStop(OptInt, OptInt, Int) [function] |
| reference-semantics/semantics/subscript.k | 84 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0 |
| reference-semantics/semantics/subscript.k | 86 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0 |
| reference-semantics/semantics/subscript.k | 88 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST)) |
| reference-semantics/semantics/subscript.k | 90 | MPY-SUBSCRIPT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= slAdjust(Int, Int, Int) [function, total] |
| reference-semantics/semantics/subscript.k | 91 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0 |
| reference-semantics/semantics/subscript.k | 93 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0 |
| reference-semantics/semantics/subscript.k | 96 | MPY-SUBSCRIPT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= clampLo(Int, Int) [function, total] |
| reference-semantics/semantics/subscript.k | 97 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0 |
| reference-semantics/semantics/subscript.k | 99 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0 |
| reference-semantics/semantics/subscript.k | 102 | MPY-SUBSCRIPT | syntax | function,total | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= clampHi(Int, Int, Int) [function, total] |
| reference-semantics/semantics/subscript.k | 103 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN |
| reference-semantics/semantics/subscript.k | 105 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN |
| reference-semantics/semantics/subscript.k | 109 | MPY-SUBSCRIPT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function] |
| reference-semantics/semantics/subscript.k | 110 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| reference-semantics/semantics/subscript.k | 113 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| reference-semantics/semantics/subscript.k | 116 | MPY-SUBSCRIPT | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function] |
| reference-semantics/semantics/subscript.k | 117 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| reference-semantics/semantics/subscript.k | 120 | MPY-SUBSCRIPT | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| reference-semantics/semantics/subscript.k | 122 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics/syntax.k | 3 | MPY-SYNTAX | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-SYNTAX |
| reference-semantics/semantics/syntax.k | 4 | MPY-SYNTAX | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports INT-SYNTAX |
| reference-semantics/semantics/syntax.k | 5 | MPY-SYNTAX | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports FLOAT-SYNTAX |
| reference-semantics/semantics/syntax.k | 6 | MPY-SYNTAX | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports BOOL-SYNTAX |
| reference-semantics/semantics/syntax.k | 7 | MPY-SYNTAX | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports STRING-SYNTAX |
| reference-semantics/semantics/syntax.k | 9 | MPY-SYNTAX | syntax | macro,strict,seqstrict | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors "… |
| reference-semantics/semantics/syntax.k | 32 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" |
| reference-semantics/semantics/syntax.k | 33 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Entry ::= "Entry" "(" Expr "," Expr ")" |
| reference-semantics/semantics/syntax.k | 34 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Entries ::= List{Entry, ","} |
| reference-semantics/semantics/syntax.k | 35 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")" |
| reference-semantics/semantics/syntax.k | 36 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax CompFors ::= List{CompFor, ""} |
| reference-semantics/semantics/syntax.k | 37 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Exprs ::= List{Expr, ","} |
| reference-semantics/semantics/syntax.k | 38 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")" |
| reference-semantics/semantics/syntax.k | 39 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Bound ::= Expr \| "NoBound" |
| reference-semantics/semantics/syntax.k | 41 | MPY-SYNTAX | syntax | strict | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [str… |
| reference-semantics/semantics/syntax.k | 56 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Stmts ::= List{Stmt, ""} |
| reference-semantics/semantics/syntax.k | 57 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Params ::= "Params" "(" ParamNames ")" |
| reference-semantics/semantics/syntax.k | 58 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax CellVars ::= "CellVars" "(" ParamNames ")" |
| reference-semantics/semantics/syntax.k | 59 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax FreeVars ::= "FreeVars" "(" ParamNames ")" |
| reference-semantics/semantics/syntax.k | 60 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax ParamNames ::= List{String, ","} |
| reference-semantics/semantics/syntax.k | 61 | MPY-SYNTAX | syntax | - | FIXED_MATERIAL_SYNTAX_REVIEWED | syntax Module ::= "Module" "(" Stmts ")" |
| reference-semantics/semantics/syntax.k | 62 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics/tuple.k | 3 | MPY-TUPLE | module | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | module MPY-TUPLE |
| reference-semantics/semantics/tuple.k | 4 | MPY-TUPLE | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-CORE |
| reference-semantics/semantics/tuple.k | 5 | MPY-TUPLE | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-ITER |
| reference-semantics/semantics/tuple.k | 6 | MPY-TUPLE | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-LIST |
| reference-semantics/semantics/tuple.k | 7 | MPY-TUPLE | imports | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | imports MPY-METHODS |
| reference-semantics/semantics/tuple.k | 10 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k> |
| reference-semantics/semantics/tuple.k | 11 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> |
| reference-semantics/semantics/tuple.k | 14 | MPY-TUPLE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax ApplyK ::= "toTuple" |
| reference-semantics/semantics/tuple.k | 15 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k> |
| reference-semantics/semantics/tuple.k | 16 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k> |
| reference-semantics/semantics/tuple.k | 18 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B |
| reference-semantics/semantics/tuple.k | 20 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k> |
| reference-semantics/semantics/tuple.k | 21 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> |
| reference-semantics/semantics/tuple.k | 23 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0) |
| reference-semantics/semantics/tuple.k | 24 | MPY-TUPLE | syntax | function | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax Int ::= idxOfVS(ValSeq, Val, Int) [function] |
| reference-semantics/semantics/tuple.k | 25 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V |
| reference-semantics/semantics/tuple.k | 26 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V) |
| reference-semantics/semantics/tuple.k | 28 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) |
| reference-semantics/semantics/tuple.k | 31 | MPY-TUPLE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #bindTgt(Expr, Val) |
| reference-semantics/semantics/tuple.k | 32 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| reference-semantics/semantics/tuple.k | 35 | MPY-TUPLE | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| reference-semantics/semantics/tuple.k | 42 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| reference-semantics/semantics/tuple.k | 43 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| reference-semantics/semantics/tuple.k | 44 | MPY-TUPLE | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/tuple.k | 49 | MPY-TUPLE | syntax | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | syntax KItem ::= #unpackSeq(Exprs, ValSeq) |
| reference-semantics/semantics/tuple.k | 50 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| reference-semantics/semantics/tuple.k | 51 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| reference-semantics/semantics/tuple.k | 52 | MPY-TUPLE | rule | priority | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| reference-semantics/semantics/tuple.k | 55 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k> |
| reference-semantics/semantics/tuple.k | 57 | MPY-TUPLE | rule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k> |
| reference-semantics/semantics/tuple.k | 58 | - | endmodule | - | FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE | endmodule |
| reference-semantics/semantics.k | 34 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/syntax.k" |
| reference-semantics/semantics.k | 35 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/core.k" |
| reference-semantics/semantics.k | 36 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/iter.k" |
| reference-semantics/semantics.k | 37 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/range.k" |
| reference-semantics/semantics.k | 38 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/operators.k" |
| reference-semantics/semantics.k | 39 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/int.k" |
| reference-semantics/semantics.k | 40 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/bool.k" |
| reference-semantics/semantics.k | 41 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/float.k" |
| reference-semantics/semantics.k | 42 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/str.k" |
| reference-semantics/semantics.k | 43 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/set.k" |
| reference-semantics/semantics.k | 44 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/list.k" |
| reference-semantics/semantics.k | 45 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/tuple.k" |
| reference-semantics/semantics.k | 46 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/subscript.k" |
| reference-semantics/semantics.k | 47 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/comprehension.k" |
| reference-semantics/semantics.k | 48 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/methods.k" |
| reference-semantics/semantics.k | 49 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/controls.k" |
| reference-semantics/semantics.k | 50 | - | requires | function | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/functions.k" |
| reference-semantics/semantics.k | 51 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/builtins.k" |
| reference-semantics/semantics.k | 52 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/call.k" |
| reference-semantics/semantics.k | 53 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/sort.k" |
| reference-semantics/semantics.k | 54 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/assert.k" |
| reference-semantics/semantics.k | 55 | - | requires | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/dict.k" |
| reference-semantics/semantics.k | 56 | - | requires | concrete | FIXED_MATERIAL_STRUCTURE_REVIEWED | requires "semantics/concrete.k" |
| reference-semantics/semantics.k | 58 | MPY | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY |
| reference-semantics/semantics.k | 59 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CORE |
| reference-semantics/semantics.k | 60 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-ITER |
| reference-semantics/semantics.k | 61 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-RANGE |
| reference-semantics/semantics.k | 62 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-OPERATORS |
| reference-semantics/semantics.k | 63 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-INT |
| reference-semantics/semantics.k | 64 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-BOOL |
| reference-semantics/semantics.k | 65 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-FLOAT |
| reference-semantics/semantics.k | 66 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-STR |
| reference-semantics/semantics.k | 67 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-SET |
| reference-semantics/semantics.k | 68 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-LIST |
| reference-semantics/semantics.k | 69 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-TUPLE |
| reference-semantics/semantics.k | 70 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-SUBSCRIPT |
| reference-semantics/semantics.k | 71 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-COMPREHENSION |
| reference-semantics/semantics.k | 72 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-METHODS |
| reference-semantics/semantics.k | 73 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CONTROLS |
| reference-semantics/semantics.k | 74 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-FUNCTIONS |
| reference-semantics/semantics.k | 75 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-BUILTINS |
| reference-semantics/semantics.k | 76 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CALL |
| reference-semantics/semantics.k | 77 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-SORT |
| reference-semantics/semantics.k | 78 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-ASSERT |
| reference-semantics/semantics.k | 79 | MPY | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-DICT |
| reference-semantics/semantics.k | 80 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| reference-semantics/semantics.k | 87 | MPY-KRUN | module | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | module MPY-KRUN |
| reference-semantics/semantics.k | 88 | MPY-KRUN | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY |
| reference-semantics/semantics.k | 89 | MPY-KRUN | imports | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | imports MPY-CONCRETE |
| reference-semantics/semantics.k | 90 | - | endmodule | - | FIXED_MATERIAL_STRUCTURE_REVIEWED | endmodule |
| verification.k | 1 | - | requires | - | CANDIDATE_STRUCTURE_OK | requires "reference-semantics/semantics.k" |
| verification.k | 3 | VERIFICATION-SYNTAX | module | - | CANDIDATE_STRUCTURE_OK | module VERIFICATION-SYNTAX |
| verification.k | 4 | VERIFICATION-SYNTAX | imports | - | CANDIDATE_STRUCTURE_OK | imports MPY-SYNTAX |
| verification.k | 5 | VERIFICATION-SYNTAX | imports | - | CANDIDATE_STRUCTURE_OK | imports BOOL |
| verification.k | 6 | VERIFICATION-SYNTAX | imports | - | CANDIDATE_STRUCTURE_OK | imports INT |
| verification.k | 10 | VERIFICATION-SYNTAX | syntax | function,total | CANDIDATE_MACRO_OR_SUMMARY_DECL_SOUND | syntax Bool ::= noDivisors(Int, Int) [function, total] |
| verification.k | 14 | VERIFICATION-SYNTAX | syntax | function,total | CANDIDATE_MACRO_OR_SUMMARY_DECL_SOUND | syntax ValSeq ::= primesBetween(Int, Int) [function, total] \| primesBelow(Int) [function, total] |
| verification.k | 19 | VERIFICATION-SYNTAX | syntax | macro | CANDIDATE_MACRO_OR_SUMMARY_DECL_SOUND | syntax Stmts ::= "innerBody" [macro] \| "outerBody" [macro] \| "countBody" [macro] \| "countBodyStart3" [macro] |
| verification.k | 24 | VERIFICATION-SYNTAX | rule | - | CANDIDATE_MACRO_EXPANSION_SOUND | rule innerBody => If(Compare(BinOp("%", Name("candidate"), Name("divisor")), CmpOp("==", Int(0))), Assign(Name("prime"), Bool(false)) .Stmts, .Stmts) Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))) .Stmts |
| verification.k | 32 | VERIFICATION-SYNTAX | rule | - | CANDIDATE_MACRO_EXPANSION_SOUND | rule outerBody => Assign(Name("divisor"), Int(2)) Assign(Name("prime"), Bool(true)) While(Compare(Name("divisor"), CmpOp("<", Name("candidate"))), innerBody) If(Name("prime"), Expr(Call(Attribute(Name("primes"), "append"), Name("candidate"))) .Stmts, .Stmts) Assign(Name("candidate"), BinOp("+", Name("candidate"), Int(1))) .Stmts |
| verification.k | 44 | VERIFICATION-SYNTAX | rule | - | CANDIDATE_MACRO_EXPANSION_SOUND | rule countBody => If(Compare(Name("n"), CmpOp("<=", Int(2))), Return(ListExpr(.Exprs)) .Stmts, .Stmts) Assign(Name("primes"), ListExpr(.Exprs)) Assign(Name("candidate"), Int(2)) Assign(Name("divisor"), Int(2)) Assign(Name("prime"), Bool(true)) While(Compare(Name("candidate"), CmpOp("<", Name("n"))), outerBody) Return(Name("primes")) .Stmts |
| verification.k | 57 | VERIFICATION-SYNTAX | rule | - | CANDIDATE_MACRO_EXPANSION_SOUND | rule countBodyStart3 => If(Compare(Name("n"), CmpOp("<=", Int(2))), Return(ListExpr(.Exprs)) .Stmts, .Stmts) Assign(Name("primes"), ListExpr(.Exprs)) Assign(Name("candidate"), Int(3)) Assign(Name("divisor"), Int(2)) Assign(Name("prime"), Bool(true)) While(Compare(Name("candidate"), CmpOp("<", Name("n"))), outerBody) Return(Name("primes")) .Stmts |
| verification.k | 68 | - | endmodule | - | CANDIDATE_STRUCTURE_OK | endmodule |
| verification.k | 70 | VERIFICATION | module | - | CANDIDATE_STRUCTURE_OK | module VERIFICATION |
| verification.k | 71 | VERIFICATION | imports | - | CANDIDATE_STRUCTURE_OK | imports MPY |
| verification.k | 72 | VERIFICATION | imports | - | CANDIDATE_STRUCTURE_OK | imports VERIFICATION-SYNTAX |
| verification.k | 73 | VERIFICATION | imports | - | CANDIDATE_STRUCTURE_OK | imports BOOL |
| verification.k | 74 | VERIFICATION | imports | - | CANDIDATE_STRUCTURE_OK | imports INT |
| verification.k | 76 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule noDivisors(N, D) => noDivisors(N, 2) requires D <Int 2 |
| verification.k | 78 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule noDivisors(N, D) => true requires D >=Int 2 andBool D >=Int N |
| verification.k | 80 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule noDivisors(N, D) => false requires D >=Int 2 andBool D <Int N andBool pyMod(N, D) ==Int 0 |
| verification.k | 83 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule noDivisors(N, D) => noDivisors(N, D +Int 1) requires D >=Int 2 andBool D <Int N andBool pyMod(N, D) =/=Int 0 |
| verification.k | 87 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule primesBetween(C, N) => .ValSeq requires C >=Int N |
| verification.k | 89 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule primesBetween(C, N) => primesBetween(C +Int 1, N) requires C <Int N andBool C <Int 2 |
| verification.k | 92 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule primesBetween(C, N) => vCons(C, primesBetween(C +Int 1, N)) requires C <Int N andBool C >=Int 2 andBool noDivisors(C, 2) |
| verification.k | 96 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule primesBetween(C, N) => primesBetween(C +Int 1, N) requires C <Int N andBool C >=Int 2 andBool notBool noDivisors(C, 2) |
| verification.k | 101 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule primesBelow(N) => .ValSeq requires N <=Int 2 |
| verification.k | 103 | VERIFICATION | rule | - | CANDIDATE_SUMMARY_EQUATION_SOUND | rule primesBelow(N) => primesBetween(2, N) requires N >Int 2 |
| verification.k | 109 | VERIFICATION | rule | simplification | CANDIDATE_DERIVED_LIST_LEMMA_SOUND | rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq) => valSeqConcat(A, valSeqConcat(B, C)) [simplification] |
| verification.k | 112 | VERIFICATION | rule | simplification | CANDIDATE_DERIVED_LIST_LEMMA_SOUND | rule valSeqConcat(A:ValSeq, .ValSeq) => A [simplification] |
| verification.k | 114 | - | endmodule | - | CANDIDATE_STRUCTURE_OK | endmodule |
| spec.k | 1 | - | requires | - | SPEC_STRUCTURE_OK | requires "verification.k" |
| spec.k | 3 | SPEC | module | - | SPEC_STRUCTURE_OK | module SPEC |
| spec.k | 4 | SPEC | imports | - | SPEC_STRUCTURE_OK | imports VERIFICATION |
| spec.k | 8 | SPEC | claim | - | POSITIVE_CLAIM_FRESHLY_MACHINE_CHECKED | claim [inner-loop]: <k> #while(Compare(Name("divisor"), CmpOp("<", Name("candidate"))), innerBody) => .K ... </k> <env> 1 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope(M0:Map, parent(-1)) 1 \|-> scope( "candidate" \|-> C:Int "divisor" \|-> (D:Int => C) "n" \|-> N:Int "prime" \|-> (B:Bool => ?PB:Bool) "primes" \|-> ref(H:Int), parent(0)) </scopes> <scopeLoc> 2 </scopeLoc> <heap> H \|-> list(P:ValSeq) </heap> <hea… |
| spec.k | 40 | SPEC | claim | - | POSITIVE_CLAIM_FRESHLY_MACHINE_CHECKED | claim [outer-loop]: <k> #while(Compare(Name("candidate"), CmpOp("<", Name("n"))), outerBody) => .K ... </k> <env> 1 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope(M0:Map, parent(-1)) 1 \|-> scope( "candidate" \|-> (C:Int => N:Int) "divisor" \|-> (D:Int => N -Int 1) "n" \|-> N "prime" \|-> (B:Bool => ?PF:Bool) "primes" \|-> ref(H:Int), parent(0)) </scopes> <scopeLoc> 2 </scopeLoc> <heap> H \|-> list(P:ValSeq => va… |
| spec.k | 73 | SPEC | claim | - | POSITIVE_CLAIM_FRESHLY_MACHINE_CHECKED | claim [count-up-to]: <k> FuncDef("count_up_to", Params("n"), countBody) ~> Call(Name("count_up_to"), (N:Int, .Exprs)) => ref(0) </k> <env> 0 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope(.Map => "count_up_to" \|-> closureVal(("n", .ParamNames), countBody, 0), parent(-1)) </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map => 0 \|-> list(primesBelow(N)) </heap> <heapLoc> 0 => 1 </heapLoc> <stack> .List </stack> <ret> … |
| spec.k | 95 | - | endmodule | - | SPEC_STRUCTURE_OK | endmodule |

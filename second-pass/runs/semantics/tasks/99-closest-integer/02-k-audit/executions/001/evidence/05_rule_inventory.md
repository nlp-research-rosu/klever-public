# Exhaustive K declaration and rule inventory

This inventory is mechanically extracted from the fresh scratch copy. Every top-level `requires`, module/import, configuration, syntax block, context, rule, and claim is listed. The exact unabridged records are also available in `05_rule_inventory.json`.

Total records: 1102

Kinds: `{"claim": 1, "configuration": 1, "context": 5, "endmodule": 27, "imports": 88, "module": 27, "requires": 25, "rule": 698, "syntax": 230}`

Decision counts:

- `PROOF_LOCAL_COPIED_BODY: exact current syntax, but no formal source dependency`: 1
- `PROOF_LOCAL_DECLARATION_REVIEWED`: 7
- `PROOF_LOCAL_IDENTITY_GAP: wrapper executes copied closestBody, not solution.mpy`: 1
- `PROOF_LOCAL_STRUCTURAL_SPEC: truthful equation, but not an independent nearest-integer theorem`: 1
- `SPEC_DECLARATION_REVIEWED`: 4
- `TARGET_CLAIM: closes structurally; fails real-program pinning and intent adequacy`: 1
- `UNUSED_FIXED_SUPPLIED_CONCRETE_RULE`: 28
- `UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY`: 16
- `UNUSED_FIXED_SUPPLIED_PRIORITY_RULE`: 41
- `UNUSED_FIXED_SUPPLIED_SEMANTICS`: 817
- `USED_FIXED_SUPPLIED_CONCRETE_RULE`: 7
- `USED_FIXED_SUPPLIED_OPAQUE_BOUNDARY`: 6
- `USED_FIXED_SUPPLIED_PRIORITY_RULE`: 4
- `USED_FIXED_SUPPLIED_SEMANTICS`: 168

| ID | Source | Lines | Kind | Attributes | Slice | Decision | Declaration/rule |
|---:|---|---:|---|---|---|---|---|
| 1 | `reference-semantics/semantics/assert.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-ASSERT |
| 2 | `reference-semantics/semantics/assert.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 3 | `reference-semantics/semantics/assert.k` | 6-7 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Assert(V:Val) =&gt; .K ... &lt;/k&gt; requires truthy(V) |
| 4 | `reference-semantics/semantics/assert.k` | 8-11 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Assert(V:Val) ~&gt; _ =&gt; .K &lt;/k&gt; &lt;exc&gt; NoExc =&gt; AssertionError &lt;/exc&gt; &lt;exit-code&gt; _ =&gt; 1 &lt;/exit-code&gt; requires notBool truthy(V) |
| 5 | `reference-semantics/semantics/assert.k` | 13-15 | `rule` | priority(40) | yes | USED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Assert(ref(H:Int)) =&gt; Assert(V) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 6 | `reference-semantics/semantics/assert.k` | 16-16 | `endmodule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 7 | `reference-semantics/semantics/bool.k` | 5-5 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-BOOL |
| 8 | `reference-semantics/semantics/bool.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 9 | `reference-semantics/semantics/bool.k` | 8-8 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyUn("not", V:Val) =&gt; notBool truthy(V) |
| 10 | `reference-semantics/semantics/bool.k` | 10-10 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", B1:Bool, B2:Bool) =&gt; B1 ==Bool B2 |
| 11 | `reference-semantics/semantics/bool.k` | 11-11 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", B1:Bool, B2:Bool) =&gt; B1 =/=Bool B2 |
| 12 | `reference-semantics/semantics/bool.k` | 16-16 | `context` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | context BoolOp(_, (HOLE:Expr, _:Exprs)) |
| 13 | `reference-semantics/semantics/bool.k` | 17-17 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; BoolOp(_:String, (V:Val, .Exprs)) =&gt; V ... &lt;/k&gt; |
| 14 | `reference-semantics/semantics/bool.k` | 18-19 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; BoolOp("and", (V:Val, A:Expr, REST:Exprs)) =&gt; BoolOp("and", (A, REST)) ... &lt;/k&gt; requires truthy(V) |
| 15 | `reference-semantics/semantics/bool.k` | 20-21 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; BoolOp("and", (V:Val, _:Expr, _:Exprs)) =&gt; V ... &lt;/k&gt; requires notBool truthy(V) |
| 16 | `reference-semantics/semantics/bool.k` | 22-23 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; BoolOp("or",  (V:Val, _:Expr, _:Exprs)) =&gt; V ... &lt;/k&gt; requires truthy(V) |
| 17 | `reference-semantics/semantics/bool.k` | 24-25 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) =&gt; BoolOp("or", (A, REST)) ... &lt;/k&gt; requires notBool truthy(V) |
| 18 | `reference-semantics/semantics/bool.k` | 29-30 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BoolOp(_:String, (ref(H:Int), .Exprs)) =&gt; ref(H) ... &lt;/k&gt; [priority(40)] |
| 19 | `reference-semantics/semantics/bool.k` | 31-34 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) =&gt; BoolOp("and", (A, REST)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires truthy(V) [priority(40)] |
| 20 | `reference-semantics/semantics/bool.k` | 35-38 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) =&gt; ref(H) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires notBool truthy(V) [priority(40)] |
| 21 | `reference-semantics/semantics/bool.k` | 39-42 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) =&gt; ref(H) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires truthy(V) [priority(40)] |
| 22 | `reference-semantics/semantics/bool.k` | 43-46 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) =&gt; BoolOp("or", (A, REST)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires notBool truthy(V) [priority(40)] |
| 23 | `reference-semantics/semantics/bool.k` | 47-47 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 24 | `reference-semantics/semantics/builtins.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-BUILTINS |
| 25 | `reference-semantics/semantics/builtins.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 26 | `reference-semantics/semantics/builtins.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-STR |
| 27 | `reference-semantics/semantics/builtins.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-SET |
| 28 | `reference-semantics/semantics/builtins.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 29 | `reference-semantics/semantics/builtins.k` | 8-8 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-RANGE |
| 30 | `reference-semantics/semantics/builtins.k` | 9-9 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-INT |
| 31 | `reference-semantics/semantics/builtins.k` | 10-10 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-METHODS |
| 32 | `reference-semantics/semantics/builtins.k` | 17-17 | `syntax` | function | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= applyBuiltin(String, Vals) [function] |
| 33 | `reference-semantics/semantics/builtins.k` | 20-20 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= seqLen(Val) [function] |
| 34 | `reference-semantics/semantics/builtins.k` | 21-21 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("len", OBJ:Val, .Vals) =&gt; seqLen(OBJ) |
| 35 | `reference-semantics/semantics/builtins.k` | 22-22 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule seqLen(list(VS:ValSeq))                  =&gt; vsLen(VS) |
| 36 | `reference-semantics/semantics/builtins.k` | 23-23 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule seqLen(tuple(VS:ValSeq))                 =&gt; vsLen(VS) |
| 37 | `reference-semantics/semantics/builtins.k` | 24-24 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule seqLen(str(IS:IntSeq))                   =&gt; isLen(IS) |
| 38 | `reference-semantics/semantics/builtins.k` | 25-25 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule seqLen(setV(DS:IntSeq))                  =&gt; isLen(DS) |
| 39 | `reference-semantics/semantics/builtins.k` | 26-26 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) =&gt; rangeLen(LO, HI, ST) |
| 40 | `reference-semantics/semantics/builtins.k` | 32-32 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) =&gt; #alloc(list(VS)) ... &lt;/k&gt; |
| 41 | `reference-semantics/semantics/builtins.k` | 33-33 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) =&gt; #alloc(list(VS)) ... &lt;/k&gt; |
| 42 | `reference-semantics/semantics/builtins.k` | 34-34 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("list")), .Vals)                     =&gt; #alloc(list(.ValSeq)) ... &lt;/k&gt; |
| 43 | `reference-semantics/semantics/builtins.k` | 35-35 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   =&gt; #alloc(list(charsOf(CS))) ... &lt;/k&gt; |
| 44 | `reference-semantics/semantics/builtins.k` | 36-36 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= charsOf(IntSeq) [function, total] |
| 45 | `reference-semantics/semantics/builtins.k` | 37-37 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule charsOf(.IntSeq)                =&gt; .ValSeq |
| 46 | `reference-semantics/semantics/builtins.k` | 38-38 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule charsOf(iCons(C:Int, R:IntSeq)) =&gt; vCons(str(iCons(C, .IntSeq)), charsOf(R)) |
| 47 | `reference-semantics/semantics/builtins.k` | 41-41 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("set", str(CS:IntSeq), .Vals) =&gt; setV(dedupCodes(CS)) |
| 48 | `reference-semantics/semantics/builtins.k` | 44-44 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("abs", I:Int, .Vals) =&gt; absInt(I) |
| 49 | `reference-semantics/semantics/builtins.k` | 47-47 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #sumAcc(Iterable, Int) &#124; #sumCont(Int) |
| 50 | `reference-semantics/semantics/builtins.k` | 48-48 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #sumAcc(IT:Iterable, ACC:Int) =&gt; #iterNext(IT) ~&gt; #sumCont(ACC) ... &lt;/k&gt; |
| 51 | `reference-semantics/semantics/builtins.k` | 49-49 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #sumCont(ACC:Int) =&gt; ACC ... &lt;/k&gt; |
| 52 | `reference-semantics/semantics/builtins.k` | 50-52 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #sumCont(ACC:Int) =&gt; #sumAcc(R, ACC +Int intOf(V)) ... &lt;/k&gt; requires isInt(V) orBool isBool(V) |
| 53 | `reference-semantics/semantics/builtins.k` | 54-54 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= intOf(Val) [function] |
| 54 | `reference-semantics/semantics/builtins.k` | 55-55 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule intOf(I:Int)  =&gt; I |
| 55 | `reference-semantics/semantics/builtins.k` | 56-56 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule intOf(B:Bool) =&gt; #if B #then 1 #else 0 #fi |
| 56 | `reference-semantics/semantics/builtins.k` | 59-59 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #allAcc(Iterable) &#124; "#allCont" |
| 57 | `reference-semantics/semantics/builtins.k` | 60-60 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #allAcc(IT:Iterable) =&gt; #iterNext(IT) ~&gt; #allCont ... &lt;/k&gt; |
| 58 | `reference-semantics/semantics/builtins.k` | 61-61 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #allCont =&gt; true ... &lt;/k&gt; |
| 59 | `reference-semantics/semantics/builtins.k` | 62-63 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #allCont =&gt; #allAcc(R) ... &lt;/k&gt; requires truthy(V) |
| 60 | `reference-semantics/semantics/builtins.k` | 64-65 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, _:Iterable) ~&gt; #allCont =&gt; false ... &lt;/k&gt; requires notBool truthy(V) |
| 61 | `reference-semantics/semantics/builtins.k` | 67-67 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #anyAcc(Iterable) &#124; "#anyCont" |
| 62 | `reference-semantics/semantics/builtins.k` | 68-68 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #anyAcc(IT:Iterable) =&gt; #iterNext(IT) ~&gt; #anyCont ... &lt;/k&gt; |
| 63 | `reference-semantics/semantics/builtins.k` | 69-69 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #anyCont =&gt; false ... &lt;/k&gt; |
| 64 | `reference-semantics/semantics/builtins.k` | 70-71 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, _:Iterable) ~&gt; #anyCont =&gt; true ... &lt;/k&gt; requires truthy(V) |
| 65 | `reference-semantics/semantics/builtins.k` | 72-73 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #anyCont =&gt; #anyAcc(R) ... &lt;/k&gt; requires notBool truthy(V) |
| 66 | `reference-semantics/semantics/builtins.k` | 76-76 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #maxAcc0(Iterable) &#124; "#maxCont0" &#124; #maxAcc(Iterable, Int) &#124; #maxCont(Int) |
| 67 | `reference-semantics/semantics/builtins.k` | 77-77 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #maxAcc0(IT:Iterable) =&gt; #iterNext(IT) ~&gt; #maxCont0 ... &lt;/k&gt; |
| 68 | `reference-semantics/semantics/builtins.k` | 78-79 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #maxCont0 =&gt; #maxAcc(R, {V}:&gt;Int) ... &lt;/k&gt; requires isInt(V) |
| 69 | `reference-semantics/semantics/builtins.k` | 80-80 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #maxAcc(IT:Iterable, M:Int) =&gt; #iterNext(IT) ~&gt; #maxCont(M) ... &lt;/k&gt; |
| 70 | `reference-semantics/semantics/builtins.k` | 81-81 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #maxCont(M:Int) =&gt; M ... &lt;/k&gt; |
| 71 | `reference-semantics/semantics/builtins.k` | 82-84 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #maxCont(M:Int) =&gt; #maxAcc(R, maxInt(M, {V}:&gt;Int)) ... &lt;/k&gt; requires isInt(V) |
| 72 | `reference-semantics/semantics/builtins.k` | 86-86 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #minAcc0(Iterable) &#124; "#minCont0" &#124; #minAcc(Iterable, Int) &#124; #minCont(Int) |
| 73 | `reference-semantics/semantics/builtins.k` | 87-87 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #minAcc0(IT:Iterable) =&gt; #iterNext(IT) ~&gt; #minCont0 ... &lt;/k&gt; |
| 74 | `reference-semantics/semantics/builtins.k` | 88-89 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #minCont0 =&gt; #minAcc(R, {V}:&gt;Int) ... &lt;/k&gt; requires isInt(V) |
| 75 | `reference-semantics/semantics/builtins.k` | 90-90 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #minAcc(IT:Iterable, M:Int) =&gt; #iterNext(IT) ~&gt; #minCont(M) ... &lt;/k&gt; |
| 76 | `reference-semantics/semantics/builtins.k` | 91-91 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #minCont(M:Int) =&gt; M ... &lt;/k&gt; |
| 77 | `reference-semantics/semantics/builtins.k` | 92-94 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #minCont(M:Int) =&gt; #minAcc(R, minInt(M, {V}:&gt;Int)) ... &lt;/k&gt; requires isInt(V) |
| 78 | `reference-semantics/semantics/builtins.k` | 97-97 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= maxVals(Int, Vals) [function] |
| 79 | `reference-semantics/semantics/builtins.k` | 98-98 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("max", I:Int, REST:Vals) =&gt; maxVals(I, REST) |
| 80 | `reference-semantics/semantics/builtins.k` | 99-99 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule maxVals(M:Int, .Vals)           =&gt; M |
| 81 | `reference-semantics/semantics/builtins.k` | 100-100 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule maxVals(M:Int, (I:Int, R:Vals)) =&gt; maxVals(maxInt(M, I), R) |
| 82 | `reference-semantics/semantics/builtins.k` | 102-102 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= minVals(Int, Vals) [function] |
| 83 | `reference-semantics/semantics/builtins.k` | 103-103 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("min", I:Int, REST:Vals) =&gt; minVals(I, REST) |
| 84 | `reference-semantics/semantics/builtins.k` | 104-104 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule minVals(M:Int, .Vals)           =&gt; M |
| 85 | `reference-semantics/semantics/builtins.k` | 105-105 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule minVals(M:Int, (I:Int, R:Vals)) =&gt; minVals(minInt(M, I), R) |
| 86 | `reference-semantics/semantics/builtins.k` | 108-109 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("bin", N:Int, .Vals) =&gt; str(iCons(48, iCons(98, binCodes(N)))) requires N &gt;=Int 0 |
| 87 | `reference-semantics/semantics/builtins.k` | 111-113 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("bin", N:Int, .Vals) =&gt; str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N &lt;Int 0 |
| 88 | `reference-semantics/semantics/builtins.k` | 114-114 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= binCodes(Int) [function, total] |
| 89 | `reference-semantics/semantics/builtins.k` | 115-115 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule binCodes(0) =&gt; iCons(48, .IntSeq) |
| 90 | `reference-semantics/semantics/builtins.k` | 116-116 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule binCodes(N:Int) =&gt; binAcc(N, .IntSeq) requires N &gt;Int 0 |
| 91 | `reference-semantics/semantics/builtins.k` | 117-117 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= binAcc(Int, IntSeq) [function, total] |
| 92 | `reference-semantics/semantics/builtins.k` | 118-118 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule binAcc(0, ACC:IntSeq) =&gt; ACC |
| 93 | `reference-semantics/semantics/builtins.k` | 119-121 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule binAcc(N:Int, ACC:IntSeq) =&gt; binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N &gt;Int 0 |
| 94 | `reference-semantics/semantics/builtins.k` | 124-125 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) =&gt; #alloc(list(enumVS(VS, 0))) ... &lt;/k&gt; |
| 95 | `reference-semantics/semantics/builtins.k` | 126-126 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= enumVS(ValSeq, Int) [function, total] |
| 96 | `reference-semantics/semantics/builtins.k` | 127-127 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule enumVS(.ValSeq, _:Int) =&gt; .ValSeq |
| 97 | `reference-semantics/semantics/builtins.k` | 128-129 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule enumVS(vCons(V:Val, R:ValSeq), I:Int) =&gt; vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) |
| 98 | `reference-semantics/semantics/builtins.k` | 132-133 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) =&gt; #alloc(list(mapStrVS(VS))) ... &lt;/k&gt; |
| 99 | `reference-semantics/semantics/builtins.k` | 134-134 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= mapStrVS(ValSeq) [function, total] |
| 100 | `reference-semantics/semantics/builtins.k` | 135-135 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapStrVS(.ValSeq) =&gt; .ValSeq |
| 101 | `reference-semantics/semantics/builtins.k` | 136-136 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapStrVS(vCons(I:Int, R:ValSeq)) =&gt; vCons(str(strToCodes(Int2String(I))), mapStrVS(R)) |
| 102 | `reference-semantics/semantics/builtins.k` | 137-137 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) =&gt; vCons(str(CS), mapStrVS(R)) |
| 103 | `reference-semantics/semantics/builtins.k` | 140-140 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("int", I:Int, .Vals) =&gt; I |
| 104 | `reference-semantics/semantics/builtins.k` | 143-143 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) =&gt; C |
| 105 | `reference-semantics/semantics/builtins.k` | 144-145 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("chr", I:Int, .Vals) =&gt; str(iCons(I, .IntSeq)) requires 0 &lt;=Int I andBool I &lt;Int 128 |
| 106 | `reference-semantics/semantics/builtins.k` | 148-148 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("str", I:Int, .Vals)       =&gt; str(strToCodes(Int2String(I))) |
| 107 | `reference-semantics/semantics/builtins.k` | 149-149 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("str", str(CS:IntSeq), .Vals) =&gt; str(CS) |
| 108 | `reference-semantics/semantics/builtins.k` | 152-153 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) =&gt; C -Int 48 requires 48 &lt;=Int C andBool C &lt;=Int 57 |
| 109 | `reference-semantics/semantics/builtins.k` | 156-157 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("int", str(CS:IntSeq), .Vals) =&gt; intDigAcc(CS, 0) requires isLen(CS) &gt;=Int 2 |
| 110 | `reference-semantics/semantics/builtins.k` | 158-158 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= intDigAcc(IntSeq, Int) [function, total] |
| 111 | `reference-semantics/semantics/builtins.k` | 159-159 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule intDigAcc(.IntSeq, ACC:Int)             =&gt; ACC |
| 112 | `reference-semantics/semantics/builtins.k` | 160-160 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) =&gt; intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) |
| 113 | `reference-semantics/semantics/builtins.k` | 163-163 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) =&gt; zipObj(A, B) |
| 114 | `reference-semantics/semantics/builtins.k` | 164-164 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   =&gt; zipObjS(A, B) |
| 115 | `reference-semantics/semantics/builtins.k` | 167-168 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) =&gt; #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... &lt;/k&gt; |
| 116 | `reference-semantics/semantics/builtins.k` | 169-169 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(zipObj(.ValSeq, _:ValSeq))               =&gt; #iterDone ... &lt;/k&gt; |
| 117 | `reference-semantics/semantics/builtins.k` | 170-170 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) =&gt; #iterDone ... &lt;/k&gt; |
| 118 | `reference-semantics/semantics/builtins.k` | 171-172 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) =&gt; #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... &lt;/k&gt; |
| 119 | `reference-semantics/semantics/builtins.k` | 173-173 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(zipObjS(.IntSeq, _:IntSeq))              =&gt; #iterDone ... &lt;/k&gt; |
| 120 | `reference-semantics/semantics/builtins.k` | 174-174 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) =&gt; #iterDone ... &lt;/k&gt; |
| 121 | `reference-semantics/semantics/builtins.k` | 177-177 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("range", I:Int, .Vals)               =&gt; rangeObj(0, I, 1) |
| 122 | `reference-semantics/semantics/builtins.k` | 178-178 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("range", A:Int, B:Int, .Vals)        =&gt; rangeObj(A, B, 1) |
| 123 | `reference-semantics/semantics/builtins.k` | 179-180 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) =&gt; rangeObj(A, B, S) requires S =/=Int 0 |
| 124 | `reference-semantics/semantics/builtins.k` | 187-187 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("eval", str(CS:IntSeq), .Vals) =&gt; evalArith(CS) |
| 125 | `reference-semantics/semantics/builtins.k` | 188-188 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= evalArith(IntSeq) [function] |
| 126 | `reference-semantics/semantics/builtins.k` | 189-190 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule evalArith(CS:IntSeq) =&gt; firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS))))) |
| 127 | `reference-semantics/semantics/builtins.k` | 192-192 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax OpSeq ::= ".OpSeq" &#124; oCons(String, OpSeq) |
| 128 | `reference-semantics/semantics/builtins.k` | 194-194 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= evDigit(Int) [function, total] |
| 129 | `reference-semantics/semantics/builtins.k` | 195-195 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule evDigit(C:Int) =&gt; C &gt;=Int 48 andBool C &lt;=Int 57 |
| 130 | `reference-semantics/semantics/builtins.k` | 196-196 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= evHead42(IntSeq) [function, total] |
| 131 | `reference-semantics/semantics/builtins.k` | 197-197 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule evHead42(iCons(42, _:IntSeq)) =&gt; true |
| 132 | `reference-semantics/semantics/builtins.k` | 198-198 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule evHead42(_:IntSeq)            =&gt; false [owise] |
| 133 | `reference-semantics/semantics/builtins.k` | 199-199 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= evHead47(IntSeq) [function, total] |
| 134 | `reference-semantics/semantics/builtins.k` | 200-200 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule evHead47(iCons(47, _:IntSeq)) =&gt; true |
| 135 | `reference-semantics/semantics/builtins.k` | 201-201 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule evHead47(_:IntSeq)            =&gt; false [owise] |
| 136 | `reference-semantics/semantics/builtins.k` | 203-203 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax OpSeq ::= tokOps(IntSeq) [function, total] |
| 137 | `reference-semantics/semantics/builtins.k` | 204-204 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(.IntSeq)                 =&gt; .OpSeq |
| 138 | `reference-semantics/semantics/builtins.k` | 205-205 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(32, R:IntSeq))     =&gt; tokOps(R) |
| 139 | `reference-semantics/semantics/builtins.k` | 206-206 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(C:Int, R:IntSeq))  =&gt; tokOps(R) requires evDigit(C) |
| 140 | `reference-semantics/semantics/builtins.k` | 207-207 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(42, iCons(42, R:IntSeq))) =&gt; oCons("**", tokOps(R)) |
| 141 | `reference-semantics/semantics/builtins.k` | 208-208 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(42, R:IntSeq))     =&gt; oCons("*", tokOps(R)) requires notBool evHead42(R) |
| 142 | `reference-semantics/semantics/builtins.k` | 209-209 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(47, iCons(47, R:IntSeq))) =&gt; oCons("//", tokOps(R)) |
| 143 | `reference-semantics/semantics/builtins.k` | 210-210 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(47, R:IntSeq))     =&gt; oCons("/", tokOps(R)) requires notBool evHead47(R) |
| 144 | `reference-semantics/semantics/builtins.k` | 211-211 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(43, R:IntSeq))     =&gt; oCons("+", tokOps(R)) |
| 145 | `reference-semantics/semantics/builtins.k` | 212-212 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokOps(iCons(45, R:IntSeq))     =&gt; oCons("-", tokOps(R)) |
| 146 | `reference-semantics/semantics/builtins.k` | 214-215 | `syntax` | function, total, function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= tokNds(IntSeq) [function, total] &#124; tokNdAcc(Int, IntSeq) [function, total] |
| 147 | `reference-semantics/semantics/builtins.k` | 216-216 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokNds(.IntSeq)                =&gt; .IntSeq |
| 148 | `reference-semantics/semantics/builtins.k` | 217-217 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokNds(iCons(32, R:IntSeq))    =&gt; tokNds(R) |
| 149 | `reference-semantics/semantics/builtins.k` | 218-218 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokNds(iCons(C:Int, R:IntSeq)) =&gt; tokNdAcc(C -Int 48, R) requires evDigit(C) |
| 150 | `reference-semantics/semantics/builtins.k` | 219-220 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokNds(iCons(C:Int, R:IntSeq)) =&gt; tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32 |
| 151 | `reference-semantics/semantics/builtins.k` | 221-222 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) =&gt; tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C) |
| 152 | `reference-semantics/semantics/builtins.k` | 223-223 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule tokNdAcc(A:Int, S:IntSeq) =&gt; iCons(A, tokNds(S)) [owise] |
| 153 | `reference-semantics/semantics/builtins.k` | 225-225 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax EvPair ::= evp(OpSeq, IntSeq) |
| 154 | `reference-semantics/semantics/builtins.k` | 226-226 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= firstNdE(EvPair) [function, total] |
| 155 | `reference-semantics/semantics/builtins.k` | 227-227 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) =&gt; N |
| 156 | `reference-semantics/semantics/builtins.k` | 228-228 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule firstNdE(_:EvPair) =&gt; 0 [owise] |
| 157 | `reference-semantics/semantics/builtins.k` | 230-230 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= applyOpE(String, Int, Int) [function, total] |
| 158 | `reference-semantics/semantics/builtins.k` | 231-231 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyOpE("+",  A:Int, B:Int) =&gt; A +Int B |
| 159 | `reference-semantics/semantics/builtins.k` | 232-232 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyOpE("-",  A:Int, B:Int) =&gt; A -Int B |
| 160 | `reference-semantics/semantics/builtins.k` | 233-233 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyOpE("*",  A:Int, B:Int) =&gt; A *Int B |
| 161 | `reference-semantics/semantics/builtins.k` | 234-234 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyOpE("//", A:Int, B:Int) =&gt; A divInt B |
| 162 | `reference-semantics/semantics/builtins.k` | 235-235 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyOpE("**", A:Int, B:Int) =&gt; A ^Int B |
| 163 | `reference-semantics/semantics/builtins.k` | 236-236 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyOpE(_:String, A:Int, _:Int) =&gt; A [owise] |
| 164 | `reference-semantics/semantics/builtins.k` | 238-238 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total] |
| 165 | `reference-semantics/semantics/builtins.k` | 239-239 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passPowE(.OpSeq, NDS:IntSeq) =&gt; evp(.OpSeq, NDS) |
| 166 | `reference-semantics/semantics/builtins.k` | 240-240 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) =&gt; powCombE(N, passPowE(OPS, NDS)) |
| 167 | `reference-semantics/semantics/builtins.k` | 241-242 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) =&gt; powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**" |
| 168 | `reference-semantics/semantics/builtins.k` | 243-243 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passPowE(_:OpSeq, .IntSeq) =&gt; evp(.OpSeq, .IntSeq) [owise] |
| 169 | `reference-semantics/semantics/builtins.k` | 244-244 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax EvPair ::= powCombE(Int, EvPair) [function, total] |
| 170 | `reference-semantics/semantics/builtins.k` | 245-245 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) =&gt; evp(OPS, iCons(N ^Int M, REST)) |
| 171 | `reference-semantics/semantics/builtins.k` | 246-246 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) =&gt; evp(OPS, iCons(N, .IntSeq)) |
| 172 | `reference-semantics/semantics/builtins.k` | 247-247 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total] |
| 173 | `reference-semantics/semantics/builtins.k` | 248-248 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) =&gt; evp(oCons(O, OPS), iCons(N, NDS)) |
| 174 | `reference-semantics/semantics/builtins.k` | 250-250 | `syntax` | function, total, function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax EvPair ::= passMulE(EvPair) [function, total] &#124; passAddE(EvPair) [function, total] |
| 175 | `reference-semantics/semantics/builtins.k` | 251-251 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) =&gt; passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq) |
| 176 | `reference-semantics/semantics/builtins.k` | 252-252 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passMulE(evp(OPS:OpSeq, .IntSeq)) =&gt; evp(OPS, .IntSeq) |
| 177 | `reference-semantics/semantics/builtins.k` | 253-253 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) =&gt; passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq) |
| 178 | `reference-semantics/semantics/builtins.k` | 254-254 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passAddE(evp(OPS:OpSeq, .IntSeq)) =&gt; evp(OPS, .IntSeq) |
| 179 | `reference-semantics/semantics/builtins.k` | 255-255 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total] |
| 180 | `reference-semantics/semantics/builtins.k` | 256-256 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) =&gt; evp(OO, appendIE(ON, CUR)) |
| 181 | `reference-semantics/semantics/builtins.k` | 257-259 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) =&gt; passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O) |
| 182 | `reference-semantics/semantics/builtins.k` | 260-262 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) =&gt; passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O) |
| 183 | `reference-semantics/semantics/builtins.k` | 263-264 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) =&gt; evp(OO, appendIE(ON, CUR)) [owise] |
| 184 | `reference-semantics/semantics/builtins.k` | 265-265 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= inLevelE(String, String) [function, total] |
| 185 | `reference-semantics/semantics/builtins.k` | 266-266 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule inLevelE("mul", O:String) =&gt; O ==String "*" orBool O ==String "//" orBool O ==String "/" |
| 186 | `reference-semantics/semantics/builtins.k` | 267-267 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule inLevelE("add", O:String) =&gt; O ==String "+" orBool O ==String "-" |
| 187 | `reference-semantics/semantics/builtins.k` | 268-268 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule inLevelE(_:String, _:String) =&gt; false [owise] |
| 188 | `reference-semantics/semantics/builtins.k` | 269-269 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax OpSeq ::= appendOpE(OpSeq, String) [function, total] |
| 189 | `reference-semantics/semantics/builtins.k` | 270-270 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule appendOpE(.OpSeq, O:String) =&gt; oCons(O, .OpSeq) |
| 190 | `reference-semantics/semantics/builtins.k` | 271-271 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule appendOpE(oCons(H:String, T:OpSeq), O:String) =&gt; oCons(H, appendOpE(T, O)) |
| 191 | `reference-semantics/semantics/builtins.k` | 272-272 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= appendIE(IntSeq, Int) [function, total] |
| 192 | `reference-semantics/semantics/builtins.k` | 273-273 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule appendIE(.IntSeq, N:Int) =&gt; iCons(N, .IntSeq) |
| 193 | `reference-semantics/semantics/builtins.k` | 274-274 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule appendIE(iCons(H:Int, T:IntSeq), N:Int) =&gt; iCons(H, appendIE(T, N)) |
| 194 | `reference-semantics/semantics/builtins.k` | 279-279 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= "#md5" |
| 195 | `reference-semantics/semantics/builtins.k` | 280-281 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) =&gt; E ~&gt; #md5 ... &lt;/k&gt; [priority(40)] |
| 196 | `reference-semantics/semantics/builtins.k` | 282-282 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; str(CS:IntSeq) ~&gt; #md5 =&gt; md5Obj(CS) ... &lt;/k&gt; |
| 197 | `reference-semantics/semantics/builtins.k` | 283-283 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= md5Obj(IntSeq) |
| 198 | `reference-semantics/semantics/builtins.k` | 284-284 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) =&gt; str(md5hexCodes(CS)) |
| 199 | `reference-semantics/semantics/builtins.k` | 285-285 | `syntax` | function, total, symbol(md5hexCodes), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] |
| 200 | `reference-semantics/semantics/builtins.k` | 291-291 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) =&gt; isIntV(V) |
| 201 | `reference-semantics/semantics/builtins.k` | 292-292 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) =&gt; isStrV(V) |
| 202 | `reference-semantics/semantics/builtins.k` | 293-293 | `syntax` | function, function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isIntV(Val) [function] &#124; isStrV(Val) [function] |
| 203 | `reference-semantics/semantics/builtins.k` | 294-294 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isIntV(_:Int)         =&gt; true |
| 204 | `reference-semantics/semantics/builtins.k` | 295-295 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isIntV(_:Val)         =&gt; false [owise] |
| 205 | `reference-semantics/semantics/builtins.k` | 296-296 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isStrV(str(_:IntSeq)) =&gt; true |
| 206 | `reference-semantics/semantics/builtins.k` | 297-297 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isStrV(_:Val)         =&gt; false [owise] |
| 207 | `reference-semantics/semantics/builtins.k` | 298-298 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 208 | `reference-semantics/semantics/call.k` | 10-10 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-CALL |
| 209 | `reference-semantics/semantics/call.k` | 11-11 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-METHODS |
| 210 | `reference-semantics/semantics/call.k` | 12-12 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-BUILTINS |
| 211 | `reference-semantics/semantics/call.k` | 13-13 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-FUNCTIONS |
| 212 | `reference-semantics/semantics/call.k` | 16-16 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Attribute(V:Val, M:String) =&gt; boundMethodV(V, M) ... &lt;/k&gt; |
| 213 | `reference-semantics/semantics/call.k` | 19-19 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #callee(Exprs) |
| 214 | `reference-semantics/semantics/call.k` | 20-20 | `rule` | owise | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Call(Fe:Expr, ARGS:Exprs) =&gt; Fe ~&gt; #callee(ARGS) ... &lt;/k&gt; [owise] |
| 215 | `reference-semantics/semantics/call.k` | 21-21 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; CV:Val ~&gt; #callee(ARGS:Exprs) =&gt; #evalArgs(ARGS, .Vals, toCall(CV)) ... &lt;/k&gt; |
| 216 | `reference-semantics/semantics/call.k` | 24-24 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) =&gt; applyMethod(OBJ, M, ACC) ... &lt;/k&gt; |
| 217 | `reference-semantics/semantics/call.k` | 26-26 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) =&gt; #sumAcc(OBJ, 0) ... &lt;/k&gt; |
| 218 | `reference-semantics/semantics/call.k` | 27-27 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) =&gt; #allAcc(OBJ)    ... &lt;/k&gt; |
| 219 | `reference-semantics/semantics/call.k` | 28-28 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) =&gt; #anyAcc(OBJ)    ... &lt;/k&gt; |
| 220 | `reference-semantics/semantics/call.k` | 29-29 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) =&gt; #maxAcc0(OBJ)   ... &lt;/k&gt; |
| 221 | `reference-semantics/semantics/call.k` | 30-30 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) =&gt; #minAcc0(OBJ)   ... &lt;/k&gt; |
| 222 | `reference-semantics/semantics/call.k` | 31-31 | `rule` | owise | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV(BN:String)), ACC:Vals) =&gt; applyBuiltin(BN, ACC) ... &lt;/k&gt; [owise] |
| 223 | `reference-semantics/semantics/call.k` | 32-32 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(typeV(T:String)),     ACC:Vals) =&gt; applyBuiltin(T, ACC)  ... &lt;/k&gt; |
| 224 | `reference-semantics/semantics/call.k` | 38-41 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) =&gt; #applyK(toCall(builtinV(BN)), (V, REST)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 225 | `reference-semantics/semantics/call.k` | 42-46 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) =&gt; #applyK(toCall(builtinV(BN)), (A, V, REST)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires notBool isRefV(A) [priority(40)] |
| 226 | `reference-semantics/semantics/call.k` | 47-50 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) =&gt; #applyK(toCall(typeV(T)), (V, REST)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 227 | `reference-semantics/semantics/call.k` | 52-52 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isMutMethod(String) [function, total] |
| 228 | `reference-semantics/semantics/call.k` | 53-55 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isMutMethod(M:String) =&gt; M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove" |
| 229 | `reference-semantics/semantics/call.k` | 56-60 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) =&gt; #applyK(toCall(boundMethodV(V, M)), ACC) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires notBool isMutMethod(M) [priority(40)] |
| 230 | `reference-semantics/semantics/call.k` | 63-67 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) =&gt; #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)] |
| 231 | `reference-semantics/semantics/call.k` | 69-74 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~&gt; CONT =&gt; #bindP(PNS, ACC) ~&gt; BODY ~&gt; #endcall &lt;/k&gt; &lt;env&gt;     CALLERL:Int =&gt; NEWL &lt;/env&gt; &lt;scopes&gt;   STORE:Map =&gt; STORE [ NEWL &lt;- scope(.Map, parent(DEFL)) ] &lt;/scopes&gt; &lt;scopeLoc&gt; NEWL:Int =&gt; NEWL +Int 1 &lt;/scopeLoc&gt; &lt;stack&gt;   .List =&gt; ListItem(frame(CONT, CALLERL, NEWL)) ... &lt;/stack&gt; |
| 232 | `reference-semantics/semantics/call.k` | 80-85 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~&gt; CONT =&gt; #allocCells(CVS) ~&gt; #bindP(PNS, ACC) ~&gt; BODY ~&gt; #endcall &lt;/k&gt; &lt;env&gt;     CALLERL:Int =&gt; NEWL &lt;/env&gt; &lt;scopes&gt;   STORE:Map =&gt; STORE [ NEWL &lt;- scope(CM [ "$cells" &lt;- cellsMark(CVS) ], parent(0)) ] &lt;/scopes&gt; &lt;scopeLoc&gt; NEWL:Int =&gt; NEWL +Int 1 &lt;/scopeLoc&gt; &lt;stack&gt;   .List =&gt; ListItem(frame(CONT, CALLERL, NEWL)) ... &lt;/stack&gt; |
| 233 | `reference-semantics/semantics/call.k` | 87-87 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #allocCells(ParamNames) |
| 234 | `reference-semantics/semantics/call.k` | 88-88 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #allocCells(.ParamNames) =&gt; .K ... &lt;/k&gt; |
| 235 | `reference-semantics/semantics/call.k` | 89-94 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #allocCells((CV:String, R:ParamNames)) =&gt; #allocCells(R) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ CV &lt;- cellRef(N) ], _) ... &lt;/scopes&gt; &lt;heap&gt;    H:Map =&gt; (N &#124;-&gt; cellV(noneV)) H &lt;/heap&gt; &lt;heapLoc&gt; N:Int =&gt; N +Int 1 &lt;/heapLoc&gt; requires notBool N in_keys(H) |
| 236 | `reference-semantics/semantics/call.k` | 95-95 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 237 | `reference-semantics/semantics/comprehension.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-COMPREHENSION |
| 238 | `reference-semantics/semantics/comprehension.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 239 | `reference-semantics/semantics/comprehension.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-OPERATORS |
| 240 | `reference-semantics/semantics/comprehension.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-LIST |
| 241 | `reference-semantics/semantics/comprehension.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CONTROLS |
| 242 | `reference-semantics/semantics/comprehension.k` | 8-8 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-FUNCTIONS |
| 243 | `reference-semantics/semantics/comprehension.k` | 11-11 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule ListComp(ELT:Expr, Gs:CompFors) =&gt; Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| 244 | `reference-semantics/semantics/comprehension.k` | 12-12 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule GenExp(ELT:Expr, Gs:CompFors)   =&gt; Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| 245 | `reference-semantics/semantics/comprehension.k` | 14-14 | `syntax` | macro | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Stmts ::= compBody(CompFors, Expr) [macro] |
| 246 | `reference-semantics/semantics/comprehension.k` | 15-16 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule compBody(Gs:CompFors, ELT:Expr) =&gt; Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc")) |
| 247 | `reference-semantics/semantics/comprehension.k` | 18-18 | `syntax` | macro-rec | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Stmt ::= compNest(CompFors, Expr) [macro-rec] |
| 248 | `reference-semantics/semantics/comprehension.k` | 19-20 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule compNest(.CompFors, ELT:Expr) =&gt; Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT))) |
| 249 | `reference-semantics/semantics/comprehension.k` | 21-22 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) =&gt; For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts)) |
| 250 | `reference-semantics/semantics/comprehension.k` | 24-24 | `syntax` | macro | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Expr ::= compGuard(Exprs) [macro] |
| 251 | `reference-semantics/semantics/comprehension.k` | 25-25 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule compGuard(.Exprs)             =&gt; Bool(true) |
| 252 | `reference-semantics/semantics/comprehension.k` | 26-26 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule compGuard((F:Expr, Fs:Exprs)) =&gt; BoolOp("and", (F, Fs)) |
| 253 | `reference-semantics/semantics/comprehension.k` | 27-27 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 254 | `reference-semantics/semantics/concrete.k` | 8-8 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-CONCRETE |
| 255 | `reference-semantics/semantics/concrete.k` | 9-9 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY |
| 256 | `reference-semantics/semantics/concrete.k` | 13-15 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) =&gt; deepEqVS(A, B, HP) ... &lt;/k&gt; &lt;heap&gt; HP:Map &lt;/heap&gt; requires hasRefVS(A) orBool hasRefVS(B) |
| 257 | `reference-semantics/semantics/concrete.k` | 16-18 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) =&gt; notBool deepEqVS(A, B, HP) ... &lt;/k&gt; &lt;heap&gt; HP:Map &lt;/heap&gt; requires hasRefVS(A) orBool hasRefVS(B) |
| 258 | `reference-semantics/semantics/concrete.k` | 25-25 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= kvP(Val, Val) |
| 259 | `reference-semantics/semantics/concrete.k` | 26-27 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) &#124; #ksIns(Val, ValSeq, Val, ValSeq, Bool) |
| 260 | `reference-semantics/semantics/concrete.k` | 28-30 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) =&gt; #ksort(VS, KV, .ValSeq, false) ... &lt;/k&gt; [priority(40)] |
| 261 | `reference-semantics/semantics/concrete.k` | 31-33 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) =&gt; #ksort(VS, KV, .ValSeq, RB) ... &lt;/k&gt; [priority(40)] |
| 262 | `reference-semantics/semantics/concrete.k` | 34-35 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) =&gt; #alloc(list(condRev(unpairVS(ACC), RB))) ... &lt;/k&gt; |
| 263 | `reference-semantics/semantics/concrete.k` | 36-37 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) =&gt; KV ~&gt; #callee((V, .Exprs)) ~&gt; #ksIns(V, R, KV, ACC, RB) ... &lt;/k&gt; |
| 264 | `reference-semantics/semantics/concrete.k` | 38-40 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; K:Val ~&gt; #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) =&gt; #ksort(R, KV, insPair(ACC, K, V), RB) ... &lt;/k&gt; requires notBool isKwV(K) |
| 265 | `reference-semantics/semantics/concrete.k` | 42-42 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= insPair(ValSeq, Val, Val) [function] |
| 266 | `reference-semantics/semantics/concrete.k` | 43-43 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule insPair(.ValSeq, K:Val, V:Val) =&gt; vCons(kvP(K, V), .ValSeq) |
| 267 | `reference-semantics/semantics/concrete.k` | 44-46 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) =&gt; vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2) |
| 268 | `reference-semantics/semantics/concrete.k` | 47-49 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) =&gt; vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2) |
| 269 | `reference-semantics/semantics/concrete.k` | 51-51 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= kLt(Val, Val) [function] |
| 270 | `reference-semantics/semantics/concrete.k` | 52-52 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule kLt(I1:Int, I2:Int)             =&gt; I1 &lt;Int I2 |
| 271 | `reference-semantics/semantics/concrete.k` | 53-53 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule kLt(F1:Float, F2:Float)         =&gt; F1 &lt;Float F2 |
| 272 | `reference-semantics/semantics/concrete.k` | 54-54 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule kLt(str(A:IntSeq), str(B:IntSeq)) =&gt; strLt(A, B) |
| 273 | `reference-semantics/semantics/concrete.k` | 56-56 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= unpairVS(ValSeq) [function, total] |
| 274 | `reference-semantics/semantics/concrete.k` | 57-57 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule unpairVS(.ValSeq) =&gt; .ValSeq |
| 275 | `reference-semantics/semantics/concrete.k` | 58-58 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) =&gt; vCons(V, unpairVS(R)) |
| 276 | `reference-semantics/semantics/concrete.k` | 59-59 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule unpairVS(vCons(V:Val, R:ValSeq)) =&gt; vCons(V, unpairVS(R)) [owise] |
| 277 | `reference-semantics/semantics/concrete.k` | 60-60 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 278 | `reference-semantics/semantics/controls.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-CONTROLS |
| 279 | `reference-semantics/semantics/controls.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 280 | `reference-semantics/semantics/controls.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-TUPLE |
| 281 | `reference-semantics/semantics/controls.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 282 | `reference-semantics/semantics/controls.k` | 9-11 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Assign(Name(X:String), V:Val) =&gt; .K ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ X &lt;- V ], _) ... &lt;/scopes&gt; |
| 283 | `reference-semantics/semantics/controls.k` | 12-18 | `rule` | priority(40) | yes | USED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Assign(Name(X:String), V:Val) =&gt; #cellW({M[X]}:&gt;Val, V) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:&gt;Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:&gt;Val) [priority(40)] |
| 284 | `reference-semantics/semantics/controls.k` | 20-23 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; AugAssign(Name(X:String), OP:String, V:Val) =&gt; .K ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ X &lt;- applyBin(OP, {M[X]}:&gt;Val, V) ], _) ... &lt;/scopes&gt; requires X in_keys(M) |
| 285 | `reference-semantics/semantics/controls.k` | 27-31 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; AugAssign(Name(X:String), OP:String, V:Val) =&gt; Assign(Name(X), BinOp(OP, Name(X), V)) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; requires X in_keys(M) andBool isRefV({M[X]}:&gt;Val) [priority(40)] |
| 286 | `reference-semantics/semantics/controls.k` | 35-35 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; ImportFrom("math", NS:ParamNames) =&gt; #bindImports(NS) ... &lt;/k&gt; |
| 287 | `reference-semantics/semantics/controls.k` | 36-36 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; ImportFrom(_:String, _:ParamNames) =&gt; .K ... &lt;/k&gt; [owise] |
| 288 | `reference-semantics/semantics/controls.k` | 37-37 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #bindImports(ParamNames) |
| 289 | `reference-semantics/semantics/controls.k` | 38-38 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindImports(.ParamNames) =&gt; .K ... &lt;/k&gt; |
| 290 | `reference-semantics/semantics/controls.k` | 39-42 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindImports((N:String, NS:ParamNames)) =&gt; #bindImports(NS) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ N &lt;- builtinV(N) ], _) ... &lt;/scopes&gt; requires N ==String "floor" orBool N ==String "ceil" |
| 291 | `reference-semantics/semantics/controls.k` | 43-44 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindImports((N:String, NS:ParamNames)) =&gt; #bindImports(NS) ... &lt;/k&gt; requires notBool (N ==String "floor" orBool N ==String "ceil") |
| 292 | `reference-semantics/semantics/controls.k` | 48-48 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Expr(_:Val) =&gt; .K ... &lt;/k&gt; |
| 293 | `reference-semantics/semantics/controls.k` | 51-51 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #branch(Bool, Stmts, Stmts) |
| 294 | `reference-semantics/semantics/controls.k` | 52-52 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; If(C:Val, T:Stmts, E:Stmts) =&gt; #branch(truthy(C), T, E) ... &lt;/k&gt; |
| 295 | `reference-semantics/semantics/controls.k` | 53-53 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #branch(true,  T:Stmts, _:Stmts) =&gt; T ... &lt;/k&gt; |
| 296 | `reference-semantics/semantics/controls.k` | 54-54 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #branch(false, _:Stmts, E:Stmts) =&gt; E ... &lt;/k&gt; |
| 297 | `reference-semantics/semantics/controls.k` | 57-58 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; IfExp(V:Val, T:Expr, _:Expr) =&gt; T ... &lt;/k&gt; requires truthy(V) |
| 298 | `reference-semantics/semantics/controls.k` | 59-60 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; IfExp(V:Val, _:Expr, E:Expr) =&gt; E ... &lt;/k&gt; requires notBool truthy(V) |
| 299 | `reference-semantics/semantics/controls.k` | 65-67 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #loop(Val, Expr, Stmts) &#124; #loopStep(Expr, Stmts) &#124; #while(Expr, Stmts) &#124; #whileCond(Expr, Stmts) &#124; #loopLbl(K) &#124; "#cont" &#124; "#brk" |
| 300 | `reference-semantics/semantics/controls.k` | 69-69 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; For(T:Expr, OBJ:Val, B:Stmts) =&gt; #loop(OBJ, T, B) ... &lt;/k&gt; |
| 301 | `reference-semantics/semantics/controls.k` | 71-71 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #loop(IT:Iterable, T:Expr, B:Stmts) =&gt; #iterNext(IT) ~&gt; #loopStep(T, B) ... &lt;/k&gt; |
| 302 | `reference-semantics/semantics/controls.k` | 72-72 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #loopStep(_:Expr, _:Stmts) =&gt; .K ... &lt;/k&gt; |
| 303 | `reference-semantics/semantics/controls.k` | 73-74 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, REST:Iterable) ~&gt; #loopStep(T:Expr, B:Stmts) =&gt; #bindTgt(T, V) ~&gt; B ~&gt; #loopLbl(#loop(REST, T, B)) ... &lt;/k&gt; |
| 304 | `reference-semantics/semantics/controls.k` | 77-77 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; While(C:Expr, B:Stmts) =&gt; #while(C, B) ... &lt;/k&gt; |
| 305 | `reference-semantics/semantics/controls.k` | 78-78 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #while(C:Expr, B:Stmts) =&gt; C ~&gt; #whileCond(C, B) ... &lt;/k&gt; |
| 306 | `reference-semantics/semantics/controls.k` | 79-80 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V:Val ~&gt; #whileCond(C:Expr, B:Stmts) =&gt; B ~&gt; #loopLbl(#while(C, B)) ... &lt;/k&gt; requires truthy(V) |
| 307 | `reference-semantics/semantics/controls.k` | 81-82 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V:Val ~&gt; #whileCond(_C:Expr, _B:Stmts) =&gt; .K ... &lt;/k&gt; requires notBool truthy(V) |
| 308 | `reference-semantics/semantics/controls.k` | 85-85 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #loopLbl(NEXT:K) =&gt; NEXT ... &lt;/k&gt; |
| 309 | `reference-semantics/semantics/controls.k` | 86-86 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Continue =&gt; #cont ... &lt;/k&gt; |
| 310 | `reference-semantics/semantics/controls.k` | 87-87 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Break =&gt; #brk ... &lt;/k&gt; |
| 311 | `reference-semantics/semantics/controls.k` | 88-88 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #cont ~&gt; #loopLbl(NEXT:K) =&gt; NEXT ... &lt;/k&gt; |
| 312 | `reference-semantics/semantics/controls.k` | 89-89 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #cont ~&gt; (_:KItem =&gt; .K) ... &lt;/k&gt; [owise] |
| 313 | `reference-semantics/semantics/controls.k` | 90-90 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #brk ~&gt; #loopLbl(_:K) =&gt; .K ... &lt;/k&gt; |
| 314 | `reference-semantics/semantics/controls.k` | 91-91 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #brk ~&gt; (_:KItem =&gt; .K) ... &lt;/k&gt; [owise] |
| 315 | `reference-semantics/semantics/controls.k` | 95-97 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; If(ref(H:Int), T:Stmts, E:Stmts) =&gt; If(V, T, E) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 316 | `reference-semantics/semantics/controls.k` | 98-100 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; IfExp(ref(H:Int), T:Expr, E:Expr) =&gt; IfExp(V, T, E) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 317 | `reference-semantics/semantics/controls.k` | 101-103 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; ref(H:Int) ~&gt; #whileCond(C:Expr, B:Stmts) =&gt; V ~&gt; #whileCond(C, B) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 318 | `reference-semantics/semantics/controls.k` | 106-108 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; For(T:Expr, ref(H:Int), B:Stmts) =&gt; For(T, V, B) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 319 | `reference-semantics/semantics/controls.k` | 109-109 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 320 | `reference-semantics/semantics/core.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-CORE |
| 321 | `reference-semantics/semantics/core.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-SYNTAX |
| 322 | `reference-semantics/semantics/core.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports INT |
| 323 | `reference-semantics/semantics/core.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports BOOL |
| 324 | `reference-semantics/semantics/core.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports STRING |
| 325 | `reference-semantics/semantics/core.k` | 8-8 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MAP |
| 326 | `reference-semantics/semantics/core.k` | 9-9 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports LIST |
| 327 | `reference-semantics/semantics/core.k` | 10-10 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports K-EQUAL |
| 328 | `reference-semantics/semantics/core.k` | 13-13 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= ".IntSeq" &#124; iCons(Int, IntSeq) |
| 329 | `reference-semantics/semantics/core.k` | 14-14 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= ".ValSeq" &#124; vCons(Val, ValSeq) |
| 330 | `reference-semantics/semantics/core.k` | 15-15 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Str    ::= str(IntSeq) |
| 331 | `reference-semantics/semantics/core.k` | 18-23 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Iterable ::= list(ValSeq) &#124; tuple(ValSeq) &#124; Str &#124; rangeObj(Int, Int, Int) &#124; zipObj(ValSeq, ValSeq) &#124; zipObjS(IntSeq, IntSeq) |
| 332 | `reference-semantics/semantics/core.k` | 25-34 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Val      ::= Int &#124; Bool &#124; "noneV" &#124; Iterable &#124; ref(Int)          // a heap object: &lt;heap&gt; holds its list(VS) &#124; cellRef(Int)      // a closure cell: &lt;heap&gt; holds cellV(V) &#124; closureVal(ParamNames, Stmts, Int) &#124; typeV(String)     // a type object (int/str), resolved from the builtins frame &#124; builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) &#124; boundMethodV(Val, String)   // a cooled Attribute: obj.method |
| 333 | `reference-semantics/semantics/core.k` | 36-36 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Parent   ::= "root" &#124; parent(Int) |
| 334 | `reference-semantics/semantics/core.k` | 37-37 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Scope    ::= scope(Map, Parent) |
| 335 | `reference-semantics/semantics/core.k` | 38-38 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax KResult  ::= Val |
| 336 | `reference-semantics/semantics/core.k` | 39-39 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Expr     ::= Val   // cooling puts results back into expression holes |
| 337 | `reference-semantics/semantics/core.k` | 40-40 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Vals     ::= List{Val, ","} |
| 338 | `reference-semantics/semantics/core.k` | 41-41 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Exc      ::= "NoExc" &#124; "AssertionError" |
| 339 | `reference-semantics/semantics/core.k` | 42-42 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax RetState ::= "noRet" &#124; retV(Val) |
| 340 | `reference-semantics/semantics/core.k` | 49-60 | `configuration` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | configuration &lt;k&gt;       #loadAll($PGM:Module) &lt;/k&gt; &lt;env&gt;     0 &lt;/env&gt; &lt;scopes&gt;   0     &#124;-&gt; scope(.Map, parent(-1)) -1    &#124;-&gt; builtinsScope &lt;/scopes&gt; &lt;scopeLoc&gt; 1 &lt;/scopeLoc&gt; &lt;heap&gt;    .Map &lt;/heap&gt; &lt;heapLoc&gt; 0 &lt;/heapLoc&gt; &lt;stack&gt;   .List &lt;/stack&gt; &lt;ret&gt;     noRet &lt;/ret&gt; &lt;exc&gt;     NoExc &lt;/exc&gt; &lt;exit-code exit=""&gt; 0 &lt;/exit-code&gt; |
| 341 | `reference-semantics/semantics/core.k` | 68-68 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isRefV(Val) [function, total] |
| 342 | `reference-semantics/semantics/core.k` | 69-69 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isRefV(ref(_:Int)) =&gt; true |
| 343 | `reference-semantics/semantics/core.k` | 70-70 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isRefV(_:Val)      =&gt; false [owise] |
| 344 | `reference-semantics/semantics/core.k` | 75-75 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax HeapVal ::= cellV(Val) |
| 345 | `reference-semantics/semantics/core.k` | 76-76 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isCellRef(Val) [function, total] |
| 346 | `reference-semantics/semantics/core.k` | 77-77 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isCellRef(cellRef(_:Int)) =&gt; true |
| 347 | `reference-semantics/semantics/core.k` | 78-78 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isCellRef(_:Val)          =&gt; false [owise] |
| 348 | `reference-semantics/semantics/core.k` | 85-90 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; cellRef(H:Int) =&gt; V ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; &lt;heap&gt; ... H &#124;-&gt; cellV(V:Val) ... &lt;/heap&gt; requires "$cells" in_keys(M) [priority(40)] |
| 349 | `reference-semantics/semantics/core.k` | 95-95 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= kwV(String, Val) |
| 350 | `reference-semantics/semantics/core.k` | 96-96 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #kwTag(String) |
| 351 | `reference-semantics/semantics/core.k` | 97-97 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; KwArg(N:String, E:Expr) =&gt; E ~&gt; #kwTag(N) ... &lt;/k&gt; |
| 352 | `reference-semantics/semantics/core.k` | 98-99 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V:Val ~&gt; #kwTag(N:String) =&gt; kwV(N, V) ... &lt;/k&gt; requires notBool isKwV(V) |
| 353 | `reference-semantics/semantics/core.k` | 100-100 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isKwV(Val) [function, total] |
| 354 | `reference-semantics/semantics/core.k` | 101-101 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isKwV(kwV(_:String, _:Val)) =&gt; true |
| 355 | `reference-semantics/semantics/core.k` | 102-102 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isKwV(_:Val)                =&gt; false [owise] |
| 356 | `reference-semantics/semantics/core.k` | 106-106 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= cellsMark(ParamNames) |
| 357 | `reference-semantics/semantics/core.k` | 107-107 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ParamNames ::= cellsOf(Val) [function] |
| 358 | `reference-semantics/semantics/core.k` | 108-108 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule cellsOf(cellsMark(CVS:ParamNames)) =&gt; CVS |
| 359 | `reference-semantics/semantics/core.k` | 109-109 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= pnMember(String, ParamNames) [function, total] |
| 360 | `reference-semantics/semantics/core.k` | 110-110 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule pnMember(_:String, .ParamNames) =&gt; false |
| 361 | `reference-semantics/semantics/core.k` | 111-111 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule pnMember(X:String, (P:String, R:ParamNames)) =&gt; X ==String P orBool pnMember(X, R) |
| 362 | `reference-semantics/semantics/core.k` | 113-113 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #cellW(Val, Val) |
| 363 | `reference-semantics/semantics/core.k` | 114-115 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #cellW(cellRef(H:Int), V:Val) =&gt; .K ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; cellV(_:Val =&gt; V) ... &lt;/heap&gt; |
| 364 | `reference-semantics/semantics/core.k` | 117-117 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #alloc(Val) |
| 365 | `reference-semantics/semantics/core.k` | 118-121 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #alloc(V:Val) =&gt; ref(N) ... &lt;/k&gt; &lt;heap&gt;    H:Map =&gt; (N &#124;-&gt; V) H &lt;/heap&gt; &lt;heapLoc&gt; N:Int =&gt; N +Int 1 &lt;/heapLoc&gt; requires notBool N in_keys(H) |
| 366 | `reference-semantics/semantics/core.k` | 124-124 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #loadAll(Module) |
| 367 | `reference-semantics/semantics/core.k` | 125-125 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #loadAll(Module(SS:Stmts)) =&gt; SS ... &lt;/k&gt; |
| 368 | `reference-semantics/semantics/core.k` | 126-126 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; (S:Stmt SS:Stmts):Stmts =&gt; S ~&gt; SS ... &lt;/k&gt; |
| 369 | `reference-semantics/semantics/core.k` | 127-127 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; .Stmts =&gt; .K ... &lt;/k&gt; |
| 370 | `reference-semantics/semantics/core.k` | 130-130 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #look(String, Int) |
| 371 | `reference-semantics/semantics/core.k` | 131-131 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Name(X:String) =&gt; #look(X, L) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; |
| 372 | `reference-semantics/semantics/core.k` | 132-134 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #look(X:String, L:Int) =&gt; {M[X]}:&gt;Val ... &lt;/k&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _:Parent) ... &lt;/scopes&gt; requires X in_keys(M) |
| 373 | `reference-semantics/semantics/core.k` | 145-151 | `rule` | priority(40) | yes | USED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #look(X:String, L:Int) =&gt; V ... &lt;/k&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _:Parent) ... &lt;/scopes&gt; &lt;heap&gt; ... H &#124;-&gt; cellV(V:Val) ... &lt;/heap&gt; requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:&gt;Val)) andBool {M[X]}:&gt;Val ==K cellRef(H) [priority(40)] |
| 374 | `reference-semantics/semantics/core.k` | 152-154 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #look(X:String, L:Int) =&gt; #look(X, P) ... &lt;/k&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, parent(P:Int)) ... &lt;/scopes&gt; requires notBool (X in_keys(M)) |
| 375 | `reference-semantics/semantics/core.k` | 157-157 | `syntax` | function, total | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Scope ::= "builtinsScope" [function, total] |
| 376 | `reference-semantics/semantics/core.k` | 158-181 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule builtinsScope =&gt; scope(.Map [ "len"    &lt;- builtinV("len")    ] [ "set"    &lt;- builtinV("set")    ] [ "sum"    &lt;- builtinV("sum")    ] [ "abs"    &lt;- builtinV("abs")    ] [ "min"    &lt;- builtinV("min")    ] [ "max"    &lt;- builtinV("max")    ] [ "ord"    &lt;- builtinV("ord")    ] [ "chr"    &lt;- builtinV("chr")    ] [ "range"  &lt;- builtinV("range")  ] [ "all"    &lt;- builtinV("all")    ] [ "any"    &lt;- builtinV("any")    ] [ "zip"    &lt;- builtinV("zip")    ] [ "isinstance" &lt;- builtinV("isinstance") ] [ "sorted" &lt;- builtinV("sorted") ] [ "list"   &lt;- builtinV("list")   ] [ "round"  &lt;- builtinV("round")  ] [ "bin"    &lt;- builtinV("bin")    ] [ "enumerate" &lt;- builtinV("enumerate") ] [ "map"    &lt;- builtinV("map")    ] [ "eval"   &lt;- builtinV("eval")   ] [ "int"    &lt;- typeV("int")       ] [ "str"    &lt;- typeV("str")       ] [ "float"  &lt;- typeV("float")     ], root) |
| 377 | `reference-semantics/semantics/core.k` | 185-185 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax ApplyK ::= toCall(Val) |
| 378 | `reference-semantics/semantics/core.k` | 186-188 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) &#124; #evalArgCont(Exprs, Vals, ApplyK) &#124; #applyK(ApplyK, Vals) |
| 379 | `reference-semantics/semantics/core.k` | 189-189 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) =&gt; A ~&gt; #evalArgCont(REST, ACC, K) ... &lt;/k&gt; |
| 380 | `reference-semantics/semantics/core.k` | 190-190 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V:Val ~&gt; #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) =&gt; #evalArgs(REST, appendVal(ACC, V), K) ... &lt;/k&gt; |
| 381 | `reference-semantics/semantics/core.k` | 191-191 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #evalArgs(.Exprs, ACC:Vals, K:ApplyK) =&gt; #applyK(K, ACC) ... &lt;/k&gt; |
| 382 | `reference-semantics/semantics/core.k` | 194-194 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Int(I:Int)   =&gt; I ... &lt;/k&gt; |
| 383 | `reference-semantics/semantics/core.k` | 195-195 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Bool(B:Bool) =&gt; B ... &lt;/k&gt; |
| 384 | `reference-semantics/semantics/core.k` | 196-196 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; NoneVal      =&gt; noneV ... &lt;/k&gt; |
| 385 | `reference-semantics/semantics/core.k` | 199-199 | `syntax` | function | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= truthy(Val) [function] |
| 386 | `reference-semantics/semantics/core.k` | 200-200 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule truthy(B:Bool)          =&gt; B |
| 387 | `reference-semantics/semantics/core.k` | 201-201 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule truthy(noneV)           =&gt; false |
| 388 | `reference-semantics/semantics/core.k` | 202-202 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule truthy(I:Int)           =&gt; I =/=Int 0 |
| 389 | `reference-semantics/semantics/core.k` | 203-203 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule truthy(str(S:IntSeq))   =&gt; notBool (S ==K .IntSeq) |
| 390 | `reference-semantics/semantics/core.k` | 204-204 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule truthy(list(V:ValSeq))  =&gt; notBool (V ==K .ValSeq) |
| 391 | `reference-semantics/semantics/core.k` | 205-205 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule truthy(tuple(V:ValSeq)) =&gt; notBool (V ==K .ValSeq) |
| 392 | `reference-semantics/semantics/core.k` | 208-208 | `syntax` | function | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Val  ::= applyUn(String, Val) [function] |
| 393 | `reference-semantics/semantics/core.k` | 209-209 | `syntax` | function | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Val  ::= applyBin(String, Val, Val) [function] |
| 394 | `reference-semantics/semantics/core.k` | 210-210 | `syntax` | function | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= applyCmp(String, Val, Val) [function] |
| 395 | `reference-semantics/semantics/core.k` | 213-213 | `syntax` | function, total | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Vals ::= appendVal(Vals, Val) [function, total] |
| 396 | `reference-semantics/semantics/core.k` | 214-214 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule appendVal(.Vals, V:Val)              =&gt; V , .Vals |
| 397 | `reference-semantics/semantics/core.k` | 215-215 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule appendVal((V0:Val, VS:Vals), V:Val)  =&gt; V0 , appendVal(VS, V) |
| 398 | `reference-semantics/semantics/core.k` | 217-217 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= vals2valSeq(Vals) [function, total] |
| 399 | `reference-semantics/semantics/core.k` | 218-218 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule vals2valSeq(.Vals)            =&gt; .ValSeq |
| 400 | `reference-semantics/semantics/core.k` | 219-219 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule vals2valSeq((V:Val, VS:Vals)) =&gt; vCons(V, vals2valSeq(VS)) |
| 401 | `reference-semantics/semantics/core.k` | 223-223 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= vsLen(ValSeq) [function, total] |
| 402 | `reference-semantics/semantics/core.k` | 224-224 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule vsLen(.ValSeq)                =&gt; 0 |
| 403 | `reference-semantics/semantics/core.k` | 225-225 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule vsLen(vCons(_:Val, S:ValSeq)) =&gt; 1 +Int vsLen(S) |
| 404 | `reference-semantics/semantics/core.k` | 227-227 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= isLen(IntSeq) [function, total] |
| 405 | `reference-semantics/semantics/core.k` | 228-228 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isLen(.IntSeq)                =&gt; 0 |
| 406 | `reference-semantics/semantics/core.k` | 229-229 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isLen(iCons(_:Int, S:IntSeq)) =&gt; 1 +Int isLen(S) |
| 407 | `reference-semantics/semantics/core.k` | 233-233 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total] |
| 408 | `reference-semantics/semantics/core.k` | 234-234 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule setVSAt(.ValSeq, _:Int, _:Val)               =&gt; .ValSeq |
| 409 | `reference-semantics/semantics/core.k` | 235-235 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    =&gt; vCons(V, S) |
| 410 | `reference-semantics/semantics/core.k` | 236-237 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) =&gt; vCons(W, setVSAt(S, I -Int 1, V)) requires I &gt;Int 0 |
| 411 | `reference-semantics/semantics/core.k` | 238-239 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule setVSAt(VS:ValSeq, I:Int, _:Val)             =&gt; VS requires I &lt;Int 0 |
| 412 | `reference-semantics/semantics/core.k` | 240-240 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 413 | `reference-semantics/semantics/dict.k` | 13-13 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-DICT |
| 414 | `reference-semantics/semantics/dict.k` | 14-14 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 415 | `reference-semantics/semantics/dict.k` | 15-15 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 416 | `reference-semantics/semantics/dict.k` | 16-16 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-METHODS |
| 417 | `reference-semantics/semantics/dict.k` | 17-17 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-LIST |
| 418 | `reference-semantics/semantics/dict.k` | 20-20 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= dictV(ValSeq, ValSeq) |
| 419 | `reference-semantics/semantics/dict.k` | 23-25 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) &#124; #dictKey(Expr, Entries, ValSeq, ValSeq) &#124; #dictVal(Val, Entries, ValSeq, ValSeq) |
| 420 | `reference-semantics/semantics/dict.k` | 26-26 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; DictExpr(ES:Entries) =&gt; #dictAcc(ES, .ValSeq, .ValSeq) ... &lt;/k&gt; |
| 421 | `reference-semantics/semantics/dict.k` | 27-27 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) =&gt; dictV(KS, VS) ... &lt;/k&gt; |
| 422 | `reference-semantics/semantics/dict.k` | 28-29 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) =&gt; K ~&gt; #dictKey(V, REST, KS, VS) ... &lt;/k&gt; |
| 423 | `reference-semantics/semantics/dict.k` | 30-31 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; KV:Val ~&gt; #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) =&gt; V ~&gt; #dictVal(KV, REST, KS, VS) ... &lt;/k&gt; |
| 424 | `reference-semantics/semantics/dict.k` | 32-33 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; VV:Val ~&gt; #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) =&gt; #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... &lt;/k&gt; |
| 425 | `reference-semantics/semantics/dict.k` | 37-37 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= dHasKey(ValSeq, Val) [function, total] |
| 426 | `reference-semantics/semantics/dict.k` | 38-38 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dHasKey(.ValSeq, _:Val)                =&gt; false |
| 427 | `reference-semantics/semantics/dict.k` | 39-39 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) =&gt; true          requires A ==K K |
| 428 | `reference-semantics/semantics/dict.k` | 40-40 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) =&gt; dHasKey(R, K) requires notBool (A ==K K) |
| 429 | `reference-semantics/semantics/dict.k` | 43-43 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= dPutK(ValSeq, Val) [function, total] |
| 430 | `reference-semantics/semantics/dict.k` | 44-44 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dPutK(KS:ValSeq, K:Val) =&gt; KS                                  requires dHasKey(KS, K) |
| 431 | `reference-semantics/semantics/dict.k` | 45-45 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dPutK(KS:ValSeq, K:Val) =&gt; valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) |
| 432 | `reference-semantics/semantics/dict.k` | 49-49 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total] |
| 433 | `reference-semantics/semantics/dict.k` | 50-51 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  =&gt; vCons(V, VR) requires A ==K K |
| 434 | `reference-semantics/semantics/dict.k` | 52-53 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) =&gt; vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K) |
| 435 | `reference-semantics/semantics/dict.k` | 54-54 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) =&gt; valSeqConcat(VS, vCons(V, .ValSeq)) [owise] |
| 436 | `reference-semantics/semantics/dict.k` | 58-60 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) =&gt; #alloc(list(KS)) ... &lt;/k&gt; [priority(40)] |
| 437 | `reference-semantics/semantics/dict.k` | 63-63 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) =&gt; dGet(KS, VS, K) |
| 438 | `reference-semantics/semantics/dict.k` | 64-64 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= applyIndexD(Val, Val) [function] |
| 439 | `reference-semantics/semantics/dict.k` | 65-66 | `rule` | priority(45) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) =&gt; applyIndexD(dictV(KS, VS), K) ... &lt;/k&gt; [priority(45)] |
| 440 | `reference-semantics/semantics/dict.k` | 70-70 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= dictSet(Val, Val, Val) [function] |
| 441 | `reference-semantics/semantics/dict.k` | 71-71 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) =&gt; dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) |
| 442 | `reference-semantics/semantics/dict.k` | 76-76 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #dsetK(String, Val) |
| 443 | `reference-semantics/semantics/dict.k` | 77-77 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Assign(Subscript(Name(X:String), K:Expr), VV:Val) =&gt; K ~&gt; #dsetK(X, VV) ... &lt;/k&gt; |
| 444 | `reference-semantics/semantics/dict.k` | 78-81 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; KV:Val ~&gt; #dsetK(X:String, VV:Val) =&gt; .K ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ X &lt;- dictSet({M[X]}:&gt;Val, KV, VV) ], _) ... &lt;/scopes&gt; requires X in_keys(M) andBool notBool isRefV({M[X]}:&gt;Val) |
| 445 | `reference-semantics/semantics/dict.k` | 82-85 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; KV:Val ~&gt; #dsetK(X:String, VV:Val) =&gt; #dsetV({M[X]}:&gt;Val, KV, VV) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; requires X in_keys(M) andBool isRefV({M[X]}:&gt;Val) |
| 446 | `reference-semantics/semantics/dict.k` | 86-86 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #dsetV(Val, Val, Val) |
| 447 | `reference-semantics/semantics/dict.k` | 87-88 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #dsetV(ref(H:Int), I:Int, VV:Val) =&gt; .K ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; list(VS:ValSeq =&gt; setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... &lt;/heap&gt; |
| 448 | `reference-semantics/semantics/dict.k` | 90-90 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= normIdxD(Int, Int) [function, total] |
| 449 | `reference-semantics/semantics/dict.k` | 91-91 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule normIdxD(I:Int, LEN:Int) =&gt; I +Int LEN requires I  &lt;Int 0 |
| 450 | `reference-semantics/semantics/dict.k` | 92-92 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule normIdxD(I:Int, _:Int)   =&gt; I          requires I &gt;=Int 0 |
| 451 | `reference-semantics/semantics/dict.k` | 95-96 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) =&gt; (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2) |
| 452 | `reference-semantics/semantics/dict.k` | 97-97 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function] |
| 453 | `reference-semantics/semantics/dict.k` | 98-98 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) =&gt; true |
| 454 | `reference-semantics/semantics/dict.k` | 99-100 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) =&gt; dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2) |
| 455 | `reference-semantics/semantics/dict.k` | 101-101 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= dGet(ValSeq, ValSeq, Val) [function] |
| 456 | `reference-semantics/semantics/dict.k` | 102-102 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) =&gt; B                requires A ==K K |
| 457 | `reference-semantics/semantics/dict.k` | 103-103 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) =&gt; dGet(KR, VR, K) requires notBool (A ==K K) |
| 458 | `reference-semantics/semantics/dict.k` | 104-104 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 459 | `reference-semantics/semantics/float.k` | 14-14 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-FLOAT |
| 460 | `reference-semantics/semantics/float.k` | 15-15 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-OPERATORS |
| 461 | `reference-semantics/semantics/float.k` | 16-16 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-BUILTINS |
| 462 | `reference-semantics/semantics/float.k` | 17-17 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports FLOAT |
| 463 | `reference-semantics/semantics/float.k` | 20-20 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= Float |
| 464 | `reference-semantics/semantics/float.k` | 21-21 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Float(F:Float) =&gt; F ... &lt;/k&gt; |
| 465 | `reference-semantics/semantics/float.k` | 24-24 | `syntax` | function, total, symbol(intFloatDiv), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators] |
| 466 | `reference-semantics/semantics/float.k` | 25-25 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule intFloatDiv(I:Int, F:Float) =&gt; Int2Float(I, 53, 11) /Float F [concrete] |
| 467 | `reference-semantics/semantics/float.k` | 27-27 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("/", I:Int, F:Float) =&gt; intFloatDiv(I, F) |
| 468 | `reference-semantics/semantics/float.k` | 30-30 | `syntax` | function, total, symbol(divII), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators] |
| 469 | `reference-semantics/semantics/float.k` | 31-31 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule divII(I1:Int, I2:Int) =&gt; Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete] |
| 470 | `reference-semantics/semantics/float.k` | 32-32 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("/", I1:Int, I2:Int) =&gt; divII(I1, I2) |
| 471 | `reference-semantics/semantics/float.k` | 37-37 | `syntax` | function, total, symbol(floatMod), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators] |
| 472 | `reference-semantics/semantics/float.k` | 38-38 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule floatMod(F1:Float, F2:Float) =&gt; F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete] |
| 473 | `reference-semantics/semantics/float.k` | 39-39 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("%", F1:Float, F2:Float) =&gt; floatMod(F1, F2) |
| 474 | `reference-semantics/semantics/float.k` | 43-43 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", F1:Float, F2:Float) =&gt; F1 ==Float F2 |
| 475 | `reference-semantics/semantics/float.k` | 44-44 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", F1:Float, F2:Float) =&gt; notBool (F1 ==Float F2) |
| 476 | `reference-semantics/semantics/float.k` | 50-50 | `syntax` | function, total, symbol(floatLt), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators] |
| 477 | `reference-semantics/semantics/float.k` | 51-51 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule floatLt(F1:Float, F2:Float) =&gt; F1 &lt;Float F2 [concrete] |
| 478 | `reference-semantics/semantics/float.k` | 52-52 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;", F1:Float, F2:Float) =&gt; floatLt(F1, F2) |
| 479 | `reference-semantics/semantics/float.k` | 54-54 | `syntax` | function, total, symbol(absF), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators] |
| 480 | `reference-semantics/semantics/float.k` | 55-55 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule absF(F:Float) =&gt; absFloat(F) [concrete] |
| 481 | `reference-semantics/semantics/float.k` | 56-56 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("abs", F:Float, .Vals) =&gt; absF(F) |
| 482 | `reference-semantics/semantics/float.k` | 61-61 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Import(_:String) =&gt; .K ... &lt;/k&gt; |
| 483 | `reference-semantics/semantics/float.k` | 65-65 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= "#mathCeil" |
| 484 | `reference-semantics/semantics/float.k` | 66-66 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) =&gt; E ~&gt; #mathCeil ... &lt;/k&gt; [priority(40)] |
| 485 | `reference-semantics/semantics/float.k` | 67-67 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V:Val ~&gt; #mathCeil =&gt; ceilF(V) ... &lt;/k&gt; |
| 486 | `reference-semantics/semantics/float.k` | 70-70 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= "#mathFloor" |
| 487 | `reference-semantics/semantics/float.k` | 71-71 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) =&gt; E ~&gt; #mathFloor ... &lt;/k&gt; [priority(40)] |
| 488 | `reference-semantics/semantics/float.k` | 72-72 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V:Val ~&gt; #mathFloor =&gt; floorFI(V) ... &lt;/k&gt; |
| 489 | `reference-semantics/semantics/float.k` | 73-73 | `syntax` | function, total, symbol(floorFI) | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)] |
| 490 | `reference-semantics/semantics/float.k` | 74-74 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule floorFI(I:Int)   =&gt; I                        [concrete] |
| 491 | `reference-semantics/semantics/float.k` | 75-75 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule floorFI(F:Float) =&gt; Float2Int(floorFloat(F)) [concrete] |
| 492 | `reference-semantics/semantics/float.k` | 78-78 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("floor", V:Val, .Vals) =&gt; floorFI(V) |
| 493 | `reference-semantics/semantics/float.k` | 79-79 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("ceil",  V:Val, .Vals) =&gt; ceilF(V) |
| 494 | `reference-semantics/semantics/float.k` | 82-82 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #mathPow1(Expr) &#124; #mathPow2(Val) |
| 495 | `reference-semantics/semantics/float.k` | 83-83 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) =&gt; E1 ~&gt; #mathPow1(E2) ... &lt;/k&gt; [priority(40)] |
| 496 | `reference-semantics/semantics/float.k` | 84-84 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V1:Val ~&gt; #mathPow1(E2:Expr) =&gt; E2 ~&gt; #mathPow2(V1) ... &lt;/k&gt; |
| 497 | `reference-semantics/semantics/float.k` | 85-85 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; V2:Val ~&gt; #mathPow2(V1:Val) =&gt; powF(toF(V1), toF(V2)) ... &lt;/k&gt; |
| 498 | `reference-semantics/semantics/float.k` | 86-86 | `syntax` | function, total, symbol(toF) | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Float ::= toF(Val) [function, total, symbol(toF)] |
| 499 | `reference-semantics/semantics/float.k` | 87-87 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule toF(F:Float) =&gt; F        [concrete] |
| 500 | `reference-semantics/semantics/float.k` | 88-88 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule toF(I:Int)   =&gt; intToF(I) [concrete] |
| 501 | `reference-semantics/semantics/float.k` | 93-93 | `syntax` | function, total, symbol(ceilF) | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)] |
| 502 | `reference-semantics/semantics/float.k` | 94-94 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule ceilF(I:Int)   =&gt; I                       [concrete] |
| 503 | `reference-semantics/semantics/float.k` | 95-95 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule ceilF(F:Float) =&gt; Float2Int(ceilFloat(F)) [concrete] |
| 504 | `reference-semantics/semantics/float.k` | 99-99 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyUn("-", F:Float) =&gt; 0.0 -Float F |
| 505 | `reference-semantics/semantics/float.k` | 103-103 | `syntax` | function, total, symbol(subF), no-evaluators | yes | USED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators] |
| 506 | `reference-semantics/semantics/float.k` | 104-104 | `rule` | concrete | yes | USED_FIXED_SUPPLIED_CONCRETE_RULE | rule subF(F1:Float, F2:Float) =&gt; F1 -Float F2 [concrete] |
| 507 | `reference-semantics/semantics/float.k` | 105-105 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("-", F1:Float, F2:Float) =&gt; subF(F1, F2) |
| 508 | `reference-semantics/semantics/float.k` | 107-107 | `syntax` | function, total, symbol(divF), no-evaluators | yes | USED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators] |
| 509 | `reference-semantics/semantics/float.k` | 108-108 | `rule` | concrete | yes | USED_FIXED_SUPPLIED_CONCRETE_RULE | rule divF(F1:Float, F2:Float) =&gt; F1 /Float F2 [concrete] |
| 510 | `reference-semantics/semantics/float.k` | 109-109 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("/", F1:Float, F2:Float) =&gt; divF(F1, F2) |
| 511 | `reference-semantics/semantics/float.k` | 111-111 | `syntax` | function, total, symbol(addF), no-evaluators | yes | USED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators] |
| 512 | `reference-semantics/semantics/float.k` | 112-112 | `rule` | concrete | yes | USED_FIXED_SUPPLIED_CONCRETE_RULE | rule addF(F1:Float, F2:Float) =&gt; F1 +Float F2 [concrete] |
| 513 | `reference-semantics/semantics/float.k` | 113-113 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+", F1:Float, F2:Float) =&gt; addF(F1, F2) |
| 514 | `reference-semantics/semantics/float.k` | 115-115 | `syntax` | function, total, symbol(mulF), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators] |
| 515 | `reference-semantics/semantics/float.k` | 116-116 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule mulF(F1:Float, F2:Float) =&gt; F1 *Float F2 [concrete] |
| 516 | `reference-semantics/semantics/float.k` | 117-117 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("*", F1:Float, F2:Float) =&gt; mulF(F1, F2) |
| 517 | `reference-semantics/semantics/float.k` | 119-119 | `syntax` | function, total, symbol(powF), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators] |
| 518 | `reference-semantics/semantics/float.k` | 120-120 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule powF(F1:Float, F2:Float) =&gt; F1 ^Float F2 [concrete] |
| 519 | `reference-semantics/semantics/float.k` | 121-121 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("**", F1:Float, F2:Float) =&gt; powF(F1, F2) |
| 520 | `reference-semantics/semantics/float.k` | 125-125 | `syntax` | function, total, symbol(gtF), no-evaluators | yes | USED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators] |
| 521 | `reference-semantics/semantics/float.k` | 126-126 | `rule` | concrete | yes | USED_FIXED_SUPPLIED_CONCRETE_RULE | rule gtF(F1:Float, F2:Float) =&gt; F1 &gt;Float F2 [concrete] |
| 522 | `reference-semantics/semantics/float.k` | 127-127 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;",  F1:Float, F2:Float) =&gt; gtF(F1, F2) |
| 523 | `reference-semantics/semantics/float.k` | 128-128 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;=", F1:Float, F2:Float) =&gt; notBool floatLt(F1, F2) |
| 524 | `reference-semantics/semantics/float.k` | 129-129 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;=", F1:Float, F2:Float) =&gt; notBool gtF(F1, F2) |
| 525 | `reference-semantics/semantics/float.k` | 132-132 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("**", I:Int, F:Float) =&gt; powF(intToF(I), F) |
| 526 | `reference-semantics/semantics/float.k` | 133-133 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("**", F:Float, I:Int) =&gt; powF(F, intToF(I)) |
| 527 | `reference-semantics/semantics/float.k` | 134-134 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("-",  I:Int, F:Float) =&gt; subF(intToF(I), F) |
| 528 | `reference-semantics/semantics/float.k` | 135-135 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("-",  F:Float, I:Int) =&gt; subF(F, intToF(I)) |
| 529 | `reference-semantics/semantics/float.k` | 136-136 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+",  I:Int, F:Float) =&gt; addF(intToF(I), F) |
| 530 | `reference-semantics/semantics/float.k` | 137-137 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+",  F:Float, I:Int) =&gt; addF(F, intToF(I)) |
| 531 | `reference-semantics/semantics/float.k` | 138-138 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("*",  I:Int, F:Float) =&gt; mulF(intToF(I), F) |
| 532 | `reference-semantics/semantics/float.k` | 139-139 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("*",  F:Float, I:Int) =&gt; mulF(F, intToF(I)) |
| 533 | `reference-semantics/semantics/float.k` | 142-142 | `syntax` | function, total, symbol(eqF), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators] |
| 534 | `reference-semantics/semantics/float.k` | 143-143 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule eqF(F1:Float, F2:Float) =&gt; F1 ==Float F2 [concrete] |
| 535 | `reference-semantics/semantics/float.k` | 144-144 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", I:Int, F:Float) =&gt; eqF(intToF(I), F) |
| 536 | `reference-semantics/semantics/float.k` | 145-145 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", F:Float, I:Int) =&gt; eqF(F, intToF(I)) |
| 537 | `reference-semantics/semantics/float.k` | 146-146 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", I:Int, F:Float) =&gt; notBool eqF(intToF(I), F) |
| 538 | `reference-semantics/semantics/float.k` | 147-147 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", F:Float, I:Int) =&gt; notBool eqF(F, intToF(I)) |
| 539 | `reference-semantics/semantics/float.k` | 148-148 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;",  I:Int, F:Float) =&gt; floatLt(intToF(I), F) |
| 540 | `reference-semantics/semantics/float.k` | 149-149 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;",  F:Float, I:Int) =&gt; floatLt(F, intToF(I)) |
| 541 | `reference-semantics/semantics/float.k` | 150-150 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;",  I:Int, F:Float) =&gt; gtF(intToF(I), F) |
| 542 | `reference-semantics/semantics/float.k` | 151-151 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;",  F:Float, I:Int) =&gt; gtF(F, intToF(I)) |
| 543 | `reference-semantics/semantics/float.k` | 154-154 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", V:Val, noneV) =&gt; V ==K noneV |
| 544 | `reference-semantics/semantics/float.k` | 155-155 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", V:Val, noneV) =&gt; notBool (V ==K noneV) |
| 545 | `reference-semantics/semantics/float.k` | 160-160 | `syntax` | function, total, symbol(decStrToF), no-evaluators | yes | USED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators] |
| 546 | `reference-semantics/semantics/float.k` | 161-161 | `rule` | concrete | yes | USED_FIXED_SUPPLIED_CONCRETE_RULE | rule decStrToF(iCons(45, CS:IntSeq)) =&gt; 0.0 -Float decStrToF(CS) [concrete] |
| 547 | `reference-semantics/semantics/float.k` | 162-164 | `rule` | concrete | yes | USED_FIXED_SUPPLIED_CONCRETE_RULE | rule decStrToF(CS:IntSeq) =&gt; intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) &gt;Int 0 andBool headIS(CS) =/=Int 45 [concrete] |
| 548 | `reference-semantics/semantics/float.k` | 165-165 | `syntax` | function | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= headIS(IntSeq) [function] |
| 549 | `reference-semantics/semantics/float.k` | 166-166 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule headIS(iCons(C:Int, _:IntSeq)) =&gt; C |
| 550 | `reference-semantics/semantics/float.k` | 167-167 | `syntax` | function, total, function, total | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= intPart(IntSeq) [function, total] &#124; intPartAcc(IntSeq, Int) [function, total] |
| 551 | `reference-semantics/semantics/float.k` | 168-168 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule intPart(CS:IntSeq) =&gt; intPartAcc(CS, 0) |
| 552 | `reference-semantics/semantics/float.k` | 169-169 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule intPartAcc(.IntSeq, A:Int) =&gt; A |
| 553 | `reference-semantics/semantics/float.k` | 170-170 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule intPartAcc(iCons(46, _:IntSeq), A:Int) =&gt; A |
| 554 | `reference-semantics/semantics/float.k` | 171-172 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) =&gt; intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46 |
| 555 | `reference-semantics/semantics/float.k` | 173-173 | `syntax` | function, total, function, total | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= fracPart(IntSeq) [function, total] &#124; fracAcc(IntSeq, Int) [function, total] |
| 556 | `reference-semantics/semantics/float.k` | 174-174 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracPart(.IntSeq) =&gt; 0 |
| 557 | `reference-semantics/semantics/float.k` | 175-175 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracPart(iCons(46, R:IntSeq)) =&gt; fracAcc(R, 0) |
| 558 | `reference-semantics/semantics/float.k` | 176-176 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracPart(iCons(C:Int, R:IntSeq)) =&gt; fracPart(R) requires C =/=Int 46 |
| 559 | `reference-semantics/semantics/float.k` | 177-177 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracAcc(.IntSeq, A:Int) =&gt; A |
| 560 | `reference-semantics/semantics/float.k` | 178-178 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) =&gt; fracAcc(R, A *Int 10 +Int (C -Int 48)) |
| 561 | `reference-semantics/semantics/float.k` | 179-179 | `syntax` | function, total, function, total | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= fracScale(IntSeq) [function, total] &#124; fscAcc(IntSeq, Int) [function, total] |
| 562 | `reference-semantics/semantics/float.k` | 180-180 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracScale(.IntSeq) =&gt; 1 |
| 563 | `reference-semantics/semantics/float.k` | 181-181 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracScale(iCons(46, R:IntSeq)) =&gt; fscAcc(R, 1) |
| 564 | `reference-semantics/semantics/float.k` | 182-182 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fracScale(iCons(C:Int, R:IntSeq)) =&gt; fracScale(R) requires C =/=Int 46 |
| 565 | `reference-semantics/semantics/float.k` | 183-183 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fscAcc(.IntSeq, A:Int) =&gt; A |
| 566 | `reference-semantics/semantics/float.k` | 184-184 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) =&gt; fscAcc(R, A *Int 10) |
| 567 | `reference-semantics/semantics/float.k` | 185-185 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("float", str(CS:IntSeq), .Vals) =&gt; decStrToF(CS) |
| 568 | `reference-semantics/semantics/float.k` | 186-186 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("float", I:Int, .Vals)          =&gt; intToF(I) |
| 569 | `reference-semantics/semantics/float.k` | 187-187 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("float", F:Float, .Vals)        =&gt; F |
| 570 | `reference-semantics/semantics/float.k` | 190-190 | `syntax` | function, total, symbol(divFloatIntV), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators] |
| 571 | `reference-semantics/semantics/float.k` | 191-191 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule divFloatIntV(F:Float, I:Int) =&gt; F /Float Int2Float(I, 53, 11) [concrete] |
| 572 | `reference-semantics/semantics/float.k` | 192-192 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("/", F:Float, I:Int) =&gt; divFloatIntV(F, I) |
| 573 | `reference-semantics/semantics/float.k` | 195-195 | `syntax` | function, total, symbol(intToF), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators] |
| 574 | `reference-semantics/semantics/float.k` | 196-196 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule intToF(I:Int) =&gt; Int2Float(I, 53, 11) [concrete] |
| 575 | `reference-semantics/semantics/float.k` | 197-197 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+", I:Int, F:Float) =&gt; addF(intToF(I), F) |
| 576 | `reference-semantics/semantics/float.k` | 198-198 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+", F:Float, I:Int) =&gt; addF(F, intToF(I)) |
| 577 | `reference-semantics/semantics/float.k` | 199-199 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("-", I:Int, F:Float) =&gt; subF(intToF(I), F) |
| 578 | `reference-semantics/semantics/float.k` | 200-200 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("-", F:Float, I:Int) =&gt; subF(F, intToF(I)) |
| 579 | `reference-semantics/semantics/float.k` | 201-201 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("*", I:Int, F:Float) =&gt; mulF(intToF(I), F) |
| 580 | `reference-semantics/semantics/float.k` | 202-202 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("*", F:Float, I:Int) =&gt; mulF(F, intToF(I)) |
| 581 | `reference-semantics/semantics/float.k` | 203-203 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;", I:Int, F:Float) =&gt; floatLt(intToF(I), F) |
| 582 | `reference-semantics/semantics/float.k` | 204-204 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;", F:Float, I:Int) =&gt; floatLt(F, intToF(I)) |
| 583 | `reference-semantics/semantics/float.k` | 205-205 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;", I:Int, F:Float) =&gt; gtF(intToF(I), F) |
| 584 | `reference-semantics/semantics/float.k` | 206-206 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;", F:Float, I:Int) =&gt; gtF(F, intToF(I)) |
| 585 | `reference-semantics/semantics/float.k` | 209-209 | `syntax` | function, total, symbol(truncF), no-evaluators | yes | USED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators] |
| 586 | `reference-semantics/semantics/float.k` | 210-210 | `rule` | concrete | yes | USED_FIXED_SUPPLIED_CONCRETE_RULE | rule truncF(F:Float) =&gt; #if F &gt;=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete] |
| 587 | `reference-semantics/semantics/float.k` | 211-211 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("int", F:Float, .Vals) =&gt; truncF(F) |
| 588 | `reference-semantics/semantics/float.k` | 213-213 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("float", I:Int, .Vals)   =&gt; intToF(I) |
| 589 | `reference-semantics/semantics/float.k` | 214-214 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("float", F:Float, .Vals) =&gt; F |
| 590 | `reference-semantics/semantics/float.k` | 217-217 | `syntax` | function, total, symbol(roundF), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators] |
| 591 | `reference-semantics/semantics/float.k` | 218-222 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule roundF(F:Float) =&gt; #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete] |
| 592 | `reference-semantics/semantics/float.k` | 223-223 | `syntax` | function, total, symbol(roundFN), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators] |
| 593 | `reference-semantics/semantics/float.k` | 224-226 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule roundFN(F:Float, N:Int) =&gt; Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete] |
| 594 | `reference-semantics/semantics/float.k` | 227-227 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("round", F:Float, .Vals)        =&gt; roundF(F) |
| 595 | `reference-semantics/semantics/float.k` | 228-228 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBuiltin("round", F:Float, N:Int, .Vals) =&gt; roundFN(F, N) |
| 596 | `reference-semantics/semantics/float.k` | 230-230 | `syntax` | function, total, symbol(sqrtF), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators] |
| 597 | `reference-semantics/semantics/float.k` | 231-231 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule sqrtF(F:Float) =&gt; sqrtFloat(F) [concrete] |
| 598 | `reference-semantics/semantics/float.k` | 232-232 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= "#mathSqrt" |
| 599 | `reference-semantics/semantics/float.k` | 233-233 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) =&gt; E ~&gt; #mathSqrt ... &lt;/k&gt; [priority(40)] |
| 600 | `reference-semantics/semantics/float.k` | 234-234 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; F:Float ~&gt; #mathSqrt =&gt; sqrtF(F) ... &lt;/k&gt; |
| 601 | `reference-semantics/semantics/float.k` | 235-235 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; I:Int ~&gt; #mathSqrt =&gt; sqrtF(intToF(I)) ... &lt;/k&gt; |
| 602 | `reference-semantics/semantics/float.k` | 243-243 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #maxAccF(Iterable, Float) &#124; #maxContF(Float) |
| 603 | `reference-semantics/semantics/float.k` | 244-244 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #maxCont0 =&gt; #maxAccF(R, {V}:&gt;Float) ... &lt;/k&gt; requires isFloat(V) |
| 604 | `reference-semantics/semantics/float.k` | 245-245 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #maxAccF(IT:Iterable, M:Float) =&gt; #iterNext(IT) ~&gt; #maxContF(M) ... &lt;/k&gt; |
| 605 | `reference-semantics/semantics/float.k` | 246-246 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #maxContF(M:Float) =&gt; M ... &lt;/k&gt; |
| 606 | `reference-semantics/semantics/float.k` | 247-248 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #maxContF(M:Float) =&gt; #maxAccF(R, maxFloat(M, {V}:&gt;Float)) ... &lt;/k&gt; requires isFloat(V) |
| 607 | `reference-semantics/semantics/float.k` | 250-250 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #minAccF(Iterable, Float) &#124; #minContF(Float) |
| 608 | `reference-semantics/semantics/float.k` | 251-251 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #minCont0 =&gt; #minAccF(R, {V}:&gt;Float) ... &lt;/k&gt; requires isFloat(V) |
| 609 | `reference-semantics/semantics/float.k` | 252-252 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #minAccF(IT:Iterable, M:Float) =&gt; #iterNext(IT) ~&gt; #minContF(M) ... &lt;/k&gt; |
| 610 | `reference-semantics/semantics/float.k` | 253-253 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #minContF(M:Float) =&gt; M ... &lt;/k&gt; |
| 611 | `reference-semantics/semantics/float.k` | 254-255 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #minContF(M:Float) =&gt; #minAccF(R, minFloat(M, {V}:&gt;Float)) ... &lt;/k&gt; requires isFloat(V) |
| 612 | `reference-semantics/semantics/float.k` | 261-261 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #sumAccF(Iterable, Float) &#124; #sumContF(Float) |
| 613 | `reference-semantics/semantics/float.k` | 262-264 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #sumCont(ACC:Int) =&gt; #sumAccF(R, addF(intToF(ACC), {V}:&gt;Float)) ... &lt;/k&gt; requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V)) |
| 614 | `reference-semantics/semantics/float.k` | 265-265 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #sumAccF(IT:Iterable, ACC:Float) =&gt; #iterNext(IT) ~&gt; #sumContF(ACC) ... &lt;/k&gt; |
| 615 | `reference-semantics/semantics/float.k` | 266-266 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #sumContF(ACC:Float) =&gt; ACC ... &lt;/k&gt; |
| 616 | `reference-semantics/semantics/float.k` | 267-269 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #sumContF(ACC:Float) =&gt; #sumAccF(R, addF(ACC, {V}:&gt;Float)) ... &lt;/k&gt; requires isFloat(V) |
| 617 | `reference-semantics/semantics/float.k` | 270-272 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(V:Val, R:Iterable) ~&gt; #sumContF(ACC:Float) =&gt; #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... &lt;/k&gt; requires isInt(V) orBool isBool(V) |
| 618 | `reference-semantics/semantics/float.k` | 273-273 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 619 | `reference-semantics/semantics/functions.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-FUNCTIONS |
| 620 | `reference-semantics/semantics/functions.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 621 | `reference-semantics/semantics/functions.k` | 8-11 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) &#124; #bindP(ParamNames, Vals) &#124; "#pop" &#124; "#endcall" |
| 622 | `reference-semantics/semantics/functions.k` | 14-16 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) =&gt; .K ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ F &lt;- closureVal(PNS, BODY, L) ], _) ... &lt;/scopes&gt; |
| 623 | `reference-semantics/semantics/functions.k` | 18-18 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Expr ::= closureExpr(ParamNames, Stmts) |
| 624 | `reference-semantics/semantics/functions.k` | 19-20 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; closureExpr(PNS:ParamNames, BODY:Stmts) =&gt; closureVal(PNS, BODY, L) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; |
| 625 | `reference-semantics/semantics/functions.k` | 27-27 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) |
| 626 | `reference-semantics/semantics/functions.k` | 31-32 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) &#124; #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map) |
| 627 | `reference-semantics/semantics/functions.k` | 33-35 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) =&gt; #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... &lt;/k&gt; |
| 628 | `reference-semantics/semantics/functions.k` | 36-41 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) =&gt; #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV &lt;- {M[FV]}:&gt;Val ]) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; requires FV in_keys(M) |
| 629 | `reference-semantics/semantics/functions.k` | 42-45 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) =&gt; .K ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ F &lt;- closureValC(PNS, CVS, BODY, CM) ], _) ... &lt;/scopes&gt; |
| 630 | `reference-semantics/semantics/functions.k` | 47-49 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Lambda(Params(PNS:ParamNames), E:Expr) =&gt; closureVal(PNS, Return(E) .Stmts, L) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; |
| 631 | `reference-semantics/semantics/functions.k` | 50-52 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) =&gt; #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... &lt;/k&gt; |
| 632 | `reference-semantics/semantics/functions.k` | 53-58 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) =&gt; #mkLambda(PNS, CVS, FVR, BODY, CM [ FV &lt;- {M[FV]}:&gt;Val ]) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; requires FV in_keys(M) |
| 633 | `reference-semantics/semantics/functions.k` | 59-60 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) =&gt; closureValC(PNS, CVS, BODY, CM) ... &lt;/k&gt; |
| 634 | `reference-semantics/semantics/functions.k` | 63-63 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindP(.ParamNames, .Vals) =&gt; .K ... &lt;/k&gt; |
| 635 | `reference-semantics/semantics/functions.k` | 64-66 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) =&gt; #bindP(PS, VS) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ P &lt;- V ], _) ... &lt;/scopes&gt; |
| 636 | `reference-semantics/semantics/functions.k` | 68-75 | `rule` | priority(40) | yes | USED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) =&gt; #cellW({M[P]}:&gt;Val, V) ~&gt; #bindP(PS, VS) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:&gt;Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:&gt;Val) [priority(40)] |
| 637 | `reference-semantics/semantics/functions.k` | 78-79 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Return(V:Val) ~&gt; _ =&gt; #pop &lt;/k&gt; &lt;ret&gt; noRet =&gt; retV(V) &lt;/ret&gt; |
| 638 | `reference-semantics/semantics/functions.k` | 80-81 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #endcall =&gt; #pop ... &lt;/k&gt; &lt;ret&gt; noRet =&gt; retV(noneV) &lt;/ret&gt; |
| 639 | `reference-semantics/semantics/functions.k` | 85-90 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #pop =&gt; V ~&gt; CONT &lt;/k&gt; &lt;ret&gt;   retV(V) =&gt; noRet &lt;/ret&gt; &lt;stack&gt; ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) =&gt; .List ... &lt;/stack&gt; &lt;env&gt;   L:Int =&gt; CALLERL &lt;/env&gt; &lt;scopes&gt; SC:Map =&gt; SC [ L &lt;- undef ] &lt;/scopes&gt; &lt;scopeLoc&gt; _ =&gt; SAVEDL &lt;/scopeLoc&gt; |
| 640 | `reference-semantics/semantics/functions.k` | 91-91 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 641 | `reference-semantics/semantics/int.k` | 4-4 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-INT |
| 642 | `reference-semantics/semantics/int.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 643 | `reference-semantics/semantics/int.k` | 7-7 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyUn("-", I:Int) =&gt; 0 -Int I |
| 644 | `reference-semantics/semantics/int.k` | 9-9 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+",  I1:Int, I2:Int) =&gt; I1 +Int I2 |
| 645 | `reference-semantics/semantics/int.k` | 11-11 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+",  I:Int, B:Bool) =&gt; I +Int #if B #then 1 #else 0 #fi |
| 646 | `reference-semantics/semantics/int.k` | 12-12 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+",  B:Bool, I:Int) =&gt; #if B #then 1 #else 0 #fi +Int I |
| 647 | `reference-semantics/semantics/int.k` | 13-13 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("-",  I1:Int, I2:Int) =&gt; I1 -Int I2 |
| 648 | `reference-semantics/semantics/int.k` | 14-14 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("*",  I1:Int, I2:Int) =&gt; I1 *Int I2 |
| 649 | `reference-semantics/semantics/int.k` | 15-15 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("%",  I1:Int, I2:Int) =&gt; pyMod(I1, I2) |
| 650 | `reference-semantics/semantics/int.k` | 16-16 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("//", I1:Int, I2:Int) =&gt; (I1 -Int pyMod(I1, I2)) /Int I2 |
| 651 | `reference-semantics/semantics/int.k` | 17-17 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("**", I1:Int, I2:Int) =&gt; I1 ^Int I2 requires I2 &gt;=Int 0 |
| 652 | `reference-semantics/semantics/int.k` | 19-19 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= pyMod(Int, Int) [function] |
| 653 | `reference-semantics/semantics/int.k` | 20-20 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule pyMod(I1:Int, I2:Int) =&gt; ((I1 %Int I2) +Int I2) %Int I2 |
| 654 | `reference-semantics/semantics/int.k` | 22-22 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;",  I1:Int, I2:Int)   =&gt; I1 &lt;Int  I2 |
| 655 | `reference-semantics/semantics/int.k` | 23-23 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;=", I1:Int, I2:Int)   =&gt; I1 &lt;=Int I2 |
| 656 | `reference-semantics/semantics/int.k` | 24-24 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;",  I1:Int, I2:Int)   =&gt; I1 &gt;Int  I2 |
| 657 | `reference-semantics/semantics/int.k` | 25-25 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;=", I1:Int, I2:Int)   =&gt; I1 &gt;=Int I2 |
| 658 | `reference-semantics/semantics/int.k` | 26-26 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", I1:Int, I2:Int)   =&gt; I1 ==Int I2 |
| 659 | `reference-semantics/semantics/int.k` | 27-27 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", I1:Int, I2:Int)   =&gt; I1 =/=Int I2 |
| 660 | `reference-semantics/semantics/int.k` | 28-28 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 661 | `reference-semantics/semantics/iter.k` | 6-6 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-ITER |
| 662 | `reference-semantics/semantics/iter.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 663 | `reference-semantics/semantics/iter.k` | 8-8 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #iterNext(Iterable) &#124; "#iterDone" &#124; #iterYield(Val, Iterable) |
| 664 | `reference-semantics/semantics/iter.k` | 9-9 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 665 | `reference-semantics/semantics/list.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-LIST |
| 666 | `reference-semantics/semantics/list.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 667 | `reference-semantics/semantics/list.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 668 | `reference-semantics/semantics/list.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-OPERATORS |
| 669 | `reference-semantics/semantics/list.k` | 9-9 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(list(.ValSeq))                =&gt; #iterDone ... &lt;/k&gt; |
| 670 | `reference-semantics/semantics/list.k` | 10-10 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(list(vCons(V:Val, R:ValSeq))) =&gt; #iterYield(V, list(R)) ... &lt;/k&gt; |
| 671 | `reference-semantics/semantics/list.k` | 13-13 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ApplyK ::= "toList" |
| 672 | `reference-semantics/semantics/list.k` | 14-14 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; ListExpr(ES:Exprs) =&gt; #evalArgs(ES, .Vals, toList) ... &lt;/k&gt; |
| 673 | `reference-semantics/semantics/list.k` | 15-15 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toList, ACC:Vals) =&gt; #alloc(list(vals2valSeq(ACC))) ... &lt;/k&gt; |
| 674 | `reference-semantics/semantics/list.k` | 18-18 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total] |
| 675 | `reference-semantics/semantics/list.k` | 19-19 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule valSeqConcat(.ValSeq, T:ValSeq)                =&gt; T |
| 676 | `reference-semantics/semantics/list.k` | 20-20 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) =&gt; vCons(V, valSeqConcat(S, T)) |
| 677 | `reference-semantics/semantics/list.k` | 24-25 | `rule` | priority(45) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BinOp("+", list(A:ValSeq), list(B:ValSeq)) =&gt; #alloc(list(valSeqConcat(A, B))) ... &lt;/k&gt; [priority(45)] |
| 678 | `reference-semantics/semantics/list.k` | 27-27 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) =&gt; A ==K B |
| 679 | `reference-semantics/semantics/list.k` | 28-28 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) =&gt; notBool (A ==K B) |
| 680 | `reference-semantics/semantics/list.k` | 33-33 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= hasRefVS(ValSeq) [function, total] |
| 681 | `reference-semantics/semantics/list.k` | 34-34 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule hasRefVS(.ValSeq)                =&gt; false |
| 682 | `reference-semantics/semantics/list.k` | 35-35 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule hasRefVS(vCons(V:Val, R:ValSeq)) =&gt; isRefV(V) orBool hasRefVS(R) |
| 683 | `reference-semantics/semantics/list.k` | 37-38 | `syntax` | function, function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] &#124; deepEqV(Val, Val, Map)        [function] |
| 684 | `reference-semantics/semantics/list.k` | 39-39 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   =&gt; true |
| 685 | `reference-semantics/semantics/list.k` | 40-40 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    =&gt; false |
| 686 | `reference-semantics/semantics/list.k` | 41-41 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    =&gt; false |
| 687 | `reference-semantics/semantics/list.k` | 42-43 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) =&gt; deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP) |
| 688 | `reference-semantics/semantics/list.k` | 45-46 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqV(ref(H:Int), B:Val, HP:Map) =&gt; deepEqV({HP[H]}:&gt;Val, B, HP) requires H in_keys(HP) |
| 689 | `reference-semantics/semantics/list.k` | 47-48 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqV(A:Val, ref(H:Int), HP:Map) =&gt; deepEqV(A, {HP[H]}:&gt;Val, HP) requires notBool isRefV(A) andBool H in_keys(HP) |
| 690 | `reference-semantics/semantics/list.k` | 49-49 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) =&gt; deepEqVS(A, B, HP) |
| 691 | `reference-semantics/semantics/list.k` | 50-50 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule deepEqV(A:Val, B:Val, _:Map) =&gt; A ==K B [owise] |
| 692 | `reference-semantics/semantics/list.k` | 53-55 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) =&gt; noneV ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; list(VS:ValSeq =&gt; valSeqConcat(VS, vCons(V, .ValSeq))) ... &lt;/heap&gt; [priority(40)] |
| 693 | `reference-semantics/semantics/list.k` | 58-58 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #memberAcc(Val, Iterable) &#124; #memberCont(Val) &#124; "#notB" |
| 694 | `reference-semantics/semantics/list.k` | 59-59 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) =&gt; #memberAcc(LV, list(VS)) ... &lt;/k&gt; |
| 695 | `reference-semantics/semantics/list.k` | 60-60 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) =&gt; #memberAcc(LV, list(VS)) ~&gt; #notB ... &lt;/k&gt; |
| 696 | `reference-semantics/semantics/list.k` | 61-61 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #memberAcc(V:Val, IT:Iterable) =&gt; #iterNext(IT) ~&gt; #memberCont(V) ... &lt;/k&gt; |
| 697 | `reference-semantics/semantics/list.k` | 62-62 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterDone ~&gt; #memberCont(_V:Val) =&gt; false ... &lt;/k&gt; |
| 698 | `reference-semantics/semantics/list.k` | 63-64 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(E:Val, _:Iterable) ~&gt; #memberCont(V:Val) =&gt; true ... &lt;/k&gt; requires E ==K V |
| 699 | `reference-semantics/semantics/list.k` | 65-66 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterYield(E:Val, R:Iterable) ~&gt; #memberCont(V:Val) =&gt; #memberAcc(V, R) ... &lt;/k&gt; requires notBool (E ==K V) |
| 700 | `reference-semantics/semantics/list.k` | 67-67 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; B:Bool ~&gt; #notB =&gt; notBool B ... &lt;/k&gt; |
| 701 | `reference-semantics/semantics/list.k` | 68-68 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 702 | `reference-semantics/semantics/methods.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-METHODS |
| 703 | `reference-semantics/semantics/methods.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 704 | `reference-semantics/semantics/methods.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports K-EQUAL |
| 705 | `reference-semantics/semantics/methods.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-STR |
| 706 | `reference-semantics/semantics/methods.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-LIST |
| 707 | `reference-semantics/semantics/methods.k` | 10-10 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= applyMethod(Val, String, Vals) [function] |
| 708 | `reference-semantics/semantics/methods.k` | 13-13 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "isupper", .Vals) =&gt; hasUpper(CS) andBool notBool hasLower(CS) |
| 709 | `reference-semantics/semantics/methods.k` | 14-14 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "islower", .Vals) =&gt; hasLower(CS) andBool notBool hasUpper(CS) |
| 710 | `reference-semantics/semantics/methods.k` | 15-15 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) =&gt; notBool (CS ==K .IntSeq) andBool allAlpha(CS) |
| 711 | `reference-semantics/semantics/methods.k` | 16-16 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) =&gt; notBool (CS ==K .IntSeq) andBool allDigit(CS) |
| 712 | `reference-semantics/semantics/methods.k` | 19-19 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "lower",    .Vals) =&gt; str(mapLower(CS)) |
| 713 | `reference-semantics/semantics/methods.k` | 20-20 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "upper",    .Vals) =&gt; str(mapUpper(CS)) |
| 714 | `reference-semantics/semantics/methods.k` | 21-21 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) =&gt; str(mapSwap(CS)) |
| 715 | `reference-semantics/semantics/methods.k` | 26-26 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) =&gt; str(joinCodes(SEP, VS)) |
| 716 | `reference-semantics/semantics/methods.k` | 27-27 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total] |
| 717 | `reference-semantics/semantics/methods.k` | 28-28 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule joinCodes(_:IntSeq, .ValSeq) =&gt; .IntSeq |
| 718 | `reference-semantics/semantics/methods.k` | 29-29 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) =&gt; CS |
| 719 | `reference-semantics/semantics/methods.k` | 30-31 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) =&gt; seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) |
| 720 | `reference-semantics/semantics/methods.k` | 34-34 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) =&gt; cntSub(CS, PC) |
| 721 | `reference-semantics/semantics/methods.k` | 35-35 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= cntSub(IntSeq, IntSeq) [function] |
| 722 | `reference-semantics/semantics/methods.k` | 36-36 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule cntSub(.IntSeq, _:IntSeq) =&gt; 0 |
| 723 | `reference-semantics/semantics/methods.k` | 37-38 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) =&gt; 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) &gt;Int 0 |
| 724 | `reference-semantics/semantics/methods.k` | 39-40 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) =&gt; cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) &lt;=Int 0 |
| 725 | `reference-semantics/semantics/methods.k` | 41-41 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= dropIS(IntSeq, Int) [function, total] |
| 726 | `reference-semantics/semantics/methods.k` | 42-42 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dropIS(S:IntSeq, N:Int) =&gt; S requires N &lt;=Int 0 |
| 727 | `reference-semantics/semantics/methods.k` | 43-43 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dropIS(.IntSeq, _:Int) =&gt; .IntSeq [owise] |
| 728 | `reference-semantics/semantics/methods.k` | 44-44 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dropIS(iCons(_:Int, R:IntSeq), N:Int) =&gt; dropIS(R, N -Int 1) requires N &gt;Int 0 |
| 729 | `reference-semantics/semantics/methods.k` | 47-47 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "strip", .Vals) =&gt; str(revIS(trimWS(revIS(trimWS(CS))))) |
| 730 | `reference-semantics/semantics/methods.k` | 48-48 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= trimWS(IntSeq) [function, total] |
| 731 | `reference-semantics/semantics/methods.k` | 49-49 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule trimWS(.IntSeq) =&gt; .IntSeq |
| 732 | `reference-semantics/semantics/methods.k` | 50-50 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule trimWS(iCons(C:Int, R:IntSeq)) =&gt; trimWS(R) requires isWSC(C) |
| 733 | `reference-semantics/semantics/methods.k` | 51-51 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule trimWS(iCons(C:Int, R:IntSeq)) =&gt; iCons(C, R) requires notBool isWSC(C) |
| 734 | `reference-semantics/semantics/methods.k` | 52-52 | `syntax` | function, total, function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= revIS(IntSeq) [function, total] &#124; revISAcc(IntSeq, IntSeq) [function, total] |
| 735 | `reference-semantics/semantics/methods.k` | 53-53 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule revIS(S:IntSeq) =&gt; revISAcc(S, .IntSeq) |
| 736 | `reference-semantics/semantics/methods.k` | 54-54 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule revISAcc(.IntSeq, A:IntSeq) =&gt; A |
| 737 | `reference-semantics/semantics/methods.k` | 55-55 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) =&gt; revISAcc(R, iCons(C, A)) |
| 738 | `reference-semantics/semantics/methods.k` | 58-58 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) =&gt; str(CS) |
| 739 | `reference-semantics/semantics/methods.k` | 61-61 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) =&gt; startsWith(PC, XC) |
| 740 | `reference-semantics/semantics/methods.k` | 64-64 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) =&gt; cntOccVS(VS, V) |
| 741 | `reference-semantics/semantics/methods.k` | 65-65 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= cntOccVS(ValSeq, Val) [function, total] |
| 742 | `reference-semantics/semantics/methods.k` | 66-66 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule cntOccVS(.ValSeq, _:Val)                =&gt; 0 |
| 743 | `reference-semantics/semantics/methods.k` | 67-67 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) =&gt; 1 +Int cntOccVS(R, V) requires A ==K V |
| 744 | `reference-semantics/semantics/methods.k` | 68-68 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) =&gt; cntOccVS(R, V)        requires notBool (A ==K V) |
| 745 | `reference-semantics/semantics/methods.k` | 72-74 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) =&gt; #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... &lt;/k&gt; [priority(40)] |
| 746 | `reference-semantics/semantics/methods.k` | 75-75 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result |
| 747 | `reference-semantics/semantics/methods.k` | 76-76 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) =&gt; flushTok(ACC, CUR) |
| 748 | `reference-semantics/semantics/methods.k` | 77-78 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) =&gt; splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C) |
| 749 | `reference-semantics/semantics/methods.k` | 79-80 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) =&gt; splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) |
| 750 | `reference-semantics/semantics/methods.k` | 82-82 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function] |
| 751 | `reference-semantics/semantics/methods.k` | 83-83 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule flushTok(ACC:ValSeq, .IntSeq)            =&gt; ACC |
| 752 | `reference-semantics/semantics/methods.k` | 84-84 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) =&gt; valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq)) |
| 753 | `reference-semantics/semantics/methods.k` | 85-85 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isWSC(Int) [function, total] |
| 754 | `reference-semantics/semantics/methods.k` | 86-86 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isWSC(C:Int) =&gt; C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 |
| 755 | `reference-semantics/semantics/methods.k` | 89-91 | `rule` | priority(39) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) =&gt; #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... &lt;/k&gt; [priority(39)] |
| 756 | `reference-semantics/semantics/methods.k` | 94-96 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) =&gt; #alloc(list(splitSep(CS, SEP, .IntSeq))) ... &lt;/k&gt; [priority(40)] |
| 757 | `reference-semantics/semantics/methods.k` | 97-97 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token |
| 758 | `reference-semantics/semantics/methods.k` | 98-98 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              =&gt; vCons(str(CUR), .ValSeq) |
| 759 | `reference-semantics/semantics/methods.k` | 99-100 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) =&gt; vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP |
| 760 | `reference-semantics/semantics/methods.k` | 101-102 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) =&gt; splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP) |
| 761 | `reference-semantics/semantics/methods.k` | 104-105 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) =&gt; str(replaceC(CS, A, B)) |
| 762 | `reference-semantics/semantics/methods.k` | 106-106 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total] |
| 763 | `reference-semantics/semantics/methods.k` | 107-107 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule replaceC(.IntSeq, _:Int, _:Int)             =&gt; .IntSeq |
| 764 | `reference-semantics/semantics/methods.k` | 108-108 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) =&gt; iCons(B, replaceC(R, A, B)) requires C ==Int A |
| 765 | `reference-semantics/semantics/methods.k` | 109-109 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) =&gt; iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) |
| 766 | `reference-semantics/semantics/methods.k` | 112-112 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isUpperC(Int) [function, total] |
| 767 | `reference-semantics/semantics/methods.k` | 113-113 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isUpperC(C:Int) =&gt; C &gt;=Int 65 andBool C &lt;=Int 90 |
| 768 | `reference-semantics/semantics/methods.k` | 115-115 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isLowerC(Int) [function, total] |
| 769 | `reference-semantics/semantics/methods.k` | 116-116 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isLowerC(C:Int) =&gt; C &gt;=Int 97 andBool C &lt;=Int 122 |
| 770 | `reference-semantics/semantics/methods.k` | 118-118 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isAlphaC(Int) [function, total] |
| 771 | `reference-semantics/semantics/methods.k` | 119-119 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isAlphaC(C:Int) =&gt; isUpperC(C) orBool isLowerC(C) |
| 772 | `reference-semantics/semantics/methods.k` | 121-121 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= isDigitC(Int) [function, total] |
| 773 | `reference-semantics/semantics/methods.k` | 122-122 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule isDigitC(C:Int) =&gt; C &gt;=Int 48 andBool C &lt;=Int 57 |
| 774 | `reference-semantics/semantics/methods.k` | 124-124 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= hasUpper(IntSeq) [function, total] |
| 775 | `reference-semantics/semantics/methods.k` | 125-125 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule hasUpper(.IntSeq) =&gt; false |
| 776 | `reference-semantics/semantics/methods.k` | 126-126 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule hasUpper(iCons(C:Int, S:IntSeq)) =&gt; isUpperC(C) orBool hasUpper(S) |
| 777 | `reference-semantics/semantics/methods.k` | 128-128 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= hasLower(IntSeq) [function, total] |
| 778 | `reference-semantics/semantics/methods.k` | 129-129 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule hasLower(.IntSeq) =&gt; false |
| 779 | `reference-semantics/semantics/methods.k` | 130-130 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule hasLower(iCons(C:Int, S:IntSeq)) =&gt; isLowerC(C) orBool hasLower(S) |
| 780 | `reference-semantics/semantics/methods.k` | 132-132 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= allAlpha(IntSeq) [function, total] |
| 781 | `reference-semantics/semantics/methods.k` | 133-133 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule allAlpha(.IntSeq) =&gt; true |
| 782 | `reference-semantics/semantics/methods.k` | 134-134 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule allAlpha(iCons(C:Int, S:IntSeq)) =&gt; isAlphaC(C) andBool allAlpha(S) |
| 783 | `reference-semantics/semantics/methods.k` | 136-136 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= allDigit(IntSeq) [function, total] |
| 784 | `reference-semantics/semantics/methods.k` | 137-137 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule allDigit(.IntSeq) =&gt; true |
| 785 | `reference-semantics/semantics/methods.k` | 138-138 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule allDigit(iCons(C:Int, S:IntSeq)) =&gt; isDigitC(C) andBool allDigit(S) |
| 786 | `reference-semantics/semantics/methods.k` | 140-140 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= lowerC(Int) [function, total] |
| 787 | `reference-semantics/semantics/methods.k` | 142-142 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule lowerC(C:Int) =&gt; C +Int 32 requires isUpperC(C) |
| 788 | `reference-semantics/semantics/methods.k` | 143-143 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule lowerC(C:Int) =&gt; C         [owise] |
| 789 | `reference-semantics/semantics/methods.k` | 145-145 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= upperC(Int) [function, total] |
| 790 | `reference-semantics/semantics/methods.k` | 146-146 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule upperC(C:Int) =&gt; C -Int 32 requires isLowerC(C) |
| 791 | `reference-semantics/semantics/methods.k` | 147-147 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule upperC(C:Int) =&gt; C         [owise] |
| 792 | `reference-semantics/semantics/methods.k` | 149-149 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= swapC(Int) [function, total] |
| 793 | `reference-semantics/semantics/methods.k` | 150-150 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule swapC(C:Int) =&gt; C +Int 32 requires isUpperC(C) |
| 794 | `reference-semantics/semantics/methods.k` | 151-151 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule swapC(C:Int) =&gt; C -Int 32 requires isLowerC(C) |
| 795 | `reference-semantics/semantics/methods.k` | 152-152 | `rule` | owise | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule swapC(C:Int) =&gt; C         [owise] |
| 796 | `reference-semantics/semantics/methods.k` | 154-154 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= mapLower(IntSeq) [function, total] |
| 797 | `reference-semantics/semantics/methods.k` | 155-155 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapLower(.IntSeq) =&gt; .IntSeq |
| 798 | `reference-semantics/semantics/methods.k` | 156-156 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapLower(iCons(C:Int, S:IntSeq)) =&gt; iCons(lowerC(C), mapLower(S)) |
| 799 | `reference-semantics/semantics/methods.k` | 158-158 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= mapUpper(IntSeq) [function, total] |
| 800 | `reference-semantics/semantics/methods.k` | 159-159 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapUpper(.IntSeq) =&gt; .IntSeq |
| 801 | `reference-semantics/semantics/methods.k` | 160-160 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapUpper(iCons(C:Int, S:IntSeq)) =&gt; iCons(upperC(C), mapUpper(S)) |
| 802 | `reference-semantics/semantics/methods.k` | 162-162 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= mapSwap(IntSeq) [function, total] |
| 803 | `reference-semantics/semantics/methods.k` | 163-163 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapSwap(.IntSeq) =&gt; .IntSeq |
| 804 | `reference-semantics/semantics/methods.k` | 164-164 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule mapSwap(iCons(C:Int, S:IntSeq)) =&gt; iCons(swapC(C), mapSwap(S)) |
| 805 | `reference-semantics/semantics/methods.k` | 166-166 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total] |
| 806 | `reference-semantics/semantics/methods.k` | 167-167 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule startsWith(.IntSeq, _:IntSeq)               =&gt; true |
| 807 | `reference-semantics/semantics/methods.k` | 168-168 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) =&gt; false |
| 808 | `reference-semantics/semantics/methods.k` | 169-169 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) =&gt; A ==Int B andBool startsWith(As, Bs) |
| 809 | `reference-semantics/semantics/methods.k` | 170-170 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 810 | `reference-semantics/semantics/operators.k` | 6-6 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-OPERATORS |
| 811 | `reference-semantics/semantics/operators.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 812 | `reference-semantics/semantics/operators.k` | 8-8 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 813 | `reference-semantics/semantics/operators.k` | 10-10 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; UnaryOp(OP:String, V:Val) =&gt; applyUn(OP, V) ... &lt;/k&gt; |
| 814 | `reference-semantics/semantics/operators.k` | 12-12 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; BinOp(OP:String, L:Val, R:Val) =&gt; applyBin(OP, L, R) ... &lt;/k&gt; |
| 815 | `reference-semantics/semantics/operators.k` | 15-15 | `context` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | context Compare(HOLE, _) |
| 816 | `reference-semantics/semantics/operators.k` | 16-16 | `context` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | context Compare(_:Val, CmpOp(_, HOLE)) |
| 817 | `reference-semantics/semantics/operators.k` | 17-17 | `rule` | owise | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Compare(LV:Val, CmpOp(OP:String, RV:Val)) =&gt; applyCmp(OP, LV, RV) ... &lt;/k&gt; [owise] |
| 818 | `reference-semantics/semantics/operators.k` | 19-19 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("is",     V:Val, noneV) =&gt; V ==K noneV |
| 819 | `reference-semantics/semantics/operators.k` | 20-20 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("is not", V:Val, noneV) =&gt; notBool (V ==K noneV) |
| 820 | `reference-semantics/semantics/operators.k` | 25-27 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BinOp(OP:String, ref(H:Int), R:Expr) =&gt; BinOp(OP, V, R) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 821 | `reference-semantics/semantics/operators.k` | 28-31 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; BinOp(OP:String, L:Val, ref(H:Int)) =&gt; BinOp(OP, L, V) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires notBool isRefV(L) [priority(40)] |
| 822 | `reference-semantics/semantics/operators.k` | 34-37 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) =&gt; Compare(V, CmpOp(OP, R)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)] |
| 823 | `reference-semantics/semantics/operators.k` | 38-42 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Compare(L:Val, CmpOp(OP:String, ref(H:Int))) =&gt; Compare(L, CmpOp(OP, V)) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)] |
| 824 | `reference-semantics/semantics/operators.k` | 44-46 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; UnaryOp(OP:String, ref(H:Int)) =&gt; UnaryOp(OP, V) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 825 | `reference-semantics/semantics/operators.k` | 47-47 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 826 | `reference-semantics/semantics/range.k` | 5-5 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-RANGE |
| 827 | `reference-semantics/semantics/range.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 828 | `reference-semantics/semantics/range.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 829 | `reference-semantics/semantics/range.k` | 9-9 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= inRange(Int, Int, Int) [function, total] |
| 830 | `reference-semantics/semantics/range.k` | 10-10 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule inRange(I:Int, HI:Int, ST:Int) =&gt; (ST &gt;Int 0 andBool I &lt;Int HI) orBool (ST &lt;Int 0 andBool I &gt;Int HI) |
| 831 | `reference-semantics/semantics/range.k` | 12-12 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= rangeLen(Int, Int, Int) [function] |
| 832 | `reference-semantics/semantics/range.k` | 13-14 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule rangeLen(LO:Int, HI:Int, ST:Int) =&gt; (HI -Int LO +Int ST -Int 1) /Int ST requires ST &gt;Int 0 andBool HI &gt;Int LO |
| 833 | `reference-semantics/semantics/range.k` | 15-16 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule rangeLen(LO:Int, HI:Int, ST:Int) =&gt; (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST &lt;Int 0 andBool HI &lt;Int LO |
| 834 | `reference-semantics/semantics/range.k` | 17-18 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule rangeLen(LO:Int, HI:Int, ST:Int) =&gt; 0 requires (ST &gt;Int 0 andBool HI &lt;=Int LO) orBool (ST &lt;Int 0 andBool HI &gt;=Int LO) |
| 835 | `reference-semantics/semantics/range.k` | 20-22 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) =&gt; #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... &lt;/k&gt; requires inRange(I, HI, ST) |
| 836 | `reference-semantics/semantics/range.k` | 23-24 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) =&gt; #iterDone ... &lt;/k&gt; requires notBool inRange(I, HI, ST) |
| 837 | `reference-semantics/semantics/range.k` | 25-25 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 838 | `reference-semantics/semantics/set.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-SET |
| 839 | `reference-semantics/semantics/set.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 840 | `reference-semantics/semantics/set.k` | 8-8 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= setV(IntSeq) |
| 841 | `reference-semantics/semantics/set.k` | 11-11 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= codeIn(Int, IntSeq) [function, total] |
| 842 | `reference-semantics/semantics/set.k` | 12-12 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule codeIn(_:Int, .IntSeq)                =&gt; false |
| 843 | `reference-semantics/semantics/set.k` | 13-13 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) =&gt; C ==Int H orBool codeIn(C, T) |
| 844 | `reference-semantics/semantics/set.k` | 16-17 | `syntax` | function, total, function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] &#124; dedupFrom(IntSeq, IntSeq)  [function, total] |
| 845 | `reference-semantics/semantics/set.k` | 18-18 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dedupCodes(CS:IntSeq) =&gt; dedupFrom(CS, .IntSeq) |
| 846 | `reference-semantics/semantics/set.k` | 19-19 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dedupFrom(.IntSeq, ACC:IntSeq) =&gt; ACC |
| 847 | `reference-semantics/semantics/set.k` | 20-21 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) =&gt; dedupFrom(S, ACC) requires codeIn(C, ACC) |
| 848 | `reference-semantics/semantics/set.k` | 22-23 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) =&gt; dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC) |
| 849 | `reference-semantics/semantics/set.k` | 25-25 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= snocCode(IntSeq, Int) [function, total] |
| 850 | `reference-semantics/semantics/set.k` | 26-26 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule snocCode(.IntSeq, C:Int)                =&gt; iCons(C, .IntSeq) |
| 851 | `reference-semantics/semantics/set.k` | 27-27 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule snocCode(iCons(H:Int, T:IntSeq), C:Int) =&gt; iCons(H, snocCode(T, C)) |
| 852 | `reference-semantics/semantics/set.k` | 31-31 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total] |
| 853 | `reference-semantics/semantics/set.k` | 32-32 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule subsetCodes(.IntSeq, _:IntSeq)                =&gt; true |
| 854 | `reference-semantics/semantics/set.k` | 33-33 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) =&gt; codeIn(C, B) andBool subsetCodes(S, B) |
| 855 | `reference-semantics/semantics/set.k` | 35-35 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total] |
| 856 | `reference-semantics/semantics/set.k` | 36-36 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule sameSet(A:IntSeq, B:IntSeq) =&gt; subsetCodes(A, B) andBool subsetCodes(B, A) |
| 857 | `reference-semantics/semantics/set.k` | 39-39 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) =&gt; sameSet(A, B) |
| 858 | `reference-semantics/semantics/set.k` | 40-40 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 859 | `reference-semantics/semantics/sort.k` | 10-10 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-SORT |
| 860 | `reference-semantics/semantics/sort.k` | 11-11 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-BUILTINS |
| 861 | `reference-semantics/semantics/sort.k` | 12-12 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-SUBSCRIPT |
| 862 | `reference-semantics/semantics/sort.k` | 18-18 | `syntax` | function, total, symbol(sortVS), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators] |
| 863 | `reference-semantics/semantics/sort.k` | 19-19 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= insVS(Int, ValSeq) [function] |
| 864 | `reference-semantics/semantics/sort.k` | 20-20 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule sortVS(.ValSeq)                =&gt; .ValSeq          [concrete] |
| 865 | `reference-semantics/semantics/sort.k` | 21-21 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule sortVS(vCons(X:Int, R:ValSeq)) =&gt; insVS(X, sortVS(R)) [concrete] |
| 866 | `reference-semantics/semantics/sort.k` | 22-22 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule insVS(X:Int, .ValSeq)                =&gt; vCons(X, .ValSeq) [concrete] |
| 867 | `reference-semantics/semantics/sort.k` | 23-23 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) =&gt; vCons(X, vCons(Y, R)) requires X &lt;=Int Y [concrete] |
| 868 | `reference-semantics/semantics/sort.k` | 24-24 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) =&gt; vCons(Y, insVS(X, R)) requires X  &gt;Int Y [concrete] |
| 869 | `reference-semantics/semantics/sort.k` | 26-26 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function] |
| 870 | `reference-semantics/semantics/sort.k` | 27-27 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) =&gt; insVSs(CS, sortVS(R)) [concrete] |
| 871 | `reference-semantics/semantics/sort.k` | 28-28 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule insVSs(A:IntSeq, .ValSeq) =&gt; vCons(str(A), .ValSeq) [concrete] |
| 872 | `reference-semantics/semantics/sort.k` | 29-30 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) =&gt; vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete] |
| 873 | `reference-semantics/semantics/sort.k` | 31-32 | `rule` | concrete | no | UNUSED_FIXED_SUPPLIED_CONCRETE_RULE | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) =&gt; vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] |
| 874 | `reference-semantics/semantics/sort.k` | 36-37 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) =&gt; #alloc(list(sortVS(VS))) ... &lt;/k&gt; |
| 875 | `reference-semantics/semantics/sort.k` | 40-42 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) =&gt; noneV ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; list(VS:ValSeq =&gt; sortVS(VS)) ... &lt;/heap&gt; [priority(40)] |
| 876 | `reference-semantics/semantics/sort.k` | 49-49 | `syntax` | function, total, symbol(sortKeyVS), no-evaluators | no | UNUSED_FIXED_SUPPLIED_OPAQUE_BOUNDARY | syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators] |
| 877 | `reference-semantics/semantics/sort.k` | 51-52 | `syntax` | function, total, function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= revVS(ValSeq) [function, total] &#124; revVSAcc(ValSeq, ValSeq) [function, total] |
| 878 | `reference-semantics/semantics/sort.k` | 53-53 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule revVS(S:ValSeq) =&gt; revVSAcc(S, .ValSeq) |
| 879 | `reference-semantics/semantics/sort.k` | 54-54 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule revVSAcc(.ValSeq, A:ValSeq) =&gt; A |
| 880 | `reference-semantics/semantics/sort.k` | 55-55 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) =&gt; revVSAcc(R, vCons(V, A)) |
| 881 | `reference-semantics/semantics/sort.k` | 57-57 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= condRev(ValSeq, Bool) [function, total] |
| 882 | `reference-semantics/semantics/sort.k` | 58-58 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule condRev(S:ValSeq, false) =&gt; S |
| 883 | `reference-semantics/semantics/sort.k` | 59-59 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule condRev(S:ValSeq, true)  =&gt; revVS(S) |
| 884 | `reference-semantics/semantics/sort.k` | 61-62 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) =&gt; #alloc(list(sortKeyVS(VS, KV))) ... &lt;/k&gt; |
| 885 | `reference-semantics/semantics/sort.k` | 63-64 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) =&gt; #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... &lt;/k&gt; |
| 886 | `reference-semantics/semantics/sort.k` | 65-66 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) =&gt; #alloc(list(condRev(sortVS(VS), RB))) ... &lt;/k&gt; |
| 887 | `reference-semantics/semantics/sort.k` | 72-72 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 888 | `reference-semantics/semantics/str.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-STR |
| 889 | `reference-semantics/semantics/str.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 890 | `reference-semantics/semantics/str.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 891 | `reference-semantics/semantics/str.k` | 8-8 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(str(.IntSeq))                 =&gt; #iterDone ... &lt;/k&gt; |
| 892 | `reference-semantics/semantics/str.k` | 9-10 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(str(iCons(C:Int, R:IntSeq))) =&gt; #iterYield(str(iCons(C, .IntSeq)), str(R)) ... &lt;/k&gt; |
| 893 | `reference-semantics/semantics/str.k` | 13-13 | `syntax` | function | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= strToCodes(String) [function] |
| 894 | `reference-semantics/semantics/str.k` | 14-14 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Str(S:String) =&gt; str(strToCodes(S)) ... &lt;/k&gt; |
| 895 | `reference-semantics/semantics/str.k` | 15-15 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule strToCodes("") =&gt; .IntSeq |
| 896 | `reference-semantics/semantics/str.k` | 16-17 | `rule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | rule strToCodes(S:String) =&gt; iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) &lt;Int 128 |
| 897 | `reference-semantics/semantics/str.k` | 20-20 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total] |
| 898 | `reference-semantics/semantics/str.k` | 21-21 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule seqConcat(.IntSeq, T:IntSeq)                =&gt; T |
| 899 | `reference-semantics/semantics/str.k` | 22-22 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) =&gt; iCons(I, seqConcat(S, T)) |
| 900 | `reference-semantics/semantics/str.k` | 24-24 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) =&gt; str(seqConcat(A, B)) |
| 901 | `reference-semantics/semantics/str.k` | 25-25 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) =&gt; A ==K B |
| 902 | `reference-semantics/semantics/str.k` | 26-26 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) =&gt; notBool (A ==K B) |
| 903 | `reference-semantics/semantics/str.k` | 29-29 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) =&gt; strContains(P, X) |
| 904 | `reference-semantics/semantics/str.k` | 30-30 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) =&gt; notBool strContains(P, X) |
| 905 | `reference-semantics/semantics/str.k` | 32-32 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total] |
| 906 | `reference-semantics/semantics/str.k` | 33-33 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strPrefix(.IntSeq, _:IntSeq)               =&gt; true |
| 907 | `reference-semantics/semantics/str.k` | 34-34 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) =&gt; false |
| 908 | `reference-semantics/semantics/str.k` | 35-35 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) =&gt; A ==Int B andBool strPrefix(As, Bs) |
| 909 | `reference-semantics/semantics/str.k` | 37-37 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= strContains(IntSeq, IntSeq) [function, total] |
| 910 | `reference-semantics/semantics/str.k` | 38-38 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strContains(P:IntSeq, X:IntSeq) =&gt; true  requires strPrefix(P, X) |
| 911 | `reference-semantics/semantics/str.k` | 39-39 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strContains(P:IntSeq, .IntSeq)  =&gt; false requires notBool strPrefix(P, .IntSeq) |
| 912 | `reference-semantics/semantics/str.k` | 40-41 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) =&gt; strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) |
| 913 | `reference-semantics/semantics/str.k` | 48-48 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bool ::= strLt(IntSeq, IntSeq) [function, total] |
| 914 | `reference-semantics/semantics/str.k` | 49-49 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strLt(.IntSeq, .IntSeq)                =&gt; false |
| 915 | `reference-semantics/semantics/str.k` | 50-50 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) =&gt; true |
| 916 | `reference-semantics/semantics/str.k` | 51-51 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) =&gt; false |
| 917 | `reference-semantics/semantics/str.k` | 52-52 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) =&gt; true          requires A  &lt;Int B |
| 918 | `reference-semantics/semantics/str.k` | 53-53 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) =&gt; false         requires A  &gt;Int B |
| 919 | `reference-semantics/semantics/str.k` | 54-54 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) =&gt; strLt(As, Bs) requires A ==Int B |
| 920 | `reference-semantics/semantics/str.k` | 56-56 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;",  str(A:IntSeq), str(B:IntSeq)) =&gt; strLt(A, B) |
| 921 | `reference-semantics/semantics/str.k` | 57-57 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;",  str(A:IntSeq), str(B:IntSeq)) =&gt; strLt(B, A) |
| 922 | `reference-semantics/semantics/str.k` | 58-58 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&lt;=", str(A:IntSeq), str(B:IntSeq)) =&gt; notBool strLt(B, A) |
| 923 | `reference-semantics/semantics/str.k` | 59-59 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("&gt;=", str(A:IntSeq), str(B:IntSeq)) =&gt; notBool strLt(A, B) |
| 924 | `reference-semantics/semantics/str.k` | 60-60 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 925 | `reference-semantics/semantics/subscript.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-SUBSCRIPT |
| 926 | `reference-semantics/semantics/subscript.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 927 | `reference-semantics/semantics/subscript.k` | 11-11 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= valSeqAt(ValSeq, Int) [function, total] |
| 928 | `reference-semantics/semantics/subscript.k` | 12-12 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     =&gt; V |
| 929 | `reference-semantics/semantics/subscript.k` | 13-14 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) =&gt; valSeqAt(S, I -Int 1) requires I &gt;Int 0 |
| 930 | `reference-semantics/semantics/subscript.k` | 16-16 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= intSeqAt(IntSeq, Int) [function] |
| 931 | `reference-semantics/semantics/subscript.k` | 17-17 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     =&gt; C |
| 932 | `reference-semantics/semantics/subscript.k` | 18-19 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) =&gt; intSeqAt(S, I -Int 1) requires I &gt;Int 0 |
| 933 | `reference-semantics/semantics/subscript.k` | 21-21 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= normIdx(Int, Int) [function, total] |
| 934 | `reference-semantics/semantics/subscript.k` | 22-22 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule normIdx(I:Int, LEN:Int) =&gt; I +Int LEN requires I  &lt;Int 0 |
| 935 | `reference-semantics/semantics/subscript.k` | 23-23 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule normIdx(I:Int, _:Int)   =&gt; I          requires I &gt;=Int 0 |
| 936 | `reference-semantics/semantics/subscript.k` | 27-27 | `context` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | context Subscript(HOLE, _) |
| 937 | `reference-semantics/semantics/subscript.k` | 28-28 | `context` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | context Subscript(_:Val, HOLE:Expr) |
| 938 | `reference-semantics/semantics/subscript.k` | 31-33 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Subscript(ref(H:Int), IX:Index) =&gt; Subscript(V, IX) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 939 | `reference-semantics/semantics/subscript.k` | 35-35 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Subscript(OBJ:Val, I:Int) =&gt; applyIndex(OBJ, I) ... &lt;/k&gt; |
| 940 | `reference-semantics/semantics/subscript.k` | 37-37 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= applyIndex(Val, Int) [function] |
| 941 | `reference-semantics/semantics/subscript.k` | 38-38 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyIndex(list(VS:ValSeq),  I:Int) =&gt; valSeqAt(VS, normIdx(I, vsLen(VS))) |
| 942 | `reference-semantics/semantics/subscript.k` | 39-39 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyIndex(tuple(VS:ValSeq), I:Int) =&gt; valSeqAt(VS, normIdx(I, vsLen(VS))) |
| 943 | `reference-semantics/semantics/subscript.k` | 40-41 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyIndex(str(IS:IntSeq),   I:Int) =&gt; str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) |
| 944 | `reference-semantics/semantics/subscript.k` | 44-47 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #evalB(Bound) &#124; "#toSome" &#124; #slLo(Val, Bound, Bound) &#124; #slHi(Val, OptInt, Bound) &#124; #slStep(Val, OptInt, OptInt) |
| 945 | `reference-semantics/semantics/subscript.k` | 49-49 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax OptInt ::= "noB" &#124; someB(Int) |
| 946 | `reference-semantics/semantics/subscript.k` | 50-50 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #evalB(NoBound)  =&gt; noB ... &lt;/k&gt; |
| 947 | `reference-semantics/semantics/subscript.k` | 51-51 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #evalB(E:Expr)   =&gt; E ~&gt; #toSome ... &lt;/k&gt; |
| 948 | `reference-semantics/semantics/subscript.k` | 52-52 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; I:Int ~&gt; #toSome =&gt; someB(I) ... &lt;/k&gt; |
| 949 | `reference-semantics/semantics/subscript.k` | 54-54 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) =&gt; #evalB(LO) ~&gt; #slLo(OBJ, HI, ST) ... &lt;/k&gt; |
| 950 | `reference-semantics/semantics/subscript.k` | 55-55 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; LO:OptInt ~&gt; #slLo(OBJ:Val, HI:Bound, ST:Bound)   =&gt; #evalB(HI) ~&gt; #slHi(OBJ, LO, ST) ... &lt;/k&gt; |
| 951 | `reference-semantics/semantics/subscript.k` | 56-56 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; HI:OptInt ~&gt; #slHi(OBJ:Val, LO:OptInt, ST:Bound)  =&gt; #evalB(ST) ~&gt; #slStep(OBJ, LO, HI) ... &lt;/k&gt; |
| 952 | `reference-semantics/semantics/subscript.k` | 58-60 | `rule` | priority(45) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; ST:OptInt ~&gt; #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) =&gt; #alloc(doSlice(list(VS), LO, HI, ST)) ... &lt;/k&gt; [priority(45)] |
| 953 | `reference-semantics/semantics/subscript.k` | 61-61 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; ST:OptInt ~&gt; #slStep(OBJ:Val, LO:OptInt, HI:OptInt) =&gt; doSlice(OBJ, LO, HI, ST) ... &lt;/k&gt; |
| 954 | `reference-semantics/semantics/subscript.k` | 63-63 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function] |
| 955 | `reference-semantics/semantics/subscript.k` | 64-65 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) =&gt; list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| 956 | `reference-semantics/semantics/subscript.k` | 66-67 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) =&gt; tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| 957 | `reference-semantics/semantics/subscript.k` | 68-69 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) =&gt; str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) |
| 958 | `reference-semantics/semantics/subscript.k` | 72-72 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= slStep(OptInt) [function, total] |
| 959 | `reference-semantics/semantics/subscript.k` | 73-73 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStep(noB)          =&gt; 1 |
| 960 | `reference-semantics/semantics/subscript.k` | 74-74 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStep(someB(S:Int)) =&gt; S |
| 961 | `reference-semantics/semantics/subscript.k` | 76-76 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= slStart(OptInt, OptInt, Int) [function] |
| 962 | `reference-semantics/semantics/subscript.k` | 77-78 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStart(noB,          ST:OptInt, _LEN:Int) =&gt; 0 requires slStep(ST) &gt;Int 0 |
| 963 | `reference-semantics/semantics/subscript.k` | 79-80 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStart(noB,          ST:OptInt, LEN:Int)  =&gt; LEN -Int 1 requires slStep(ST) &lt;Int 0 |
| 964 | `reference-semantics/semantics/subscript.k` | 81-81 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  =&gt; slAdjust(I, LEN, slStep(ST)) |
| 965 | `reference-semantics/semantics/subscript.k` | 83-83 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= slStop(OptInt, OptInt, Int) [function] |
| 966 | `reference-semantics/semantics/subscript.k` | 84-85 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStop(noB,          ST:OptInt, LEN:Int)  =&gt; LEN requires slStep(ST) &gt;Int 0 |
| 967 | `reference-semantics/semantics/subscript.k` | 86-87 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStop(noB,          ST:OptInt, _LEN:Int) =&gt; -1 requires slStep(ST) &lt;Int 0 |
| 968 | `reference-semantics/semantics/subscript.k` | 88-88 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  =&gt; slAdjust(I, LEN, slStep(ST)) |
| 969 | `reference-semantics/semantics/subscript.k` | 90-90 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= slAdjust(Int, Int, Int) [function, total] |
| 970 | `reference-semantics/semantics/subscript.k` | 91-92 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slAdjust(I:Int, LEN:Int, STEP:Int) =&gt; clampLo(I +Int LEN, STEP) requires I  &lt;Int 0 |
| 971 | `reference-semantics/semantics/subscript.k` | 93-94 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule slAdjust(I:Int, LEN:Int, STEP:Int) =&gt; clampHi(I, LEN, STEP) requires I &gt;=Int 0 |
| 972 | `reference-semantics/semantics/subscript.k` | 96-96 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= clampLo(Int, Int) [function, total] |
| 973 | `reference-semantics/semantics/subscript.k` | 97-98 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule clampLo(J:Int, _STEP:Int) =&gt; J requires J &gt;=Int 0 |
| 974 | `reference-semantics/semantics/subscript.k` | 99-100 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule clampLo(J:Int, STEP:Int)  =&gt; #if STEP &lt;Int 0 #then -1 #else 0 #fi requires J &lt;Int 0 |
| 975 | `reference-semantics/semantics/subscript.k` | 102-102 | `syntax` | function, total | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= clampHi(Int, Int, Int) [function, total] |
| 976 | `reference-semantics/semantics/subscript.k` | 103-104 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule clampHi(I:Int, LEN:Int, _STEP:Int) =&gt; I requires I  &lt;Int LEN |
| 977 | `reference-semantics/semantics/subscript.k` | 105-106 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule clampHi(I:Int, LEN:Int, STEP:Int)  =&gt; #if STEP &lt;Int 0 #then LEN -Int 1 #else LEN #fi requires I &gt;=Int LEN |
| 978 | `reference-semantics/semantics/subscript.k` | 109-109 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function] |
| 979 | `reference-semantics/semantics/subscript.k` | 110-112 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) =&gt; vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP &gt;Int 0 andBool I &lt;Int STOP) orBool (STEP &lt;Int 0 andBool I &gt;Int STOP) |
| 980 | `reference-semantics/semantics/subscript.k` | 113-114 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) =&gt; .ValSeq requires notBool ((STEP &gt;Int 0 andBool I &lt;Int STOP) orBool (STEP &lt;Int 0 andBool I &gt;Int STOP)) |
| 981 | `reference-semantics/semantics/subscript.k` | 116-116 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function] |
| 982 | `reference-semantics/semantics/subscript.k` | 117-119 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) =&gt; iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP &gt;Int 0 andBool I &lt;Int STOP) orBool (STEP &lt;Int 0 andBool I &gt;Int STOP) |
| 983 | `reference-semantics/semantics/subscript.k` | 120-121 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) =&gt; .IntSeq requires notBool ((STEP &gt;Int 0 andBool I &lt;Int STOP) orBool (STEP &lt;Int 0 andBool I &gt;Int STOP)) |
| 984 | `reference-semantics/semantics/subscript.k` | 122-122 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 985 | `reference-semantics/semantics/syntax.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-SYNTAX |
| 986 | `reference-semantics/semantics/syntax.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports INT-SYNTAX |
| 987 | `reference-semantics/semantics/syntax.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports FLOAT-SYNTAX |
| 988 | `reference-semantics/semantics/syntax.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports BOOL-SYNTAX |
| 989 | `reference-semantics/semantics/syntax.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports STRING-SYNTAX |
| 990 | `reference-semantics/semantics/syntax.k` | 9-30 | `syntax` | strict(2), seqstrict(2, 3), macro, macro, strict(1), strict(1) | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Expr ::= "Int"      "(" Int ")" &#124; "Float"    "(" Float ")" &#124; "Bool"     "(" Bool ")" &#124; "Name"     "(" String ")" &#124; "Str"      "(" String ")" &#124; "UnaryOp"  "(" String "," Expr ")" [strict(2)] &#124; "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] &#124; "BoolOp"    "(" String "," Exprs ")" &#124; "ListExpr"  "(" Exprs ")" &#124; "DictExpr"  "(" Entries ")" &#124; "ListComp"  "(" Expr "," CompFors ")" [macro] &#124; "GenExp"    "(" Expr "," CompFors ")" [macro] &#124; "TupleExpr" "(" Exprs ")" &#124; "Subscript" "(" Expr "," Index ")" &#124; "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] &#124; "Lambda"    "(" Params "," Expr ")" &#124; "KwArg"     "(" String "," Expr ")" &#124; "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" &#124; "NoneVal" &#124; "Call"      "(" Expr "," Exprs ")" &#124; "Attribute" "(" Expr "," String ")" [strict(1)] &#124; "Compare"   "(" Expr "," CmpOp ")" |
| 991 | `reference-semantics/semantics/syntax.k` | 32-32 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")" |
| 992 | `reference-semantics/semantics/syntax.k` | 33-33 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Entry    ::= "Entry" "(" Expr "," Expr ")" |
| 993 | `reference-semantics/semantics/syntax.k` | 34-34 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Entries  ::= List{Entry, ","} |
| 994 | `reference-semantics/semantics/syntax.k` | 35-35 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")" |
| 995 | `reference-semantics/semantics/syntax.k` | 36-36 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax CompFors ::= List{CompFor, ""} |
| 996 | `reference-semantics/semantics/syntax.k` | 37-37 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Exprs    ::= List{Expr, ","} |
| 997 | `reference-semantics/semantics/syntax.k` | 38-38 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Index    ::= Expr &#124; "Slice" "(" Bound "," Bound "," Bound ")" |
| 998 | `reference-semantics/semantics/syntax.k` | 39-39 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Bound    ::= Expr &#124; "NoBound" |
| 999 | `reference-semantics/semantics/syntax.k` | 41-54 | `syntax` | strict(2), strict(3), strict(2), strict(1), strict, strict, strict | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] &#124; "Import"    "(" String ")" &#124; "ImportFrom" "(" String "," ParamNames ")" &#124; "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] &#124; "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] &#124; "While"     "(" Expr "," Stmts ")" &#124; "Break" &#124; "Continue" &#124; "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] &#124; "Return"    "(" Expr ")" [strict] &#124; "Assert"    "(" Expr ")" [strict] &#124; "Expr"      "(" Expr ")" [strict] &#124; "FuncDef"   "(" String "," Params "," Stmts ")" &#124; "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")" |
| 1000 | `reference-semantics/semantics/syntax.k` | 56-56 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Stmts      ::= List{Stmt, ""} |
| 1001 | `reference-semantics/semantics/syntax.k` | 57-57 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Params     ::= "Params" "(" ParamNames ")" |
| 1002 | `reference-semantics/semantics/syntax.k` | 58-58 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax CellVars   ::= "CellVars" "(" ParamNames ")" |
| 1003 | `reference-semantics/semantics/syntax.k` | 59-59 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax FreeVars   ::= "FreeVars" "(" ParamNames ")" |
| 1004 | `reference-semantics/semantics/syntax.k` | 60-60 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax ParamNames ::= List{String, ","} |
| 1005 | `reference-semantics/semantics/syntax.k` | 61-61 | `syntax` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | syntax Module     ::= "Module" "(" Stmts ")" |
| 1006 | `reference-semantics/semantics/syntax.k` | 62-62 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 1007 | `reference-semantics/semantics/tuple.k` | 3-3 | `module` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | module MPY-TUPLE |
| 1008 | `reference-semantics/semantics/tuple.k` | 4-4 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 1009 | `reference-semantics/semantics/tuple.k` | 5-5 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 1010 | `reference-semantics/semantics/tuple.k` | 6-6 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-LIST |
| 1011 | `reference-semantics/semantics/tuple.k` | 7-7 | `imports` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | imports MPY-METHODS |
| 1012 | `reference-semantics/semantics/tuple.k` | 10-10 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(tuple(.ValSeq))                =&gt; #iterDone ... &lt;/k&gt; |
| 1013 | `reference-semantics/semantics/tuple.k` | 11-11 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #iterNext(tuple(vCons(V:Val, R:ValSeq))) =&gt; #iterYield(V, tuple(R)) ... &lt;/k&gt; |
| 1014 | `reference-semantics/semantics/tuple.k` | 14-14 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax ApplyK ::= "toTuple" |
| 1015 | `reference-semantics/semantics/tuple.k` | 15-15 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; TupleExpr(ES:Exprs) =&gt; #evalArgs(ES, .Vals, toTuple) ... &lt;/k&gt; |
| 1016 | `reference-semantics/semantics/tuple.k` | 16-16 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #applyK(toTuple, ACC:Vals) =&gt; tuple(vals2valSeq(ACC)) ... &lt;/k&gt; |
| 1017 | `reference-semantics/semantics/tuple.k` | 18-18 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) =&gt; A ==K B |
| 1018 | `reference-semantics/semantics/tuple.k` | 20-20 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) =&gt; #memberAcc(LV, tuple(VS)) ... &lt;/k&gt; |
| 1019 | `reference-semantics/semantics/tuple.k` | 21-21 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) =&gt; #memberAcc(LV, tuple(VS)) ~&gt; #notB ... &lt;/k&gt; |
| 1020 | `reference-semantics/semantics/tuple.k` | 23-23 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) =&gt; idxOfVS(VS, V, 0) |
| 1021 | `reference-semantics/semantics/tuple.k` | 24-24 | `syntax` | function | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax Int ::= idxOfVS(ValSeq, Val, Int) [function] |
| 1022 | `reference-semantics/semantics/tuple.k` | 25-25 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) =&gt; I requires A ==K V |
| 1023 | `reference-semantics/semantics/tuple.k` | 26-27 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) =&gt; idxOfVS(R, V, I +Int 1) requires notBool (A ==K V) |
| 1024 | `reference-semantics/semantics/tuple.k` | 28-28 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) =&gt; notBool (A ==K B) |
| 1025 | `reference-semantics/semantics/tuple.k` | 31-31 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #bindTgt(Expr, Val) |
| 1026 | `reference-semantics/semantics/tuple.k` | 32-34 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindTgt(Name(X:String), V:Val) =&gt; .K ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map =&gt; M [ X &lt;- V ], _) ... &lt;/scopes&gt; |
| 1027 | `reference-semantics/semantics/tuple.k` | 35-41 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #bindTgt(Name(X:String), V:Val) =&gt; #cellW({M[X]}:&gt;Val, V) ... &lt;/k&gt; &lt;env&gt; L:Int &lt;/env&gt; &lt;scopes&gt; ... L &#124;-&gt; scope(M:Map, _) ... &lt;/scopes&gt; requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:&gt;Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:&gt;Val) [priority(40)] |
| 1028 | `reference-semantics/semantics/tuple.k` | 42-42 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) =&gt; #unpackSeq(TS, VS) ... &lt;/k&gt; |
| 1029 | `reference-semantics/semantics/tuple.k` | 43-43 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  =&gt; #unpackSeq(TS, VS) ... &lt;/k&gt; |
| 1030 | `reference-semantics/semantics/tuple.k` | 44-46 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) =&gt; #bindTgt(TupleExpr(TS), V) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 1031 | `reference-semantics/semantics/tuple.k` | 49-49 | `syntax` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | syntax KItem ::= #unpackSeq(Exprs, ValSeq) |
| 1032 | `reference-semantics/semantics/tuple.k` | 50-50 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) =&gt; #unpackSeq(TS, VS) ... &lt;/k&gt; |
| 1033 | `reference-semantics/semantics/tuple.k` | 51-51 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  =&gt; #unpackSeq(TS, VS) ... &lt;/k&gt; |
| 1034 | `reference-semantics/semantics/tuple.k` | 52-54 | `rule` | priority(40) | no | UNUSED_FIXED_SUPPLIED_PRIORITY_RULE | rule &lt;k&gt; Assign(TupleExpr(TS:Exprs), ref(H:Int)) =&gt; Assign(TupleExpr(TS), V) ... &lt;/k&gt; &lt;heap&gt; ... H &#124;-&gt; V:Val ... &lt;/heap&gt; [priority(40)] |
| 1035 | `reference-semantics/semantics/tuple.k` | 55-56 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) =&gt; #bindTgt(T, V) ~&gt; #unpackSeq(TS, VS) ... &lt;/k&gt; |
| 1036 | `reference-semantics/semantics/tuple.k` | 57-57 | `rule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | rule &lt;k&gt; #unpackSeq(.Exprs, .ValSeq) =&gt; .K ... &lt;/k&gt; |
| 1037 | `reference-semantics/semantics/tuple.k` | 58-58 | `endmodule` |  | no | UNUSED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 1038 | `reference-semantics/semantics.k` | 34-34 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/syntax.k" |
| 1039 | `reference-semantics/semantics.k` | 35-35 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/core.k" |
| 1040 | `reference-semantics/semantics.k` | 36-36 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/iter.k" |
| 1041 | `reference-semantics/semantics.k` | 37-37 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/range.k" |
| 1042 | `reference-semantics/semantics.k` | 38-38 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/operators.k" |
| 1043 | `reference-semantics/semantics.k` | 39-39 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/int.k" |
| 1044 | `reference-semantics/semantics.k` | 40-40 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/bool.k" |
| 1045 | `reference-semantics/semantics.k` | 41-41 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/float.k" |
| 1046 | `reference-semantics/semantics.k` | 42-42 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/str.k" |
| 1047 | `reference-semantics/semantics.k` | 43-43 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/set.k" |
| 1048 | `reference-semantics/semantics.k` | 44-44 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/list.k" |
| 1049 | `reference-semantics/semantics.k` | 45-45 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/tuple.k" |
| 1050 | `reference-semantics/semantics.k` | 46-46 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/subscript.k" |
| 1051 | `reference-semantics/semantics.k` | 47-47 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/comprehension.k" |
| 1052 | `reference-semantics/semantics.k` | 48-48 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/methods.k" |
| 1053 | `reference-semantics/semantics.k` | 49-49 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/controls.k" |
| 1054 | `reference-semantics/semantics.k` | 50-50 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/functions.k" |
| 1055 | `reference-semantics/semantics.k` | 51-51 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/builtins.k" |
| 1056 | `reference-semantics/semantics.k` | 52-52 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/call.k" |
| 1057 | `reference-semantics/semantics.k` | 53-53 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/sort.k" |
| 1058 | `reference-semantics/semantics.k` | 54-54 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/assert.k" |
| 1059 | `reference-semantics/semantics.k` | 55-55 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/dict.k" |
| 1060 | `reference-semantics/semantics.k` | 56-56 | `requires` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | requires "semantics/concrete.k" |
| 1061 | `reference-semantics/semantics.k` | 58-58 | `module` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | module MPY |
| 1062 | `reference-semantics/semantics.k` | 59-59 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CORE |
| 1063 | `reference-semantics/semantics.k` | 60-60 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ITER |
| 1064 | `reference-semantics/semantics.k` | 61-61 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-RANGE |
| 1065 | `reference-semantics/semantics.k` | 62-62 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-OPERATORS |
| 1066 | `reference-semantics/semantics.k` | 63-63 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-INT |
| 1067 | `reference-semantics/semantics.k` | 64-64 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-BOOL |
| 1068 | `reference-semantics/semantics.k` | 65-65 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-FLOAT |
| 1069 | `reference-semantics/semantics.k` | 66-66 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-STR |
| 1070 | `reference-semantics/semantics.k` | 67-67 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-SET |
| 1071 | `reference-semantics/semantics.k` | 68-68 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-LIST |
| 1072 | `reference-semantics/semantics.k` | 69-69 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-TUPLE |
| 1073 | `reference-semantics/semantics.k` | 70-70 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-SUBSCRIPT |
| 1074 | `reference-semantics/semantics.k` | 71-71 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-COMPREHENSION |
| 1075 | `reference-semantics/semantics.k` | 72-72 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-METHODS |
| 1076 | `reference-semantics/semantics.k` | 73-73 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CONTROLS |
| 1077 | `reference-semantics/semantics.k` | 74-74 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-FUNCTIONS |
| 1078 | `reference-semantics/semantics.k` | 75-75 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-BUILTINS |
| 1079 | `reference-semantics/semantics.k` | 76-76 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CALL |
| 1080 | `reference-semantics/semantics.k` | 77-77 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-SORT |
| 1081 | `reference-semantics/semantics.k` | 78-78 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-ASSERT |
| 1082 | `reference-semantics/semantics.k` | 79-79 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-DICT |
| 1083 | `reference-semantics/semantics.k` | 80-80 | `endmodule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 1084 | `reference-semantics/semantics.k` | 87-87 | `module` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | module MPY-KRUN |
| 1085 | `reference-semantics/semantics.k` | 88-88 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY |
| 1086 | `reference-semantics/semantics.k` | 89-89 | `imports` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | imports MPY-CONCRETE |
| 1087 | `reference-semantics/semantics.k` | 90-90 | `endmodule` |  | yes | USED_FIXED_SUPPLIED_SEMANTICS | endmodule |
| 1088 | `verification.k` | 1-1 | `requires` |  | yes | PROOF_LOCAL_DECLARATION_REVIEWED | requires "reference-semantics/semantics.k" |
| 1089 | `verification.k` | 3-3 | `module` |  | yes | PROOF_LOCAL_DECLARATION_REVIEWED | module CLOSEST-INTEGER-VERIFICATION |
| 1090 | `verification.k` | 4-4 | `imports` |  | yes | PROOF_LOCAL_DECLARATION_REVIEWED | imports MPY |
| 1091 | `verification.k` | 9-9 | `syntax` | function, total | yes | PROOF_LOCAL_DECLARATION_REVIEWED | syntax Stmts ::= "closestBody" "(" ")" [function, total] |
| 1092 | `verification.k` | 10-17 | `rule` |  | yes | PROOF_LOCAL_COPIED_BODY: exact current syntax, but no formal source dependency | rule closestBody() =&gt; Assign(Name("number"), Call(Name("float"), Name("value"))) If(Compare(Name("number"), CmpOp("&gt;", Float(0.0))), Return(Call(Name("int"), BinOp("+", Name("number"), Float(0.5)))), .Stmts) Return(Call(Name("int"), BinOp("-", Name("number"), Float(0.5)))) |
| 1093 | `verification.k` | 20-20 | `syntax` |  | yes | PROOF_LOCAL_DECLARATION_REVIEWED | syntax KItem ::= "runClosest" "(" Str ")" |
| 1094 | `verification.k` | 21-23 | `rule` |  | yes | PROOF_LOCAL_IDENTITY_GAP: wrapper executes copied closestBody, not solution.mpy | rule runClosest(S:Str) =&gt; Call(closureVal(("value", .ParamNames), closestBody(), 0), (S, .Exprs)) |
| 1095 | `verification.k` | 29-29 | `syntax` | function, total | yes | PROOF_LOCAL_DECLARATION_REVIEWED | syntax Int ::= nearestAway(Float) [function, total] |
| 1096 | `verification.k` | 30-34 | `rule` |  | yes | PROOF_LOCAL_STRUCTURAL_SPEC: truthful equation, but not an independent nearest-integer theorem | rule nearestAway(F:Float) =&gt; #if gtF(F, 0.0) #then truncF(addF(F, 0.5)) #else truncF(subF(F, 0.5)) #fi |
| 1097 | `verification.k` | 35-35 | `endmodule` |  | yes | PROOF_LOCAL_DECLARATION_REVIEWED | endmodule |
| 1098 | `spec.k` | 1-1 | `requires` |  | yes | SPEC_DECLARATION_REVIEWED | requires "verification.k" |
| 1099 | `spec.k` | 3-3 | `module` |  | yes | SPEC_DECLARATION_REVIEWED | module CLOSEST-INTEGER-SPEC |
| 1100 | `spec.k` | 4-4 | `imports` |  | yes | SPEC_DECLARATION_REVIEWED | imports CLOSEST-INTEGER-VERIFICATION |
| 1101 | `spec.k` | 9-24 | `claim` |  | yes | TARGET_CLAIM: closes structurally; fails real-program pinning and intent adequacy | claim &lt;k&gt; runClosest(str(CS:IntSeq)) =&gt; nearestAway(decStrToF(CS)) &lt;/k&gt; &lt;env&gt; 0 &lt;/env&gt; &lt;scopes&gt; 0  &#124;-&gt; scope(.Map, parent(-1)) -1 &#124;-&gt; builtinsScope &lt;/scopes&gt; &lt;scopeLoc&gt; 1 &lt;/scopeLoc&gt; &lt;heap&gt; .Map &lt;/heap&gt; &lt;heapLoc&gt; 0 &lt;/heapLoc&gt; &lt;stack&gt; .List &lt;/stack&gt; &lt;ret&gt; noRet &lt;/ret&gt; &lt;exc&gt; NoExc &lt;/exc&gt; &lt;exit-code&gt; 0 &lt;/exit-code&gt; |
| 1102 | `spec.k` | 25-25 | `endmodule` |  | yes | SPEC_DECLARATION_REVIEWED | endmodule |

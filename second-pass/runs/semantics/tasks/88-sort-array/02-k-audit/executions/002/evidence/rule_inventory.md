# Exhaustive K source inventory

Generated from the trusted supplied-semantics mount plus the candidate `verification.k` and `spec.k`. Imported K builtin modules are outside this local-source inventory.

## Counts

- `category:claim`: 4
- `category:configuration`: 1
- `category:context`: 5
- `category:equation`: 465
- `category:operational`: 239
- `category:syntax`: 232
- `kind:claim`: 4
- `kind:configuration`: 1
- `kind:context`: 5
- `kind:rule`: 704
- `kind:syntax`: 232
- `tag:concrete`: 54
- `tag:function`: 150
- `tag:macro`: 4
- `tag:macro-rec`: 1
- `tag:no-evaluators`: 22
- `tag:owise`: 29
- `tag:priority`: 53
- `tag:seqstrict`: 1
- `tag:strict`: 2
- `tag:symbol`: 25
- `tag:total`: 111

## `semantics.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| — | — | — | — | No local declaration, rule, context, configuration, or claim |

## `semantics/assert.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 6-7 | rule | operational | - | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 8-12 | rule | operational | - | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V) ` |
| 13-15 | rule | operational | priority | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |

## `semantics/bool.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 8-9 | rule | equation | - | `rule applyUn("not", V:Val) => notBool truthy(V) ` |
| 10 | rule | equation | - | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 11-15 | rule | equation | - | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 // ==== BoolOp: short-circuit, value-returning and / or ===================== // the node is its own accumulator: heat the HEAD element only, then either return it // (short-circuit) or drop it and continue` |
| 16 | context | context | - | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 17 | rule | operational | - | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 18-19 | rule | operational | - | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 20-21 | rule | operational | - | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 22-23 | rule | operational | - | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 24-28 | rule | operational | - | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the // operand — and/or return the OBJECT itself (Python identity), not its structure` |
| 29-30 | rule | operational | priority | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 31-34 | rule | operational | priority | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 35-38 | rule | operational | priority | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 39-42 | rule | operational | priority | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 43-46 | rule | operational | priority | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |

## `semantics/builtins.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 17-19 | syntax | syntax | function | `syntax Val ::= applyBuiltin(String, Vals) [function] // ==== len(obj) — O(1) per kind ============================================` |
| 20 | syntax | syntax | function | `syntax Int ::= seqLen(Val) [function]` |
| 21 | rule | equation | - | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 22 | rule | equation | - | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| 23 | rule | equation | - | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| 24 | rule | equation | - | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| 25 | rule | equation | - | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| 26-31 | rule | equation | - | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) == // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order). // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed. // (k-cell — list() constructs a NEW object)` |
| 32 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 33 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 34 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| 35 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| 36 | syntax | syntax | function,total | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 37 | rule | equation | - | `rule charsOf(.IntSeq) => .ValSeq` |
| 38-40 | rule | equation | - | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) // ==== set(str) — distinct character codes =================================` |
| 41-43 | rule | equation | - | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) // ==== abs(int) ============================================================` |
| 44-46 | rule | equation | - | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==` |
| 47 | syntax | syntax | - | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 48 | rule | operational | - | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 49 | rule | operational | - | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 50-53 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V) ` |
| 54 | syntax | syntax | function | `syntax Int ::= intOf(Val) [function]` |
| 55 | rule | equation | - | `rule intOf(I:Int) => I` |
| 56-58 | rule | equation | - | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi // ==== all / any (short-circuiting #iterNext folds) ========================` |
| 59 | syntax | syntax | - | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 60 | rule | operational | - | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 61 | rule | operational | - | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 62-63 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 64-66 | rule | operational | - | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V) ` |
| 67 | syntax | syntax | - | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 68 | rule | operational | - | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 69 | rule | operational | - | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 70-71 | rule | operational | - | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 72-75 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) // ==== max / min over an iterable (#iterNext folds; first element seeds) ====` |
| 76 | syntax | syntax | - | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 77 | rule | operational | - | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 78-79 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 80 | rule | operational | - | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 81 | rule | operational | - | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 82-85 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V) ` |
| 86 | syntax | syntax | - | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 87 | rule | operational | - | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 88-89 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 90 | rule | operational | - | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 91 | rule | operational | - | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 92-96 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) // ==== variadic max / min (a Vals fold) ====================================` |
| 97 | syntax | syntax | function | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 98 | rule | equation | - | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 99 | rule | equation | - | `rule maxVals(M:Int, .Vals) => M` |
| 100-101 | rule | equation | - | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R) ` |
| 102 | syntax | syntax | function | `syntax Int ::= minVals(Int, Vals) [function]` |
| 103 | rule | equation | - | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 104 | rule | equation | - | `rule minVals(M:Int, .Vals) => M` |
| 105-107 | rule | equation | - | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==` |
| 108-110 | rule | equation | - | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits` |
| 111-113 | rule | equation | - | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 114 | syntax | syntax | function,total | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 115 | rule | equation | - | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 116 | rule | equation | - | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 117 | syntax | syntax | function,total | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 118 | rule | equation | - | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 119-123 | rule | equation | - | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========` |
| 124-125 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 126 | syntax | syntax | function,total | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 127 | rule | equation | - | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 128-131 | rule | equation | - | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) // ==== map(str, xs) — eager (only the str case is in the subset) =============` |
| 132-133 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 134 | syntax | syntax | function,total | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 135 | rule | equation | - | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 136 | rule | equation | - | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 137-139 | rule | equation | - | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) // ==== int(x) identities (int(round(x)) composes through) ====================` |
| 140-142 | rule | equation | - | `rule applyBuiltin("int", I:Int, .Vals) => I // ==== ord / chr ===========================================================` |
| 143 | rule | equation | - | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 144-147 | rule | equation | - | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 // ==== str(int) / str(str) =================================================` |
| 148 | rule | equation | - | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| 149-151 | rule | equation | - | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====` |
| 152-155 | rule | equation | - | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)` |
| 156-157 | rule | equation | - | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 158 | syntax | syntax | function,total | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 159 | rule | equation | - | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| 160-162 | rule | equation | - | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====` |
| 163 | rule | equation | - | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 164-166 | rule | equation | - | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)` |
| 167-168 | rule | operational | - | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 169 | rule | operational | - | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| 170 | rule | operational | - | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 171-172 | rule | operational | - | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 173 | rule | operational | - | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| 174-176 | rule | operational | - | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> // ==== range(stop) / range(start, stop) / range(start, stop, step) =========` |
| 177 | rule | equation | - | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| 178 | rule | equation | - | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| 179-186 | rule | equation | concrete | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ======== // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's // trusted pass evaluator, now DEFINED in the reference and driven by a // code-level tokenizer. Reduces on concrete strings (krun); a symbolic // argument leaves the call unevaluated for problem-level folds.` |
| 187 | rule | equation | - | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 188 | syntax | syntax | function | `syntax Int ::= evalArith(IntSeq) [function]` |
| 189-191 | rule | equation | - | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS))))) ` |
| 192-193 | syntax | syntax | - | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq) ` |
| 194 | syntax | syntax | function,total | `syntax Bool ::= evDigit(Int) [function, total]` |
| 195 | rule | equation | - | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 196 | syntax | syntax | function,total | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 197 | rule | equation | - | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 198 | rule | equation | owise | `rule evHead42(_:IntSeq) => false [owise]` |
| 199 | syntax | syntax | function,total | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 200 | rule | equation | - | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 201-202 | rule | equation | owise | `rule evHead47(_:IntSeq) => false [owise] ` |
| 203 | syntax | syntax | function,total | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 204 | rule | equation | - | `rule tokOps(.IntSeq) => .OpSeq` |
| 205 | rule | equation | - | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| 206 | rule | equation | - | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| 207 | rule | equation | - | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 208 | rule | equation | - | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 209 | rule | equation | - | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 210 | rule | equation | - | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 211 | rule | equation | - | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| 212-213 | rule | equation | - | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R)) ` |
| 214-215 | syntax | syntax | function,total | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 216 | rule | equation | - | `rule tokNds(.IntSeq) => .IntSeq` |
| 217 | rule | equation | - | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| 218 | rule | equation | - | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 219-220 | rule | equation | - | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 221-222 | rule | equation | - | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 223-224 | rule | equation | owise | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise] ` |
| 225 | syntax | syntax | - | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 226 | syntax | syntax | function,total | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 227 | rule | equation | - | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 228-229 | rule | equation | owise | `rule firstNdE(_:EvPair) => 0 [owise] ` |
| 230 | syntax | syntax | function,total | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 231 | rule | equation | - | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| 232 | rule | equation | - | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| 233 | rule | equation | - | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| 234 | rule | equation | - | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 235 | rule | equation | - | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 236-237 | rule | equation | owise | `rule applyOpE(_:String, A:Int, _:Int) => A [owise] ` |
| 238 | syntax | syntax | function,total | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 239 | rule | equation | - | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 240 | rule | equation | - | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 241-242 | rule | equation | - | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 243 | rule | equation | owise | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 244 | syntax | syntax | function,total | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 245 | rule | equation | - | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 246 | rule | equation | - | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 247 | syntax | syntax | function,total | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 248-249 | rule | equation | - | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS)) ` |
| 250 | syntax | syntax | function,total | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 251 | rule | equation | - | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 252 | rule | equation | - | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 253 | rule | equation | - | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 254 | rule | equation | - | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 255 | syntax | syntax | function,total | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 256 | rule | equation | - | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 257-259 | rule | equation | - | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 260-262 | rule | equation | - | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 263-264 | rule | equation | owise | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 265 | syntax | syntax | function,total | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 266 | rule | equation | - | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 267 | rule | equation | - | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 268 | rule | equation | owise | `rule inLevelE(_:String, _:String) => false [owise]` |
| 269 | syntax | syntax | function,total | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 270 | rule | equation | - | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 271 | rule | equation | - | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 272 | syntax | syntax | function,total | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 273 | rule | equation | - | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 274-278 | rule | equation | concrete | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ================== // The md5 value itself is a named shared trust (sortVS-style, no concrete // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).` |
| 279 | syntax | syntax | - | `syntax KItem ::= "#md5"` |
| 280-281 | rule | operational | priority | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 282 | rule | operational | - | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 283 | syntax | syntax | - | `syntax Val ::= md5Obj(IntSeq)` |
| 284 | rule | equation | - | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 285-290 | syntax | syntax | function,total,symbol,no-evaluators | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int\|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary name that resolves via the builtins frame to // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).` |
| 291 | rule | equation | - | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 292 | rule | equation | - | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 293 | syntax | syntax | function | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 294 | rule | equation | - | `rule isIntV(_:Int) => true` |
| 295 | rule | equation | owise | `rule isIntV(_:Val) => false [owise]` |
| 296 | rule | equation | - | `rule isStrV(str(_:IntSeq)) => true` |
| 297 | rule | equation | owise | `rule isStrV(_:Val) => false [owise]` |

## `semantics/call.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 16-18 | rule | operational | owise | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)` |
| 19 | syntax | syntax | - | `syntax KItem ::= #callee(Exprs)` |
| 20 | rule | operational | owise | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 21-23 | rule | operational | - | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> // ==== dispatch on the callee value ========================================` |
| 24-25 | rule | operational | - | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k> ` |
| 26 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 27 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| 28 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| 29 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| 30 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| 31 | rule | operational | owise | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 32-37 | rule | operational | - | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> // ==== heap-object arguments/receivers ===================================== // Builtins and type calls READ structure — deref the first two arg positions // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list // methods take the ref itself; every other method receiver is deref'd.` |
| 38-41 | rule | operational | priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 42-46 | rule | operational | priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 47-51 | rule | operational | priority | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] ` |
| 52 | syntax | syntax | function,total | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 53-55 | rule | equation | - | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 56-62 | rule | operational | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mutating methods READ their heap-object arguments too (join's list); // mutators keep refs (append of a list into a list-of-lists stays aliased)` |
| 63-68 | rule | operational | priority | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)] ` |
| 69-79 | rule | operational | - | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> // annotated closure: the frame starts with the captured freevar cells, its // parent is the module scope (all enclosing-local reads go through cells), // and the cellvars' fresh cells allocate before params bind (a cellvar param // then writes through its cell in #bindP).` |
| 80-86 | rule | operational | - | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> ` |
| 87 | syntax | syntax | - | `syntax KItem ::= #allocCells(ParamNames)` |
| 88 | rule | operational | - | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 89-94 | rule | operational | - | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |

## `semantics/comprehension.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 11 | rule | equation | - | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 12-13 | rule | equation | - | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) ` |
| 14 | syntax | syntax | macro | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 15-17 | rule | equation | - | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc")) ` |
| 18 | syntax | syntax | macro,macro-rec | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 19-20 | rule | equation | - | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 21-23 | rule | equation | - | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts)) ` |
| 24 | syntax | syntax | macro | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 25 | rule | equation | - | `rule compGuard(.Exprs) => Bool(true)` |
| 26 | rule | equation | - | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |

## `semantics/concrete.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 13-15 | rule | operational | - | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 16-24 | rule | operational | priority,concrete | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) // ==== keyed sort, concrete leg ============================================ // Computes each key by a REAL call through the uniform #callee machinery // (closures, len, type objects all work), stable-inserts on the key, and // allocates the result. priority(40) beats sort.k's opaque rules, so krun // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.` |
| 25 | syntax | syntax | - | `syntax Val ::= kvP(Val, Val)` |
| 26-27 | syntax | syntax | - | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 28-30 | rule | operational | priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 31-33 | rule | operational | priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 34-35 | rule | operational | - | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 36-37 | rule | operational | - | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 38-41 | rule | operational | - | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K) ` |
| 42 | syntax | syntax | function | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 43 | rule | equation | - | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 44-46 | rule | equation | - | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 47-50 | rule | equation | - | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2) ` |
| 51 | syntax | syntax | function | `syntax Bool ::= kLt(Val, Val) [function]` |
| 52 | rule | equation | - | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| 53 | rule | equation | - | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| 54-55 | rule | equation | - | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) ` |
| 56 | syntax | syntax | function,total | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 57 | rule | equation | - | `rule unpairVS(.ValSeq) => .ValSeq` |
| 58 | rule | equation | - | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 59 | rule | equation | owise | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |

## `semantics/controls.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 9-11 | rule | operational | - | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 12-19 | rule | operational | priority | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] ` |
| 20-26 | rule | operational | - | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).` |
| 27-34 | rule | operational | priority | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] // ==== import trivia: `from math import floor, ceil` binds the supported // names as builtins in the current scope; every other import is a no-op` |
| 35 | rule | operational | - | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 36 | rule | operational | owise | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 37 | syntax | syntax | - | `syntax KItem ::= #bindImports(ParamNames)` |
| 38 | rule | operational | - | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 39-42 | rule | operational | - | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| 43-47 | rule | operational | - | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") // ==== Expr statement: evaluate for effect, discard the value =============== // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)` |
| 48-50 | rule | operational | - | `rule <k> Expr(_:Val) => .K ... </k> // ==== If (condition evaluated by strictness) ==============================` |
| 51 | syntax | syntax | - | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 52 | rule | operational | - | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 53 | rule | operational | - | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| 54-56 | rule | operational | - | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> // ==== IfExp: ternary T if C else E ========================================` |
| 57-58 | rule | operational | - | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 59-64 | rule | operational | - | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) // ==== For: one loop, in-cell continuation, over #iterNext ================= // (the iterable is evaluated once, by strictness; the protocol stays rewrites — // circularities anchor on #loop and narrowing substitutes the structure)` |
| 65-68 | syntax | syntax | - | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk" ` |
| 69-70 | rule | operational | - | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k> ` |
| 71 | rule | operational | - | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 72 | rule | operational | - | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 73-76 | rule | operational | - | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> // ==== While ==============================================================` |
| 77 | rule | operational | - | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 78 | rule | operational | - | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 79-80 | rule | operational | - | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 81-84 | rule | operational | - | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) // ==== loop control (break / continue) =====================================` |
| 85 | rule | operational | - | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 86 | rule | operational | - | `rule <k> Continue => #cont ... </k>` |
| 87 | rule | operational | - | `rule <k> Break => #brk ... </k>` |
| 88 | rule | operational | - | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 89 | rule | operational | owise | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 90 | rule | operational | - | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 91-94 | rule | operational | priority,owise | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] // ==== heap-object deref at the truthiness/iteration consumers ============== // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)` |
| 95-97 | rule | operational | priority | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 98-100 | rule | operational | priority | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 101-105 | rule | operational | priority | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; // mutating the iterated list inside its own loop is outside the subset)` |
| 106-108 | rule | operational | priority | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |

## `semantics/core.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 13 | syntax | syntax | - | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 14 | syntax | syntax | - | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 15-17 | syntax | syntax | - | `syntax Str ::= str(IntSeq) // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)` |
| 18-24 | syntax | syntax | - | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq) ` |
| 25-35 | syntax | syntax | function | `syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) // a type object (int/str), resolved from the builtins frame \| builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String) // a cooled Attribute: obj.method ` |
| 36 | syntax | syntax | - | `syntax Parent ::= "root" \| parent(Int)` |
| 37 | syntax | syntax | - | `syntax Scope ::= scope(Map, Parent)` |
| 38 | syntax | syntax | - | `syntax KResult ::= Val` |
| 39 | syntax | syntax | - | `syntax Expr ::= Val // cooling puts results back into expression holes` |
| 40 | syntax | syntax | - | `syntax Vals ::= List{Val, ","}` |
| 41 | syntax | syntax | - | `syntax Exc ::= "NoExc" \| "AssertionError"` |
| 42-48 | syntax | syntax | - | `syntax RetState ::= "noRet" \| retV(Val) // ==== configuration ======================================================= // The builtins namespace is a real scope at reserved location -1 (the bottom of every // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0) // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str` // resolve to their type objects; any local/global binding shadows them via normal lookup.` |
| 49-67 | configuration | configuration | - | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code> // ==== heap allocation (constructed lists become objects) ================== // Cons-form emission with a freshness guard (the heap-list-probe discipline: // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is // monotonic — it does NOT wind back at #pop: returned lists escape by ref. // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed); // only CONSTRUCTORS in program syntax allocate.` |
| 68 | syntax | syntax | function,total | `syntax Bool ::= isRefV(Val) [function, total]` |
| 69 | rule | equation | - | `rule isRefV(ref(_:Int)) => true` |
| 70-74 | rule | equation | owise | `rule isRefV(_:Val) => false [owise] // closure cells (Python-faithful capture): the heap holds cellV(V); a // cellRef surfacing as the k-redex reads through (lookup is the only use — // cellRefs never escape to user-visible values)` |
| 75 | syntax | syntax | - | `syntax HeapVal ::= cellV(Val)` |
| 76 | syntax | syntax | function,total | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 77 | rule | equation | - | `rule isCellRef(cellRef(_:Int)) => true` |
| 78-84 | rule | equation | owise | `rule isCellRef(_:Val) => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in plain frames — an unguarded rule lets the // prover narrow abstract k-top values into cellRef junk (probed on // 26-remove-duplicates). Cross-frame reads (a comprehension closure // reading the enclosing function's cellvar) deref inside #look instead.` |
| 85-94 | rule | operational | priority | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] // write through a cell (Assign / #bindP / #bindTgt dispatch here on // cell-bound names) // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)` |
| 95 | syntax | syntax | - | `syntax Val ::= kwV(String, Val)` |
| 96 | syntax | syntax | - | `syntax KItem ::= #kwTag(String)` |
| 97 | rule | operational | - | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 98-99 | rule | operational | - | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 100 | syntax | syntax | function,total | `syntax Bool ::= isKwV(Val) [function, total]` |
| 101 | rule | equation | - | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 102-105 | rule | equation | owise | `rule isKwV(_:Val) => false [owise] // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch // decides by pnMember even over an abstract frame rest (no prover branching)` |
| 106 | syntax | syntax | - | `syntax Val ::= cellsMark(ParamNames)` |
| 107 | syntax | syntax | function | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 108 | rule | equation | - | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 109 | syntax | syntax | function,total | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 110 | rule | equation | - | `rule pnMember(_:String, .ParamNames) => false` |
| 111-112 | rule | equation | - | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R) ` |
| 113 | syntax | syntax | - | `syntax KItem ::= #cellW(Val, Val)` |
| 114-116 | rule | operational | - | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap> ` |
| 117 | syntax | syntax | - | `syntax KItem ::= #alloc(Val)` |
| 118-123 | rule | operational | - | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) // ==== module load + statement sequencing ==================================` |
| 124 | syntax | syntax | - | `syntax KItem ::= #loadAll(Module)` |
| 125 | rule | operational | - | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 126 | rule | operational | - | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 127-129 | rule | operational | - | `rule <k> .Stmts => .K ... </k> // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====` |
| 130 | syntax | syntax | - | `syntax KItem ::= #look(String, Int)` |
| 131 | rule | operational | - | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 132-144 | rule | operational | priority,concrete | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (higher priority beats the plain return above on concrete cell // bindings; abstract claim values take the plain rule unchanged) — this // covers cross-frame cell reads (a comprehension closure reading the // enclosing function's cellvar) without a narrowing-prone k-top redex // guarded on the FOUND frame's DECLARED cellvars (pnMember over the // cellsMark): decidable for every concrete frame pin — plain frames and // non-cell names prune outright, so an abstract looked-up value never // drags a narrowing cellV heap match along (probed on 5-intersperse and // Q4's abstract `numbers` in the annotated frame)` |
| 145-151 | rule | operational | priority | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| 152-156 | rule | operational | - | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) // the ONE predefined builtins scope (the -1 frame; claims write `-1 \|-> builtinsScope`)` |
| 157 | syntax | syntax | function,total | `syntax Scope ::= "builtinsScope" [function, total]` |
| 158-184 | rule | equation | - | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root) // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination == // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)` |
| 185 | syntax | syntax | - | `syntax ApplyK ::= toCall(Val)` |
| 186-188 | syntax | syntax | - | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 189 | rule | operational | - | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 190 | rule | operational | - | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 191-193 | rule | operational | - | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> // ==== Int / Bool / None literals ==========================================` |
| 194 | rule | operational | - | `rule <k> Int(I:Int) => I ... </k>` |
| 195 | rule | operational | - | `rule <k> Bool(B:Bool) => B ... </k>` |
| 196-198 | rule | operational | - | `rule <k> NoneVal => noneV ... </k> // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================` |
| 199 | syntax | syntax | function | `syntax Bool ::= truthy(Val) [function]` |
| 200 | rule | equation | - | `rule truthy(B:Bool) => B` |
| 201 | rule | equation | - | `rule truthy(noneV) => false` |
| 202 | rule | equation | - | `rule truthy(I:Int) => I =/=Int 0` |
| 203 | rule | equation | - | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| 204 | rule | equation | - | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 205-207 | rule | equation | - | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) // ==== extensible operator dispatch (cases added by the construct modules) ==` |
| 208 | syntax | syntax | function | `syntax Val ::= applyUn(String, Val) [function]` |
| 209 | syntax | syntax | function | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| 210-212 | syntax | syntax | function | `syntax Bool ::= applyCmp(String, Val, Val) [function] // ==== shared list helpers =================================================` |
| 213 | syntax | syntax | function,total | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 214 | rule | equation | - | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| 215-216 | rule | equation | - | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V) ` |
| 217 | syntax | syntax | function,total | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 218 | rule | equation | - | `rule vals2valSeq(.Vals) => .ValSeq` |
| 219-222 | rule | equation | - | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) // ==== shared sequence length (len / summaries across many modules) ======== // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)` |
| 223 | syntax | syntax | function,total | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 224 | rule | equation | - | `rule vsLen(.ValSeq) => 0` |
| 225-226 | rule | equation | - | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S) ` |
| 227 | syntax | syntax | function,total | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 228 | rule | equation | - | `rule isLen(.IntSeq) => 0` |
| 229-232 | rule | equation | - | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)` |
| 233 | syntax | syntax | function,total | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 234 | rule | equation | - | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| 235 | rule | equation | - | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| 236-237 | rule | equation | - | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 238-239 | rule | equation | - | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` |

## `semantics/dict.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 20-22 | syntax | syntax | - | `syntax Val ::= dictV(ValSeq, ValSeq) // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.` |
| 23-25 | syntax | syntax | - | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 26 | rule | operational | - | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 27 | rule | operational | - | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 28-29 | rule | operational | - | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 30-31 | rule | operational | - | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 32-36 | rule | operational | concrete | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.` |
| 37 | syntax | syntax | function,total | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 38 | rule | equation | - | `rule dHasKey(.ValSeq, _:Val) => false` |
| 39 | rule | equation | - | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| 40-42 | rule | equation | - | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) // dPutK: KS unchanged if K already present, else append K (keep-first-position).` |
| 43 | syntax | syntax | function,total | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 44 | rule | equation | - | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| 45-48 | rule | equation | owise | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).` |
| 49 | syntax | syntax | function,total | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 50-51 | rule | equation | - | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` |
| 52-53 | rule | equation | - | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 54-57 | rule | equation | owise | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] // ==== dict methods ======================================================== // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).` |
| 58-62 | rule | operational | priority | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==` |
| 63 | rule | equation | - | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 64 | syntax | syntax | function | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 65-69 | rule | operational | priority | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] // ==== dict subscript-assign: d[k] = v (insert/update in place) ============= // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.` |
| 70 | syntax | syntax | function | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 71-75 | rule | equation | - | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope // value: a bare dict updates in the scope (dicts stay values); a ref (a heap // list — or a heap dict later) writes the heap in place.` |
| 76 | syntax | syntax | - | `syntax KItem ::= #dsetK(String, Val)` |
| 77 | rule | operational | - | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 78-81 | rule | operational | - | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| 82-85 | rule | operational | - | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 86 | syntax | syntax | - | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 87-89 | rule | operational | - | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is not imported here)` |
| 90 | syntax | syntax | function,total | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 91 | rule | equation | - | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 92-94 | rule | equation | - | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 // ==== dict == (order-insensitive: same size + same key->value pairs) =======` |
| 95-96 | rule | equation | - | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 97 | syntax | syntax | function | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 98 | rule | equation | - | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 99-100 | rule | equation | - | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 101 | syntax | syntax | function | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 102 | rule | equation | - | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| 103 | rule | equation | - | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |

## `semantics/float.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 20 | syntax | syntax | - | `syntax Val ::= Float` |
| 21-23 | rule | operational | concrete | `rule <k> Float(F:Float) => F ... </k> // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.` |
| 24 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 25-26 | rule | equation | concrete | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete] ` |
| 27-29 | rule | equation | concrete | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.` |
| 30 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 31 | rule | equation | concrete | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 32-36 | rule | equation | concrete | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).` |
| 37 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 38 | rule | equation | concrete | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 39-42 | rule | equation | concrete | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on // concrete floats. kprove proofs return floats structurally and do not compare them.` |
| 43 | rule | equation | - | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 44-49 | rule | equation | concrete | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade), // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise // `abs(a-b) < t` proximity test.)` |
| 50 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 51 | rule | equation | concrete | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 52-53 | rule | equation | - | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2) ` |
| 54 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 55 | rule | equation | concrete | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 56-60 | rule | equation | - | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F) // ==== math.ceil =========================================================== // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is // never bound as a value).` |
| 61-64 | rule | operational | priority | `rule <k> Import(_:String) => .K ... </k> // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher // priority than the generic Attribute/method dispatch in call.k).` |
| 65 | syntax | syntax | - | `syntax KItem ::= "#mathCeil"` |
| 66 | rule | operational | priority | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 67-69 | rule | operational | - | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> // math.floor(x) — same interception shape as math.ceil` |
| 70 | syntax | syntax | - | `syntax KItem ::= "#mathFloor"` |
| 71 | rule | operational | priority | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 72 | rule | operational | - | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 73 | syntax | syntax | function,total,symbol | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 74 | rule | equation | concrete | `rule floorFI(I:Int) => I [concrete]` |
| 75-77 | rule | equation | concrete | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] // bare floor/ceil (bound by `from math import floor, ceil`)` |
| 78 | rule | equation | - | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 79-81 | rule | equation | - | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) // math.pow(x, y) — a two-arg interception onto powF (ints promote)` |
| 82 | syntax | syntax | - | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 83 | rule | operational | priority | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 84 | rule | operational | - | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 85 | rule | operational | - | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 86 | syntax | syntax | function,total,symbol | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 87 | rule | equation | concrete | `rule toF(F:Float) => F [concrete]` |
| 88-92 | rule | equation | concrete | `rule toF(I:Int) => intToF(I) [concrete] // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm). // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).` |
| 93 | syntax | syntax | function,total,symbol | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 94 | rule | equation | concrete | `rule ceilF(I:Int) => I [concrete]` |
| 95-98 | rule | equation | concrete | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun; // proofs use symbolic elements, never a float literal.` |
| 99-102 | rule | equation | concrete | `rule applyUn("-", F:Float) => 0.0 -Float F // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.` |
| 103 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 104 | rule | equation | concrete | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 105-106 | rule | equation | - | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2) ` |
| 107 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 108 | rule | equation | concrete | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 109-110 | rule | equation | - | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2) ` |
| 111 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 112 | rule | equation | concrete | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 113-114 | rule | equation | - | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2) ` |
| 115 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 116 | rule | equation | concrete | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 117-118 | rule | equation | - | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2) ` |
| 119 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 120 | rule | equation | concrete | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 121-124 | rule | equation | - | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) // ---- the remaining comparisons (gtF promoted from find_zero — its summaries // case-split on the atom; >= / <= derive from the two opaque compares) ----` |
| 125 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 126 | rule | equation | concrete | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 127 | rule | equation | - | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| 128 | rule | equation | - | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 129-131 | rule | equation | - | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----` |
| 132 | rule | equation | - | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 133 | rule | equation | - | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 134 | rule | equation | - | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 135 | rule | equation | - | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 136 | rule | equation | - | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 137 | rule | equation | - | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 138 | rule | equation | - | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 139-141 | rule | equation | concrete | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----` |
| 142 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 143 | rule | equation | concrete | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 144 | rule | equation | - | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 145 | rule | equation | - | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 146 | rule | equation | - | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 147 | rule | equation | - | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 148 | rule | equation | - | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 149 | rule | equation | - | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 150 | rule | equation | - | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 151-153 | rule | equation | - | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- x == None (promoted from 137; `is` cases live in operators.k) ----` |
| 154 | rule | equation | - | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 155-159 | rule | equation | concrete | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) // ---- float(str): decimal parse (promoted from 137's defined chain) ---- // digits '.' digits, optional leading '-'; concrete evaluation only (the // symbolic side stays an opaque decStrToF term a proof case-splits on).` |
| 160 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 161 | rule | equation | concrete | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 162-164 | rule | equation | concrete | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 165 | syntax | syntax | function | `syntax Int ::= headIS(IntSeq) [function]` |
| 166 | rule | equation | - | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 167 | syntax | syntax | function,total | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 168 | rule | equation | - | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 169 | rule | equation | - | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 170 | rule | equation | - | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 171-172 | rule | equation | - | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 173 | syntax | syntax | function,total | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 174 | rule | equation | - | `rule fracPart(.IntSeq) => 0` |
| 175 | rule | equation | - | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 176 | rule | equation | - | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 177 | rule | equation | - | `rule fracAcc(.IntSeq, A:Int) => A` |
| 178 | rule | equation | - | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 179 | syntax | syntax | function,total | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 180 | rule | equation | - | `rule fracScale(.IntSeq) => 1` |
| 181 | rule | equation | - | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 182 | rule | equation | - | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 183 | rule | equation | - | `rule fscAcc(.IntSeq, A:Int) => A` |
| 184 | rule | equation | - | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 185 | rule | equation | - | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 186 | rule | equation | - | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 187-189 | rule | equation | - | `rule applyBuiltin("float", F:Float, .Vals) => F // ---- float / int division (promoted from mean_absolute_deviation) ----` |
| 190 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 191 | rule | equation | concrete | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 192-194 | rule | equation | - | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) // ---- int -> float promotion for the remaining mixed arithmetic/compares ----` |
| 195 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 196 | rule | equation | concrete | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 197 | rule | equation | - | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 198 | rule | equation | - | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 199 | rule | equation | - | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 200 | rule | equation | - | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 201 | rule | equation | - | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 202 | rule | equation | - | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 203 | rule | equation | - | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 204 | rule | equation | - | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 205 | rule | equation | - | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 206-208 | rule | equation | - | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----` |
| 209 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 210 | rule | equation | concrete | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 211-212 | rule | equation | - | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F) ` |
| 213 | rule | equation | - | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 214-216 | rule | equation | - | `rule applyBuiltin("float", F:Float, .Vals) => F // round: Python half-even (banker's); round(F, N) scales by 10^N` |
| 217 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 218-222 | rule | equation | concrete | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| 223 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 224-226 | rule | equation | concrete | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 227 | rule | equation | - | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| 228-229 | rule | equation | - | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N) ` |
| 230 | syntax | syntax | function,total,symbol,no-evaluators | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 231 | rule | equation | concrete | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 232 | syntax | syntax | - | `syntax KItem ::= "#mathSqrt"` |
| 233 | rule | operational | priority | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 234 | rule | operational | - | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 235-242 | rule | operational | priority,concrete | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive: // the isFloat guard is disjoint from the existing isInt one.` |
| 243 | syntax | syntax | - | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 244 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 245 | rule | operational | - | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 246 | rule | operational | - | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 247-249 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V) ` |
| 250 | syntax | syntax | - | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 251 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 252 | rule | operational | - | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 253 | rule | operational | - | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 254-260 | rule | operational | concrete | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin). // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof // with isInt(V) in its path condition refutes this branch without sort reasoning.` |
| 261 | syntax | syntax | - | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 262-264 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 265 | rule | operational | - | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 266 | rule | operational | - | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 267-269 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 270-272 | rule | operational | - | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |

## `semantics/functions.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 8-13 | syntax | syntax | - | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" // ==== def / anonymous closure =============================================` |
| 14-17 | rule | operational | - | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes> ` |
| 18 | syntax | syntax | - | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 19-26 | rule | operational | - | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> // ==== annotated def/lambda (closure cells; spec 2.3) ====================== // closureValC(params, cellvars, body, captured-cells). No frame anchor: all // enclosing-local reads are freevars (symtable-complete) and go through the // captured cells; everything else is global/builtin, so the callee frame's // parent is the module scope (0) — sound after the defining frame dies.` |
| 27-30 | syntax | syntax | - | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) // capture: resolve each freevar to the enclosing frame's cellRef, then bind // (FuncDef) or yield (Lambda) the closure value.` |
| 31-32 | syntax | syntax | - | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 33-35 | rule | operational | - | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 36-41 | rule | operational | - | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 42-46 | rule | operational | - | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes> ` |
| 47-49 | rule | operational | - | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 50-52 | rule | operational | - | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 53-58 | rule | operational | - | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 59-62 | rule | operational | - | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> // ==== bind params ========================================================` |
| 63 | rule | operational | - | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 64-67 | rule | operational | - | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound to its cell at frame entry` |
| 68-77 | rule | operational | priority | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] // ==== return / pop the frame (the returned expr evaluates by strictness) ==` |
| 78-79 | rule | operational | - | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 80-84 | rule | operational | - | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).` |
| 85-90 | rule | operational | - | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |

## `semantics/int.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 7-8 | rule | equation | - | `rule applyUn("-", I:Int) => 0 -Int I ` |
| 9-10 | rule | equation | - | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b))` |
| 11 | rule | equation | - | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 12 | rule | equation | - | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 13 | rule | equation | - | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| 14 | rule | equation | - | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| 15 | rule | equation | - | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| 16 | rule | equation | - | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 17-18 | rule | equation | - | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0 ` |
| 19 | syntax | syntax | function | `syntax Int ::= pyMod(Int, Int) [function]` |
| 20-21 | rule | equation | - | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2 ` |
| 22 | rule | equation | - | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| 23 | rule | equation | - | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| 24 | rule | equation | - | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| 25 | rule | equation | - | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| 26 | rule | equation | - | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| 27 | rule | equation | - | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |

## `semantics/iter.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 8 | syntax | syntax | - | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |

## `semantics/list.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 9 | rule | operational | - | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| 10-12 | rule | operational | - | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> // ==== ListExpr: [...] literal -> a fresh heap object =======================` |
| 13 | syntax | syntax | - | `syntax ApplyK ::= "toList"` |
| 14 | rule | operational | - | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 15-17 | rule | operational | - | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> // ==== list ops: + / == / != ===============================================` |
| 18 | syntax | syntax | function,total | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 19 | rule | equation | - | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| 20-23 | rule | equation | priority | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) // list + list constructs a NEW object (k-cell — it allocates; operands land here // already deref'd). priority(45) beats the generic BinOp dispatch.` |
| 24-26 | rule | operational | priority | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)] ` |
| 27 | rule | equation | - | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 28-32 | rule | equation | concrete | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) // ==== deep equality when elements are heap objects (list-of-lists) ======== // Python == is structural at every depth. Fires ONLY when a ref is present // (the guard decides on concrete seqs); the plain ==K path above is unchanged.` |
| 33 | syntax | syntax | function,total | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 34 | rule | equation | - | `rule hasRefVS(.ValSeq) => false` |
| 35-36 | rule | equation | - | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R) ` |
| 37-38 | syntax | syntax | function | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function]` |
| 39 | rule | equation | - | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| 40 | rule | equation | - | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| 41 | rule | equation | - | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| 42-44 | rule | equation | - | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP) ` |
| 45-46 | rule | equation | - | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 47-48 | rule | equation | - | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 49 | rule | equation | - | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 50-52 | rule | equation | owise | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] // ==== mutator: xs.append(v) — an in-place heap write ======================` |
| 53-57 | rule | operational | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] // ==== `x in list` — a <k>-cell fold over #iterNext ========================` |
| 58 | syntax | syntax | - | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 59 | rule | operational | - | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 60 | rule | operational | - | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 61 | rule | operational | - | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 62 | rule | operational | - | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 63-64 | rule | operational | - | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 65-66 | rule | operational | - | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 67 | rule | operational | - | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |

## `semantics/methods.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 10-12 | syntax | syntax | function | `syntax Val ::= applyMethod(Val, String, Vals) [function] // ==== string predicates (Python semantics) =================================` |
| 13 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 14 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 15 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 16-18 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) // ==== case maps ============================================================` |
| 19 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| 20 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| 21-25 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) // ==== join / count / strip / encode ======================================== // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by // the call layer; the result str is a value)` |
| 26 | rule | equation | - | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 27 | syntax | syntax | function,total | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 28 | rule | equation | - | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 29 | rule | equation | - | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 30-33 | rule | equation | - | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) // S.count(sub): non-overlapping window scan (Python str.count)` |
| 34 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 35 | syntax | syntax | function | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 36 | rule | equation | - | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 37-38 | rule | equation | - | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 39-40 | rule | equation | - | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 41 | syntax | syntax | function,total | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 42 | rule | equation | - | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 43 | rule | equation | owise | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 44-46 | rule | equation | - | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 // S.strip(): trim whitespace runs from both ends` |
| 47 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 48 | syntax | syntax | function,total | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 49 | rule | equation | - | `rule trimWS(.IntSeq) => .IntSeq` |
| 50 | rule | equation | - | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 51 | rule | equation | - | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 52 | syntax | syntax | function,total | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 53 | rule | equation | - | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 54 | rule | equation | - | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 55-57 | rule | equation | - | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) // S.encode('ascii'): identity on the code-sequence model (bytes == codes)` |
| 58-60 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) // ==== prefix ===============================================================` |
| 61-63 | rule | equation | concrete | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========` |
| 64 | rule | equation | - | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 65 | syntax | syntax | function,total | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 66 | rule | equation | - | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| 67 | rule | equation | - | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 68-71 | rule | equation | - | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ========== // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.` |
| 72-74 | rule | operational | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 75 | syntax | syntax | function | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` |
| 76 | rule | equation | - | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 77-78 | rule | equation | - | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 79-81 | rule | equation | - | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty.` |
| 82 | syntax | syntax | function | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 83 | rule | equation | - | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| 84 | rule | equation | - | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 85 | syntax | syntax | function,total | `syntax Bool ::= isWSC(Int) [function, total]` |
| 86-88 | rule | equation | - | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 // split(sep='x') keyword form delegates to the positional k-cell rule` |
| 89-93 | rule | operational | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).` |
| 94-96 | rule | operational | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 97 | syntax | syntax | function | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` |
| 98 | rule | equation | - | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| 99-100 | rule | equation | - | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 101-103 | rule | equation | - | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP) ` |
| 104-105 | rule | equation | - | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 106 | syntax | syntax | function,total | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 107 | rule | equation | - | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| 108 | rule | equation | - | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 109-111 | rule | equation | - | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) // ==== char helpers =========================================================` |
| 112 | syntax | syntax | function,total | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 113-114 | rule | equation | - | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90 ` |
| 115 | syntax | syntax | function,total | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 116-117 | rule | equation | - | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122 ` |
| 118 | syntax | syntax | function,total | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 119-120 | rule | equation | - | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C) ` |
| 121 | syntax | syntax | function,total | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 122-123 | rule | equation | - | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57 ` |
| 124 | syntax | syntax | function,total | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 125 | rule | equation | - | `rule hasUpper(.IntSeq) => false` |
| 126-127 | rule | equation | - | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S) ` |
| 128 | syntax | syntax | function,total | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 129 | rule | equation | - | `rule hasLower(.IntSeq) => false` |
| 130-131 | rule | equation | - | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S) ` |
| 132 | syntax | syntax | function,total | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 133 | rule | equation | - | `rule allAlpha(.IntSeq) => true` |
| 134-135 | rule | equation | - | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S) ` |
| 136 | syntax | syntax | function,total | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 137 | rule | equation | - | `rule allDigit(.IntSeq) => true` |
| 138-139 | rule | equation | - | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S) ` |
| 140-141 | syntax | syntax | function,total | `syntax Int ::= lowerC(Int) [function, total] ` |
| 142 | rule | equation | - | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 143-144 | rule | equation | owise | `rule lowerC(C:Int) => C [owise] ` |
| 145 | syntax | syntax | function,total | `syntax Int ::= upperC(Int) [function, total]` |
| 146 | rule | equation | - | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 147-148 | rule | equation | owise | `rule upperC(C:Int) => C [owise] ` |
| 149 | syntax | syntax | function,total | `syntax Int ::= swapC(Int) [function, total]` |
| 150 | rule | equation | - | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 151 | rule | equation | - | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 152-153 | rule | equation | owise | `rule swapC(C:Int) => C [owise] ` |
| 154 | syntax | syntax | function,total | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 155 | rule | equation | - | `rule mapLower(.IntSeq) => .IntSeq` |
| 156-157 | rule | equation | - | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S)) ` |
| 158 | syntax | syntax | function,total | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 159 | rule | equation | - | `rule mapUpper(.IntSeq) => .IntSeq` |
| 160-161 | rule | equation | - | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S)) ` |
| 162 | syntax | syntax | function,total | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 163 | rule | equation | - | `rule mapSwap(.IntSeq) => .IntSeq` |
| 164-165 | rule | equation | - | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S)) ` |
| 166 | syntax | syntax | function,total | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 167 | rule | equation | - | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| 168 | rule | equation | - | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 169 | rule | equation | - | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |

## `semantics/operators.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 10-11 | rule | operational | - | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k> ` |
| 12-14 | rule | operational | - | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes` |
| 15 | context | context | - | `context Compare(HOLE, _)` |
| 16 | context | context | - | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 17-18 | rule | operational | owise | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise] ` |
| 19 | rule | equation | - | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| 20-24 | rule | equation | priority | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) // ==== operand deref: heap objects combine/compare by STRUCTURE ============ // (Python: list == is structural; identity only via `is`.) priority(40) // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.` |
| 25-27 | rule | operational | priority | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 28-33 | rule | operational | priority | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd` |
| 34-37 | rule | operational | priority | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 38-43 | rule | operational | priority | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)] ` |
| 44-46 | rule | operational | priority | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |

## `semantics/range.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 9 | syntax | syntax | function,total | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 10-11 | rule | equation | - | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI) ` |
| 12 | syntax | syntax | function | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 13-14 | rule | equation | - | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 15-16 | rule | equation | - | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 17-19 | rule | equation | - | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO) ` |
| 20-22 | rule | operational | - | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 23-24 | rule | operational | - | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |

## `semantics/set.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 8-10 | syntax | syntax | - | `syntax Val ::= setV(IntSeq) // membership of a code in the accumulated distinct-code sequence` |
| 11 | syntax | syntax | function,total | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 12 | rule | equation | - | `rule codeIn(_:Int, .IntSeq) => false` |
| 13-15 | rule | equation | - | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) // the distinct codes of CS (insert-if-absent fold, first-seen order)` |
| 16-17 | syntax | syntax | function,total | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total]` |
| 18 | rule | equation | - | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 19 | rule | equation | - | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 20-21 | rule | equation | - | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 22-24 | rule | equation | - | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC) ` |
| 25 | syntax | syntax | function,total | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 26 | rule | equation | - | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| 27-30 | rule | equation | - | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) // ==== set equality: two sets are equal iff mutually subsuming ============== // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).` |
| 31 | syntax | syntax | function,total | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 32 | rule | equation | - | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| 33-34 | rule | equation | - | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B) ` |
| 35 | syntax | syntax | function,total | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 36-38 | rule | equation | - | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) // set == set (the only comparison sets support here)` |
| 39 | rule | equation | - | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |

## `semantics/sort.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 18 | syntax | syntax | function,total,symbol,no-evaluators | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 19 | syntax | syntax | function | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 20 | rule | equation | concrete | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| 21 | rule | equation | concrete | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 22 | rule | equation | concrete | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| 23 | rule | equation | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 24-25 | rule | equation | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k)` |
| 26 | syntax | syntax | function | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 27 | rule | equation | concrete | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 28 | rule | equation | concrete | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 29-30 | rule | equation | concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 31-35 | rule | equation | concrete,owise | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise] // applyBuiltin routing in call.k) so the result allocates.` |
| 36-39 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> // mutator: xs.sort() — the in-place heap write over the same trusted sortVS` |
| 40-48 | rule | operational | priority,concrete | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] // ==== keyed / reversed sorted() (WP2) ===================================== // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV // (a closure/builtin/type — anything callable). OPAQUE here; the concrete // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable- // inserts, at priority(40) over these.` |
| 49-50 | syntax | syntax | function,total,symbol,no-evaluators | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators] ` |
| 51-52 | syntax | syntax | function,total | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 53 | rule | equation | - | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 54 | rule | equation | - | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 55-56 | rule | equation | - | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A)) ` |
| 57 | syntax | syntax | function,total | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 58 | rule | equation | - | `rule condRev(S:ValSeq, false) => S` |
| 59-60 | rule | equation | - | `rule condRev(S:ValSeq, true) => revVS(S) ` |
| 61-62 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 63-64 | rule | operational | - | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 65-71 | rule | operational | concrete | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write // their postcondition directly as valSeqAt(sortVS(VS), …).` |

## `semantics/str.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 8 | rule | operational | - | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| 9-12 | rule | operational | - | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> // ==== str literal (ASCII-only) ============================================` |
| 13 | syntax | syntax | function | `syntax IntSeq ::= strToCodes(String) [function]` |
| 14 | rule | operational | - | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 15 | rule | equation | - | `rule strToCodes("") => .IntSeq` |
| 16-19 | rule | equation | - | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 // ==== operators: + / == / != / in =========================================` |
| 20 | syntax | syntax | function,total | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 21 | rule | equation | - | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| 22-23 | rule | equation | - | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T)) ` |
| 24 | rule | equation | - | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 25 | rule | equation | - | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 26-28 | rule | equation | - | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) // substring membership: `P in X` iff the code-seq P occurs contiguously in X` |
| 29 | rule | equation | - | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 30-31 | rule | equation | - | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X) ` |
| 32 | syntax | syntax | function,total | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 33 | rule | equation | - | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| 34 | rule | equation | - | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 35-36 | rule | equation | - | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs) ` |
| 37 | syntax | syntax | function,total | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 38 | rule | equation | - | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| 39 | rule | equation | - | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| 40-47 | rule | equation | - | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on // str </<=/>/>= comparisons.` |
| 48 | syntax | syntax | function,total | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 49 | rule | equation | - | `rule strLt(.IntSeq, .IntSeq) => false` |
| 50 | rule | equation | - | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 51 | rule | equation | - | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 52 | rule | equation | - | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| 53 | rule | equation | - | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| 54-55 | rule | equation | - | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B ` |
| 56 | rule | equation | - | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 57 | rule | equation | - | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 58 | rule | equation | - | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 59 | rule | equation | - | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |

## `semantics/subscript.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 11 | syntax | syntax | function,total | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 12 | rule | equation | - | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| 13-15 | rule | equation | - | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0 ` |
| 16 | syntax | syntax | function | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 17 | rule | equation | - | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| 18-20 | rule | equation | - | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0 ` |
| 21 | syntax | syntax | function,total | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 22 | rule | equation | - | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 23-26 | rule | equation | - | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0 // ==== Subscript: indexing obj[i] (list / tuple / str) ===================== // contexts (not strict attrs): the Index slot's Slice alternative must never heat` |
| 27 | context | context | - | `context Subscript(HOLE, _)` |
| 28-30 | context | context | - | `context Subscript(_:Val, HOLE:Expr) // heap-object deref (covers both the index and slice forms via the Index slot)` |
| 31-34 | rule | operational | priority | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] ` |
| 35-36 | rule | operational | - | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k> ` |
| 37 | syntax | syntax | function | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 38 | rule | equation | - | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 39 | rule | equation | - | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 40-43 | rule | equation | - | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========` |
| 44-48 | syntax | syntax | - | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt) ` |
| 49 | syntax | syntax | - | `syntax OptInt ::= "noB" \| someB(Int)` |
| 50 | rule | operational | - | `rule <k> #evalB(NoBound) => noB ... </k>` |
| 51 | rule | operational | - | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| 52-53 | rule | operational | - | `rule <k> I:Int ~> #toSome => someB(I) ... </k> ` |
| 54 | rule | operational | - | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 55 | rule | operational | - | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 56-57 | rule | operational | - | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value` |
| 58-60 | rule | operational | priority | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 61-62 | rule | operational | - | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k> ` |
| 63 | syntax | syntax | function | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 64-65 | rule | equation | - | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 66-67 | rule | equation | - | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 68-71 | rule | equation | - | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) // ==== slice.indices: step / start / stop / clamp ==========================` |
| 72 | syntax | syntax | function,total | `syntax Int ::= slStep(OptInt) [function, total]` |
| 73 | rule | equation | - | `rule slStep(noB) => 1` |
| 74-75 | rule | equation | - | `rule slStep(someB(S:Int)) => S ` |
| 76 | syntax | syntax | function | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 77-78 | rule | equation | - | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 79-80 | rule | equation | - | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` |
| 81-82 | rule | equation | - | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST)) ` |
| 83 | syntax | syntax | function | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 84-85 | rule | equation | - | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` |
| 86-87 | rule | equation | - | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 88-89 | rule | equation | - | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST)) ` |
| 90 | syntax | syntax | function,total | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 91-92 | rule | equation | - | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` |
| 93-95 | rule | equation | - | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0 ` |
| 96 | syntax | syntax | function,total | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 97-98 | rule | equation | - | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 99-101 | rule | equation | - | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0 ` |
| 102 | syntax | syntax | function,total | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 103-104 | rule | equation | - | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` |
| 105-108 | rule | equation | - | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN // ==== build the strided sub-sequence (indices in range by construction) ====` |
| 109 | syntax | syntax | function | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 110-112 | rule | equation | - | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 113-115 | rule | equation | - | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) ` |
| 116 | syntax | syntax | function | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 117-119 | rule | equation | - | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 120-121 | rule | equation | - | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |

## `semantics/syntax.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 9-31 | syntax | syntax | macro,strict,seqstrict | `syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda" "(" Params "," Expr ")" \| "KwArg" "(" String "," Expr ")" \| "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call" "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare" "(" Expr "," CmpOp ")" ` |
| 32 | syntax | syntax | - | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| 33 | syntax | syntax | - | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| 34 | syntax | syntax | - | `syntax Entries ::= List{Entry, ","}` |
| 35 | syntax | syntax | - | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 36 | syntax | syntax | - | `syntax CompFors ::= List{CompFor, ""}` |
| 37 | syntax | syntax | - | `syntax Exprs ::= List{Expr, ","}` |
| 38 | syntax | syntax | - | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 39-40 | syntax | syntax | - | `syntax Bound ::= Expr \| "NoBound" ` |
| 41-55 | syntax | syntax | strict | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [strict] \| "Expr" "(" Expr ")" [strict] \| "FuncDef" "(" String "," Params "," Stmts ")" \| "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")" ` |
| 56 | syntax | syntax | - | `syntax Stmts ::= List{Stmt, ""}` |
| 57 | syntax | syntax | - | `syntax Params ::= "Params" "(" ParamNames ")"` |
| 58 | syntax | syntax | - | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| 59 | syntax | syntax | - | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| 60 | syntax | syntax | - | `syntax ParamNames ::= List{String, ","}` |
| 61 | syntax | syntax | - | `syntax Module ::= "Module" "(" Stmts ")"` |

## `semantics/tuple.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 10 | rule | operational | - | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| 11-13 | rule | operational | - | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================` |
| 14 | syntax | syntax | - | `syntax ApplyK ::= "toTuple"` |
| 15 | rule | operational | - | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 16-17 | rule | operational | - | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k> ` |
| 18-19 | rule | equation | - | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k)` |
| 20 | rule | operational | - | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 21-22 | rule | operational | - | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset)` |
| 23 | rule | equation | - | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 24 | syntax | syntax | function | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 25 | rule | equation | - | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 26-27 | rule | equation | - | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 28-30 | rule | equation | - | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) // ==== target binding: bind a Name or a TupleExpr target to a value ========` |
| 31 | syntax | syntax | - | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 32-34 | rule | operational | - | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 35-41 | rule | operational | priority | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 42 | rule | operational | - | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 43 | rule | operational | - | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 44-48 | rule | operational | priority | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // ==== unpacking: a, b = <tuple\|list> (RHS evaluated by strictness) ========` |
| 49 | syntax | syntax | - | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 50 | rule | operational | - | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 51 | rule | operational | - | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 52-54 | rule | operational | priority | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 55-56 | rule | operational | - | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 57 | rule | operational | - | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |

## `/candidate/verification.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 9 | syntax | syntax | function,total | `syntax Stmts ::= "sortArrayBody" [function, total]` |
| 10-32 | rule | equation | - | `rule sortArrayBody => If( UnaryOp("not", Name("array")), Return(ListExpr(.Exprs)) .Stmts, .Stmts) If( Compare( BinOp( "%", BinOp( "+", Subscript(Name("array"), Int(0)), Subscript(Name("array"), UnaryOp("-", Int(1)))), Int(2)), CmpOp("==", Int(1))), Return(Call(Name("sorted"), (Name("array"), .Exprs))) .Stmts, .Stmts) Return( Call( Name("sorted"), (Name("array"), KwArg("reverse", Bool(true)), .Exprs))) .Stmts ` |
| 33 | syntax | syntax | function,total | `syntax Val ::= "sortArrayClosure" [function, total]` |
| 34-37 | rule | equation | - | `rule sortArrayClosure => closureVal(("array", .ParamNames), sortArrayBody, 0) // Symbolic integer lists used by the quantified middle segment in spec.k.` |
| 38 | syntax | syntax | function,total | `syntax ValSeq ::= intsVS(IntSeq) [function, total]` |
| 39 | rule | equation | - | `rule intsVS(.IntSeq) => .ValSeq` |
| 40-41 | rule | equation | - | `rule intsVS(iCons(I:Int, IS:IntSeq)) => vCons(I, intsVS(IS)) ` |
| 42 | syntax | syntax | function,total | `syntax Bool ::= nonNegativeIS(IntSeq) [function, total]` |
| 43 | rule | equation | - | `rule nonNegativeIS(.IntSeq) => true` |
| 44-49 | rule | equation | - | `rule nonNegativeIS(iCons(I:Int, IS:IntSeq)) => I >=Int 0 andBool nonNegativeIS(IS) // snocVS(M, L) is M followed by L. The final rule is a derived // negative-index lemma. It prevents the symbolic rewriter from unfolding // an arbitrary-length middle segment merely to establish Python's a[-1].` |
| 50 | syntax | syntax | - | `syntax ValSeq ::= snocVS(ValSeq, Val)` |
| 51 | rule | equation | - | `rule snocVS(.ValSeq, V:Val) => vCons(V, .ValSeq)` |
| 52-54 | rule | equation | - | `rule snocVS(vCons(H:Val, T:ValSeq), V:Val) => vCons(H, snocVS(T, V)) ` |
| 55-62 | rule | operational | priority | `rule <k> Subscript( list(vCons(_F:Int, snocVS(_M:ValSeq, L:Int))), UnaryOp("-", Int(1))) => L ... </k> [priority(40)]` |

## `/candidate/spec.k`

| Location | Kind | Category | Attributes | Source declaration/rule |
|---|---|---|---|---|
| 7-31 | claim | claim | - | `claim <k> Call(Name("sort_array"), (ref(0), .Exprs)) => ref(1) </k> <env> 0 </env> <scopes> 0 \|-> scope("sort_array" \|-> sortArrayClosure, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> 0 \|-> list(.ValSeq) => (0 \|-> list(.ValSeq)) (1 \|-> list(.ValSeq)) </heap> <heapLoc> 1 => 2 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> // A singleton is necessarily in the even branch. The result is fresh and // the original heap object is unchanged.` |
| 32-57 | claim | claim | - | `claim <k> Call(Name("sort_array"), (ref(0), .Exprs)) => ref(1) </k> <env> 0 </env> <scopes> 0 \|-> scope("sort_array" \|-> sortArrayClosure, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> 0 \|-> list(vCons(F:Int, .ValSeq)) => (0 \|-> list(vCons(F, .ValSeq))) (1 \|-> list(condRev(sortVS(vCons(F, .ValSeq)), true))) </heap> <heapLoc> 1 => 2 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires F >=Int 0 // Every list of length at least two is head ++ middle ++ last. Odd endpoint // parity selects ascending sorted order.` |
| 58-87 | claim | claim | - | `claim <k> Call(Name("sort_array"), (ref(0), .Exprs)) => ref(1) </k> <env> 0 </env> <scopes> 0 \|-> scope("sort_array" \|-> sortArrayClosure, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> 0 \|-> list( vCons(F:Int, snocVS(intsVS(MIDDLE:IntSeq), L:Int))) => (0 \|-> list(vCons(F, snocVS(intsVS(MIDDLE), L)))) (1 \|-> list( sortVS(vCons(F, snocVS(intsVS(MIDDLE), L))))) </heap> <heapLoc> 1 => 2 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires F >=Int 0 andBool L >=Int 0 andBool nonNegativeIS(MIDDLE) andBool pyMod(F +Int L, 2) ==Int 1 // Even endpoint parity selects descending (reverse of ascending) order.` |
| 88-116 | claim | claim | - | `claim <k> Call(Name("sort_array"), (ref(0), .Exprs)) => ref(1) </k> <env> 0 </env> <scopes> 0 \|-> scope("sort_array" \|-> sortArrayClosure, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> 0 \|-> list( vCons(F:Int, snocVS(intsVS(MIDDLE:IntSeq), L:Int))) => (0 \|-> list(vCons(F, snocVS(intsVS(MIDDLE), L)))) (1 \|-> list(condRev( sortVS(vCons(F, snocVS(intsVS(MIDDLE), L))), true))) </heap> <heapLoc> 1 => 2 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires F >=Int 0 andBool L >=Int 0 andBool nonNegativeIS(MIDDLE) andBool pyMod(F +Int L, 2) ==Int 0` |


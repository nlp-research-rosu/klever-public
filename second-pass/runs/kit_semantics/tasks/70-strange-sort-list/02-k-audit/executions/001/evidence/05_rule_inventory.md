# Exhaustive K sentence inventory

Every outer `configuration`, `syntax`, `context`, `rule`, `claim`, and `alias` sentence in the mounted supplied tree, `verification.k`, and `spec.k` is listed below. Continuation lines belong to the preceding row.

| Source | Lines | Kind | Attributes | Assessment | Normalized sentence |
|---|---:|---|---|---|---|
| `semantics/assert.k` | 6-7 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| `semantics/assert.k` | 8-12 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| `semantics/assert.k` | 13-15 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/bool.k` | 8-9 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| `semantics/bool.k` | 10-10 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| `semantics/bool.k` | 11-15 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 // ==== BoolOp: short-circuit, value-returning and / or ===================== // the node is its own accumulator: heat the HEAD element only, then either return it // (short-circuit) or drop it and continue` |
| `semantics/bool.k` | 16-16 | context | `-` | FIXED_RULE_UNUSED_BY_TASK | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| `semantics/bool.k` | 17-17 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| `semantics/bool.k` | 18-19 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| `semantics/bool.k` | 20-21 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| `semantics/bool.k` | 22-23 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| `semantics/bool.k` | 24-28 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the // operand — and/or return the OBJECT itself (Python identity), not its structure` |
| `semantics/bool.k` | 29-30 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| `semantics/bool.k` | 31-34 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `semantics/bool.k` | 35-38 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `semantics/bool.k` | 39-42 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `semantics/bool.k` | 43-46 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `semantics/builtins.k` | 17-19 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Val ::= applyBuiltin(String, Vals) [function] // ==== len(obj) — O(1) per kind ============================================` |
| `semantics/builtins.k` | 20-20 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Int ::= seqLen(Val) [function]` |
| `semantics/builtins.k` | 21-21 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| `semantics/builtins.k` | 22-22 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| `semantics/builtins.k` | 23-23 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| `semantics/builtins.k` | 24-24 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| `semantics/builtins.k` | 25-25 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| `semantics/builtins.k` | 26-31 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) == // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order). // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed. // (k-cell — list() constructs a NEW object)` |
| `semantics/builtins.k` | 32-32 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| `semantics/builtins.k` | 33-33 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| `semantics/builtins.k` | 34-34 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| `semantics/builtins.k` | 35-35 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| `semantics/builtins.k` | 36-36 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| `semantics/builtins.k` | 37-37 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule charsOf(.IntSeq) => .ValSeq` |
| `semantics/builtins.k` | 38-40 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) // ==== set(str) — distinct character codes =================================` |
| `semantics/builtins.k` | 41-43 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) // ==== abs(int) ============================================================` |
| `semantics/builtins.k` | 44-46 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==` |
| `semantics/builtins.k` | 47-47 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| `semantics/builtins.k` | 48-48 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| `semantics/builtins.k` | 49-49 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| `semantics/builtins.k` | 50-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| `semantics/builtins.k` | 54-54 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= intOf(Val) [function]` |
| `semantics/builtins.k` | 55-55 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intOf(I:Int) => I` |
| `semantics/builtins.k` | 56-58 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi // ==== all / any (short-circuiting #iterNext folds) ========================` |
| `semantics/builtins.k` | 59-59 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| `semantics/builtins.k` | 60-60 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| `semantics/builtins.k` | 61-61 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| `semantics/builtins.k` | 62-63 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| `semantics/builtins.k` | 64-66 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| `semantics/builtins.k` | 67-67 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| `semantics/builtins.k` | 68-68 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| `semantics/builtins.k` | 69-69 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| `semantics/builtins.k` | 70-71 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| `semantics/builtins.k` | 72-75 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) // ==== max / min over an iterable (#iterNext folds; first element seeds) ====` |
| `semantics/builtins.k` | 76-76 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| `semantics/builtins.k` | 77-77 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| `semantics/builtins.k` | 78-79 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `semantics/builtins.k` | 80-80 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| `semantics/builtins.k` | 81-81 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| `semantics/builtins.k` | 82-85 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| `semantics/builtins.k` | 86-86 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| `semantics/builtins.k` | 87-87 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| `semantics/builtins.k` | 88-89 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `semantics/builtins.k` | 90-90 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| `semantics/builtins.k` | 91-91 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| `semantics/builtins.k` | 92-96 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) // ==== variadic max / min (a Vals fold) ====================================` |
| `semantics/builtins.k` | 97-97 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= maxVals(Int, Vals) [function]` |
| `semantics/builtins.k` | 98-98 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| `semantics/builtins.k` | 99-99 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule maxVals(M:Int, .Vals) => M` |
| `semantics/builtins.k` | 100-101 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| `semantics/builtins.k` | 102-102 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= minVals(Int, Vals) [function]` |
| `semantics/builtins.k` | 103-103 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| `semantics/builtins.k` | 104-104 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule minVals(M:Int, .Vals) => M` |
| `semantics/builtins.k` | 105-107 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==` |
| `semantics/builtins.k` | 108-110 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits` |
| `semantics/builtins.k` | 111-113 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| `semantics/builtins.k` | 114-114 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| `semantics/builtins.k` | 115-115 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule binCodes(0) => iCons(48, .IntSeq)` |
| `semantics/builtins.k` | 116-116 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| `semantics/builtins.k` | 117-117 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| `semantics/builtins.k` | 118-118 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule binAcc(0, ACC:IntSeq) => ACC` |
| `semantics/builtins.k` | 119-123 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========` |
| `semantics/builtins.k` | 124-125 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| `semantics/builtins.k` | 126-126 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| `semantics/builtins.k` | 127-127 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| `semantics/builtins.k` | 128-131 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) // ==== map(str, xs) — eager (only the str case is in the subset) =============` |
| `semantics/builtins.k` | 132-133 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| `semantics/builtins.k` | 134-134 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| `semantics/builtins.k` | 135-135 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapStrVS(.ValSeq) => .ValSeq` |
| `semantics/builtins.k` | 136-136 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| `semantics/builtins.k` | 137-139 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) // ==== int(x) identities (int(round(x)) composes through) ====================` |
| `semantics/builtins.k` | 140-142 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("int", I:Int, .Vals) => I // ==== ord / chr ===========================================================` |
| `semantics/builtins.k` | 143-143 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| `semantics/builtins.k` | 144-147 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 // ==== str(int) / str(str) =================================================` |
| `semantics/builtins.k` | 148-148 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| `semantics/builtins.k` | 149-151 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====` |
| `semantics/builtins.k` | 152-155 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)` |
| `semantics/builtins.k` | 156-157 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| `semantics/builtins.k` | 158-158 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| `semantics/builtins.k` | 159-159 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| `semantics/builtins.k` | 160-162 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====` |
| `semantics/builtins.k` | 163-163 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| `semantics/builtins.k` | 164-166 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)` |
| `semantics/builtins.k` | 167-168 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| `semantics/builtins.k` | 169-169 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| `semantics/builtins.k` | 170-170 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| `semantics/builtins.k` | 171-172 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| `semantics/builtins.k` | 173-173 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| `semantics/builtins.k` | 174-176 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> // ==== range(stop) / range(start, stop) / range(start, stop, step) =========` |
| `semantics/builtins.k` | 177-177 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| `semantics/builtins.k` | 178-178 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| `semantics/builtins.k` | 179-186 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ======== // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's // trusted pass evaluator, now DEFINED in the reference and driven by a // code-level tokenizer. Reduces on concrete strings (krun); a symbolic // argument leaves the call unevaluated for problem-level folds.` |
| `semantics/builtins.k` | 187-187 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| `semantics/builtins.k` | 188-188 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= evalArith(IntSeq) [function]` |
| `semantics/builtins.k` | 189-191 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| `semantics/builtins.k` | 192-193 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| `semantics/builtins.k` | 194-194 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= evDigit(Int) [function, total]` |
| `semantics/builtins.k` | 195-195 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `semantics/builtins.k` | 196-196 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| `semantics/builtins.k` | 197-197 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| `semantics/builtins.k` | 198-198 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule evHead42(_:IntSeq) => false [owise]` |
| `semantics/builtins.k` | 199-199 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| `semantics/builtins.k` | 200-200 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| `semantics/builtins.k` | 201-202 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule evHead47(_:IntSeq) => false [owise]` |
| `semantics/builtins.k` | 203-203 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| `semantics/builtins.k` | 204-204 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(.IntSeq) => .OpSeq` |
| `semantics/builtins.k` | 205-205 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| `semantics/builtins.k` | 206-206 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| `semantics/builtins.k` | 207-207 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| `semantics/builtins.k` | 208-208 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| `semantics/builtins.k` | 209-209 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| `semantics/builtins.k` | 210-210 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| `semantics/builtins.k` | 211-211 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| `semantics/builtins.k` | 212-213 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` |
| `semantics/builtins.k` | 214-215 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| `semantics/builtins.k` | 216-216 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokNds(.IntSeq) => .IntSeq` |
| `semantics/builtins.k` | 217-217 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| `semantics/builtins.k` | 218-218 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| `semantics/builtins.k` | 219-220 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| `semantics/builtins.k` | 221-222 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| `semantics/builtins.k` | 223-224 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| `semantics/builtins.k` | 225-225 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| `semantics/builtins.k` | 226-226 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| `semantics/builtins.k` | 227-227 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| `semantics/builtins.k` | 228-229 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule firstNdE(_:EvPair) => 0 [owise]` |
| `semantics/builtins.k` | 230-230 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| `semantics/builtins.k` | 231-231 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| `semantics/builtins.k` | 232-232 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| `semantics/builtins.k` | 233-233 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| `semantics/builtins.k` | 234-234 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| `semantics/builtins.k` | 235-235 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| `semantics/builtins.k` | 236-237 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| `semantics/builtins.k` | 238-238 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| `semantics/builtins.k` | 239-239 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| `semantics/builtins.k` | 240-240 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| `semantics/builtins.k` | 241-242 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| `semantics/builtins.k` | 243-243 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| `semantics/builtins.k` | 244-244 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| `semantics/builtins.k` | 245-245 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| `semantics/builtins.k` | 246-246 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| `semantics/builtins.k` | 247-247 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| `semantics/builtins.k` | 248-249 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| `semantics/builtins.k` | 250-250 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| `semantics/builtins.k` | 251-251 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `semantics/builtins.k` | 252-252 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `semantics/builtins.k` | 253-253 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `semantics/builtins.k` | 254-254 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `semantics/builtins.k` | 255-255 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| `semantics/builtins.k` | 256-256 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| `semantics/builtins.k` | 257-259 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| `semantics/builtins.k` | 260-262 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| `semantics/builtins.k` | 263-264 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| `semantics/builtins.k` | 265-265 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| `semantics/builtins.k` | 266-266 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| `semantics/builtins.k` | 267-267 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| `semantics/builtins.k` | 268-268 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule inLevelE(_:String, _:String) => false [owise]` |
| `semantics/builtins.k` | 269-269 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| `semantics/builtins.k` | 270-270 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| `semantics/builtins.k` | 271-271 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| `semantics/builtins.k` | 272-272 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| `semantics/builtins.k` | 273-273 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| `semantics/builtins.k` | 274-278 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ================== // The md5 value itself is a named shared trust (sortVS-style, no concrete // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).` |
| `semantics/builtins.k` | 279-279 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= "#md5"` |
| `semantics/builtins.k` | 280-281 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| `semantics/builtins.k` | 282-282 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| `semantics/builtins.k` | 283-283 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= md5Obj(IntSeq)` |
| `semantics/builtins.k` | 284-284 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| `semantics/builtins.k` | 285-290 | function-declaration | `function; total; symbol(md5hexCodes); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int\|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary name that resolves via the builtins frame to // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).` |
| `semantics/builtins.k` | 291-291 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| `semantics/builtins.k` | 292-292 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| `semantics/builtins.k` | 293-293 | function-declaration | `function; function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| `semantics/builtins.k` | 294-294 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isIntV(_:Int) => true` |
| `semantics/builtins.k` | 295-295 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule isIntV(_:Val) => false [owise]` |
| `semantics/builtins.k` | 296-296 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isStrV(str(_:IntSeq)) => true` |
| `semantics/builtins.k` | 297-297 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule isStrV(_:Val) => false [owise]` |
| `semantics/call.k` | 16-18 | ordinary-rule | `owise` | USED_FIXED_RULE_REVIEWED | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)` |
| `semantics/call.k` | 19-19 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= #callee(Exprs)` |
| `semantics/call.k` | 20-20 | ordinary-rule | `owise` | USED_FIXED_RULE_REVIEWED | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| `semantics/call.k` | 21-23 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> // ==== dispatch on the callee value ========================================` |
| `semantics/call.k` | 24-25 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| `semantics/call.k` | 26-26 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| `semantics/call.k` | 27-27 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| `semantics/call.k` | 28-28 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| `semantics/call.k` | 29-29 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| `semantics/call.k` | 30-30 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| `semantics/call.k` | 31-31 | ordinary-rule | `owise` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| `semantics/call.k` | 32-37 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> // ==== heap-object arguments/receivers ===================================== // Builtins and type calls READ structure — deref the first two arg positions // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list // methods take the ref itself; every other method receiver is deref'd.` |
| `semantics/call.k` | 38-41 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/call.k` | 42-46 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| `semantics/call.k` | 47-51 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/call.k` | 52-52 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax Bool ::= isMutMethod(String) [function, total]` |
| `semantics/call.k` | 53-55 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| `semantics/call.k` | 56-62 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mutating methods READ their heap-object arguments too (join's list); // mutators keep refs (append of a list into a list-of-lists stays aliased)` |
| `semantics/call.k` | 63-68 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| `semantics/call.k` | 69-79 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> // annotated closure: the frame starts with the captured freevar cells, its // parent is the module scope (all enclosing-local reads go through cells), // and the cellvars' fresh cells allocate before params bind (a cellvar param // then writes through its cell in #bindP).` |
| `semantics/call.k` | 80-86 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| `semantics/call.k` | 87-87 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #allocCells(ParamNames)` |
| `semantics/call.k` | 88-88 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| `semantics/call.k` | 89-94 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| `semantics/comprehension.k` | 11-11 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `semantics/comprehension.k` | 12-13 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `semantics/comprehension.k` | 14-14 | syntax-declaration | `macro` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| `semantics/comprehension.k` | 15-17 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| `semantics/comprehension.k` | 18-18 | syntax-declaration | `macro-rec` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| `semantics/comprehension.k` | 19-20 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| `semantics/comprehension.k` | 21-23 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| `semantics/comprehension.k` | 24-24 | syntax-declaration | `macro` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Expr ::= compGuard(Exprs) [macro]` |
| `semantics/comprehension.k` | 25-25 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule compGuard(.Exprs) => Bool(true)` |
| `semantics/comprehension.k` | 26-26 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| `semantics/concrete.k` | 13-15 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| `semantics/concrete.k` | 16-24 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) // ==== keyed sort, concrete leg ============================================ // Computes each key by a REAL call through the uniform #callee machinery // (closures, len, type objects all work), stable-inserts on the key, and // allocates the result. priority(40) beats sort.k's opaque rules, so krun // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.` |
| `semantics/concrete.k` | 25-25 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= kvP(Val, Val)` |
| `semantics/concrete.k` | 26-27 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| `semantics/concrete.k` | 28-30 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| `semantics/concrete.k` | 31-33 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| `semantics/concrete.k` | 34-35 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| `semantics/concrete.k` | 36-37 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| `semantics/concrete.k` | 38-41 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| `semantics/concrete.k` | 42-42 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| `semantics/concrete.k` | 43-43 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| `semantics/concrete.k` | 44-46 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| `semantics/concrete.k` | 47-50 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| `semantics/concrete.k` | 51-51 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= kLt(Val, Val) [function]` |
| `semantics/concrete.k` | 52-52 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| `semantics/concrete.k` | 53-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| `semantics/concrete.k` | 54-55 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `semantics/concrete.k` | 56-56 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| `semantics/concrete.k` | 57-57 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule unpairVS(.ValSeq) => .ValSeq` |
| `semantics/concrete.k` | 58-58 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| `semantics/concrete.k` | 59-59 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| `semantics/controls.k` | 9-11 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `semantics/controls.k` | 12-19 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `semantics/controls.k` | 20-26 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).` |
| `semantics/controls.k` | 27-34 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] // ==== import trivia: `from math import floor, ceil` binds the supported // names as builtins in the current scope; every other import is a no-op` |
| `semantics/controls.k` | 35-35 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| `semantics/controls.k` | 36-36 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| `semantics/controls.k` | 37-37 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #bindImports(ParamNames)` |
| `semantics/controls.k` | 38-38 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| `semantics/controls.k` | 39-42 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| `semantics/controls.k` | 43-47 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") // ==== Expr statement: evaluate for effect, discard the value =============== // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)` |
| `semantics/controls.k` | 48-50 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Expr(_:Val) => .K ... </k> // ==== If (condition evaluated by strictness) ==============================` |
| `semantics/controls.k` | 51-51 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| `semantics/controls.k` | 52-52 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| `semantics/controls.k` | 53-53 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| `semantics/controls.k` | 54-56 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> // ==== IfExp: ternary T if C else E ========================================` |
| `semantics/controls.k` | 57-58 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| `semantics/controls.k` | 59-64 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) // ==== For: one loop, in-cell continuation, over #iterNext ================= // (the iterable is evaluated once, by strictness; the protocol stays rewrites — // circularities anchor on #loop and narrowing substitutes the structure)` |
| `semantics/controls.k` | 65-68 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| `semantics/controls.k` | 69-70 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| `semantics/controls.k` | 71-71 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| `semantics/controls.k` | 72-72 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| `semantics/controls.k` | 73-76 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> // ==== While ==============================================================` |
| `semantics/controls.k` | 77-77 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| `semantics/controls.k` | 78-78 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| `semantics/controls.k` | 79-80 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| `semantics/controls.k` | 81-84 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) // ==== loop control (break / continue) =====================================` |
| `semantics/controls.k` | 85-85 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `semantics/controls.k` | 86-86 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Continue => #cont ... </k>` |
| `semantics/controls.k` | 87-87 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Break => #brk ... </k>` |
| `semantics/controls.k` | 88-88 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `semantics/controls.k` | 89-89 | ordinary-rule | `owise` | USED_FIXED_RULE_REVIEWED | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| `semantics/controls.k` | 90-90 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| `semantics/controls.k` | 91-94 | ordinary-rule | `owise` | USED_FIXED_RULE_REVIEWED | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] // ==== heap-object deref at the truthiness/iteration consumers ============== // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)` |
| `semantics/controls.k` | 95-97 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/controls.k` | 98-100 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/controls.k` | 101-105 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; // mutating the iterated list inside its own loop is outside the subset)` |
| `semantics/controls.k` | 106-108 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/core.k` | 13-13 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| `semantics/core.k` | 14-14 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| `semantics/core.k` | 15-17 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Str ::= str(IntSeq) // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)` |
| `semantics/core.k` | 18-24 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| `semantics/core.k` | 25-35 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) // a type object (int/str), resolved from the builtins frame \| builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String) // a cooled Attribute: obj.method` |
| `semantics/core.k` | 36-36 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Parent ::= "root" \| parent(Int)` |
| `semantics/core.k` | 37-37 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Scope ::= scope(Map, Parent)` |
| `semantics/core.k` | 38-38 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KResult ::= Val` |
| `semantics/core.k` | 39-39 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Expr ::= Val // cooling puts results back into expression holes` |
| `semantics/core.k` | 40-40 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Vals ::= List{Val, ","}` |
| `semantics/core.k` | 41-41 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax Exc ::= "NoExc" \| "AssertionError"` |
| `semantics/core.k` | 42-48 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax RetState ::= "noRet" \| retV(Val) // ==== configuration ======================================================= // The builtins namespace is a real scope at reserved location -1 (the bottom of every // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0) // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str` // resolve to their type objects; any local/global binding shadows them via normal lookup.` |
| `semantics/core.k` | 49-67 | configuration | `-` | USED_FIXED_RULE_REVIEWED | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code> // ==== heap allocation (constructed lists become objects) ================== // Cons-form emission with a freshness guard (the heap-list-probe discipline: // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is // monotonic — it does NOT wind back at #pop: returned lists escape by ref. // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed); // only CONSTRUCTORS in program syntax allocate.` |
| `semantics/core.k` | 68-68 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax Bool ::= isRefV(Val) [function, total]` |
| `semantics/core.k` | 69-69 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule isRefV(ref(_:Int)) => true` |
| `semantics/core.k` | 70-74 | ordinary-rule | `owise` | USED_FIXED_RULE_REVIEWED | `rule isRefV(_:Val) => false [owise] // closure cells (Python-faithful capture): the heap holds cellV(V); a // cellRef surfacing as the k-redex reads through (lookup is the only use — // cellRefs never escape to user-visible values)` |
| `semantics/core.k` | 75-75 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax HeapVal ::= cellV(Val)` |
| `semantics/core.k` | 76-76 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isCellRef(Val) [function, total]` |
| `semantics/core.k` | 77-77 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isCellRef(cellRef(_:Int)) => true` |
| `semantics/core.k` | 78-84 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule isCellRef(_:Val) => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in plain frames — an unguarded rule lets the // prover narrow abstract k-top values into cellRef junk (probed on // 26-remove-duplicates). Cross-frame reads (a comprehension closure // reading the enclosing function's cellvar) deref inside #look instead.` |
| `semantics/core.k` | 85-94 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] // write through a cell (Assign / #bindP / #bindTgt dispatch here on // cell-bound names) // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)` |
| `semantics/core.k` | 95-95 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= kwV(String, Val)` |
| `semantics/core.k` | 96-96 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #kwTag(String)` |
| `semantics/core.k` | 97-97 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| `semantics/core.k` | 98-99 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| `semantics/core.k` | 100-100 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isKwV(Val) [function, total]` |
| `semantics/core.k` | 101-101 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isKwV(kwV(_:String, _:Val)) => true` |
| `semantics/core.k` | 102-105 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule isKwV(_:Val) => false [owise] // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch // decides by pnMember even over an abstract frame rest (no prover branching)` |
| `semantics/core.k` | 106-106 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= cellsMark(ParamNames)` |
| `semantics/core.k` | 107-107 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ParamNames ::= cellsOf(Val) [function]` |
| `semantics/core.k` | 108-108 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| `semantics/core.k` | 109-109 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| `semantics/core.k` | 110-110 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule pnMember(_:String, .ParamNames) => false` |
| `semantics/core.k` | 111-112 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| `semantics/core.k` | 113-113 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #cellW(Val, Val)` |
| `semantics/core.k` | 114-116 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| `semantics/core.k` | 117-117 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= #alloc(Val)` |
| `semantics/core.k` | 118-123 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) // ==== module load + statement sequencing ==================================` |
| `semantics/core.k` | 124-124 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= #loadAll(Module)` |
| `semantics/core.k` | 125-125 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| `semantics/core.k` | 126-126 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| `semantics/core.k` | 127-129 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> .Stmts => .K ... </k> // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====` |
| `semantics/core.k` | 130-130 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= #look(String, Int)` |
| `semantics/core.k` | 131-131 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| `semantics/core.k` | 132-144 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (higher priority beats the plain return above on concrete cell // bindings; abstract claim values take the plain rule unchanged) — this // covers cross-frame cell reads (a comprehension closure reading the // enclosing function's cellvar) without a narrowing-prone k-top redex // guarded on the FOUND frame's DECLARED cellvars (pnMember over the // cellsMark): decidable for every concrete frame pin — plain frames and // non-cell names prune outright, so an abstract looked-up value never // drags a narrowing cellV heap match along (probed on 5-intersperse and // Q4's abstract `numbers` in the annotated frame)` |
| `semantics/core.k` | 145-151 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| `semantics/core.k` | 152-156 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) // the ONE predefined builtins scope (the -1 frame; claims write `-1 \|-> builtinsScope`)` |
| `semantics/core.k` | 157-157 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax Scope ::= "builtinsScope" [function, total]` |
| `semantics/core.k` | 158-184 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root) // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination == // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)` |
| `semantics/core.k` | 185-185 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax ApplyK ::= toCall(Val)` |
| `semantics/core.k` | 186-188 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| `semantics/core.k` | 189-189 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| `semantics/core.k` | 190-190 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| `semantics/core.k` | 191-193 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> // ==== Int / Bool / None literals ==========================================` |
| `semantics/core.k` | 194-194 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Int(I:Int) => I ... </k>` |
| `semantics/core.k` | 195-195 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Bool(B:Bool) => B ... </k>` |
| `semantics/core.k` | 196-198 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> NoneVal => noneV ... </k> // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================` |
| `semantics/core.k` | 199-199 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Bool ::= truthy(Val) [function]` |
| `semantics/core.k` | 200-200 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule truthy(B:Bool) => B` |
| `semantics/core.k` | 201-201 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule truthy(noneV) => false` |
| `semantics/core.k` | 202-202 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule truthy(I:Int) => I =/=Int 0` |
| `semantics/core.k` | 203-203 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| `semantics/core.k` | 204-204 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| `semantics/core.k` | 205-207 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) // ==== extensible operator dispatch (cases added by the construct modules) ==` |
| `semantics/core.k` | 208-208 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Val ::= applyUn(String, Val) [function]` |
| `semantics/core.k` | 209-209 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| `semantics/core.k` | 210-212 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Bool ::= applyCmp(String, Val, Val) [function] // ==== shared list helpers =================================================` |
| `semantics/core.k` | 213-213 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| `semantics/core.k` | 214-214 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| `semantics/core.k` | 215-216 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` |
| `semantics/core.k` | 217-217 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| `semantics/core.k` | 218-218 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule vals2valSeq(.Vals) => .ValSeq` |
| `semantics/core.k` | 219-222 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) // ==== shared sequence length (len / summaries across many modules) ======== // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)` |
| `semantics/core.k` | 223-223 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| `semantics/core.k` | 224-224 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule vsLen(.ValSeq) => 0` |
| `semantics/core.k` | 225-226 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| `semantics/core.k` | 227-227 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= isLen(IntSeq) [function, total]` |
| `semantics/core.k` | 228-228 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isLen(.IntSeq) => 0` |
| `semantics/core.k` | 229-232 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)` |
| `semantics/core.k` | 233-233 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| `semantics/core.k` | 234-234 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| `semantics/core.k` | 235-235 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| `semantics/core.k` | 236-237 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| `semantics/core.k` | 238-239 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` |
| `semantics/dict.k` | 20-22 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= dictV(ValSeq, ValSeq) // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.` |
| `semantics/dict.k` | 23-25 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| `semantics/dict.k` | 26-26 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| `semantics/dict.k` | 27-27 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| `semantics/dict.k` | 28-29 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| `semantics/dict.k` | 30-31 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| `semantics/dict.k` | 32-36 | ordinary-rule | `total` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.` |
| `semantics/dict.k` | 37-37 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| `semantics/dict.k` | 38-38 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dHasKey(.ValSeq, _:Val) => false` |
| `semantics/dict.k` | 39-39 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| `semantics/dict.k` | 40-42 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) // dPutK: KS unchanged if K already present, else append K (keep-first-position).` |
| `semantics/dict.k` | 43-43 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| `semantics/dict.k` | 44-44 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| `semantics/dict.k` | 45-48 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).` |
| `semantics/dict.k` | 49-49 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| `semantics/dict.k` | 50-51 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` |
| `semantics/dict.k` | 52-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| `semantics/dict.k` | 54-57 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] // ==== dict methods ======================================================== // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).` |
| `semantics/dict.k` | 58-62 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==` |
| `semantics/dict.k` | 63-63 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| `semantics/dict.k` | 64-64 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| `semantics/dict.k` | 65-69 | priority-rule | `priority(45)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] // ==== dict subscript-assign: d[k] = v (insert/update in place) ============= // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.` |
| `semantics/dict.k` | 70-70 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| `semantics/dict.k` | 71-75 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope // value: a bare dict updates in the scope (dicts stay values); a ref (a heap // list — or a heap dict later) writes the heap in place.` |
| `semantics/dict.k` | 76-76 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #dsetK(String, Val)` |
| `semantics/dict.k` | 77-77 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| `semantics/dict.k` | 78-81 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| `semantics/dict.k` | 82-85 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| `semantics/dict.k` | 86-86 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| `semantics/dict.k` | 87-89 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is not imported here)` |
| `semantics/dict.k` | 90-90 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| `semantics/dict.k` | 91-91 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| `semantics/dict.k` | 92-94 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 // ==== dict == (order-insensitive: same size + same key->value pairs) =======` |
| `semantics/dict.k` | 95-96 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| `semantics/dict.k` | 97-97 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| `semantics/dict.k` | 98-98 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| `semantics/dict.k` | 99-100 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| `semantics/dict.k` | 101-101 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| `semantics/dict.k` | 102-102 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| `semantics/dict.k` | 103-103 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| `semantics/float.k` | 20-20 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= Float` |
| `semantics/float.k` | 21-23 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Float(F:Float) => F ... </k> // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.` |
| `semantics/float.k` | 24-24 | function-declaration | `function; total; symbol(intFloatDiv); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| `semantics/float.k` | 25-26 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| `semantics/float.k` | 27-29 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.` |
| `semantics/float.k` | 30-30 | function-declaration | `function; total; symbol(divII); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| `semantics/float.k` | 31-31 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| `semantics/float.k` | 32-36 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).` |
| `semantics/float.k` | 37-37 | function-declaration | `function; total; symbol(floatMod); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| `semantics/float.k` | 38-38 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| `semantics/float.k` | 39-42 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on // concrete floats. kprove proofs return floats structurally and do not compare them.` |
| `semantics/float.k` | 43-43 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| `semantics/float.k` | 44-49 | concrete-rule | `no-evaluators; concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade), // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise // `abs(a-b) < t` proximity test.)` |
| `semantics/float.k` | 50-50 | function-declaration | `function; total; symbol(floatLt); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| `semantics/float.k` | 51-51 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| `semantics/float.k` | 52-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| `semantics/float.k` | 54-54 | function-declaration | `function; total; symbol(absF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| `semantics/float.k` | 55-55 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule absF(F:Float) => absFloat(F) [concrete]` |
| `semantics/float.k` | 56-60 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F) // ==== math.ceil =========================================================== // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is // never bound as a value).` |
| `semantics/float.k` | 61-64 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Import(_:String) => .K ... </k> // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher // priority than the generic Attribute/method dispatch in call.k).` |
| `semantics/float.k` | 65-65 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= "#mathCeil"` |
| `semantics/float.k` | 66-66 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| `semantics/float.k` | 67-69 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> // math.floor(x) — same interception shape as math.ceil` |
| `semantics/float.k` | 70-70 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= "#mathFloor"` |
| `semantics/float.k` | 71-71 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| `semantics/float.k` | 72-72 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| `semantics/float.k` | 73-73 | function-declaration | `function; total; symbol(floorFI)` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| `semantics/float.k` | 74-74 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule floorFI(I:Int) => I [concrete]` |
| `semantics/float.k` | 75-77 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] // bare floor/ceil (bound by `from math import floor, ceil`)` |
| `semantics/float.k` | 78-78 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| `semantics/float.k` | 79-81 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) // math.pow(x, y) — a two-arg interception onto powF (ints promote)` |
| `semantics/float.k` | 82-82 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| `semantics/float.k` | 83-83 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| `semantics/float.k` | 84-84 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| `semantics/float.k` | 85-85 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| `semantics/float.k` | 86-86 | function-declaration | `function; total; symbol(toF)` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| `semantics/float.k` | 87-87 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule toF(F:Float) => F [concrete]` |
| `semantics/float.k` | 88-92 | concrete-rule | `concrete; concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule toF(I:Int) => intToF(I) [concrete] // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm). // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).` |
| `semantics/float.k` | 93-93 | function-declaration | `function; total; symbol(ceilF)` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| `semantics/float.k` | 94-94 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule ceilF(I:Int) => I [concrete]` |
| `semantics/float.k` | 95-98 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun; // proofs use symbolic elements, never a float literal.` |
| `semantics/float.k` | 99-102 | ordinary-rule | `no-evaluators` | FIXED_RULE_UNUSED_BY_TASK | `rule applyUn("-", F:Float) => 0.0 -Float F // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.` |
| `semantics/float.k` | 103-103 | function-declaration | `function; total; symbol(subF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| `semantics/float.k` | 104-104 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| `semantics/float.k` | 105-106 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| `semantics/float.k` | 107-107 | function-declaration | `function; total; symbol(divF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| `semantics/float.k` | 108-108 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| `semantics/float.k` | 109-110 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| `semantics/float.k` | 111-111 | function-declaration | `function; total; symbol(addF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| `semantics/float.k` | 112-112 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| `semantics/float.k` | 113-114 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| `semantics/float.k` | 115-115 | function-declaration | `function; total; symbol(mulF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| `semantics/float.k` | 116-116 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| `semantics/float.k` | 117-118 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| `semantics/float.k` | 119-119 | function-declaration | `function; total; symbol(powF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| `semantics/float.k` | 120-120 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| `semantics/float.k` | 121-124 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) // ---- the remaining comparisons (gtF promoted from find_zero — its summaries // case-split on the atom; >= / <= derive from the two opaque compares) ----` |
| `semantics/float.k` | 125-125 | function-declaration | `function; total; symbol(gtF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| `semantics/float.k` | 126-126 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| `semantics/float.k` | 127-127 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| `semantics/float.k` | 128-128 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| `semantics/float.k` | 129-131 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----` |
| `semantics/float.k` | 132-132 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| `semantics/float.k` | 133-133 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| `semantics/float.k` | 134-134 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| `semantics/float.k` | 135-135 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| `semantics/float.k` | 136-136 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| `semantics/float.k` | 137-137 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| `semantics/float.k` | 138-138 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| `semantics/float.k` | 139-141 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----` |
| `semantics/float.k` | 142-142 | function-declaration | `function; total; symbol(eqF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| `semantics/float.k` | 143-143 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| `semantics/float.k` | 144-144 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| `semantics/float.k` | 145-145 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| `semantics/float.k` | 146-146 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| `semantics/float.k` | 147-147 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| `semantics/float.k` | 148-148 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| `semantics/float.k` | 149-149 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| `semantics/float.k` | 150-150 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| `semantics/float.k` | 151-153 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- x == None (promoted from 137; `is` cases live in operators.k) ----` |
| `semantics/float.k` | 154-154 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| `semantics/float.k` | 155-159 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) // ---- float(str): decimal parse (promoted from 137's defined chain) ---- // digits '.' digits, optional leading '-'; concrete evaluation only (the // symbolic side stays an opaque decStrToF term a proof case-splits on).` |
| `semantics/float.k` | 160-160 | function-declaration | `function; total; symbol(decStrToF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| `semantics/float.k` | 161-161 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| `semantics/float.k` | 162-164 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| `semantics/float.k` | 165-165 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= headIS(IntSeq) [function]` |
| `semantics/float.k` | 166-166 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| `semantics/float.k` | 167-167 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k` | 168-168 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| `semantics/float.k` | 169-169 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intPartAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k` | 170-170 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| `semantics/float.k` | 171-172 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| `semantics/float.k` | 173-173 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k` | 174-174 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracPart(.IntSeq) => 0` |
| `semantics/float.k` | 175-175 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| `semantics/float.k` | 176-176 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| `semantics/float.k` | 177-177 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k` | 178-178 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| `semantics/float.k` | 179-179 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k` | 180-180 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracScale(.IntSeq) => 1` |
| `semantics/float.k` | 181-181 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| `semantics/float.k` | 182-182 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| `semantics/float.k` | 183-183 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fscAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k` | 184-184 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| `semantics/float.k` | 185-185 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| `semantics/float.k` | 186-186 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| `semantics/float.k` | 187-189 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("float", F:Float, .Vals) => F // ---- float / int division (promoted from mean_absolute_deviation) ----` |
| `semantics/float.k` | 190-190 | function-declaration | `function; total; symbol(divFloatIntV); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| `semantics/float.k` | 191-191 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| `semantics/float.k` | 192-194 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) // ---- int -> float promotion for the remaining mixed arithmetic/compares ----` |
| `semantics/float.k` | 195-195 | function-declaration | `function; total; symbol(intToF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| `semantics/float.k` | 196-196 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| `semantics/float.k` | 197-197 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| `semantics/float.k` | 198-198 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| `semantics/float.k` | 199-199 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| `semantics/float.k` | 200-200 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| `semantics/float.k` | 201-201 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| `semantics/float.k` | 202-202 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| `semantics/float.k` | 203-203 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| `semantics/float.k` | 204-204 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| `semantics/float.k` | 205-205 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| `semantics/float.k` | 206-208 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----` |
| `semantics/float.k` | 209-209 | function-declaration | `function; total; symbol(truncF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| `semantics/float.k` | 210-210 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| `semantics/float.k` | 211-212 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| `semantics/float.k` | 213-213 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| `semantics/float.k` | 214-216 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("float", F:Float, .Vals) => F // round: Python half-even (banker's); round(F, N) scales by 10^N` |
| `semantics/float.k` | 217-217 | function-declaration | `function; total; symbol(roundF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| `semantics/float.k` | 218-222 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| `semantics/float.k` | 223-223 | function-declaration | `function; total; symbol(roundFN); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| `semantics/float.k` | 224-226 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| `semantics/float.k` | 227-227 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| `semantics/float.k` | 228-229 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| `semantics/float.k` | 230-230 | function-declaration | `function; total; symbol(sqrtF); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| `semantics/float.k` | 231-231 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| `semantics/float.k` | 232-232 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= "#mathSqrt"` |
| `semantics/float.k` | 233-233 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| `semantics/float.k` | 234-234 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| `semantics/float.k` | 235-242 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive: // the isFloat guard is disjoint from the existing isInt one.` |
| `semantics/float.k` | 243-243 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| `semantics/float.k` | 244-244 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `semantics/float.k` | 245-245 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| `semantics/float.k` | 246-246 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| `semantics/float.k` | 247-249 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| `semantics/float.k` | 250-250 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| `semantics/float.k` | 251-251 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `semantics/float.k` | 252-252 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| `semantics/float.k` | 253-253 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| `semantics/float.k` | 254-260 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin). // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof // with isInt(V) in its path condition refutes this branch without sort reasoning.` |
| `semantics/float.k` | 261-261 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| `semantics/float.k` | 262-264 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| `semantics/float.k` | 265-265 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| `semantics/float.k` | 266-266 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| `semantics/float.k` | 267-269 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| `semantics/float.k` | 270-272 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| `semantics/functions.k` | 8-13 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" // ==== def / anonymous closure =============================================` |
| `semantics/functions.k` | 14-17 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| `semantics/functions.k` | 18-18 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| `semantics/functions.k` | 19-26 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> // ==== annotated def/lambda (closure cells; spec 2.3) ====================== // closureValC(params, cellvars, body, captured-cells). No frame anchor: all // enclosing-local reads are freevars (symtable-complete) and go through the // captured cells; everything else is global/builtin, so the callee frame's // parent is the module scope (0) — sound after the defining frame dies.` |
| `semantics/functions.k` | 27-30 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) // capture: resolve each freevar to the enclosing frame's cellRef, then bind // (FuncDef) or yield (Lambda) the closure value.` |
| `semantics/functions.k` | 31-32 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| `semantics/functions.k` | 33-35 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| `semantics/functions.k` | 36-41 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `semantics/functions.k` | 42-46 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| `semantics/functions.k` | 47-49 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| `semantics/functions.k` | 50-52 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| `semantics/functions.k` | 53-58 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `semantics/functions.k` | 59-62 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> // ==== bind params ========================================================` |
| `semantics/functions.k` | 63-63 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| `semantics/functions.k` | 64-67 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound to its cell at frame entry` |
| `semantics/functions.k` | 68-77 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] // ==== return / pop the frame (the returned expr evaluates by strictness) ==` |
| `semantics/functions.k` | 78-79 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| `semantics/functions.k` | 80-84 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).` |
| `semantics/functions.k` | 85-90 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| `semantics/int.k` | 7-8 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyUn("-", I:Int) => 0 -Int I` |
| `semantics/int.k` | 9-10 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b))` |
| `semantics/int.k` | 11-11 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| `semantics/int.k` | 12-12 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| `semantics/int.k` | 13-13 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| `semantics/int.k` | 14-14 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| `semantics/int.k` | 15-15 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| `semantics/int.k` | 16-16 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| `semantics/int.k` | 17-18 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| `semantics/int.k` | 19-19 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= pyMod(Int, Int) [function]` |
| `semantics/int.k` | 20-21 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| `semantics/int.k` | 22-22 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| `semantics/int.k` | 23-23 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| `semantics/int.k` | 24-24 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| `semantics/int.k` | 25-25 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| `semantics/int.k` | 26-26 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| `semantics/int.k` | 27-27 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |
| `semantics/iter.k` | 8-8 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| `semantics/list.k` | 9-9 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| `semantics/list.k` | 10-12 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> // ==== ListExpr: [...] literal -> a fresh heap object =======================` |
| `semantics/list.k` | 13-13 | syntax-declaration | `-` | USED_FIXED_RULE_REVIEWED | `syntax ApplyK ::= "toList"` |
| `semantics/list.k` | 14-14 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| `semantics/list.k` | 15-17 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> // ==== list ops: + / == / != ===============================================` |
| `semantics/list.k` | 18-18 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| `semantics/list.k` | 19-19 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| `semantics/list.k` | 20-23 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) // list + list constructs a NEW object (k-cell — it allocates; operands land here // already deref'd). priority(45) beats the generic BinOp dispatch.` |
| `semantics/list.k` | 24-26 | priority-rule | `priority(45)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| `semantics/list.k` | 27-27 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| `semantics/list.k` | 28-32 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) // ==== deep equality when elements are heap objects (list-of-lists) ======== // Python == is structural at every depth. Fires ONLY when a ref is present // (the guard decides on concrete seqs); the plain ==K path above is unchanged.` |
| `semantics/list.k` | 33-33 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| `semantics/list.k` | 34-34 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule hasRefVS(.ValSeq) => false` |
| `semantics/list.k` | 35-36 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| `semantics/list.k` | 37-38 | function-declaration | `function; function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function]` |
| `semantics/list.k` | 39-39 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| `semantics/list.k` | 40-40 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| `semantics/list.k` | 41-41 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| `semantics/list.k` | 42-44 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| `semantics/list.k` | 45-46 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| `semantics/list.k` | 47-48 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| `semantics/list.k` | 49-49 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| `semantics/list.k` | 50-52 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] // ==== mutator: xs.append(v) — an in-place heap write ======================` |
| `semantics/list.k` | 53-57 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] // ==== `x in list` — a <k>-cell fold over #iterNext ========================` |
| `semantics/list.k` | 58-58 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| `semantics/list.k` | 59-59 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| `semantics/list.k` | 60-60 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| `semantics/list.k` | 61-61 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| `semantics/list.k` | 62-62 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| `semantics/list.k` | 63-64 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| `semantics/list.k` | 65-66 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| `semantics/list.k` | 67-67 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| `semantics/methods.k` | 10-12 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= applyMethod(Val, String, Vals) [function] // ==== string predicates (Python semantics) =================================` |
| `semantics/methods.k` | 13-13 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| `semantics/methods.k` | 14-14 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| `semantics/methods.k` | 15-15 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| `semantics/methods.k` | 16-18 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) // ==== case maps ============================================================` |
| `semantics/methods.k` | 19-19 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| `semantics/methods.k` | 20-20 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| `semantics/methods.k` | 21-25 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) // ==== join / count / strip / encode ======================================== // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by // the call layer; the result str is a value)` |
| `semantics/methods.k` | 26-26 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| `semantics/methods.k` | 27-27 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| `semantics/methods.k` | 28-28 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| `semantics/methods.k` | 29-29 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| `semantics/methods.k` | 30-33 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) // S.count(sub): non-overlapping window scan (Python str.count)` |
| `semantics/methods.k` | 34-34 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| `semantics/methods.k` | 35-35 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| `semantics/methods.k` | 36-36 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| `semantics/methods.k` | 37-38 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| `semantics/methods.k` | 39-40 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| `semantics/methods.k` | 41-41 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| `semantics/methods.k` | 42-42 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| `semantics/methods.k` | 43-43 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| `semantics/methods.k` | 44-46 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 // S.strip(): trim whitespace runs from both ends` |
| `semantics/methods.k` | 47-47 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| `semantics/methods.k` | 48-48 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| `semantics/methods.k` | 49-49 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule trimWS(.IntSeq) => .IntSeq` |
| `semantics/methods.k` | 50-50 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| `semantics/methods.k` | 51-51 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| `semantics/methods.k` | 52-52 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| `semantics/methods.k` | 53-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| `semantics/methods.k` | 54-54 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| `semantics/methods.k` | 55-57 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) // S.encode('ascii'): identity on the code-sequence model (bytes == codes)` |
| `semantics/methods.k` | 58-60 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) // ==== prefix ===============================================================` |
| `semantics/methods.k` | 61-63 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========` |
| `semantics/methods.k` | 64-64 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| `semantics/methods.k` | 65-65 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| `semantics/methods.k` | 66-66 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| `semantics/methods.k` | 67-67 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| `semantics/methods.k` | 68-71 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ========== // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.` |
| `semantics/methods.k` | 72-74 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| `semantics/methods.k` | 75-75 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` |
| `semantics/methods.k` | 76-76 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| `semantics/methods.k` | 77-78 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| `semantics/methods.k` | 79-81 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty.` |
| `semantics/methods.k` | 82-82 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| `semantics/methods.k` | 83-83 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| `semantics/methods.k` | 84-84 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| `semantics/methods.k` | 85-85 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isWSC(Int) [function, total]` |
| `semantics/methods.k` | 86-88 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 // split(sep='x') keyword form delegates to the positional k-cell rule` |
| `semantics/methods.k` | 89-93 | priority-rule | `priority(39)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).` |
| `semantics/methods.k` | 94-96 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| `semantics/methods.k` | 97-97 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` |
| `semantics/methods.k` | 98-98 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| `semantics/methods.k` | 99-100 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| `semantics/methods.k` | 101-103 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| `semantics/methods.k` | 104-105 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| `semantics/methods.k` | 106-106 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| `semantics/methods.k` | 107-107 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| `semantics/methods.k` | 108-108 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| `semantics/methods.k` | 109-111 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) // ==== char helpers =========================================================` |
| `semantics/methods.k` | 112-112 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isUpperC(Int) [function, total]` |
| `semantics/methods.k` | 113-114 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| `semantics/methods.k` | 115-115 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isLowerC(Int) [function, total]` |
| `semantics/methods.k` | 116-117 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| `semantics/methods.k` | 118-118 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| `semantics/methods.k` | 119-120 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| `semantics/methods.k` | 121-121 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= isDigitC(Int) [function, total]` |
| `semantics/methods.k` | 122-123 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `semantics/methods.k` | 124-124 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| `semantics/methods.k` | 125-125 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule hasUpper(.IntSeq) => false` |
| `semantics/methods.k` | 126-127 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| `semantics/methods.k` | 128-128 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| `semantics/methods.k` | 129-129 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule hasLower(.IntSeq) => false` |
| `semantics/methods.k` | 130-131 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| `semantics/methods.k` | 132-132 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| `semantics/methods.k` | 133-133 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule allAlpha(.IntSeq) => true` |
| `semantics/methods.k` | 134-135 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| `semantics/methods.k` | 136-136 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| `semantics/methods.k` | 137-137 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule allDigit(.IntSeq) => true` |
| `semantics/methods.k` | 138-139 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| `semantics/methods.k` | 140-141 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= lowerC(Int) [function, total]` |
| `semantics/methods.k` | 142-142 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `semantics/methods.k` | 143-144 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule lowerC(C:Int) => C [owise]` |
| `semantics/methods.k` | 145-145 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= upperC(Int) [function, total]` |
| `semantics/methods.k` | 146-146 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `semantics/methods.k` | 147-148 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule upperC(C:Int) => C [owise]` |
| `semantics/methods.k` | 149-149 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= swapC(Int) [function, total]` |
| `semantics/methods.k` | 150-150 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `semantics/methods.k` | 151-151 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `semantics/methods.k` | 152-153 | ordinary-rule | `owise` | FIXED_RULE_UNUSED_BY_TASK | `rule swapC(C:Int) => C [owise]` |
| `semantics/methods.k` | 154-154 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| `semantics/methods.k` | 155-155 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapLower(.IntSeq) => .IntSeq` |
| `semantics/methods.k` | 156-157 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| `semantics/methods.k` | 158-158 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| `semantics/methods.k` | 159-159 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapUpper(.IntSeq) => .IntSeq` |
| `semantics/methods.k` | 160-161 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| `semantics/methods.k` | 162-162 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| `semantics/methods.k` | 163-163 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapSwap(.IntSeq) => .IntSeq` |
| `semantics/methods.k` | 164-165 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| `semantics/methods.k` | 166-166 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| `semantics/methods.k` | 167-167 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| `semantics/methods.k` | 168-168 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/methods.k` | 169-169 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| `semantics/operators.k` | 10-11 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| `semantics/operators.k` | 12-14 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes` |
| `semantics/operators.k` | 15-15 | context | `-` | USED_FIXED_RULE_REVIEWED | `context Compare(HOLE, _)` |
| `semantics/operators.k` | 16-16 | context | `-` | USED_FIXED_RULE_REVIEWED | `context Compare(_:Val, CmpOp(_, HOLE))` |
| `semantics/operators.k` | 17-18 | ordinary-rule | `owise` | USED_FIXED_RULE_REVIEWED | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| `semantics/operators.k` | 19-19 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| `semantics/operators.k` | 20-24 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) // ==== operand deref: heap objects combine/compare by STRUCTURE ============ // (Python: list == is structural; identity only via `is`.) priority(40) // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.` |
| `semantics/operators.k` | 25-27 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/operators.k` | 28-33 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd` |
| `semantics/operators.k` | 34-37 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| `semantics/operators.k` | 38-43 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| `semantics/operators.k` | 44-46 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/range.k` | 9-9 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| `semantics/range.k` | 10-11 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| `semantics/range.k` | 12-12 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| `semantics/range.k` | 13-14 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| `semantics/range.k` | 15-16 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| `semantics/range.k` | 17-19 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| `semantics/range.k` | 20-22 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| `semantics/range.k` | 23-24 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| `semantics/set.k` | 8-10 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= setV(IntSeq) // membership of a code in the accumulated distinct-code sequence` |
| `semantics/set.k` | 11-11 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| `semantics/set.k` | 12-12 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule codeIn(_:Int, .IntSeq) => false` |
| `semantics/set.k` | 13-15 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) // the distinct codes of CS (insert-if-absent fold, first-seen order)` |
| `semantics/set.k` | 16-17 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total]` |
| `semantics/set.k` | 18-18 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| `semantics/set.k` | 19-19 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| `semantics/set.k` | 20-21 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| `semantics/set.k` | 22-24 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| `semantics/set.k` | 25-25 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| `semantics/set.k` | 26-26 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| `semantics/set.k` | 27-30 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) // ==== set equality: two sets are equal iff mutually subsuming ============== // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).` |
| `semantics/set.k` | 31-31 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| `semantics/set.k` | 32-32 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| `semantics/set.k` | 33-34 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| `semantics/set.k` | 35-35 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| `semantics/set.k` | 36-38 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) // set == set (the only comparison sets support here)` |
| `semantics/set.k` | 39-39 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| `semantics/sort.k` | 18-18 | function-declaration | `function; total; symbol(sortVS); no-evaluators` | USED_TRUSTED_OPAQUE_SORT_PRIMITIVE | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| `semantics/sort.k` | 19-19 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| `semantics/sort.k` | 20-20 | concrete-rule | `concrete` | USED_FIXED_RULE_REVIEWED | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| `semantics/sort.k` | 21-21 | concrete-rule | `concrete` | USED_FIXED_RULE_REVIEWED | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| `semantics/sort.k` | 22-22 | concrete-rule | `concrete` | USED_FIXED_RULE_REVIEWED | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| `semantics/sort.k` | 23-23 | concrete-rule | `concrete` | USED_FIXED_RULE_REVIEWED | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| `semantics/sort.k` | 24-25 | concrete-rule | `concrete` | USED_FIXED_RULE_REVIEWED | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k)` |
| `semantics/sort.k` | 26-26 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| `semantics/sort.k` | 27-27 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| `semantics/sort.k` | 28-28 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| `semantics/sort.k` | 29-30 | concrete-rule | `concrete` | FIXED_RULE_UNUSED_BY_TASK | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| `semantics/sort.k` | 31-35 | concrete-rule | `concrete; owise` | FIXED_RULE_UNUSED_BY_TASK | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise] // applyBuiltin routing in call.k) so the result allocates.` |
| `semantics/sort.k` | 36-39 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> // mutator: xs.sort() — the in-place heap write over the same trusted sortVS` |
| `semantics/sort.k` | 40-48 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] // ==== keyed / reversed sorted() (WP2) ===================================== // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV // (a closure/builtin/type — anything callable). OPAQUE here; the concrete // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable- // inserts, at priority(40) over these.` |
| `semantics/sort.k` | 49-50 | function-declaration | `function; total; symbol(sortKeyVS); no-evaluators` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| `semantics/sort.k` | 51-52 | function-declaration | `function; total; function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| `semantics/sort.k` | 53-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| `semantics/sort.k` | 54-54 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| `semantics/sort.k` | 55-56 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| `semantics/sort.k` | 57-57 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| `semantics/sort.k` | 58-58 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule condRev(S:ValSeq, false) => S` |
| `semantics/sort.k` | 59-60 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule condRev(S:ValSeq, true) => revVS(S)` |
| `semantics/sort.k` | 61-62 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| `semantics/sort.k` | 63-64 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| `semantics/sort.k` | 65-71 | ordinary-rule | `total` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write // their postcondition directly as valSeqAt(sortVS(VS), …).` |
| `semantics/str.k` | 8-8 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| `semantics/str.k` | 9-12 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> // ==== str literal (ASCII-only) ============================================` |
| `semantics/str.k` | 13-13 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= strToCodes(String) [function]` |
| `semantics/str.k` | 14-14 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| `semantics/str.k` | 15-15 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strToCodes("") => .IntSeq` |
| `semantics/str.k` | 16-19 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 // ==== operators: + / == / != / in =========================================` |
| `semantics/str.k` | 20-20 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k` | 21-21 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| `semantics/str.k` | 22-23 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| `semantics/str.k` | 24-24 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| `semantics/str.k` | 25-25 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| `semantics/str.k` | 26-28 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) // substring membership: `P in X` iff the code-seq P occurs contiguously in X` |
| `semantics/str.k` | 29-29 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| `semantics/str.k` | 30-31 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| `semantics/str.k` | 32-32 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k` | 33-33 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| `semantics/str.k` | 34-34 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/str.k` | 35-36 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| `semantics/str.k` | 37-37 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k` | 38-38 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| `semantics/str.k` | 39-39 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| `semantics/str.k` | 40-47 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on // str </<=/>/>= comparisons.` |
| `semantics/str.k` | 48-48 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k` | 49-49 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strLt(.IntSeq, .IntSeq) => false` |
| `semantics/str.k` | 50-50 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| `semantics/str.k` | 51-51 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/str.k` | 52-52 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| `semantics/str.k` | 53-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| `semantics/str.k` | 54-55 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| `semantics/str.k` | 56-56 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `semantics/str.k` | 57-57 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| `semantics/str.k` | 58-58 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| `semantics/str.k` | 59-59 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| `semantics/subscript.k` | 11-11 | function-declaration | `function; total` | USED_TOTAL_UNDERSPECIFIED_OOB_INBOUNDS_ON_ENTRY_PATH | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| `semantics/subscript.k` | 12-12 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| `semantics/subscript.k` | 13-15 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| `semantics/subscript.k` | 16-16 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| `semantics/subscript.k` | 17-17 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| `semantics/subscript.k` | 18-20 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| `semantics/subscript.k` | 21-21 | function-declaration | `function; total` | USED_FIXED_RULE_REVIEWED | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| `semantics/subscript.k` | 22-22 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| `semantics/subscript.k` | 23-26 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0 // ==== Subscript: indexing obj[i] (list / tuple / str) ===================== // contexts (not strict attrs): the Index slot's Slice alternative must never heat` |
| `semantics/subscript.k` | 27-27 | context | `-` | USED_FIXED_RULE_REVIEWED | `context Subscript(HOLE, _)` |
| `semantics/subscript.k` | 28-30 | context | `-` | USED_FIXED_RULE_REVIEWED | `context Subscript(_:Val, HOLE:Expr) // heap-object deref (covers both the index and slice forms via the Index slot)` |
| `semantics/subscript.k` | 31-34 | priority-rule | `priority(40)` | USED_FIXED_RULE_REVIEWED | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/subscript.k` | 35-36 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| `semantics/subscript.k` | 37-37 | function-declaration | `function` | USED_FIXED_RULE_REVIEWED | `syntax Val ::= applyIndex(Val, Int) [function]` |
| `semantics/subscript.k` | 38-38 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `semantics/subscript.k` | 39-39 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `semantics/subscript.k` | 40-43 | ordinary-rule | `-` | USED_FIXED_RULE_REVIEWED | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========` |
| `semantics/subscript.k` | 44-48 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| `semantics/subscript.k` | 49-49 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax OptInt ::= "noB" \| someB(Int)` |
| `semantics/subscript.k` | 50-50 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #evalB(NoBound) => noB ... </k>` |
| `semantics/subscript.k` | 51-51 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| `semantics/subscript.k` | 52-53 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| `semantics/subscript.k` | 54-54 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| `semantics/subscript.k` | 55-55 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| `semantics/subscript.k` | 56-57 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value` |
| `semantics/subscript.k` | 58-60 | priority-rule | `priority(45)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| `semantics/subscript.k` | 61-62 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| `semantics/subscript.k` | 63-63 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| `semantics/subscript.k` | 64-65 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `semantics/subscript.k` | 66-67 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `semantics/subscript.k` | 68-71 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) // ==== slice.indices: step / start / stop / clamp ==========================` |
| `semantics/subscript.k` | 72-72 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= slStep(OptInt) [function, total]` |
| `semantics/subscript.k` | 73-73 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStep(noB) => 1` |
| `semantics/subscript.k` | 74-75 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStep(someB(S:Int)) => S` |
| `semantics/subscript.k` | 76-76 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| `semantics/subscript.k` | 77-78 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| `semantics/subscript.k` | 79-80 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` |
| `semantics/subscript.k` | 81-82 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| `semantics/subscript.k` | 83-83 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| `semantics/subscript.k` | 84-85 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` |
| `semantics/subscript.k` | 86-87 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| `semantics/subscript.k` | 88-89 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| `semantics/subscript.k` | 90-90 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| `semantics/subscript.k` | 91-92 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` |
| `semantics/subscript.k` | 93-95 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| `semantics/subscript.k` | 96-96 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| `semantics/subscript.k` | 97-98 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| `semantics/subscript.k` | 99-101 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| `semantics/subscript.k` | 102-102 | function-declaration | `function; total` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| `semantics/subscript.k` | 103-104 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` |
| `semantics/subscript.k` | 105-108 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN // ==== build the strided sub-sequence (indices in range by construction) ====` |
| `semantics/subscript.k` | 109-109 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| `semantics/subscript.k` | 110-112 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `semantics/subscript.k` | 113-115 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `semantics/subscript.k` | 116-116 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| `semantics/subscript.k` | 117-119 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `semantics/subscript.k` | 120-121 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `semantics/syntax.k` | 9-31 | syntax-declaration | `strict(2); macro; macro; strict(1); strict(1)` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda" "(" Params "," Expr ")" \| "KwArg" "(" String "," Expr ")" \| "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call" "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare" "(" Expr "," CmpOp ")"` |
| `semantics/syntax.k` | 32-32 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| `semantics/syntax.k` | 33-33 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| `semantics/syntax.k` | 34-34 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Entries ::= List{Entry, ","}` |
| `semantics/syntax.k` | 35-35 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| `semantics/syntax.k` | 36-36 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax CompFors ::= List{CompFor, ""}` |
| `semantics/syntax.k` | 37-37 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Exprs ::= List{Expr, ","}` |
| `semantics/syntax.k` | 38-38 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| `semantics/syntax.k` | 39-40 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Bound ::= Expr \| "NoBound"` |
| `semantics/syntax.k` | 41-55 | syntax-declaration | `strict(2); strict(3); strict(2); strict(1); strict; strict; strict` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [strict] \| "Expr" "(" Expr ")" [strict] \| "FuncDef" "(" String "," Params "," Stmts ")" \| "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| `semantics/syntax.k` | 56-56 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Stmts ::= List{Stmt, ""}` |
| `semantics/syntax.k` | 57-57 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Params ::= "Params" "(" ParamNames ")"` |
| `semantics/syntax.k` | 58-58 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| `semantics/syntax.k` | 59-59 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| `semantics/syntax.k` | 60-60 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ParamNames ::= List{String, ","}` |
| `semantics/syntax.k` | 61-61 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Module ::= "Module" "(" Stmts ")"` |
| `semantics/tuple.k` | 10-10 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| `semantics/tuple.k` | 11-13 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================` |
| `semantics/tuple.k` | 14-14 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax ApplyK ::= "toTuple"` |
| `semantics/tuple.k` | 15-15 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| `semantics/tuple.k` | 16-17 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| `semantics/tuple.k` | 18-19 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k)` |
| `semantics/tuple.k` | 20-20 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| `semantics/tuple.k` | 21-22 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset)` |
| `semantics/tuple.k` | 23-23 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| `semantics/tuple.k` | 24-24 | function-declaration | `function` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| `semantics/tuple.k` | 25-25 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| `semantics/tuple.k` | 26-27 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| `semantics/tuple.k` | 28-30 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) // ==== target binding: bind a Name or a TupleExpr target to a value ========` |
| `semantics/tuple.k` | 31-31 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #bindTgt(Expr, Val)` |
| `semantics/tuple.k` | 32-34 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `semantics/tuple.k` | 35-41 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `semantics/tuple.k` | 42-42 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k` | 43-43 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k` | 44-48 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // ==== unpacking: a, b = <tuple\|list> (RHS evaluated by strictness) ========` |
| `semantics/tuple.k` | 49-49 | syntax-declaration | `-` | FIXED_DECLARATION_UNUSED_BY_TASK | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| `semantics/tuple.k` | 50-50 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k` | 51-51 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k` | 52-54 | priority-rule | `priority(40)` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `semantics/tuple.k` | 55-56 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k` | 57-57 | ordinary-rule | `-` | FIXED_RULE_UNUSED_BY_TASK | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| `verification.k` | 7-7 | function-declaration | `function; total` | VALID_DEFINITIONAL_ALLINTS | `syntax Bool ::= allInts(ValSeq) [function, total]` |
| `verification.k` | 8-8 | ordinary-rule | `-` | VALID_DEFINITIONAL_ALLINTS | `rule allInts(.ValSeq) => true` |
| `verification.k` | 9-13 | ordinary-rule | `-` | VALID_DEFINITIONAL_ALLINTS | `rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R) // Append the alternating leftmost/rightmost elements from S[L..R] to A. // The three guards partition all integer bounds, and recursive calls shrink // R - L by two.` |
| `verification.k` | 14-14 | function-declaration | `function; total` | VALID_DEFINITIONAL_STRANGEACC | `syntax ValSeq ::= strangeAcc(ValSeq, ValSeq, Int, Int) [function, total]` |
| `verification.k` | 15-16 | ordinary-rule | `-` | VALID_DEFINITIONAL_STRANGEACC | `rule strangeAcc(A:ValSeq, _:ValSeq, L:Int, R:Int) => A requires L >Int R` |
| `verification.k` | 17-19 | ordinary-rule | `-` | VALID_DEFINITIONAL_STRANGEACC | `rule strangeAcc(A:ValSeq, S:ValSeq, L:Int, R:Int) => valSeqConcat(A, vCons(valSeqAt(S, L), .ValSeq)) requires L ==Int R` |
| `verification.k` | 20-30 | ordinary-rule | `-` | VALID_DEFINITIONAL_STRANGEACC | `rule strangeAcc(A:ValSeq, S:ValSeq, L:Int, R:Int) => strangeAcc( valSeqConcat( valSeqConcat(A, vCons(valSeqAt(S, L), .ValSeq)), vCons(valSeqAt(S, R), .ValSeq)), S, L +Int 1, R -Int 1) requires L <Int R // Removing a known-present integer key from a disjoint Map fragment leaves // exactly that fragment. This only canonicalizes the Map update emitted by // the fixed #pop rule.` |
| `verification.k` | 31-33 | simplification-rule | `simplification` | VALID_MAP_DELETE_SIMPLIFICATION | `rule (M:Map K:Int \|-> _V:Scope) [K <- undef] => M requires notBool K in_keys(M) [simplification]` |
| `spec.k` | 6-57 | claim | `-` | POSITIVE_LOOP_CONNECTION_CLAIM | `claim [loop-invariant]: <k> #while( Compare(Name("left"), CmpOp("<", Name("right"))), Expr( Call( Attribute(Name("result"), "append"), Subscript(Name("ordered"), Name("left")))) Expr( Call( Attribute(Name("result"), "append"), Subscript(Name("ordered"), Name("right")))) AugAssign(Name("left"), "+", Int(1)) AugAssign(Name("right"), "-", Int(1))) ~> ( If( Compare(Name("left"), CmpOp("==", Name("right"))), Expr( Call( Attribute(Name("result"), "append"), Subscript(Name("ordered"), Name("left")))), .Stmts) Return(Name("result")) .Stmts ) ~> #endcall => ref(HR) </k> <env> 1 => 0 </env> <scopes> (SC:Map 1 \|-> scope( "lst" \|-> list(VS) "ordered" \|-> ref(HO) "result" \|-> ref(HR) "left" \|-> L "right" \|-> R, parent(0))) => SC </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> HO \|-> list(S) HR \|-> (list(A) => list(strangeAcc(A, S, L, R))) </heap> <heapLoc> HL </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires L >=Int 0` |
| `spec.k` | 58-113 | claim | `-` | POSITIVE_ENTRY_CLAIM | `claim [entry-point]: <k> Call(Name("strange_sort_list"), list(VS)) => ref(1) </k> <env> 0 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope( "strange_sort_list" \|-> closureVal( "lst", Assign(Name("ordered"), Call(Name("sorted"), Name("lst"))) Assign(Name("result"), ListExpr(.Exprs)) Assign(Name("left"), Int(0)) Assign( Name("right"), BinOp("-", Call(Name("len"), Name("ordered")), Int(1))) While( Compare(Name("left"), CmpOp("<", Name("right"))), Expr( Call( Attribute(Name("result"), "append"), Subscript(Name("ordered"), Name("left")))) Expr( Call( Attribute(Name("result"), "append"), Subscript(Name("ordered"), Name("right")))) AugAssign(Name("left"), "+", Int(1)) AugAssign(Name("right"), "-", Int(1))) If( Compare(Name("left"), CmpOp("==", Name("right"))), Expr( Call( Attribute(Name("result"), "append"), Subscript(Name("ordered"), Name("left")))), .Stmts) Return(Name("result")), 0), parent(-1)) </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map => 0 \|-> list(sortVS(VS)) 1 \|-> list( strangeAcc( .ValSeq, sortVS(VS), 0, vsLen(sortVS(VS)) -Int 1)) </heap> <heapLoc> 0 => 2 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(VS)` |

## Counts

- claim: 2
- concrete-rule: 36
- configuration: 1
- context: 5
- function-declaration: 147
- ordinary-rule: 619
- priority-rule: 45
- simplification-rule: 1
- syntax-declaration: 82
- total: 938

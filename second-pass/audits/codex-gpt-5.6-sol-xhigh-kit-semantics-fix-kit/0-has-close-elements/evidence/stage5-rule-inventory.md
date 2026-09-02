# Exhaustive K source inventory

Files: 26; inventoried items: 957

Kinds: {'claim': 3, 'configuration': 1, 'context': 5, 'rule': 713, 'syntax': 235}

Attributes: {'concrete': 35, 'function': 152, 'macro': 5, 'opaque/no-evaluators': 22, 'owise': 26, 'priority': 45, 'strict': 2, 'symbol': 25, 'total': 114}

No item is omitted: entries begin at every top-level `configuration`, `syntax`, `rule`, `context`, `claim`, or `alias` source line.

## `reference-semantics/semantics/assert.k`

- L6 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)`

- L8 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)`

- L13 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/bool.k`

- L8 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyUn("not", V:Val) => notBool truthy(V)`

- L10 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`

- L11 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`

- L16 — context; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `context BoolOp(_, (HOLE:Expr, _:Exprs))`

- L17 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`

- L18 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)`

- L22 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)`

- L24 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)`

- L29 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`

- L31 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`

- L35 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`

- L39 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`

- L43 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`

## `reference-semantics/semantics/builtins.k`

- L17 — syntax; attributes: function; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Val ::= applyBuiltin(String, Vals) [function]`

- L20 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= seqLen(Val) [function]`

- L21 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`

- L22 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule seqLen(list(VS:ValSeq)) => vsLen(VS)`

- L23 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)`

- L24 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule seqLen(str(IS:IntSeq)) => isLen(IS)`

- L25 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule seqLen(setV(DS:IntSeq)) => isLen(DS)`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`

- L32 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`

- L33 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`

- L34 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>`

- L35 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>`

- L36 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= charsOf(IntSeq) [function, total]`

- L37 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule charsOf(.IntSeq) => .ValSeq`

- L38 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`

- L41 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`

- L44 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`

- L47 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`

- L48 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`

- L49 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`

- L50 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)`

- L54 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= intOf(Val) [function]`

- L55 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intOf(I:Int) => I`

- L56 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`

- L59 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #allAcc(Iterable) | "#allCont"`

- L60 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`

- L61 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #allCont => true ... </k>`

- L62 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)`

- L64 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)`

- L67 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`

- L68 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`

- L69 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #anyCont => false ... </k>`

- L70 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)`

- L72 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)`

- L76 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`

- L77 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`

- L78 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)`

- L80 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`

- L81 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`

- L82 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)`

- L86 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`

- L87 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`

- L88 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)`

- L90 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`

- L91 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`

- L92 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)`

- L97 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= maxVals(Int, Vals) [function]`

- L98 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`

- L99 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule maxVals(M:Int, .Vals) => M`

- L100 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`

- L102 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= minVals(Int, Vals) [function]`

- L103 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`

- L104 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule minVals(M:Int, .Vals) => M`

- L105 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`

- L108 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0`

- L111 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0`

- L114 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= binCodes(Int) [function, total]`

- L115 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule binCodes(0) => iCons(48, .IntSeq)`

- L116 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`

- L117 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`

- L118 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule binAcc(0, ACC:IntSeq) => ACC`

- L119 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0`

- L124 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`

- L126 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`

- L127 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule enumVS(.ValSeq, _:Int) => .ValSeq`

- L128 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`

- L132 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`

- L134 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`

- L135 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapStrVS(.ValSeq) => .ValSeq`

- L136 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`

- L137 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`

- L140 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("int", I:Int, .Vals) => I`

- L143 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`

- L144 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128`

- L148 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))`

- L149 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`

- L152 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57`

- L156 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2`

- L158 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`

- L159 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intDigAcc(.IntSeq, ACC:Int) => ACC`

- L160 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`

- L163 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`

- L164 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)`

- L167 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`

- L169 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>`

- L170 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`

- L171 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`

- L173 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>`

- L174 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`

- L177 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)`

- L178 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)`

- L179 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0`

- L187 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`

- L188 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= evalArith(IntSeq) [function]`

- L189 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`

- L192 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`

- L194 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= evDigit(Int) [function, total]`

- L195 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`

- L196 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= evHead42(IntSeq) [function, total]`

- L197 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule evHead42(iCons(42, _:IntSeq)) => true`

- L198 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule evHead42(_:IntSeq) => false [owise]`

- L199 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= evHead47(IntSeq) [function, total]`

- L200 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule evHead47(iCons(47, _:IntSeq)) => true`

- L201 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule evHead47(_:IntSeq) => false [owise]`

- L203 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax OpSeq ::= tokOps(IntSeq) [function, total]`

- L204 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(.IntSeq) => .OpSeq`

- L205 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)`

- L206 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)`

- L207 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`

- L208 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)`

- L209 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("`

- L210 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)`

- L211 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))`

- L212 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))`

- L214 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`

- L216 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokNds(.IntSeq) => .IntSeq`

- L217 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)`

- L218 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`

- L219 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32`

- L221 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)`

- L223 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`

- L225 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax EvPair ::= evp(OpSeq, IntSeq)`

- L226 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= firstNdE(EvPair) [function, total]`

- L227 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`

- L228 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule firstNdE(_:EvPair) => 0 [owise]`

- L230 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= applyOpE(String, Int, Int) [function, total]`

- L231 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyOpE("+", A:Int, B:Int) => A +Int B`

- L232 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyOpE("-", A:Int, B:Int) => A -Int B`

- L233 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyOpE("*", A:Int, B:Int) => A *Int B`

- L234 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyOpE("`

- L235 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyOpE("**", A:Int, B:Int) => A ^Int B`

- L236 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`

- L238 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`

- L239 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`

- L240 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`

- L241 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"`

- L243 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`

- L244 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`

- L245 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`

- L246 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`

- L247 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`

- L248 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`

- L250 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`

- L251 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`

- L252 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`

- L253 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`

- L254 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`

- L255 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`

- L256 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`

- L257 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)`

- L260 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)`

- L263 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`

- L265 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= inLevelE(String, String) [function, total]`

- L266 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "`

- L267 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`

- L268 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule inLevelE(_:String, _:String) => false [owise]`

- L269 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`

- L270 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`

- L271 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`

- L272 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`

- L273 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`

- L274 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`

- L279 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= "#md5"`

- L280 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`

- L282 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`

- L283 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= md5Obj(IntSeq)`

- L284 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`

- L285 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`

- L291 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`

- L292 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`

- L293 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`

- L294 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isIntV(_:Int) => true`

- L295 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isIntV(_:Val) => false [owise]`

- L296 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isStrV(str(_:IntSeq)) => true`

- L297 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isStrV(_:Val) => false [owise]`

## `reference-semantics/semantics/call.k`

- L16 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`

- L19 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #callee(Exprs)`

- L20 — rule; attributes: owise; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`

- L21 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`

- L24 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`

- L27 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>`

- L28 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>`

- L29 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>`

- L30 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>`

- L31 — rule; attributes: owise; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`

- L32 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>`

- L38 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L42 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]`

- L47 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L52 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isMutMethod(String) [function, total]`

- L53 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`

- L56 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]`

- L63 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]`

- L69 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`

- L80 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`

- L87 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #allocCells(ParamNames)`

- L88 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #allocCells(.ParamNames) => .K ... </k>`

- L89 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`

## `reference-semantics/semantics/comprehension.k`

- L11 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`

- L12 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`

- L14 — syntax; attributes: macro; assessment: SUPPLIED-UNREACHED declaration

  `syntax Stmts ::= compBody(CompFors, Expr) [macro]`

- L15 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`

- L18 — syntax; attributes: macro; assessment: SUPPLIED-UNREACHED declaration

  `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`

- L19 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`

- L21 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`

- L24 — syntax; attributes: macro; assessment: SUPPLIED-UNREACHED declaration

  `syntax Expr ::= compGuard(Exprs) [macro]`

- L25 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule compGuard(.Exprs) => Bool(true)`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`

## `reference-semantics/semantics/concrete.k`

- L13 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`

- L16 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`

- L25 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= kvP(Val, Val)`

- L26 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`

- L28 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`

- L31 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`

- L34 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`

- L36 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`

- L38 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)`

- L42 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`

- L43 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`

- L44 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)`

- L47 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)`

- L51 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= kLt(Val, Val) [function]`

- L52 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule kLt(I1:Int, I2:Int) => I1 <Int I2`

- L53 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule kLt(F1:Float, F2:Float) => F1 <Float F2`

- L54 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`

- L56 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`

- L57 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule unpairVS(.ValSeq) => .ValSeq`

- L58 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`

- L59 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`

## `reference-semantics/semantics/controls.k`

- L9 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`

- L12 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`

- L20 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)`

- L27 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]`

- L35 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`

- L36 — rule; attributes: owise; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`

- L37 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #bindImports(ParamNames)`

- L38 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #bindImports(.ParamNames) => .K ... </k>`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"`

- L43 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")`

- L48 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Expr(_:Val) => .K ... </k>`

- L51 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax KItem ::= #branch(Bool, Stmts, Stmts)`

- L52 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`

- L53 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>`

- L54 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`

- L57 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)`

- L59 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)`

- L65 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`

- L69 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`

- L71 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`

- L72 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`

- L73 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`

- L77 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`

- L78 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`

- L79 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)`

- L81 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)`

- L85 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`

- L86 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Continue => #cont ... </k>`

- L87 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Break => #brk ... </k>`

- L88 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`

- L89 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`

- L90 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`

- L91 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`

- L95 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L98 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L101 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L106 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/core.k`

- L13 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`

- L14 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`

- L15 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Str ::= str(IntSeq)`

- L18 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`

- L25 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Val ::= Int | Bool | "noneV" | Iterable | ref(Int) | cellRef(Int) | closureVal(ParamNames, Stmts, Int) | typeV(String) | builtinV(String) | boundMethodV(Val, String)`

- L36 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Parent ::= "root" | parent(Int)`

- L37 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Scope ::= scope(Map, Parent)`

- L38 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax KResult ::= Val`

- L39 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Expr ::= Val`

- L40 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Vals ::= List{Val, ","}`

- L41 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Exc ::= "NoExc" | "AssertionError"`

- L42 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax RetState ::= "noRet" | retV(Val)`

- L49 — configuration; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code>`

- L68 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isRefV(Val) [function, total]`

- L69 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isRefV(ref(_:Int)) => true`

- L70 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isRefV(_:Val) => false [owise]`

- L75 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax HeapVal ::= cellV(Val)`

- L76 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isCellRef(Val) [function, total]`

- L77 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isCellRef(cellRef(_:Int)) => true`

- L78 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isCellRef(_:Val) => false [owise]`

- L85 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]`

- L95 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Val ::= kwV(String, Val)`

- L96 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #kwTag(String)`

- L97 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`

- L98 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)`

- L100 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isKwV(Val) [function, total]`

- L101 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isKwV(kwV(_:String, _:Val)) => true`

- L102 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isKwV(_:Val) => false [owise]`

- L106 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Val ::= cellsMark(ParamNames)`

- L107 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ParamNames ::= cellsOf(Val) [function]`

- L108 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`

- L109 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= pnMember(String, ParamNames) [function, total]`

- L110 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule pnMember(_:String, .ParamNames) => false`

- L111 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`

- L113 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #cellW(Val, Val)`

- L114 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`

- L117 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #alloc(Val)`

- L118 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`

- L124 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax KItem ::= #loadAll(Module)`

- L125 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`

- L126 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`

- L127 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> .Stmts => .K ... </k>`

- L130 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #look(String, Int)`

- L131 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`

- L132 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)`

- L145 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]`

- L152 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))`

- L157 — syntax; attributes: function, total; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Scope ::= "builtinsScope" [function, total]`

- L158 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root)`

- L185 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax ApplyK ::= toCall(Val)`

- L186 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`

- L189 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`

- L190 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`

- L191 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`

- L194 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Int(I:Int) => I ... </k>`

- L195 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Bool(B:Bool) => B ... </k>`

- L196 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> NoneVal => noneV ... </k>`

- L199 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= truthy(Val) [function]`

- L200 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule truthy(B:Bool) => B`

- L201 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule truthy(noneV) => false`

- L202 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule truthy(I:Int) => I =/=Int 0`

- L203 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)`

- L204 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)`

- L205 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`

- L208 — syntax; attributes: function; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Val ::= applyUn(String, Val) [function]`

- L209 — syntax; attributes: function; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Val ::= applyBin(String, Val, Val) [function]`

- L210 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= applyCmp(String, Val, Val) [function]`

- L213 — syntax; attributes: function, total; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Vals ::= appendVal(Vals, Val) [function, total]`

- L214 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule appendVal(.Vals, V:Val) => V , .Vals`

- L215 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)`

- L217 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`

- L218 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule vals2valSeq(.Vals) => .ValSeq`

- L219 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`

- L223 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= vsLen(ValSeq) [function, total]`

- L224 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule vsLen(.ValSeq) => 0`

- L225 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`

- L227 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= isLen(IntSeq) [function, total]`

- L228 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isLen(.IntSeq) => 0`

- L229 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`

- L233 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`

- L234 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq`

- L235 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)`

- L236 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0`

- L238 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0`

## `reference-semantics/semantics/dict.k`

- L20 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= dictV(ValSeq, ValSeq)`

- L23 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`

- L27 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`

- L28 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`

- L30 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`

- L32 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`

- L37 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`

- L38 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dHasKey(.ValSeq, _:Val) => false`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K`

- L40 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`

- L43 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`

- L44 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)`

- L45 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`

- L49 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`

- L50 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K`

- L52 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)`

- L54 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`

- L58 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`

- L63 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`

- L64 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= applyIndexD(Val, Val) [function]`

- L65 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`

- L70 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= dictSet(Val, Val, Val) [function]`

- L71 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`

- L76 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #dsetK(String, Val)`

- L77 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`

- L78 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`

- L82 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)`

- L86 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #dsetV(Val, Val, Val)`

- L87 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`

- L90 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= normIdxD(Int, Int) [function, total]`

- L91 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`

- L92 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0`

- L95 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`

- L97 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`

- L98 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`

- L99 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`

- L101 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`

- L102 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K`

- L103 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`

## `reference-semantics/semantics/float.k`

- L20 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= Float`

- L21 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Float(F:Float) => F ... </k>`

- L24 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`

- L25 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`

- L27 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`

- L30 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`

- L31 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`

- L32 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`

- L37 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`

- L38 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`

- L43 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`

- L44 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`

- L50 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`

- L51 — rule; attributes: concrete; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`

- L52 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`

- L54 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`

- L55 — rule; attributes: concrete; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule absF(F:Float) => absFloat(F) [concrete]`

- L56 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`

- L61 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Import(_:String) => .K ... </k>`

- L65 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= "#mathCeil"`

- L66 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`

- L67 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`

- L70 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= "#mathFloor"`

- L71 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`

- L72 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`

- L73 — syntax; attributes: function, total, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`

- L74 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule floorFI(I:Int) => I [concrete]`

- L75 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`

- L78 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`

- L79 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)`

- L82 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`

- L83 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`

- L84 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`

- L85 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`

- L86 — syntax; attributes: function, total, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= toF(Val) [function, total, symbol(toF)]`

- L87 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule toF(F:Float) => F [concrete]`

- L88 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule toF(I:Int) => intToF(I) [concrete]`

- L93 — syntax; attributes: function, total, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`

- L94 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule ceilF(I:Int) => I [concrete]`

- L95 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`

- L99 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyUn("-", F:Float) => 0.0 -Float F`

- L103 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`

- L104 — rule; attributes: concrete; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`

- L105 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`

- L107 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`

- L108 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`

- L109 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`

- L111 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`

- L112 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`

- L113 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`

- L115 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`

- L116 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`

- L117 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`

- L119 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`

- L120 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`

- L121 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`

- L125 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`

- L126 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`

- L127 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)`

- L128 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`

- L129 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`

- L132 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`

- L133 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`

- L134 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`

- L135 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`

- L136 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`

- L137 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`

- L138 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`

- L139 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`

- L142 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`

- L143 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`

- L144 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`

- L145 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`

- L146 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`

- L147 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`

- L148 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`

- L149 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`

- L150 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`

- L151 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`

- L154 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", V:Val, noneV) => V ==K noneV`

- L155 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`

- L160 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`

- L161 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`

- L162 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`

- L165 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= headIS(IntSeq) [function]`

- L166 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule headIS(iCons(C:Int, _:IntSeq)) => C`

- L167 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`

- L168 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`

- L169 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intPartAcc(.IntSeq, A:Int) => A`

- L170 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`

- L171 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46`

- L173 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`

- L174 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracPart(.IntSeq) => 0`

- L175 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`

- L176 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`

- L177 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracAcc(.IntSeq, A:Int) => A`

- L178 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`

- L179 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`

- L180 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracScale(.IntSeq) => 1`

- L181 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`

- L182 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`

- L183 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fscAcc(.IntSeq, A:Int) => A`

- L184 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`

- L185 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`

- L186 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`

- L187 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("float", F:Float, .Vals) => F`

- L190 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`

- L191 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`

- L192 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`

- L195 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`

- L196 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`

- L197 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`

- L198 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`

- L199 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`

- L200 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`

- L201 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`

- L202 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`

- L203 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`

- L204 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`

- L205 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`

- L206 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`

- L209 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`

- L210 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`

- L211 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`

- L213 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`

- L214 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("float", F:Float, .Vals) => F`

- L217 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`

- L218 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`

- L223 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`

- L224 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`

- L227 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)`

- L228 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`

- L230 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`

- L231 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`

- L232 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= "#mathSqrt"`

- L233 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`

- L234 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`

- L235 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`

- L243 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`

- L244 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`

- L245 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`

- L246 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`

- L247 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`

- L250 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`

- L251 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`

- L252 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`

- L253 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`

- L254 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`

- L261 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`

- L262 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`

- L265 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`

- L266 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`

- L267 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)`

- L270 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)`

## `reference-semantics/semantics/functions.k`

- L8 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`

- L14 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`

- L18 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Expr ::= closureExpr(ParamNames, Stmts)`

- L19 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`

- L27 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`

- L31 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`

- L33 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`

- L36 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`

- L42 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`

- L47 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`

- L50 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`

- L53 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`

- L59 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`

- L63 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`

- L64 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`

- L68 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]`

- L78 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`

- L80 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`

- L85 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`

## `reference-semantics/semantics/int.k`

- L7 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyUn("-", I:Int) => 0 -Int I`

- L9 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2`

- L11 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`

- L12 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`

- L13 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2`

- L14 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2`

- L15 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)`

- L16 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("`

- L17 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`

- L19 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= pyMod(Int, Int) [function]`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`

- L22 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2`

- L23 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2`

- L24 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2`

- L25 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2`

- L27 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2`

## `reference-semantics/semantics/iter.k`

- L8 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`

## `reference-semantics/semantics/list.k`

- L9 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>`

- L10 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`

- L13 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax ApplyK ::= "toList"`

- L14 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`

- L15 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`

- L18 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`

- L19 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule valSeqConcat(.ValSeq, T:ValSeq) => T`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`

- L24 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`

- L27 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`

- L28 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`

- L33 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= hasRefVS(ValSeq) [function, total]`

- L34 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule hasRefVS(.ValSeq) => false`

- L35 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`

- L37 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map) [function]`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true`

- L40 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false`

- L41 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false`

- L42 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`

- L45 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)`

- L47 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)`

- L49 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`

- L50 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`

- L53 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`

- L58 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`

- L59 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`

- L60 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`

- L61 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`

- L62 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`

- L63 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V`

- L65 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)`

- L67 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> B:Bool ~> #notB => notBool B ... </k>`

## `reference-semantics/semantics/methods.k`

- L10 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= applyMethod(Val, String, Vals) [function]`

- L13 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`

- L14 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`

- L15 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`

- L16 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`

- L19 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))`

- L21 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`

- L27 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`

- L28 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`

- L29 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`

- L30 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`

- L34 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`

- L35 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`

- L36 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule cntSub(.IntSeq, _:IntSeq) => 0`

- L37 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`

- L41 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`

- L42 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`

- L43 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`

- L44 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`

- L47 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`

- L48 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= trimWS(IntSeq) [function, total]`

- L49 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule trimWS(.IntSeq) => .IntSeq`

- L50 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`

- L51 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`

- L52 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`

- L53 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`

- L54 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule revISAcc(.IntSeq, A:IntSeq) => A`

- L55 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`

- L58 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`

- L61 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`

- L64 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`

- L65 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`

- L66 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule cntOccVS(.ValSeq, _:Val) => 0`

- L67 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`

- L68 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)`

- L72 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`

- L75 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]`

- L76 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`

- L77 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)`

- L79 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)`

- L82 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`

- L83 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule flushTok(ACC:ValSeq, .IntSeq) => ACC`

- L84 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`

- L85 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isWSC(Int) [function, total]`

- L86 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`

- L89 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`

- L94 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`

- L97 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]`

- L98 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)`

- L99 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP`

- L101 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)`

- L104 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`

- L106 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`

- L107 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq`

- L108 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`

- L109 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`

- L112 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isUpperC(Int) [function, total]`

- L113 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`

- L115 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isLowerC(Int) [function, total]`

- L116 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`

- L118 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isAlphaC(Int) [function, total]`

- L119 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`

- L121 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= isDigitC(Int) [function, total]`

- L122 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`

- L124 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= hasUpper(IntSeq) [function, total]`

- L125 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule hasUpper(.IntSeq) => false`

- L126 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`

- L128 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= hasLower(IntSeq) [function, total]`

- L129 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule hasLower(.IntSeq) => false`

- L130 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`

- L132 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= allAlpha(IntSeq) [function, total]`

- L133 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule allAlpha(.IntSeq) => true`

- L134 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`

- L136 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= allDigit(IntSeq) [function, total]`

- L137 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule allDigit(.IntSeq) => true`

- L138 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`

- L140 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= lowerC(Int) [function, total]`

- L142 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`

- L143 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule lowerC(C:Int) => C [owise]`

- L145 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= upperC(Int) [function, total]`

- L146 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`

- L147 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule upperC(C:Int) => C [owise]`

- L149 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= swapC(Int) [function, total]`

- L150 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`

- L151 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`

- L152 — rule; attributes: owise; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule swapC(C:Int) => C [owise]`

- L154 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= mapLower(IntSeq) [function, total]`

- L155 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapLower(.IntSeq) => .IntSeq`

- L156 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`

- L158 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`

- L159 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapUpper(.IntSeq) => .IntSeq`

- L160 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`

- L162 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`

- L163 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapSwap(.IntSeq) => .IntSeq`

- L164 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`

- L166 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`

- L167 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule startsWith(.IntSeq, _:IntSeq) => true`

- L168 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`

- L169 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`

## `reference-semantics/semantics/operators.k`

- L10 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`

- L12 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`

- L15 — context; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `context Compare(HOLE, _)`

- L16 — context; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `context Compare(_:Val, CmpOp(_, HOLE))`

- L17 — rule; attributes: owise; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`

- L19 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("is", V:Val, noneV) => V ==K noneV`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`

- L25 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L28 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]`

- L34 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]`

- L38 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]`

- L44 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/range.k`

- L9 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= inRange(Int, Int, Int) [function, total]`

- L10 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`

- L12 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= rangeLen(Int, Int, Int) [function]`

- L13 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO`

- L15 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO`

- L17 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)`

- L23 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)`

## `reference-semantics/semantics/set.k`

- L8 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= setV(IntSeq)`

- L11 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`

- L12 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule codeIn(_:Int, .IntSeq) => false`

- L13 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`

- L16 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] | dedupFrom(IntSeq, IntSeq) [function, total]`

- L18 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`

- L19 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)`

- L22 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)`

- L25 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)`

- L27 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`

- L31 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`

- L32 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule subsetCodes(.IntSeq, _:IntSeq) => true`

- L33 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`

- L35 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`

- L36 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`

## `reference-semantics/semantics/sort.k`

- L18 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`

- L19 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= insVS(Int, ValSeq) [function]`

- L20 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule sortVS(.ValSeq) => .ValSeq [concrete]`

- L21 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`

- L22 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]`

- L23 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`

- L24 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]`

- L26 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`

- L27 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`

- L28 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`

- L29 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]`

- L31 — rule; attributes: concrete; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]`

- L36 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`

- L40 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`

- L49 — syntax; attributes: function, total, opaque/no-evaluators, symbol; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`

- L51 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`

- L53 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`

- L54 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule revVSAcc(.ValSeq, A:ValSeq) => A`

- L55 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`

- L57 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`

- L58 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule condRev(S:ValSeq, false) => S`

- L59 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule condRev(S:ValSeq, true) => revVS(S)`

- L61 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`

- L63 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`

- L65 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`

## `reference-semantics/semantics/str.k`

- L8 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>`

- L9 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`

- L13 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= strToCodes(String) [function]`

- L14 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`

- L15 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strToCodes("") => .IntSeq`

- L16 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128`

- L20 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`

- L21 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule seqConcat(.IntSeq, T:IntSeq) => T`

- L22 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`

- L24 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`

- L25 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`

- L29 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`

- L30 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`

- L32 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`

- L33 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strPrefix(.IntSeq, _:IntSeq) => true`

- L34 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`

- L35 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`

- L37 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`

- L38 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)`

- L40 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))`

- L48 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`

- L49 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strLt(.IntSeq, .IntSeq) => false`

- L50 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`

- L51 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`

- L52 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B`

- L53 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B`

- L54 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`

- L56 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`

- L57 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`

- L58 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`

- L59 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`

## `reference-semantics/semantics/subscript.k`

- L11 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`

- L12 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V`

- L13 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0`

- L16 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= intSeqAt(IntSeq, Int) [function]`

- L17 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C`

- L18 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0`

- L21 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= normIdx(Int, Int) [function, total]`

- L22 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`

- L23 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule normIdx(I:Int, _:Int) => I requires I >=Int 0`

- L27 — context; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `context Subscript(HOLE, _)`

- L28 — context; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `context Subscript(_:Val, HOLE:Expr)`

- L31 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L35 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`

- L37 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= applyIndex(Val, Int) [function]`

- L38 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`

- L39 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`

- L40 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`

- L44 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`

- L49 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax OptInt ::= "noB" | someB(Int)`

- L50 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #evalB(NoBound) => noB ... </k>`

- L51 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>`

- L52 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> I:Int ~> #toSome => someB(I) ... </k>`

- L54 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`

- L55 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`

- L56 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`

- L58 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`

- L61 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`

- L63 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`

- L64 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`

- L66 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`

- L68 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`

- L72 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= slStep(OptInt) [function, total]`

- L73 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStep(noB) => 1`

- L74 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStep(someB(S:Int)) => S`

- L76 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`

- L77 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0`

- L79 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0`

- L81 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`

- L83 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`

- L84 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0`

- L86 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0`

- L88 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`

- L90 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`

- L91 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0`

- L93 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0`

- L96 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= clampLo(Int, Int) [function, total]`

- L97 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0`

- L99 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0`

- L102 — syntax; attributes: function, total; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= clampHi(Int, Int, Int) [function, total]`

- L103 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN`

- L105 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN`

- L109 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`

- L110 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`

- L113 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`

- L116 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`

- L117 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`

- L120 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`

## `reference-semantics/semantics/syntax.k`

- L9 — syntax; attributes: macro, strict; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Expr ::= "Int" "(" Int ")" | "Float" "(" Float ")" | "Bool" "(" Bool ")" | "Name" "(" String ")" | "Str" "(" String ")" | "UnaryOp" "(" String "," Expr ")" [strict(2)] | "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp" "(" String "," Exprs ")" | "ListExpr" "(" Exprs ")" | "DictExpr" "(" Entries ")" | "ListComp" "(" Expr "," CompFors ")" [macro] | "GenExp" "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda" "(" Params "," Expr ")" | "KwArg" "(" String "," Expr ")" | "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call" "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare" "(" Expr "," CmpOp ")"`

- L32 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"`

- L33 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Entry ::= "Entry" "(" Expr "," Expr ")"`

- L34 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Entries ::= List{Entry, ","}`

- L35 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`

- L36 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax CompFors ::= List{CompFor, ""}`

- L37 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Exprs ::= List{Expr, ","}`

- L38 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Index ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`

- L39 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax Bound ::= Expr | "NoBound"`

- L41 — syntax; attributes: strict; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] | "Import" "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While" "(" Expr "," Stmts ")" | "Break" | "Continue" | "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return" "(" Expr ")" [strict] | "Assert" "(" Expr ")" [strict] | "Expr" "(" Expr ")" [strict] | "FuncDef" "(" String "," Params "," Stmts ")" | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`

- L56 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Stmts ::= List{Stmt, ""}`

- L57 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Params ::= "Params" "(" ParamNames ")"`

- L58 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax CellVars ::= "CellVars" "(" ParamNames ")"`

- L59 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"`

- L60 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax ParamNames ::= List{String, ","}`

- L61 — syntax; attributes: none; assessment: SUPPLIED-REACHED declaration/evaluation-order mechanism

  `syntax Module ::= "Module" "(" Stmts ")"`

## `reference-semantics/semantics/tuple.k`

- L10 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>`

- L11 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`

- L14 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax ApplyK ::= "toTuple"`

- L15 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`

- L16 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`

- L18 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`

- L20 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`

- L21 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`

- L23 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`

- L24 — syntax; attributes: function; assessment: SUPPLIED-UNREACHED declaration

  `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`

- L25 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`

- L26 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)`

- L28 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`

- L31 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #bindTgt(Expr, Val)`

- L32 — rule; attributes: none; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`

- L35 — rule; attributes: priority; assessment: SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)

  `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`

- L42 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

- L43 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

- L44 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L49 — syntax; attributes: none; assessment: SUPPLIED-UNREACHED declaration

  `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`

- L50 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

- L51 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

- L52 — rule; attributes: priority; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

- L55 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`

- L57 — rule; attributes: none; assessment: SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)

  `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`

## `reference-semantics/semantics.k`

No local configuration/syntax/rule/context/claim/alias declarations.

## `verification.k`

- L11 — syntax; attributes: macro; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Stmts ::= "HC-INNER-BODY" [macro] | "HC-OUTER-BODY" [macro] | "HC-FUNCTION-BODY" [macro]`

- L15 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule HC-INNER-BODY => If(Compare(Name("i"), CmpOp("!=", Name("j"))), If(Compare(Call(Name("abs"), BinOp("-", Name("x"), Name("y"))), CmpOp("<", Name("threshold"))), Assign(Name("result"), Bool(true)), .Stmts), .Stmts) AugAssign(Name("j"), "+", Int(1))`

- L24 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule HC-OUTER-BODY => Assign(Name("j"), Int(0)) For(Name("y"), Name("numbers"), HC-INNER-BODY) AugAssign(Name("i"), "+", Int(1))`

- L29 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule HC-FUNCTION-BODY => Assign(Name("result"), Bool(false)) Assign(Name("i"), Int(0)) Assign(Name("j"), Int(0)) Assign(Name("x"), Float(0.0)) Assign(Name("y"), Float(0.0)) For(Name("x"), Name("numbers"), HC-OUTER-BODY) Return(Name("result"))`

- L39 — syntax; attributes: function, total; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Bool ::= allFloatVS(ValSeq) [function, total]`

- L40 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule allFloatVS(.ValSeq) => true`

- L41 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule allFloatVS(vCons(V:Val, VS:ValSeq)) => isFloat(V) andBool allFloatVS(VS)`

- L45 — syntax; attributes: function, total; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Int ::= advanceIndex(Int, ValSeq) [function, total]`

- L46 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule advanceIndex(I:Int, .ValSeq) => I`

- L47 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule advanceIndex(I:Int, vCons(_:Val, VS:ValSeq)) => advanceIndex(I +Int 1, VS)`

- L55 — syntax; attributes: function, total; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Float ::= asFloat(Val) [function, total]`

- L56 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule asFloat(F:Float) => F`

- L57 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule asFloat(V:Val) => 0.0 requires notBool isFloat(V)`

- L62 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule applyBin("-", X:Val, Y:Val) => subF(asFloat(X), asFloat(Y)) requires isFloat(X) andBool isFloat(Y)`

- L65 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule applyBuiltin("abs", X:Val, .Vals) => absF(asFloat(X)) requires isFloat(X)`

- L68 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule applyCmp("<", X:Val, Y:Val) => floatLt(asFloat(X), asFloat(Y)) requires isFloat(X) andBool isFloat(Y)`

- L72 — syntax; attributes: function, total; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Bool ::= closeV(Val, Val, Val) [function, total]`

- L73 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule closeV(X:Val, Y:Val, T:Val) => floatLt(absF(subF(asFloat(X), asFloat(Y))), asFloat(T))`

- L78 — syntax; attributes: function, total; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Bool ::= closeInner(Val, Val, Int, Int, ValSeq) [function, total]`

- L79 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule closeInner(_:Val, _:Val, _:Int, _:Int, .ValSeq) => false`

- L80 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule closeInner(X:Val, T:Val, I:Int, J:Int, vCons(Y:Val, YS:ValSeq)) => ((I =/=Int J andBool closeV(X, Y, T)) orBool closeInner(X, T, I, J +Int 1, YS))`

- L87 — syntax; attributes: function, total; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Bool ::= closeOuter(Val, Int, ValSeq, ValSeq) [function, total]`

- L88 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule closeOuter(_:Val, _:Int, .ValSeq, _:ValSeq) => false`

- L89 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule closeOuter(T:Val, I:Int, vCons(X:Val, XS:ValSeq), ALL:ValSeq) => (closeInner(X, T, I, 0, ALL) orBool closeOuter(T, I +Int 1, XS, ALL))`

- L93 — syntax; attributes: function, total; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `syntax Bool ::= hasClose(ValSeq, Val) [function, total]`

- L94 — rule; attributes: none; assessment: CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)

  `rule hasClose(VS:ValSeq, T:Val) => closeOuter(T, 0, VS, VS)`

## `spec.k`

- L7 — claim; attributes: none; assessment: CLAIM (manual pre/post and adequacy assessment in REVIEW.md)

  `claim [inner-loop]: <k> #loop(list(YS:ValSeq), Name("y"), HC-INNER-BODY) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope( "numbers" |-> list(ALL:ValSeq) "threshold" |-> T:Float "result" |-> (R:Bool => R orBool closeInner(X, T, I, J, YS)) "i" |-> I:Int "j" |-> (J:Int => advanceIndex(J, YS)) "x" |-> X:Val "y" |-> (_Y0:Val => ?Y:Val), parent(0)) 0 |-> scope(M0:Map, parent(-1)) -1 |-> builtinsScope ... </scopes> requires isFloat(X) andBool allFloatVS(YS) andBool notBool ("abs" in_keys(M0))`

- L29 — claim; attributes: none; assessment: CLAIM (manual pre/post and adequacy assessment in REVIEW.md)

  `claim [outer-loop]: <k> #loop(list(XS:ValSeq), Name("x"), HC-OUTER-BODY) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope( "numbers" |-> list(ALL:ValSeq) "threshold" |-> T:Float "result" |-> (R:Bool => R orBool closeOuter(T, I, XS, ALL)) "i" |-> (I:Int => advanceIndex(I, XS)) "j" |-> (_J0:Int => ?J:Int) "x" |-> (_X0:Val => ?X:Val) "y" |-> (_Y0:Val => ?Y:Val), parent(0)) 0 |-> scope(M0:Map, parent(-1)) -1 |-> builtinsScope ... </scopes> requires allFloatVS(XS) andBool allFloatVS(ALL) andBool notBool ("abs" in_keys(M0))`

- L51 — claim; attributes: none; assessment: CLAIM (manual pre/post and adequacy assessment in REVIEW.md)

  `claim [has-close-elements]: <k> #loadAll(Module( ImportFrom("typing", "List") FuncDef("has_close_elements", Params("numbers", "threshold"), HC-FUNCTION-BODY))) ~> Call(Name("has_close_elements"), list(VS:ValSeq), T:Float) => ?R:Bool </k> <env> 0 </env> <scopes> 0 |-> scope(.Map => ?MODULE:Map, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allFloatVS(VS) ensures ?R ==Bool hasClose(VS, T)`


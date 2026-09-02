# Exhaustive K declaration and rule inventory

Generated from the clean trusted-semantics scratch copy and candidate proof sources.
Each source-starting declaration is listed exactly once; multiline bodies, guards, cells,
attributes, and right-hand sides are collapsed onto one line.

## reference-semantics/semantics.k

Counts: endmodule=2, imports=23, module=2, requires=23

- `requires` L34: `requires "semantics/syntax.k"`
- `requires` L35: `requires "semantics/core.k"`
- `requires` L36: `requires "semantics/iter.k"`
- `requires` L37: `requires "semantics/range.k"`
- `requires` L38: `requires "semantics/operators.k"`
- `requires` L39: `requires "semantics/int.k"`
- `requires` L40: `requires "semantics/bool.k"`
- `requires` L41: `requires "semantics/float.k"`
- `requires` L42: `requires "semantics/str.k"`
- `requires` L43: `requires "semantics/set.k"`
- `requires` L44: `requires "semantics/list.k"`
- `requires` L45: `requires "semantics/tuple.k"`
- `requires` L46: `requires "semantics/subscript.k"`
- `requires` L47: `requires "semantics/comprehension.k"`
- `requires` L48: `requires "semantics/methods.k"`
- `requires` L49: `requires "semantics/controls.k"`
- `requires` L50: `requires "semantics/functions.k"`
- `requires` L51: `requires "semantics/builtins.k"`
- `requires` L52: `requires "semantics/call.k"`
- `requires` L53: `requires "semantics/sort.k"`
- `requires` L54: `requires "semantics/assert.k"`
- `requires` L55: `requires "semantics/dict.k"`
- `requires` L56: `requires "semantics/concrete.k"`
- `module` L58: `module MPY`
- `imports` L59: `imports MPY-CORE`
- `imports` L60: `imports MPY-ITER`
- `imports` L61: `imports MPY-RANGE`
- `imports` L62: `imports MPY-OPERATORS`
- `imports` L63: `imports MPY-INT`
- `imports` L64: `imports MPY-BOOL`
- `imports` L65: `imports MPY-FLOAT`
- `imports` L66: `imports MPY-STR`
- `imports` L67: `imports MPY-SET`
- `imports` L68: `imports MPY-LIST`
- `imports` L69: `imports MPY-TUPLE`
- `imports` L70: `imports MPY-SUBSCRIPT`
- `imports` L71: `imports MPY-COMPREHENSION`
- `imports` L72: `imports MPY-METHODS`
- `imports` L73: `imports MPY-CONTROLS`
- `imports` L74: `imports MPY-FUNCTIONS`
- `imports` L75: `imports MPY-BUILTINS`
- `imports` L76: `imports MPY-CALL`
- `imports` L77: `imports MPY-SORT`
- `imports` L78: `imports MPY-ASSERT`
- `imports` L79: `imports MPY-DICT`
- `endmodule` L80: `endmodule`
- `module` L87: `module MPY-KRUN`
- `imports` L88: `imports MPY`
- `imports` L89: `imports MPY-CONCRETE`
- `endmodule` L90: `endmodule`

## reference-semantics/semantics/assert.k

Counts: endmodule=1, imports=1, module=1, requires=2, rule=3, rule:priority=1

- `module` L3: `module MPY-ASSERT`
- `imports` L4: `imports MPY-CORE`
- `rule` L6: `rule <k> Assert(V:Val) => .K ... </k>`
- `requires` L7: `requires truthy(V)`
- `rule` L8-10: `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code>`
- `requires` L11: `requires notBool truthy(V)`
- `rule` L13-15: `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `endmodule` L16: `endmodule`

## reference-semantics/semantics/bool.k

Counts: context=1, endmodule=1, imports=1, module=1, requires=8, rule=13, rule:priority=1

- `module` L5: `module MPY-BOOL`
- `imports` L6: `imports MPY-CORE`
- `rule` L8: `rule applyUn("not", V:Val) => notBool truthy(V)`
- `rule` L10: `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`
- `rule` L11: `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`
- `context` L16: `context BoolOp(_, (HOLE:Expr, _:Exprs))`
- `rule` L17: `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`
- `rule` L18: `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>`
- `requires` L19: `requires truthy(V)`
- `rule` L20: `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>`
- `requires` L21: `requires notBool truthy(V)`
- `rule` L22: `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>`
- `requires` L23: `requires truthy(V)`
- `rule` L24: `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>`
- `requires` L25: `requires notBool truthy(V)`
- `rule` L29-30: `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`
- `rule` L31-32: `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L33: `requires truthy(V)`
- `rule` L35-36: `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L37: `requires notBool truthy(V)`
- `rule` L39-40: `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L41: `requires truthy(V)`
- `rule` L43-44: `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L45: `requires notBool truthy(V)`
- `endmodule` L47: `endmodule`

## reference-semantics/semantics/builtins.k

Counts: endmodule=1, imports=7, module=1, requires=21, rule=137, rule:owise=10, rule:priority=1, syntax=38, syntax:function=29, syntax:total=22

- `module` L3: `module MPY-BUILTINS`
- `imports` L4: `imports MPY-CORE`
- `imports` L5: `imports MPY-STR`
- `imports` L6: `imports MPY-SET`
- `imports` L7: `imports MPY-ITER`
- `imports` L8: `imports MPY-RANGE`
- `imports` L9: `imports MPY-INT`
- `imports` L10: `imports MPY-METHODS`
- `syntax` L17: `syntax Val ::= applyBuiltin(String, Vals) [function]`
- `syntax` L20: `syntax Int ::= seqLen(Val) [function]`
- `rule` L21: `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`
- `rule` L22: `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)`
- `rule` L23: `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)`
- `rule` L24: `rule seqLen(str(IS:IntSeq))                   => isLen(IS)`
- `rule` L25: `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)`
- `rule` L26: `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`
- `rule` L32: `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>`
- `rule` L33: `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
- `rule` L34: `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>`
- `rule` L35: `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>`
- `syntax` L36: `syntax ValSeq ::= charsOf(IntSeq) [function, total]`
- `rule` L37: `rule charsOf(.IntSeq)                => .ValSeq`
- `rule` L38: `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`
- `rule` L41: `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`
- `rule` L44: `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`
- `syntax` L47: `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`
- `rule` L48: `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`
- `rule` L49: `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`
- `rule` L50-51: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k>`
- `requires` L52: `requires isInt(V) orBool isBool(V)`
- `syntax` L54: `syntax Int ::= intOf(Val) [function]`
- `rule` L55: `rule intOf(I:Int)  => I`
- `rule` L56: `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`
- `syntax` L59: `syntax KItem ::= #allAcc(Iterable) | "#allCont"`
- `rule` L60: `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`
- `rule` L61: `rule <k> #iterDone ~> #allCont => true ... </k>`
- `rule` L62: `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>`
- `requires` L63: `requires truthy(V)`
- `rule` L64: `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>`
- `requires` L65: `requires notBool truthy(V)`
- `syntax` L67: `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`
- `rule` L68: `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`
- `rule` L69: `rule <k> #iterDone ~> #anyCont => false ... </k>`
- `rule` L70: `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>`
- `requires` L71: `requires truthy(V)`
- `rule` L72: `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>`
- `requires` L73: `requires notBool truthy(V)`
- `syntax` L76: `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`
- `rule` L77: `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`
- `rule` L78: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>`
- `requires` L79: `requires isInt(V)`
- `rule` L80: `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`
- `rule` L81: `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`
- `rule` L82-83: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>`
- `requires` L84: `requires isInt(V)`
- `syntax` L86: `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`
- `rule` L87: `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`
- `rule` L88: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>`
- `requires` L89: `requires isInt(V)`
- `rule` L90: `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`
- `rule` L91: `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`
- `rule` L92-93: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k>`
- `requires` L94: `requires isInt(V)`
- `syntax` L97: `syntax Int ::= maxVals(Int, Vals) [function]`
- `rule` L98: `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`
- `rule` L99: `rule maxVals(M:Int, .Vals)           => M`
- `rule` L100: `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`
- `syntax` L102: `syntax Int ::= minVals(Int, Vals) [function]`
- `rule` L103: `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`
- `rule` L104: `rule minVals(M:Int, .Vals)           => M`
- `rule` L105: `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`
- `rule` L108: `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))`
- `requires` L109: `requires N >=Int 0`
- `rule` L111-112: `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))`
- `requires` L113: `requires N <Int 0`
- `syntax` L114: `syntax IntSeq ::= binCodes(Int) [function, total]`
- `rule` L115: `rule binCodes(0) => iCons(48, .IntSeq)`
- `rule` L116: `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`
- `syntax` L117: `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`
- `rule` L118: `rule binAcc(0, ACC:IntSeq) => ACC`
- `rule` L119-120: `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))`
- `requires` L121: `requires N >Int 0`
- `rule` L124-125: `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`
- `syntax` L126: `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`
- `rule` L127: `rule enumVS(.ValSeq, _:Int) => .ValSeq`
- `rule` L128-129: `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`
- `rule` L132-133: `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`
- `syntax` L134: `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`
- `rule` L135: `rule mapStrVS(.ValSeq) => .ValSeq`
- `rule` L136: `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`
- `rule` L137: `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`
- `rule` L140: `rule applyBuiltin("int", I:Int, .Vals) => I`
- `rule` L143: `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`
- `rule` L144: `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))`
- `requires` L145: `requires 0 <=Int I andBool I <Int 128`
- `rule` L148: `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))`
- `rule` L149: `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`
- `rule` L152: `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48`
- `requires` L153: `requires 48 <=Int C andBool C <=Int 57`
- `rule` L156: `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)`
- `requires` L157: `requires isLen(CS) >=Int 2`
- `syntax` L158: `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`
- `rule` L159: `rule intDigAcc(.IntSeq, ACC:Int)             => ACC`
- `rule` L160: `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`
- `rule` L163: `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`
- `rule` L164: `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)`
- `rule` L167-168: `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`
- `rule` L169: `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>`
- `rule` L170: `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`
- `rule` L171-172: `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`
- `rule` L173: `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>`
- `rule` L174: `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`
- `rule` L177: `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)`
- `rule` L178: `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)`
- `rule` L179: `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)`
- `requires` L180: `requires S =/=Int 0`
- `rule` L187: `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`
- `syntax` L188: `syntax Int ::= evalArith(IntSeq) [function]`
- `rule` L189-190: `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`
- `syntax` L192: `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`
- `syntax` L194: `syntax Bool ::= evDigit(Int) [function, total]`
- `rule` L195: `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`
- `syntax` L196: `syntax Bool ::= evHead42(IntSeq) [function, total]`
- `rule` L197: `rule evHead42(iCons(42, _:IntSeq)) => true`
- `rule` L198: `rule evHead42(_:IntSeq)            => false [owise]`
- `syntax` L199: `syntax Bool ::= evHead47(IntSeq) [function, total]`
- `rule` L200: `rule evHead47(iCons(47, _:IntSeq)) => true`
- `rule` L201: `rule evHead47(_:IntSeq)            => false [owise]`
- `syntax` L203: `syntax OpSeq ::= tokOps(IntSeq) [function, total]`
- `rule` L204: `rule tokOps(.IntSeq)                 => .OpSeq`
- `rule` L205: `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)`
- `rule` L206: `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)`
- `rule` L207: `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`
- `rule` L208: `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)`
- `rule` L209: `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))`
- `rule` L210: `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)`
- `rule` L211: `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))`
- `rule` L212: `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))`
- `syntax` L214-215: `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`
- `rule` L216: `rule tokNds(.IntSeq)                => .IntSeq`
- `rule` L217: `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)`
- `rule` L218: `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`
- `rule` L219: `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)`
- `requires` L220: `requires notBool evDigit(C) andBool C =/=Int 32`
- `rule` L221: `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)`
- `requires` L222: `requires evDigit(C)`
- `rule` L223: `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`
- `syntax` L225: `syntax EvPair ::= evp(OpSeq, IntSeq)`
- `syntax` L226: `syntax Int ::= firstNdE(EvPair) [function, total]`
- `rule` L227: `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`
- `rule` L228: `rule firstNdE(_:EvPair) => 0 [owise]`
- `syntax` L230: `syntax Int ::= applyOpE(String, Int, Int) [function, total]`
- `rule` L231: `rule applyOpE("+",  A:Int, B:Int) => A +Int B`
- `rule` L232: `rule applyOpE("-",  A:Int, B:Int) => A -Int B`
- `rule` L233: `rule applyOpE("*",  A:Int, B:Int) => A *Int B`
- `rule` L234: `rule applyOpE("//", A:Int, B:Int) => A divInt B`
- `rule` L235: `rule applyOpE("**", A:Int, B:Int) => A ^Int B`
- `rule` L236: `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`
- `syntax` L238: `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`
- `rule` L239: `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`
- `rule` L240: `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`
- `rule` L241: `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))`
- `requires` L242: `requires O =/=String "**"`
- `rule` L243: `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`
- `syntax` L244: `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`
- `rule` L245: `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`
- `rule` L246: `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`
- `syntax` L247: `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`
- `rule` L248: `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`
- `syntax` L250: `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`
- `rule` L251: `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`
- `rule` L252: `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
- `rule` L253: `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`
- `rule` L254: `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
- `syntax` L255: `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`
- `rule` L256: `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`
- `rule` L257-258: `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)`
- `requires` L259: `requires inLevelE(L, O)`
- `rule` L260-261: `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))`
- `requires` L262: `requires notBool inLevelE(L, O)`
- `rule` L263-264: `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`
- `syntax` L265: `syntax Bool ::= inLevelE(String, String) [function, total]`
- `rule` L266: `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"`
- `rule` L267: `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`
- `rule` L268: `rule inLevelE(_:String, _:String) => false [owise]`
- `syntax` L269: `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`
- `rule` L270: `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`
- `rule` L271: `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`
- `syntax` L272: `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`
- `rule` L273: `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`
- `rule` L274: `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`
- `syntax` L279: `syntax KItem ::= "#md5"`
- `rule` L280-281: `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`
- `rule` L282: `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`
- `syntax` L283: `syntax Val ::= md5Obj(IntSeq)`
- `rule` L284: `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`
- `syntax` L285: `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`
- `rule` L291: `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`
- `rule` L292: `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`
- `syntax` L293: `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`
- `rule` L294: `rule isIntV(_:Int)         => true`
- `rule` L295: `rule isIntV(_:Val)         => false [owise]`
- `rule` L296: `rule isStrV(str(_:IntSeq)) => true`
- `rule` L297: `rule isStrV(_:Val)         => false [owise]`
- `endmodule` L298: `endmodule`

## reference-semantics/semantics/call.k

Counts: endmodule=1, imports=3, module=1, requires=4, rule=21, rule:owise=2, rule:priority=2, syntax=3, syntax:function=1, syntax:total=1

- `module` L10: `module MPY-CALL`
- `imports` L11: `imports MPY-METHODS`
- `imports` L12: `imports MPY-BUILTINS`
- `imports` L13: `imports MPY-FUNCTIONS`
- `rule` L16: `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`
- `syntax` L19: `syntax KItem ::= #callee(Exprs)`
- `rule` L20: `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`
- `rule` L21: `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`
- `rule` L24: `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`
- `rule` L26: `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`
- `rule` L27: `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>`
- `rule` L28: `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>`
- `rule` L29: `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>`
- `rule` L30: `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>`
- `rule` L31: `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`
- `rule` L32: `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>`
- `rule` L38-41: `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` L42-44: `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L45: `requires notBool isRefV(A)`
- `rule` L47-50: `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `syntax` L52: `syntax Bool ::= isMutMethod(String) [function, total]`
- `rule` L53-55: `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`
- `rule` L56-58: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L59: `requires notBool isMutMethod(M)`
- `rule` L63-65: `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L66: `requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)`
- `rule` L69-74: `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
- `rule` L80-85: `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
- `syntax` L87: `syntax KItem ::= #allocCells(ParamNames)`
- `rule` L88: `rule <k> #allocCells(.ParamNames) => .K ... </k>`
- `rule` L89-93: `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc>`
- `requires` L94: `requires notBool N in_keys(H)`
- `endmodule` L95: `endmodule`

## reference-semantics/semantics/comprehension.k

Counts: endmodule=1, imports=5, module=1, rule=7, syntax=3, syntax:macro=3

- `module` L3: `module MPY-COMPREHENSION`
- `imports` L4: `imports MPY-CORE`
- `imports` L5: `imports MPY-OPERATORS`
- `imports` L6: `imports MPY-LIST`
- `imports` L7: `imports MPY-CONTROLS`
- `imports` L8: `imports MPY-FUNCTIONS`
- `rule` L11: `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
- `rule` L12: `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
- `syntax` L14: `syntax Stmts ::= compBody(CompFors, Expr) [macro]`
- `rule` L15-16: `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`
- `syntax` L18: `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`
- `rule` L19-20: `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`
- `rule` L21-22: `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`
- `syntax` L24: `syntax Expr ::= compGuard(Exprs) [macro]`
- `rule` L25: `rule compGuard(.Exprs)             => Bool(true)`
- `rule` L26: `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`
- `endmodule` L27: `endmodule`

## reference-semantics/semantics/concrete.k

Counts: endmodule=1, imports=1, module=1, requires=5, rule=16, rule:owise=1, rule:priority=2, syntax=5, syntax:function=3, syntax:total=1

- `module` L8: `module MPY-CONCRETE`
- `imports` L9: `imports MPY`
- `rule` L13-14: `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap>`
- `requires` L15: `requires hasRefVS(A) orBool hasRefVS(B)`
- `rule` L16-17: `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap>`
- `requires` L18: `requires hasRefVS(A) orBool hasRefVS(B)`
- `syntax` L25: `syntax Val ::= kvP(Val, Val)`
- `syntax` L26-27: `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`
- `rule` L28-30: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`
- `rule` L31-33: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`
- `rule` L34-35: `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`
- `rule` L36-37: `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`
- `rule` L38-39: `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>`
- `requires` L40: `requires notBool isKwV(K)`
- `syntax` L42: `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`
- `rule` L43: `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`
- `rule` L44-45: `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R))`
- `requires` L46: `requires kLt(K, K2)`
- `rule` L47-48: `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V))`
- `requires` L49: `requires notBool kLt(K, K2)`
- `syntax` L51: `syntax Bool ::= kLt(Val, Val) [function]`
- `rule` L52: `rule kLt(I1:Int, I2:Int)             => I1 <Int I2`
- `rule` L53: `rule kLt(F1:Float, F2:Float)         => F1 <Float F2`
- `rule` L54: `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
- `syntax` L56: `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`
- `rule` L57: `rule unpairVS(.ValSeq) => .ValSeq`
- `rule` L58: `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`
- `rule` L59: `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`
- `endmodule` L60: `endmodule`

## reference-semantics/semantics/controls.k

Counts: endmodule=1, imports=3, module=1, requires=9, rule=34, rule:owise=3, rule:priority=4, syntax=3

- `module` L3: `module MPY-CONTROLS`
- `imports` L4: `imports MPY-CORE`
- `imports` L5: `imports MPY-TUPLE`
- `imports` L6: `imports MPY-ITER`
- `rule` L9-11: `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
- `rule` L12-14: `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
- `requires` L15: `requires "$cells" in_keys(M)`
- `rule` L20-22: `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>`
- `requires` L23: `requires X in_keys(M)`
- `rule` L27-29: `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
- `requires` L30: `requires X in_keys(M) andBool isRefV({M[X]}:>Val)`
- `rule` L35: `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`
- `rule` L36: `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`
- `syntax` L37: `syntax KItem ::= #bindImports(ParamNames)`
- `rule` L38: `rule <k> #bindImports(.ParamNames) => .K ... </k>`
- `rule` L39-41: `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>`
- `requires` L42: `requires N ==String "floor" orBool N ==String "ceil"`
- `rule` L43: `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>`
- `requires` L44: `requires notBool (N ==String "floor" orBool N ==String "ceil")`
- `rule` L48: `rule <k> Expr(_:Val) => .K ... </k>`
- `syntax` L51: `syntax KItem ::= #branch(Bool, Stmts, Stmts)`
- `rule` L52: `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`
- `rule` L53: `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>`
- `rule` L54: `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`
- `rule` L57: `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>`
- `requires` L58: `requires truthy(V)`
- `rule` L59: `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>`
- `requires` L60: `requires notBool truthy(V)`
- `syntax` L65-67: `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`
- `rule` L69: `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`
- `rule` L71: `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`
- `rule` L72: `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`
- `rule` L73-74: `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`
- `rule` L77: `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`
- `rule` L78: `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`
- `rule` L79: `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>`
- `requires` L80: `requires truthy(V)`
- `rule` L81: `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>`
- `requires` L82: `requires notBool truthy(V)`
- `rule` L85: `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`
- `rule` L86: `rule <k> Continue => #cont ... </k>`
- `rule` L87: `rule <k> Break => #brk ... </k>`
- `rule` L88: `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`
- `rule` L89: `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`
- `rule` L90: `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`
- `rule` L91: `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`
- `rule` L95-97: `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` L98-100: `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` L101-103: `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` L106-108: `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `endmodule` L109: `endmodule`

## reference-semantics/semantics/core.k

Counts: configuration=1, endmodule=1, imports=7, module=1, requires=8, rule=46, rule:owise=3, syntax=37, syntax:function=16, syntax:total=10

- `module` L3: `module MPY-CORE`
- `imports` L4: `imports MPY-SYNTAX`
- `imports` L5: `imports INT`
- `imports` L6: `imports BOOL`
- `imports` L7: `imports STRING`
- `imports` L8: `imports MAP`
- `imports` L9: `imports LIST`
- `imports` L10: `imports K-EQUAL`
- `syntax` L13: `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`
- `syntax` L14: `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`
- `syntax` L15: `syntax Str    ::= str(IntSeq)`
- `syntax` L18-23: `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`
- `syntax` L25-34: `syntax Val      ::= Int | Bool | "noneV" | Iterable | ref(Int)          // a heap object: <heap> holds its list(VS) | cellRef(Int)      // a closure cell: <heap> holds cellV(V) | closureVal(ParamNames, Stmts, Int) | typeV(String)     // a type object (int/str), resolved from the builtins frame | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) | boundMethodV(Val, String)   // a cooled Attribute: obj.method`
- `syntax` L36: `syntax Parent   ::= "root" | parent(Int)`
- `syntax` L37: `syntax Scope    ::= scope(Map, Parent)`
- `syntax` L38: `syntax KResult  ::= Val`
- `syntax` L39: `syntax Expr     ::= Val   // cooling puts results back into expression holes`
- `syntax` L40: `syntax Vals     ::= List{Val, ","}`
- `syntax` L41: `syntax Exc      ::= "NoExc" | "AssertionError"`
- `syntax` L42: `syntax RetState ::= "noRet" | retV(Val)`
- `configuration` L49-60: `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     |-> scope(.Map, parent(-1)) -1    |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>`
- `syntax` L68: `syntax Bool ::= isRefV(Val) [function, total]`
- `rule` L69: `rule isRefV(ref(_:Int)) => true`
- `rule` L70: `rule isRefV(_:Val)      => false [owise]`
- `syntax` L75: `syntax HeapVal ::= cellV(Val)`
- `syntax` L76: `syntax Bool ::= isCellRef(Val) [function, total]`
- `rule` L77: `rule isCellRef(cellRef(_:Int)) => true`
- `rule` L78: `rule isCellRef(_:Val)          => false [owise]`
- `rule` L85-88: `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap>`
- `requires` L89: `requires "$cells" in_keys(M)`
- `syntax` L95: `syntax Val ::= kwV(String, Val)`
- `syntax` L96: `syntax KItem ::= #kwTag(String)`
- `rule` L97: `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`
- `rule` L98: `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>`
- `requires` L99: `requires notBool isKwV(V)`
- `syntax` L100: `syntax Bool ::= isKwV(Val) [function, total]`
- `rule` L101: `rule isKwV(kwV(_:String, _:Val)) => true`
- `rule` L102: `rule isKwV(_:Val)                => false [owise]`
- `syntax` L106: `syntax Val ::= cellsMark(ParamNames)`
- `syntax` L107: `syntax ParamNames ::= cellsOf(Val) [function]`
- `rule` L108: `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`
- `syntax` L109: `syntax Bool ::= pnMember(String, ParamNames) [function, total]`
- `rule` L110: `rule pnMember(_:String, .ParamNames) => false`
- `rule` L111: `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`
- `syntax` L113: `syntax KItem ::= #cellW(Val, Val)`
- `rule` L114-115: `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`
- `syntax` L117: `syntax KItem ::= #alloc(Val)`
- `rule` L118-120: `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc>`
- `requires` L121: `requires notBool N in_keys(H)`
- `syntax` L124: `syntax KItem ::= #loadAll(Module)`
- `rule` L125: `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`
- `rule` L126: `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`
- `rule` L127: `rule <k> .Stmts => .K ... </k>`
- `syntax` L130: `syntax KItem ::= #look(String, Int)`
- `rule` L131: `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`
- `rule` L132-133: `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>`
- `requires` L134: `requires X in_keys(M)`
- `rule` L145-147: `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap>`
- `requires` L148: `requires X in_keys(M) andBool "$cells" in_keys(M)`
- `rule` L152-153: `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>`
- `requires` L154: `requires notBool (X in_keys(M))`
- `syntax` L157: `syntax Scope ::= "builtinsScope" [function, total]`
- `rule` L158-181: `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)`
- `syntax` L185: `syntax ApplyK ::= toCall(Val)`
- `syntax` L186-188: `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`
- `rule` L189: `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`
- `rule` L190: `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`
- `rule` L191: `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`
- `rule` L194: `rule <k> Int(I:Int)   => I ... </k>`
- `rule` L195: `rule <k> Bool(B:Bool) => B ... </k>`
- `rule` L196: `rule <k> NoneVal      => noneV ... </k>`
- `syntax` L199: `syntax Bool ::= truthy(Val) [function]`
- `rule` L200: `rule truthy(B:Bool)          => B`
- `rule` L201: `rule truthy(noneV)           => false`
- `rule` L202: `rule truthy(I:Int)           => I =/=Int 0`
- `rule` L203: `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)`
- `rule` L204: `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)`
- `rule` L205: `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`
- `syntax` L208: `syntax Val  ::= applyUn(String, Val) [function]`
- `syntax` L209: `syntax Val  ::= applyBin(String, Val, Val) [function]`
- `syntax` L210: `syntax Bool ::= applyCmp(String, Val, Val) [function]`
- `syntax` L213: `syntax Vals ::= appendVal(Vals, Val) [function, total]`
- `rule` L214: `rule appendVal(.Vals, V:Val)              => V , .Vals`
- `rule` L215: `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)`
- `syntax` L217: `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`
- `rule` L218: `rule vals2valSeq(.Vals)            => .ValSeq`
- `rule` L219: `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`
- `syntax` L223: `syntax Int ::= vsLen(ValSeq) [function, total]`
- `rule` L224: `rule vsLen(.ValSeq)                => 0`
- `rule` L225: `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`
- `syntax` L227: `syntax Int ::= isLen(IntSeq) [function, total]`
- `rule` L228: `rule isLen(.IntSeq)                => 0`
- `rule` L229: `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`
- `syntax` L233: `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`
- `rule` L234: `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq`
- `rule` L235: `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)`
- `rule` L236: `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))`
- `requires` L237: `requires I >Int 0`
- `rule` L238: `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS`
- `requires` L239: `requires I <Int 0`
- `endmodule` L240: `endmodule`

## reference-semantics/semantics/dict.k

Counts: endmodule=1, imports=4, module=1, requires=4, rule=28, rule:owise=1, rule:priority=2, syntax=12, syntax:function=8, syntax:total=4

- `module` L13: `module MPY-DICT`
- `imports` L14: `imports MPY-CORE`
- `imports` L15: `imports MPY-ITER`
- `imports` L16: `imports MPY-METHODS`
- `imports` L17: `imports MPY-LIST`
- `syntax` L20: `syntax Val ::= dictV(ValSeq, ValSeq)`
- `syntax` L23-25: `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`
- `rule` L26: `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`
- `rule` L27: `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`
- `rule` L28-29: `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`
- `rule` L30-31: `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`
- `rule` L32-33: `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`
- `syntax` L37: `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`
- `rule` L38: `rule dHasKey(.ValSeq, _:Val)                => false`
- `rule` L39: `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K`
- `rule` L40: `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`
- `syntax` L43: `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`
- `rule` L44: `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)`
- `rule` L45: `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`
- `syntax` L49: `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`
- `rule` L50: `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)`
- `requires` L51: `requires A ==K K`
- `rule` L52: `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))`
- `requires` L53: `requires notBool (A ==K K)`
- `rule` L54: `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`
- `rule` L58-60: `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`
- `rule` L63: `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`
- `syntax` L64: `syntax Val ::= applyIndexD(Val, Val) [function]`
- `rule` L65-66: `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`
- `syntax` L70: `syntax Val ::= dictSet(Val, Val, Val) [function]`
- `rule` L71: `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`
- `syntax` L76: `syntax KItem ::= #dsetK(String, Val)`
- `rule` L77: `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`
- `rule` L78-80: `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>`
- `requires` L81: `requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`
- `rule` L82-84: `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
- `requires` L85: `requires X in_keys(M) andBool isRefV({M[X]}:>Val)`
- `syntax` L86: `syntax KItem ::= #dsetV(Val, Val, Val)`
- `rule` L87-88: `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`
- `syntax` L90: `syntax Int ::= normIdxD(Int, Int) [function, total]`
- `rule` L91: `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`
- `rule` L92: `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0`
- `rule` L95-96: `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`
- `syntax` L97: `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`
- `rule` L98: `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`
- `rule` L99-100: `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`
- `syntax` L101: `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`
- `rule` L102: `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K`
- `rule` L103: `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`
- `endmodule` L104: `endmodule`

## reference-semantics/semantics/float.k

Counts: endmodule=1, imports=3, module=1, requires=7, rule=121, rule:concrete=25, rule:priority=4, syntax=34, syntax:function=26, syntax:total=25

- `module` L14: `module MPY-FLOAT`
- `imports` L15: `imports MPY-OPERATORS`
- `imports` L16: `imports MPY-BUILTINS`
- `imports` L17: `imports FLOAT`
- `syntax` L20: `syntax Val ::= Float`
- `rule` L21: `rule <k> Float(F:Float) => F ... </k>`
- `syntax` L24: `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
- `rule` L25: `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`
- `rule` L27: `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`
- `syntax` L30: `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
- `rule` L31: `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`
- `rule` L32: `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`
- `syntax` L37: `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
- `rule` L38: `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`
- `rule` L39: `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`
- `rule` L43: `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`
- `rule` L44: `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`
- `syntax` L50: `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
- `rule` L51: `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`
- `rule` L52: `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`
- `syntax` L54: `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
- `rule` L55: `rule absF(F:Float) => absFloat(F) [concrete]`
- `rule` L56: `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`
- `rule` L61: `rule <k> Import(_:String) => .K ... </k>`
- `syntax` L65: `syntax KItem ::= "#mathCeil"`
- `rule` L66: `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`
- `rule` L67: `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`
- `syntax` L70: `syntax KItem ::= "#mathFloor"`
- `rule` L71: `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`
- `rule` L72: `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`
- `syntax` L73: `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
- `rule` L74: `rule floorFI(I:Int)   => I                        [concrete]`
- `rule` L75: `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`
- `rule` L78: `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`
- `rule` L79: `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)`
- `syntax` L82: `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`
- `rule` L83: `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`
- `rule` L84: `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`
- `rule` L85: `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`
- `syntax` L86: `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
- `rule` L87: `rule toF(F:Float) => F        [concrete]`
- `rule` L88: `rule toF(I:Int)   => intToF(I) [concrete]`
- `syntax` L93: `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
- `rule` L94: `rule ceilF(I:Int)   => I                       [concrete]`
- `rule` L95: `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`
- `rule` L99: `rule applyUn("-", F:Float) => 0.0 -Float F`
- `syntax` L103: `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
- `rule` L104: `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`
- `rule` L105: `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`
- `syntax` L107: `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
- `rule` L108: `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`
- `rule` L109: `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`
- `syntax` L111: `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
- `rule` L112: `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`
- `rule` L113: `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`
- `syntax` L115: `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
- `rule` L116: `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`
- `rule` L117: `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`
- `syntax` L119: `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
- `rule` L120: `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`
- `rule` L121: `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`
- `syntax` L125: `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
- `rule` L126: `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`
- `rule` L127: `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)`
- `rule` L128: `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`
- `rule` L129: `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`
- `rule` L132: `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`
- `rule` L133: `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`
- `rule` L134: `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)`
- `rule` L135: `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))`
- `rule` L136: `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)`
- `rule` L137: `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))`
- `rule` L138: `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)`
- `rule` L139: `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))`
- `syntax` L142: `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
- `rule` L143: `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`
- `rule` L144: `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`
- `rule` L145: `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`
- `rule` L146: `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`
- `rule` L147: `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`
- `rule` L148: `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)`
- `rule` L149: `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))`
- `rule` L150: `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)`
- `rule` L151: `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))`
- `rule` L154: `rule applyCmp("==", V:Val, noneV) => V ==K noneV`
- `rule` L155: `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`
- `syntax` L160: `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
- `rule` L161: `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`
- `rule` L162-163: `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))`
- `requires` L164: `requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`
- `syntax` L165: `syntax Int ::= headIS(IntSeq) [function]`
- `rule` L166: `rule headIS(iCons(C:Int, _:IntSeq)) => C`
- `syntax` L167: `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`
- `rule` L168: `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`
- `rule` L169: `rule intPartAcc(.IntSeq, A:Int) => A`
- `rule` L170: `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`
- `rule` L171: `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))`
- `requires` L172: `requires C =/=Int 46`
- `syntax` L173: `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`
- `rule` L174: `rule fracPart(.IntSeq) => 0`
- `rule` L175: `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`
- `rule` L176: `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`
- `rule` L177: `rule fracAcc(.IntSeq, A:Int) => A`
- `rule` L178: `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`
- `syntax` L179: `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`
- `rule` L180: `rule fracScale(.IntSeq) => 1`
- `rule` L181: `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`
- `rule` L182: `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`
- `rule` L183: `rule fscAcc(.IntSeq, A:Int) => A`
- `rule` L184: `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`
- `rule` L185: `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`
- `rule` L186: `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)`
- `rule` L187: `rule applyBuiltin("float", F:Float, .Vals)        => F`
- `syntax` L190: `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
- `rule` L191: `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`
- `rule` L192: `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`
- `syntax` L195: `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
- `rule` L196: `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`
- `rule` L197: `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
- `rule` L198: `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
- `rule` L199: `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
- `rule` L200: `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
- `rule` L201: `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
- `rule` L202: `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
- `rule` L203: `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
- `rule` L204: `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
- `rule` L205: `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
- `rule` L206: `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`
- `syntax` L209: `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
- `rule` L210: `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`
- `rule` L211: `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`
- `rule` L213: `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)`
- `rule` L214: `rule applyBuiltin("float", F:Float, .Vals) => F`
- `syntax` L217: `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
- `rule` L218-222: `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`
- `syntax` L223: `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
- `rule` L224-226: `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`
- `rule` L227: `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)`
- `rule` L228: `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`
- `syntax` L230: `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
- `rule` L231: `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`
- `syntax` L232: `syntax KItem ::= "#mathSqrt"`
- `rule` L233: `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`
- `rule` L234: `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`
- `rule` L235: `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`
- `syntax` L243: `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`
- `rule` L244: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
- `rule` L245: `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`
- `rule` L246: `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`
- `rule` L247: `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>`
- `requires` L248: `requires isFloat(V)`
- `syntax` L250: `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`
- `rule` L251: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
- `rule` L252: `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`
- `rule` L253: `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`
- `rule` L254: `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>`
- `requires` L255: `requires isFloat(V)`
- `syntax` L261: `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`
- `rule` L262-263: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>`
- `requires` L264: `requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`
- `rule` L265: `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`
- `rule` L266: `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`
- `rule` L267-268: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>`
- `requires` L269: `requires isFloat(V)`
- `rule` L270-271: `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>`
- `requires` L272: `requires isInt(V) orBool isBool(V)`
- `endmodule` L273: `endmodule`

## reference-semantics/semantics/functions.k

Counts: endmodule=1, imports=1, module=1, requires=3, rule=15, syntax=4

- `module` L3: `module MPY-FUNCTIONS`
- `imports` L4: `imports MPY-CORE`
- `syntax` L8-11: `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`
- `rule` L14-16: `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`
- `syntax` L18: `syntax Expr ::= closureExpr(ParamNames, Stmts)`
- `rule` L19-20: `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`
- `syntax` L27: `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`
- `syntax` L31-32: `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`
- `rule` L33-35: `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`
- `rule` L36-40: `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
- `requires` L41: `requires FV in_keys(M)`
- `rule` L42-45: `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`
- `rule` L47-49: `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`
- `rule` L50-52: `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`
- `rule` L53-57: `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
- `requires` L58: `requires FV in_keys(M)`
- `rule` L59-60: `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`
- `rule` L63: `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`
- `rule` L64-66: `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`
- `rule` L68-71: `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
- `requires` L72: `requires "$cells" in_keys(M)`
- `rule` L78-79: `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`
- `rule` L80-81: `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`
- `rule` L85-90: `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`
- `endmodule` L91: `endmodule`

## reference-semantics/semantics/int.k

Counts: endmodule=1, imports=1, module=1, rule=16, syntax=1, syntax:function=1

- `module` L4: `module MPY-INT`
- `imports` L5: `imports MPY-CORE`
- `rule` L7: `rule applyUn("-", I:Int) => 0 -Int I`
- `rule` L9: `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2`
- `rule` L11: `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`
- `rule` L12: `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`
- `rule` L13: `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2`
- `rule` L14: `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2`
- `rule` L15: `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)`
- `rule` L16: `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2`
- `rule` L17: `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`
- `syntax` L19: `syntax Int ::= pyMod(Int, Int) [function]`
- `rule` L20: `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`
- `rule` L22: `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2`
- `rule` L23: `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2`
- `rule` L24: `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2`
- `rule` L25: `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2`
- `rule` L26: `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2`
- `rule` L27: `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2`
- `endmodule` L28: `endmodule`

## reference-semantics/semantics/iter.k

Counts: endmodule=1, imports=1, module=1, syntax=1

- `module` L6: `module MPY-ITER`
- `imports` L7: `imports MPY-CORE`
- `syntax` L8: `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`
- `endmodule` L9: `endmodule`

## reference-semantics/semantics/list.k

Counts: endmodule=1, imports=3, module=1, requires=4, rule=27, rule:owise=1, rule:priority=2, syntax=5, syntax:function=3, syntax:total=2

- `module` L3: `module MPY-LIST`
- `imports` L4: `imports MPY-CORE`
- `imports` L5: `imports MPY-ITER`
- `imports` L6: `imports MPY-OPERATORS`
- `rule` L9: `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>`
- `rule` L10: `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`
- `syntax` L13: `syntax ApplyK ::= "toList"`
- `rule` L14: `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`
- `rule` L15: `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`
- `syntax` L18: `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`
- `rule` L19: `rule valSeqConcat(.ValSeq, T:ValSeq)                => T`
- `rule` L20: `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`
- `rule` L24-25: `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`
- `rule` L27: `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`
- `rule` L28: `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`
- `syntax` L33: `syntax Bool ::= hasRefVS(ValSeq) [function, total]`
- `rule` L34: `rule hasRefVS(.ValSeq)                => false`
- `rule` L35: `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`
- `syntax` L37-38: `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map)        [function]`
- `rule` L39: `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true`
- `rule` L40: `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false`
- `rule` L41: `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false`
- `rule` L42-43: `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`
- `rule` L45: `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)`
- `requires` L46: `requires H in_keys(HP)`
- `rule` L47: `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)`
- `requires` L48: `requires notBool isRefV(A) andBool H in_keys(HP)`
- `rule` L49: `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`
- `rule` L50: `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`
- `rule` L53-55: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`
- `syntax` L58: `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`
- `rule` L59: `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`
- `rule` L60: `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`
- `rule` L61: `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`
- `rule` L62: `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`
- `rule` L63: `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>`
- `requires` L64: `requires E ==K V`
- `rule` L65: `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>`
- `requires` L66: `requires notBool (E ==K V)`
- `rule` L67: `rule <k> B:Bool ~> #notB => notBool B ... </k>`
- `endmodule` L68: `endmodule`

## reference-semantics/semantics/methods.k

Counts: endmodule=1, imports=4, module=1, requires=6, rule=75, rule:owise=4, rule:priority=3, syntax=27, syntax:function=27, syntax:total=22

- `module` L3: `module MPY-METHODS`
- `imports` L4: `imports MPY-CORE`
- `imports` L5: `imports K-EQUAL`
- `imports` L6: `imports MPY-STR`
- `imports` L7: `imports MPY-LIST`
- `syntax` L10: `syntax Val ::= applyMethod(Val, String, Vals) [function]`
- `rule` L13: `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`
- `rule` L14: `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`
- `rule` L15: `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`
- `rule` L16: `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`
- `rule` L19: `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))`
- `rule` L20: `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))`
- `rule` L21: `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`
- `rule` L26: `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`
- `syntax` L27: `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`
- `rule` L28: `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`
- `rule` L29: `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`
- `rule` L30-31: `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`
- `rule` L34: `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`
- `syntax` L35: `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`
- `rule` L36: `rule cntSub(.IntSeq, _:IntSeq) => 0`
- `rule` L37: `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)`
- `requires` L38: `requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`
- `rule` L39: `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)`
- `requires` L40: `requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`
- `syntax` L41: `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`
- `rule` L42: `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`
- `rule` L43: `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`
- `rule` L44: `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`
- `rule` L47: `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`
- `syntax` L48: `syntax IntSeq ::= trimWS(IntSeq) [function, total]`
- `rule` L49: `rule trimWS(.IntSeq) => .IntSeq`
- `rule` L50: `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`
- `rule` L51: `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`
- `syntax` L52: `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`
- `rule` L53: `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`
- `rule` L54: `rule revISAcc(.IntSeq, A:IntSeq) => A`
- `rule` L55: `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`
- `rule` L58: `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`
- `rule` L61: `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`
- `rule` L64: `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`
- `syntax` L65: `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`
- `rule` L66: `rule cntOccVS(.ValSeq, _:Val)                => 0`
- `rule` L67: `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`
- `rule` L68: `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)`
- `rule` L72-74: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`
- `syntax` L75: `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result`
- `rule` L76: `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`
- `rule` L77: `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))`
- `requires` L78: `requires isWSC(C)`
- `rule` L79: `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)`
- `requires` L80: `requires notBool isWSC(C)`
- `syntax` L82: `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`
- `rule` L83: `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC`
- `rule` L84: `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`
- `syntax` L85: `syntax Bool ::= isWSC(Int) [function, total]`
- `rule` L86: `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`
- `rule` L89-91: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`
- `rule` L94-96: `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`
- `syntax` L97: `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token`
- `rule` L98: `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)`
- `rule` L99: `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))`
- `requires` L100: `requires C ==Int SEP`
- `rule` L101: `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))`
- `requires` L102: `requires notBool (C ==Int SEP)`
- `rule` L104-105: `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`
- `syntax` L106: `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`
- `rule` L107: `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq`
- `rule` L108: `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`
- `rule` L109: `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`
- `syntax` L112: `syntax Bool ::= isUpperC(Int) [function, total]`
- `rule` L113: `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`
- `syntax` L115: `syntax Bool ::= isLowerC(Int) [function, total]`
- `rule` L116: `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`
- `syntax` L118: `syntax Bool ::= isAlphaC(Int) [function, total]`
- `rule` L119: `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`
- `syntax` L121: `syntax Bool ::= isDigitC(Int) [function, total]`
- `rule` L122: `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`
- `syntax` L124: `syntax Bool ::= hasUpper(IntSeq) [function, total]`
- `rule` L125: `rule hasUpper(.IntSeq) => false`
- `rule` L126: `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`
- `syntax` L128: `syntax Bool ::= hasLower(IntSeq) [function, total]`
- `rule` L129: `rule hasLower(.IntSeq) => false`
- `rule` L130: `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`
- `syntax` L132: `syntax Bool ::= allAlpha(IntSeq) [function, total]`
- `rule` L133: `rule allAlpha(.IntSeq) => true`
- `rule` L134: `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`
- `syntax` L136: `syntax Bool ::= allDigit(IntSeq) [function, total]`
- `rule` L137: `rule allDigit(.IntSeq) => true`
- `rule` L138: `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`
- `syntax` L140: `syntax Int ::= lowerC(Int) [function, total]`
- `rule` L142: `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`
- `rule` L143: `rule lowerC(C:Int) => C         [owise]`
- `syntax` L145: `syntax Int ::= upperC(Int) [function, total]`
- `rule` L146: `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`
- `rule` L147: `rule upperC(C:Int) => C         [owise]`
- `syntax` L149: `syntax Int ::= swapC(Int) [function, total]`
- `rule` L150: `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`
- `rule` L151: `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`
- `rule` L152: `rule swapC(C:Int) => C         [owise]`
- `syntax` L154: `syntax IntSeq ::= mapLower(IntSeq) [function, total]`
- `rule` L155: `rule mapLower(.IntSeq) => .IntSeq`
- `rule` L156: `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`
- `syntax` L158: `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`
- `rule` L159: `rule mapUpper(.IntSeq) => .IntSeq`
- `rule` L160: `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`
- `syntax` L162: `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`
- `rule` L163: `rule mapSwap(.IntSeq) => .IntSeq`
- `rule` L164: `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`
- `syntax` L166: `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`
- `rule` L167: `rule startsWith(.IntSeq, _:IntSeq)               => true`
- `rule` L168: `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- `rule` L169: `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`
- `endmodule` L170: `endmodule`

## reference-semantics/semantics/operators.k

Counts: context=2, endmodule=1, imports=2, module=1, requires=3, rule=10, rule:owise=1, rule:priority=2

- `module` L6: `module MPY-OPERATORS`
- `imports` L7: `imports MPY-CORE`
- `imports` L8: `imports MPY-ITER`
- `rule` L10: `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`
- `rule` L12: `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`
- `context` L15: `context Compare(HOLE, _)`
- `context` L16: `context Compare(_:Val, CmpOp(_, HOLE))`
- `rule` L17: `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`
- `rule` L19: `rule applyCmp("is",     V:Val, noneV) => V ==K noneV`
- `rule` L20: `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`
- `rule` L25-27: `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` L28-29: `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L30: `requires notBool isRefV(L)`
- `rule` L34-35: `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L36: `requires OP =/=String "in" andBool OP =/=String "not in"`
- `rule` L38-39: `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap>`
- `requires` L40: `requires notBool isRefV(L)`
- `rule` L44-46: `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `endmodule` L47: `endmodule`

## reference-semantics/semantics/range.k

Counts: endmodule=1, imports=2, module=1, requires=5, rule=6, syntax=2, syntax:function=2, syntax:total=1

- `module` L5: `module MPY-RANGE`
- `imports` L6: `imports MPY-CORE`
- `imports` L7: `imports MPY-ITER`
- `syntax` L9: `syntax Bool ::= inRange(Int, Int, Int) [function, total]`
- `rule` L10: `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`
- `syntax` L12: `syntax Int ::= rangeLen(Int, Int, Int) [function]`
- `rule` L13: `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST`
- `requires` L14: `requires ST >Int 0 andBool HI >Int LO`
- `rule` L15: `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)`
- `requires` L16: `requires ST <Int 0 andBool HI <Int LO`
- `rule` L17: `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0`
- `requires` L18: `requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`
- `rule` L20-21: `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>`
- `requires` L22: `requires inRange(I, HI, ST)`
- `rule` L23: `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>`
- `requires` L24: `requires notBool inRange(I, HI, ST)`
- `endmodule` L25: `endmodule`

## reference-semantics/semantics/set.k

Counts: endmodule=1, imports=1, module=1, requires=2, rule=12, syntax=6, syntax:function=5, syntax:total=5

- `module` L3: `module MPY-SET`
- `imports` L4: `imports MPY-CORE`
- `syntax` L8: `syntax Val ::= setV(IntSeq)`
- `syntax` L11: `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`
- `rule` L12: `rule codeIn(_:Int, .IntSeq)                => false`
- `rule` L13: `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`
- `syntax` L16-17: `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] | dedupFrom(IntSeq, IntSeq)  [function, total]`
- `rule` L18: `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`
- `rule` L19: `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`
- `rule` L20: `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)`
- `requires` L21: `requires codeIn(C, ACC)`
- `rule` L22: `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))`
- `requires` L23: `requires notBool codeIn(C, ACC)`
- `syntax` L25: `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`
- `rule` L26: `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)`
- `rule` L27: `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`
- `syntax` L31: `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`
- `rule` L32: `rule subsetCodes(.IntSeq, _:IntSeq)                => true`
- `rule` L33: `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`
- `syntax` L35: `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`
- `rule` L36: `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`
- `rule` L39: `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`
- `endmodule` L40: `endmodule`

## reference-semantics/semantics/sort.k

Counts: endmodule=1, imports=2, module=1, requires=2, rule=19, rule:concrete=7, rule:priority=1, syntax=6, syntax:function=6, syntax:total=4

- `module` L10: `module MPY-SORT`
- `imports` L11: `imports MPY-BUILTINS`
- `imports` L12: `imports MPY-SUBSCRIPT`
- `syntax` L18: `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
- `syntax` L19: `syntax ValSeq ::= insVS(Int, ValSeq) [function]`
- `rule` L20: `rule sortVS(.ValSeq)                => .ValSeq          [concrete]`
- `rule` L21: `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`
- `rule` L22: `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]`
- `rule` L23: `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`
- `rule` L24: `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]`
- `syntax` L26: `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`
- `rule` L27: `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`
- `rule` L28: `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`
- `rule` L29: `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))`
- `requires` L30: `requires strLt(A, B) orBool A ==K B [concrete]`
- `rule` L31: `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))`
- `requires` L32: `requires notBool (strLt(A, B) orBool A ==K B) [concrete]`
- `rule` L36-37: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`
- `rule` L40-42: `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`
- `syntax` L49: `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`
- `syntax` L51-52: `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`
- `rule` L53: `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`
- `rule` L54: `rule revVSAcc(.ValSeq, A:ValSeq) => A`
- `rule` L55: `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`
- `syntax` L57: `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`
- `rule` L58: `rule condRev(S:ValSeq, false) => S`
- `rule` L59: `rule condRev(S:ValSeq, true)  => revVS(S)`
- `rule` L61-62: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`
- `rule` L63-64: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`
- `rule` L65-66: `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`
- `endmodule` L72: `endmodule`

## reference-semantics/semantics/str.k

Counts: endmodule=1, imports=2, module=1, requires=2, rule=28, syntax=5, syntax:function=5, syntax:total=4

- `module` L3: `module MPY-STR`
- `imports` L4: `imports MPY-CORE`
- `imports` L5: `imports MPY-ITER`
- `rule` L8: `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>`
- `rule` L9-10: `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`
- `syntax` L13: `syntax IntSeq ::= strToCodes(String) [function]`
- `rule` L14: `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`
- `rule` L15: `rule strToCodes("") => .IntSeq`
- `rule` L16: `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))`
- `requires` L17: `requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128`
- `syntax` L20: `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`
- `rule` L21: `rule seqConcat(.IntSeq, T:IntSeq)                => T`
- `rule` L22: `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`
- `rule` L24: `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`
- `rule` L25: `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`
- `rule` L26: `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`
- `rule` L29: `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`
- `rule` L30: `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`
- `syntax` L32: `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`
- `rule` L33: `rule strPrefix(.IntSeq, _:IntSeq)               => true`
- `rule` L34: `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- `rule` L35: `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`
- `syntax` L37: `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`
- `rule` L38: `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)`
- `rule` L39: `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)`
- `rule` L40: `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)`
- `requires` L41: `requires notBool strPrefix(P, iCons(C, Xs))`
- `syntax` L48: `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`
- `rule` L49: `rule strLt(.IntSeq, .IntSeq)                => false`
- `rule` L50: `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`
- `rule` L51: `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- `rule` L52: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B`
- `rule` L53: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B`
- `rule` L54: `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`
- `rule` L56: `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
- `rule` L57: `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`
- `rule` L58: `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`
- `rule` L59: `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`
- `endmodule` L60: `endmodule`

## reference-semantics/semantics/subscript.k

Counts: context=2, endmodule=1, imports=1, module=1, requires=16, rule=40, rule:priority=2, syntax=15, syntax:function=13, syntax:total=6

- `module` L3: `module MPY-SUBSCRIPT`
- `imports` L4: `imports MPY-CORE`
- `syntax` L11: `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`
- `rule` L12: `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V`
- `rule` L13: `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)`
- `requires` L14: `requires I >Int 0`
- `syntax` L16: `syntax Int ::= intSeqAt(IntSeq, Int) [function]`
- `rule` L17: `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C`
- `rule` L18: `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)`
- `requires` L19: `requires I >Int 0`
- `syntax` L21: `syntax Int ::= normIdx(Int, Int) [function, total]`
- `rule` L22: `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`
- `rule` L23: `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0`
- `context` L27: `context Subscript(HOLE, _)`
- `context` L28: `context Subscript(_:Val, HOLE:Expr)`
- `rule` L31-33: `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` L35: `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`
- `syntax` L37: `syntax Val ::= applyIndex(Val, Int) [function]`
- `rule` L38: `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
- `rule` L39: `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
- `rule` L40-41: `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`
- `syntax` L44-47: `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`
- `syntax` L49: `syntax OptInt ::= "noB" | someB(Int)`
- `rule` L50: `rule <k> #evalB(NoBound)  => noB ... </k>`
- `rule` L51: `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>`
- `rule` L52: `rule <k> I:Int ~> #toSome => someB(I) ... </k>`
- `rule` L54: `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`
- `rule` L55: `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`
- `rule` L56: `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`
- `rule` L58-60: `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`
- `rule` L61: `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`
- `syntax` L63: `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`
- `rule` L64-65: `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
- `rule` L66-67: `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
- `rule` L68-69: `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`
- `syntax` L72: `syntax Int ::= slStep(OptInt) [function, total]`
- `rule` L73: `rule slStep(noB)          => 1`
- `rule` L74: `rule slStep(someB(S:Int)) => S`
- `syntax` L76: `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`
- `rule` L77: `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0`
- `requires` L78: `requires slStep(ST) >Int 0`
- `rule` L79: `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1`
- `requires` L80: `requires slStep(ST) <Int 0`
- `rule` L81: `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`
- `syntax` L83: `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`
- `rule` L84: `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN`
- `requires` L85: `requires slStep(ST) >Int 0`
- `rule` L86: `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1`
- `requires` L87: `requires slStep(ST) <Int 0`
- `rule` L88: `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`
- `syntax` L90: `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`
- `rule` L91: `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)`
- `requires` L92: `requires I  <Int 0`
- `rule` L93: `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)`
- `requires` L94: `requires I >=Int 0`
- `syntax` L96: `syntax Int ::= clampLo(Int, Int) [function, total]`
- `rule` L97: `rule clampLo(J:Int, _STEP:Int) => J`
- `requires` L98: `requires J >=Int 0`
- `rule` L99: `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi`
- `requires` L100: `requires J <Int 0`
- `syntax` L102: `syntax Int ::= clampHi(Int, Int, Int) [function, total]`
- `rule` L103: `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I`
- `requires` L104: `requires I  <Int LEN`
- `rule` L105: `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi`
- `requires` L106: `requires I >=Int LEN`
- `syntax` L109: `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`
- `rule` L110-111: `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))`
- `requires` L112: `requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
- `rule` L113: `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq`
- `requires` L114: `requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
- `syntax` L116: `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`
- `rule` L117-118: `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))`
- `requires` L119: `requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
- `rule` L120: `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq`
- `requires` L121: `requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
- `endmodule` L122: `endmodule`

## reference-semantics/semantics/syntax.k

Counts: endmodule=1, imports=4, module=1, syntax=16, syntax:macro=1, syntax:seqstrict=1, syntax:strict=2

- `module` L3: `module MPY-SYNTAX`
- `imports` L4: `imports INT-SYNTAX`
- `imports` L5: `imports FLOAT-SYNTAX`
- `imports` L6: `imports BOOL-SYNTAX`
- `imports` L7: `imports STRING-SYNTAX`
- `syntax` L9-30: `syntax Expr ::= "Int"      "(" Int ")" | "Float"    "(" Float ")" | "Bool"     "(" Bool ")" | "Name"     "(" String ")" | "Str"      "(" String ")" | "UnaryOp"  "(" String "," Expr ")" [strict(2)] | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp"    "(" String "," Exprs ")" | "ListExpr"  "(" Exprs ")" | "DictExpr"  "(" Entries ")" | "ListComp"  "(" Expr "," CompFors ")" [macro] | "GenExp"    "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda"    "(" Params "," Expr ")" | "KwArg"     "(" String "," Expr ")" | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call"      "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare"   "(" Expr "," CmpOp ")"`
- `syntax` L32: `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"`
- `syntax` L33: `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"`
- `syntax` L34: `syntax Entries  ::= List{Entry, ","}`
- `syntax` L35: `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`
- `syntax` L36: `syntax CompFors ::= List{CompFor, ""}`
- `syntax` L37: `syntax Exprs    ::= List{Expr, ","}`
- `syntax` L38: `syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`
- `syntax` L39: `syntax Bound    ::= Expr | "NoBound"`
- `syntax` L41-54: `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] | "Import"    "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While"     "(" Expr "," Stmts ")" | "Break" | "Continue" | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return"    "(" Expr ")" [strict] | "Assert"    "(" Expr ")" [strict] | "Expr"      "(" Expr ")" [strict] | "FuncDef"   "(" String "," Params "," Stmts ")" | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`
- `syntax` L56: `syntax Stmts      ::= List{Stmt, ""}`
- `syntax` L57: `syntax Params     ::= "Params" "(" ParamNames ")"`
- `syntax` L58: `syntax CellVars   ::= "CellVars" "(" ParamNames ")"`
- `syntax` L59: `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"`
- `syntax` L60: `syntax ParamNames ::= List{String, ","}`
- `syntax` L61: `syntax Module     ::= "Module" "(" Stmts ")"`
- `endmodule` L62: `endmodule`

## reference-semantics/semantics/tuple.k

Counts: endmodule=1, imports=4, module=1, requires=2, rule=21, rule:priority=2, syntax=4, syntax:function=1

- `module` L3: `module MPY-TUPLE`
- `imports` L4: `imports MPY-CORE`
- `imports` L5: `imports MPY-ITER`
- `imports` L6: `imports MPY-LIST`
- `imports` L7: `imports MPY-METHODS`
- `rule` L10: `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>`
- `rule` L11: `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`
- `syntax` L14: `syntax ApplyK ::= "toTuple"`
- `rule` L15: `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`
- `rule` L16: `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`
- `rule` L18: `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`
- `rule` L20: `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`
- `rule` L21: `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`
- `rule` L23: `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`
- `syntax` L24: `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`
- `rule` L25: `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`
- `rule` L26: `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)`
- `requires` L27: `requires notBool (A ==K V)`
- `rule` L28: `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`
- `syntax` L31: `syntax KItem ::= #bindTgt(Expr, Val)`
- `rule` L32-34: `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
- `rule` L35-37: `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
- `requires` L38: `requires "$cells" in_keys(M)`
- `rule` L42: `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- `rule` L43: `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`
- `rule` L44-46: `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `syntax` L49: `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`
- `rule` L50: `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- `rule` L51: `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`
- `rule` L52-54: `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` L55-56: `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`
- `rule` L57: `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`
- `endmodule` L58: `endmodule`

## verification.k

Counts: endmodule=1, imports=1, module=1, requires=1, rule=2, syntax=2, syntax:function=2, syntax:total=1

- `requires` L1: `requires "reference-semantics/semantics.k"`
- `module` L3: `module WORDS-STRING-VERIFICATION`
- `imports` L4: `imports MPY`
- `syntax` L8: `syntax Val ::= "wordsStringFunction" [function]`
- `rule` L9-21: `rule wordsStringFunction => closureVal( ("s", .ParamNames), Return( Call( Attribute( Call( Attribute(Name("s"), "replace"), (Str(","), Str(" "), .Exprs)), "split"), .Exprs)) .Stmts, 0)`
- `syntax` L25: `syntax ValSeq ::= wordsStringExpected(IntSeq) [function, total]`
- `rule` L26-27: `rule wordsStringExpected(CS:IntSeq) => splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq)`
- `endmodule` L28: `endmodule`

## spec.k

Counts: claim=1, endmodule=1, imports=1, module=1, requires=1

- `requires` L1: `requires "verification.k"`
- `module` L3: `module WORDS-STRING-SPEC`
- `imports` L4: `imports WORDS-STRING-VERIFICATION`
- `claim` L6-27: `claim <k> Call(wordsStringFunction, (str(CS), .Exprs)) => ref(0) </k> <env> 0 </env> <scopes> 0  |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map => 0 |-> list(wordsStringExpected(CS)) </heap> <heapLoc> 0 => 1 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>`
- `endmodule` L28: `endmodule`

## Grand totals

- claim: 1
- configuration: 1
- context: 5
- endmodule: 27
- imports: 88
- module: 27
- requires: 138
- rule: 697
- rule:concrete: 32
- rule:owise: 26
- rule:priority: 29
- syntax: 229
- syntax:function: 148
- syntax:macro: 4
- syntax:seqstrict: 1
- syntax:strict: 2
- syntax:total: 108

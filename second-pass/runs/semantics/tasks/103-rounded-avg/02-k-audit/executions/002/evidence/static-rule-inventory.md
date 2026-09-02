# Exhaustive source inventory

Inputs: trusted `/reference/reference-semantics/**/*.k`, candidate
`verification.k`, and candidate `spec.k`.

## /reference/reference-semantics/semantics.k

Counts: endmodule=2, imports=23, module=2, requires=23

- L34 `requires`
  `requires "semantics/syntax.k"`
- L35 `requires`
  `requires "semantics/core.k"`
- L36 `requires`
  `requires "semantics/iter.k"`
- L37 `requires`
  `requires "semantics/range.k"`
- L38 `requires`
  `requires "semantics/operators.k"`
- L39 `requires`
  `requires "semantics/int.k"`
- L40 `requires`
  `requires "semantics/bool.k"`
- L41 `requires`
  `requires "semantics/float.k"`
- L42 `requires`
  `requires "semantics/str.k"`
- L43 `requires`
  `requires "semantics/set.k"`
- L44 `requires`
  `requires "semantics/list.k"`
- L45 `requires`
  `requires "semantics/tuple.k"`
- L46 `requires`
  `requires "semantics/subscript.k"`
- L47 `requires`
  `requires "semantics/comprehension.k"`
- L48 `requires`
  `requires "semantics/methods.k"`
- L49 `requires`
  `requires "semantics/controls.k"`
- L50 `requires`
  `requires "semantics/functions.k"`
- L51 `requires`
  `requires "semantics/builtins.k"`
- L52 `requires`
  `requires "semantics/call.k"`
- L53 `requires`
  `requires "semantics/sort.k"`
- L54 `requires`
  `requires "semantics/assert.k"`
- L55 `requires`
  `requires "semantics/dict.k"`
- L56 `requires`
  `requires "semantics/concrete.k"`
- L58 `module`
  `module MPY`
- L59 `imports`
  `imports MPY-CORE`
- L60 `imports`
  `imports MPY-ITER`
- L61 `imports`
  `imports MPY-RANGE`
- L62 `imports`
  `imports MPY-OPERATORS`
- L63 `imports`
  `imports MPY-INT`
- L64 `imports`
  `imports MPY-BOOL`
- L65 `imports`
  `imports MPY-FLOAT`
- L66 `imports`
  `imports MPY-STR`
- L67 `imports`
  `imports MPY-SET`
- L68 `imports`
  `imports MPY-LIST`
- L69 `imports`
  `imports MPY-TUPLE`
- L70 `imports`
  `imports MPY-SUBSCRIPT`
- L71 `imports`
  `imports MPY-COMPREHENSION`
- L72 `imports`
  `imports MPY-METHODS`
- L73 `imports`
  `imports MPY-CONTROLS`
- L74 `imports`
  `imports MPY-FUNCTIONS`
- L75 `imports`
  `imports MPY-BUILTINS`
- L76 `imports`
  `imports MPY-CALL`
- L77 `imports`
  `imports MPY-SORT`
- L78 `imports`
  `imports MPY-ASSERT`
- L79 `imports`
  `imports MPY-DICT`
- L80 `endmodule`
  `endmodule`
- L87 `module`
  `module MPY-KRUN`
- L88 `imports`
  `imports MPY`
- L89 `imports`
  `imports MPY-CONCRETE`
- L90 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/assert.k

Counts: endmodule=1, imports=1, module=1, rule=3

- L3 `module`
  `module MPY-ASSERT`
- L4 `imports`
  `imports MPY-CORE`
- L6 `rule` [ordinary-rule]

  ```k
  rule <k> Assert(V:Val) => .K ... </k>
         requires truthy(V)
  ```
- L8 `rule` [ordinary-rule]

  ```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
         <exc> NoExc => AssertionError </exc>
         <exit-code> _ => 1 </exit-code>
         requires notBool truthy(V)
  ```
- L13 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L16 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/bool.k

Counts: context=1, endmodule=1, imports=1, module=1, rule=13

- L5 `module`
  `module MPY-BOOL`
- L6 `imports`
  `imports MPY-CORE`
- L8 `rule` [ordinary-rule]

  ```k
  rule applyUn("not", V:Val) => notBool truthy(V)
  ```
- L10 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
  ```
- L11 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
  
    // ==== BoolOp: short-circuit, value-returning and / or =====================
    // the node is its own accumulator: heat the HEAD element only, then either return it
    // (short-circuit) or drop it and continue
  ```
- L16 `context`

  ```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
  ```
- L17 `rule` [ordinary-rule]

  ```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
  ```
- L18 `rule` [ordinary-rule]

  ```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
         requires truthy(V)
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
         requires notBool truthy(V)
  ```
- L22 `rule` [ordinary-rule]

  ```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
         requires truthy(V)
  ```
- L24 `rule` [ordinary-rule]

  ```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
         requires notBool truthy(V)
  
    // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
    // operand — and/or return the OBJECT itself (Python identity), not its structure
  ```
- L29 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
         [priority(40)]
  ```
- L31 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires truthy(V)
         [priority(40)]
  ```
- L35 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool truthy(V)
         [priority(40)]
  ```
- L39 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires truthy(V)
         [priority(40)]
  ```
- L43 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool truthy(V)
         [priority(40)]
  ```
- L47 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/builtins.k

Counts: endmodule=1, imports=7, module=1, rule=137, syntax=38

- L3 `module`
  `module MPY-BUILTINS`
- L4 `imports`
  `imports MPY-CORE`
- L5 `imports`
  `imports MPY-STR`
- L6 `imports`
  `imports MPY-SET`
- L7 `imports`
  `imports MPY-ITER`
- L8 `imports`
  `imports MPY-RANGE`
- L9 `imports`
  `imports MPY-INT`
- L10 `imports`
  `imports MPY-METHODS`
- L17 `syntax` attrs=function

  ```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
  
    // ==== len(obj) — O(1) per kind ============================================
  ```
- L20 `syntax` attrs=function

  ```k
  syntax Int ::= seqLen(Val) [function]
  ```
- L21 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
  ```
- L22 `rule` [ordinary-rule]

  ```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
  ```
- L23 `rule` [ordinary-rule]

  ```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
  ```
- L24 `rule` [ordinary-rule]

  ```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
  ```
- L25 `rule` [ordinary-rule]

  ```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
  
    // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
    // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
    // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
    // (k-cell — list() constructs a NEW object)
  ```
- L32 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
  ```
- L33 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
  ```
- L34 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
  ```
- L35 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
  ```
- L36 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
  ```
- L37 `rule` [ordinary-rule]

  ```k
  rule charsOf(.IntSeq)                => .ValSeq
  ```
- L38 `rule` [ordinary-rule]

  ```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
  
    // ==== set(str) — distinct character codes =================================
  ```
- L41 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
  
    // ==== abs(int) ============================================================
  ```
- L44 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
  
    // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
  ```
- L47 `syntax`

  ```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
  ```
- L48 `rule` [ordinary-rule]

  ```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
  ```
- L49 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
  ```
- L50 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
          => #sumAcc(R, ACC +Int intOf(V)) ... </k>
         requires isInt(V) orBool isBool(V)
  ```
- L54 `syntax` attrs=function

  ```k
  syntax Int ::= intOf(Val) [function]
  ```
- L55 `rule` [ordinary-rule]

  ```k
  rule intOf(I:Int)  => I
  ```
- L56 `rule` [ordinary-rule]

  ```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
  
    // ==== all / any (short-circuiting #iterNext folds) ========================
  ```
- L59 `syntax`

  ```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
  ```
- L60 `rule` [ordinary-rule]

  ```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
  ```
- L61 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #allCont => true ... </k>
  ```
- L62 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
         requires truthy(V)
  ```
- L64 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
         requires notBool truthy(V)
  ```
- L67 `syntax`

  ```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
  ```
- L68 `rule` [ordinary-rule]

  ```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
  ```
- L69 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
  ```
- L70 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
         requires truthy(V)
  ```
- L72 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
         requires notBool truthy(V)
  
    // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
  ```
- L76 `syntax`

  ```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
  ```
- L77 `rule` [ordinary-rule]

  ```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
  ```
- L78 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
         requires isInt(V)
  ```
- L80 `rule` [ordinary-rule]

  ```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
  ```
- L81 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
  ```
- L82 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
          => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
         requires isInt(V)
  ```
- L86 `syntax`

  ```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
  ```
- L87 `rule` [ordinary-rule]

  ```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
  ```
- L88 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
         requires isInt(V)
  ```
- L90 `rule` [ordinary-rule]

  ```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
  ```
- L91 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
  ```
- L92 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
          => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
         requires isInt(V)
  
    // ==== variadic max / min (a Vals fold) ====================================
  ```
- L97 `syntax` attrs=function

  ```k
  syntax Int ::= maxVals(Int, Vals) [function]
  ```
- L98 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
  ```
- L99 `rule` [ordinary-rule]

  ```k
  rule maxVals(M:Int, .Vals)           => M
  ```
- L100 `rule` [ordinary-rule]

  ```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
  ```
- L102 `syntax` attrs=function

  ```k
  syntax Int ::= minVals(Int, Vals) [function]
  ```
- L103 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
  ```
- L104 `rule` [ordinary-rule]

  ```k
  rule minVals(M:Int, .Vals)           => M
  ```
- L105 `rule` [ordinary-rule]

  ```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
  
    // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
  ```
- L108 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
         requires N >=Int 0
    // negative operand: the '-' sign prefixes the magnitude's digits
  ```
- L111 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("bin", N:Int, .Vals)
      => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
         requires N <Int 0
  ```
- L114 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= binCodes(Int) [function, total]
  ```
- L115 `rule` [ordinary-rule]

  ```k
  rule binCodes(0) => iCons(48, .IntSeq)
  ```
- L116 `rule` [ordinary-rule]

  ```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
  ```
- L117 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
  ```
- L118 `rule` [ordinary-rule]

  ```k
  rule binAcc(0, ACC:IntSeq) => ACC
  ```
- L119 `rule` [ordinary-rule]

  ```k
  rule binAcc(N:Int, ACC:IntSeq)
      => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
         requires N >Int 0
  
    // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
  ```
- L124 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
          => #alloc(list(enumVS(VS, 0))) ... </k>
  ```
- L126 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
  ```
- L127 `rule` [ordinary-rule]

  ```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
  ```
- L128 `rule` [ordinary-rule]

  ```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
      => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
  
    // ==== map(str, xs) — eager (only the str case is in the subset) =============
  ```
- L132 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
          => #alloc(list(mapStrVS(VS))) ... </k>
  ```
- L134 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
  ```
- L135 `rule` [ordinary-rule]

  ```k
  rule mapStrVS(.ValSeq) => .ValSeq
  ```
- L136 `rule` [ordinary-rule]

  ```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
  ```
- L137 `rule` [ordinary-rule]

  ```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
  
    // ==== int(x) identities (int(round(x)) composes through) ====================
  ```
- L140 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("int", I:Int, .Vals) => I
  
    // ==== ord / chr ===========================================================
  ```
- L143 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
  ```
- L144 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
         requires 0 <=Int I andBool I <Int 128
  
    // ==== str(int) / str(str) =================================================
  ```
- L148 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
  ```
- L149 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
  
    // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
  ```
- L152 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
         requires 48 <=Int C andBool C <=Int 57
  
    // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
  ```
- L156 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
         requires isLen(CS) >=Int 2
  ```
- L158 `syntax` attrs=function,total

  ```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
  ```
- L159 `rule` [ordinary-rule]

  ```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
  ```
- L160 `rule` [ordinary-rule]

  ```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
  
    // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
  ```
- L163 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
  ```
- L164 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
  
    // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
  ```
- L167 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
          => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
  ```
- L169 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
  ```
- L170 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
  ```
- L171 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
          => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
  ```
- L173 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
  ```
- L174 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
  
    // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
  ```
- L177 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
  ```
- L178 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
  ```
- L179 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
         requires S =/=Int 0
  
    // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
    // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
    // trusted pass evaluator, now DEFINED in the reference and driven by a
    // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
    // argument leaves the call unevaluated for problem-level folds.
  ```
- L187 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
  ```
- L188 `syntax` attrs=function

  ```k
  syntax Int ::= evalArith(IntSeq) [function]
  ```
- L189 `rule` [ordinary-rule]

  ```k
  rule evalArith(CS:IntSeq)
      => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
  ```
- L192 `syntax`

  ```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
  ```
- L194 `syntax` attrs=function,total

  ```k
  syntax Bool ::= evDigit(Int) [function, total]
  ```
- L195 `rule` [ordinary-rule]

  ```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
  ```
- L196 `syntax` attrs=function,total

  ```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
  ```
- L197 `rule` [ordinary-rule]

  ```k
  rule evHead42(iCons(42, _:IntSeq)) => true
  ```
- L198 `rule` [owise-rule] attrs=owise

  ```k
  rule evHead42(_:IntSeq)            => false [owise]
  ```
- L199 `syntax` attrs=function,total

  ```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
  ```
- L200 `rule` [ordinary-rule]

  ```k
  rule evHead47(iCons(47, _:IntSeq)) => true
  ```
- L201 `rule` [owise-rule] attrs=owise

  ```k
  rule evHead47(_:IntSeq)            => false [owise]
  ```
- L203 `syntax` attrs=function,total

  ```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
  ```
- L204 `rule` [ordinary-rule]

  ```k
  rule tokOps(.IntSeq)                 => .OpSeq
  ```
- L205 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
  ```
- L206 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
  ```
- L207 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
  ```
- L208 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
  ```
- L209 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
  ```
- L210 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
  ```
- L211 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
  ```
- L212 `rule` [ordinary-rule]

  ```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
  ```
- L214 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                    | tokNdAcc(Int, IntSeq) [function, total]
  ```
- L216 `rule` [ordinary-rule]

  ```k
  rule tokNds(.IntSeq)                => .IntSeq
  ```
- L217 `rule` [ordinary-rule]

  ```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
  ```
- L218 `rule` [ordinary-rule]

  ```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
  ```
- L219 `rule` [ordinary-rule]

  ```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
         requires notBool evDigit(C) andBool C =/=Int 32
  ```
- L221 `rule` [ordinary-rule]

  ```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
         requires evDigit(C)
  ```
- L223 `rule` [owise-rule] attrs=owise

  ```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
  ```
- L225 `syntax`

  ```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
  ```
- L226 `syntax` attrs=function,total

  ```k
  syntax Int ::= firstNdE(EvPair) [function, total]
  ```
- L227 `rule` [ordinary-rule]

  ```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
  ```
- L228 `rule` [owise-rule] attrs=owise

  ```k
  rule firstNdE(_:EvPair) => 0 [owise]
  ```
- L230 `syntax` attrs=function,total

  ```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
  ```
- L231 `rule` [ordinary-rule]

  ```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
  ```
- L232 `rule` [ordinary-rule]

  ```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
  ```
- L233 `rule` [ordinary-rule]

  ```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
  ```
- L234 `rule` [ordinary-rule]

  ```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
  ```
- L235 `rule` [ordinary-rule]

  ```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
  ```
- L236 `rule` [owise-rule] attrs=owise

  ```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
  ```
- L238 `syntax` attrs=function,total

  ```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
  ```
- L239 `rule` [ordinary-rule]

  ```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
  ```
- L240 `rule` [ordinary-rule]

  ```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
  ```
- L241 `rule` [ordinary-rule]

  ```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
         requires O =/=String "**"
  ```
- L243 `rule` [owise-rule] attrs=owise

  ```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
  ```
- L244 `syntax` attrs=function,total

  ```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
  ```
- L245 `rule` [ordinary-rule]

  ```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
  ```
- L246 `rule` [ordinary-rule]

  ```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
  ```
- L247 `syntax` attrs=function,total

  ```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
  ```
- L248 `rule` [ordinary-rule]

  ```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
  ```
- L250 `syntax` attrs=function,total

  ```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
  ```
- L251 `rule` [ordinary-rule]

  ```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
  ```
- L252 `rule` [ordinary-rule]

  ```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
  ```
- L253 `rule` [ordinary-rule]

  ```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
  ```
- L254 `rule` [ordinary-rule]

  ```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
  ```
- L255 `syntax` attrs=function,total

  ```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
  ```
- L256 `rule` [ordinary-rule]

  ```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
  ```
- L257 `rule` [ordinary-rule]

  ```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
      => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
         requires inLevelE(L, O)
  ```
- L260 `rule` [ordinary-rule]

  ```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
      => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
         requires notBool inLevelE(L, O)
  ```
- L263 `rule` [owise-rule] attrs=owise

  ```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
      => evp(OO, appendIE(ON, CUR)) [owise]
  ```
- L265 `syntax` attrs=function,total

  ```k
  syntax Bool ::= inLevelE(String, String) [function, total]
  ```
- L266 `rule` [ordinary-rule]

  ```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
  ```
- L267 `rule` [ordinary-rule]

  ```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
  ```
- L268 `rule` [owise-rule] attrs=owise

  ```k
  rule inLevelE(_:String, _:String) => false [owise]
  ```
- L269 `syntax` attrs=function,total

  ```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
  ```
- L270 `rule` [ordinary-rule]

  ```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
  ```
- L271 `rule` [ordinary-rule]

  ```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
  ```
- L272 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
  ```
- L273 `rule` [ordinary-rule]

  ```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
  ```
- L274 `rule` [ordinary-rule]

  ```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
  
    // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
    // The md5 value itself is a named shared trust (sortVS-style, no concrete
    // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
  ```
- L279 `syntax`

  ```k
  syntax KItem ::= "#md5"
  ```
- L280 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
         [priority(40)]
  ```
- L282 `rule` [ordinary-rule]

  ```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
  ```
- L283 `syntax`

  ```k
  syntax Val ::= md5Obj(IntSeq)
  ```
- L284 `rule` [ordinary-rule]

  ```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
  ```
- L285 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
  
    // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
    // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
    // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
    // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
  ```
- L291 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
  ```
- L292 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
  ```
- L293 `syntax` attrs=function

  ```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
  ```
- L294 `rule` [ordinary-rule]

  ```k
  rule isIntV(_:Int)         => true
  ```
- L295 `rule` [owise-rule] attrs=owise

  ```k
  rule isIntV(_:Val)         => false [owise]
  ```
- L296 `rule` [ordinary-rule]

  ```k
  rule isStrV(str(_:IntSeq)) => true
  ```
- L297 `rule` [owise-rule] attrs=owise

  ```k
  rule isStrV(_:Val)         => false [owise]
  ```
- L298 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/call.k

Counts: endmodule=1, imports=3, module=1, rule=21, syntax=3

- L10 `module`
  `module MPY-CALL`
- L11 `imports`
  `imports MPY-METHODS`
- L12 `imports`
  `imports MPY-BUILTINS`
- L13 `imports`
  `imports MPY-FUNCTIONS`
- L16 `rule` [ordinary-rule]

  ```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
  
    // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
  ```
- L19 `syntax`

  ```k
  syntax KItem ::= #callee(Exprs)
  ```
- L20 `rule` [owise-rule] attrs=owise

  ```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
  ```
- L21 `rule` [ordinary-rule]

  ```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
  
    // ==== dispatch on the callee value ========================================
  ```
- L24 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
  ```
- L27 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
  ```
- L28 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
  ```
- L29 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
  ```
- L30 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
  ```
- L31 `rule` [owise-rule] attrs=owise

  ```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
  ```
- L32 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
  
    // ==== heap-object arguments/receivers =====================================
    // Builtins and type calls READ structure — deref the first two arg positions
    // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
    // methods take the ref itself; every other method receiver is deref'd.
  ```
- L38 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L42 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
          => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(A)
         [priority(40)]
  ```
- L47 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L52 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isMutMethod(String) [function, total]
  ```
- L53 `rule` [ordinary-rule]

  ```k
  rule isMutMethod(M:String)
      => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
         orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
  ```
- L56 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
          => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isMutMethod(M)
         [priority(40)]
    // non-mutating methods READ their heap-object arguments too (join's list);
    // mutators keep refs (append of a list into a list-of-lists stays aliased)
  ```
- L63 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
         [priority(40)]
  ```
- L69 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
          => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
         <env>     CALLERL:Int => NEWL </env>
         <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
         <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
         <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
  
    // annotated closure: the frame starts with the captured freevar cells, its
    // parent is the module scope (all enclosing-local reads go through cells),
    // and the cellvars' fresh cells allocate before params bind (a cellvar param
    // then writes through its cell in #bindP).
  ```
- L80 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
          => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
         <env>     CALLERL:Int => NEWL </env>
         <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
         <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
         <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
  ```
- L87 `syntax`

  ```k
  syntax KItem ::= #allocCells(ParamNames)
  ```
- L88 `rule` [ordinary-rule]

  ```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
  ```
- L89 `rule` [ordinary-rule]

  ```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
         <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
         <heapLoc> N:Int => N +Int 1 </heapLoc>
         requires notBool N in_keys(H)
  ```
- L95 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/comprehension.k

Counts: endmodule=1, imports=5, module=1, rule=7, syntax=3

- L3 `module`
  `module MPY-COMPREHENSION`
- L4 `imports`
  `imports MPY-CORE`
- L5 `imports`
  `imports MPY-OPERATORS`
- L6 `imports`
  `imports MPY-LIST`
- L7 `imports`
  `imports MPY-CONTROLS`
- L8 `imports`
  `imports MPY-FUNCTIONS`
- L11 `rule` [ordinary-rule]

  ```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
  ```
- L12 `rule` [ordinary-rule]

  ```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
  ```
- L14 `syntax` attrs=macro

  ```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
  ```
- L15 `rule` [ordinary-rule]

  ```k
  rule compBody(Gs:CompFors, ELT:Expr)
      => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
  ```
- L18 `syntax` attrs=macro

  ```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
  ```
- L19 `rule` [ordinary-rule]

  ```k
  rule compNest(.CompFors, ELT:Expr)
      => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
  ```
- L21 `rule` [ordinary-rule]

  ```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
      => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
  ```
- L24 `syntax` attrs=macro

  ```k
  syntax Expr ::= compGuard(Exprs) [macro]
  ```
- L25 `rule` [ordinary-rule]

  ```k
  rule compGuard(.Exprs)             => Bool(true)
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
  ```
- L27 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/concrete.k

Counts: endmodule=1, imports=1, module=1, rule=16, syntax=5

- L8 `module`
  `module MPY-CONCRETE`
- L9 `imports`
  `imports MPY`
- L13 `rule` [ordinary-rule]

  ```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
         <heap> HP:Map </heap>
         requires hasRefVS(A) orBool hasRefVS(B)
  ```
- L16 `rule` [ordinary-rule]

  ```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
         <heap> HP:Map </heap>
         requires hasRefVS(A) orBool hasRefVS(B)
  
    // ==== keyed sort, concrete leg ============================================
    // Computes each key by a REAL call through the uniform #callee machinery
    // (closures, len, type objects all work), stable-inserts on the key, and
    // allocates the result. priority(40) beats sort.k's opaque rules, so krun
    // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.
  ```
- L25 `syntax`

  ```k
  syntax Val ::= kvP(Val, Val)
  ```
- L26 `syntax`

  ```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                   | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
  ```
- L28 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
          => #ksort(VS, KV, .ValSeq, false) ... </k>
         [priority(40)]
  ```
- L31 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
          => #ksort(VS, KV, .ValSeq, RB) ... </k>
         [priority(40)]
  ```
- L34 `rule` [ordinary-rule]

  ```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
          => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
  ```
- L36 `rule` [ordinary-rule]

  ```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
          => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
  ```
- L38 `rule` [ordinary-rule]

  ```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
          => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
         requires notBool isKwV(K)
  ```
- L42 `syntax` attrs=function

  ```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
  ```
- L43 `rule` [ordinary-rule]

  ```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
  ```
- L44 `rule` [ordinary-rule]

  ```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
      => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
         requires kLt(K, K2)
  ```
- L47 `rule` [ordinary-rule]

  ```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
      => vCons(kvP(K2, V2), insPair(R, K, V))
         requires notBool kLt(K, K2)
  ```
- L51 `syntax` attrs=function

  ```k
  syntax Bool ::= kLt(Val, Val) [function]
  ```
- L52 `rule` [ordinary-rule]

  ```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
  ```
- L53 `rule` [ordinary-rule]

  ```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
  ```
- L54 `rule` [ordinary-rule]

  ```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
  ```
- L56 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
  ```
- L57 `rule` [ordinary-rule]

  ```k
  rule unpairVS(.ValSeq) => .ValSeq
  ```
- L58 `rule` [ordinary-rule]

  ```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
  ```
- L59 `rule` [owise-rule] attrs=owise

  ```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
  ```
- L60 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/controls.k

Counts: endmodule=1, imports=3, module=1, requires=1, rule=34, syntax=3

- L3 `module`
  `module MPY-CONTROLS`
- L4 `imports`
  `imports MPY-CORE`
- L5 `imports`
  `imports MPY-TUPLE`
- L6 `imports`
  `imports MPY-ITER`
- L9 `rule` [ordinary-rule]

  ```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
  ```
- L12 `rule` [ordinary-rule]

  ```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
  ```
- L15 `requires`
  `requires "$cells" in_keys(M)`
- L20 `rule` [ordinary-rule]

  ```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
         requires X in_keys(M)
    // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
    // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
    // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
  ```
- L27 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires X in_keys(M) andBool isRefV({M[X]}:>Val)
         [priority(40)]
  
    // ==== import trivia: `from math import floor, ceil` binds the supported
    // names as builtins in the current scope; every other import is a no-op
  ```
- L35 `rule` [ordinary-rule]

  ```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
  ```
- L36 `rule` [owise-rule] attrs=owise

  ```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
  ```
- L37 `syntax`

  ```k
  syntax KItem ::= #bindImports(ParamNames)
  ```
- L38 `rule` [ordinary-rule]

  ```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
         requires N ==String "floor" orBool N ==String "ceil"
  ```
- L43 `rule` [ordinary-rule]

  ```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
         requires notBool (N ==String "floor" orBool N ==String "ceil")
  
    // ==== Expr statement: evaluate for effect, discard the value ===============
    // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
  ```
- L48 `rule` [ordinary-rule]

  ```k
  rule <k> Expr(_:Val) => .K ... </k>
  
    // ==== If (condition evaluated by strictness) ==============================
  ```
- L51 `syntax`

  ```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
  ```
- L52 `rule` [ordinary-rule]

  ```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
  ```
- L53 `rule` [ordinary-rule]

  ```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
  ```
- L54 `rule` [ordinary-rule]

  ```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
  
    // ==== IfExp: ternary T if C else E ========================================
  ```
- L57 `rule` [ordinary-rule]

  ```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
         requires truthy(V)
  ```
- L59 `rule` [ordinary-rule]

  ```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
         requires notBool truthy(V)
  
    // ==== For: one loop, in-cell continuation, over #iterNext =================
    // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
    // circularities anchor on #loop and narrowing substitutes the structure)
  ```
- L65 `syntax`

  ```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                   | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                   | #loopLbl(K) | "#cont" | "#brk"
  ```
- L69 `rule` [ordinary-rule]

  ```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
  ```
- L71 `rule` [ordinary-rule]

  ```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
  ```
- L72 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
  ```
- L73 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
          => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
  
    // ==== While ==============================================================
  ```
- L77 `rule` [ordinary-rule]

  ```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
  ```
- L78 `rule` [ordinary-rule]

  ```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
  ```
- L79 `rule` [ordinary-rule]

  ```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
         requires truthy(V)
  ```
- L81 `rule` [ordinary-rule]

  ```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
         requires notBool truthy(V)
  
    // ==== loop control (break / continue) =====================================
  ```
- L85 `rule` [ordinary-rule]

  ```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
  ```
- L86 `rule` [ordinary-rule]

  ```k
  rule <k> Continue => #cont ... </k>
  ```
- L87 `rule` [ordinary-rule]

  ```k
  rule <k> Break => #brk ... </k>
  ```
- L88 `rule` [ordinary-rule]

  ```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
  ```
- L89 `rule` [owise-rule] attrs=owise

  ```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
  ```
- L90 `rule` [ordinary-rule]

  ```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
  ```
- L91 `rule` [owise-rule] attrs=owise

  ```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
  
    // ==== heap-object deref at the truthiness/iteration consumers ==============
    // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
  ```
- L95 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L98 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L101 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
    // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
    // mutating the iterated list inside its own loop is outside the subset)
  ```
- L106 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L109 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/core.k

Counts: configuration=1, endmodule=1, imports=7, module=1, requires=1, rule=46, syntax=37

- L3 `module`
  `module MPY-CORE`
- L4 `imports`
  `imports MPY-SYNTAX`
- L5 `imports`
  `imports INT`
- L6 `imports`
  `imports BOOL`
- L7 `imports`
  `imports STRING`
- L8 `imports`
  `imports MAP`
- L9 `imports`
  `imports LIST`
- L10 `imports`
  `imports K-EQUAL`
- L13 `syntax`

  ```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  ```
- L14 `syntax`

  ```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
  ```
- L15 `syntax`

  ```k
  syntax Str    ::= str(IntSeq)
  
    // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
  ```
- L18 `syntax`

  ```k
  syntax Iterable ::= list(ValSeq)
                      | tuple(ValSeq)
                      | Str
                      | rangeObj(Int, Int, Int)
                      | zipObj(ValSeq, ValSeq)
                      | zipObjS(IntSeq, IntSeq)
  ```
- L25 `syntax`

  ```k
  syntax Val      ::= Int
                      | Bool
                      | "noneV"
                      | Iterable
                      | ref(Int)          // a heap object: <heap> holds its list(VS)
                      | cellRef(Int)      // a closure cell: <heap> holds cellV(V)
                      | closureVal(ParamNames, Stmts, Int)
                      | typeV(String)     // a type object (int/str), resolved from the builtins frame
                      | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough)
                      | boundMethodV(Val, String)   // a cooled Attribute: obj.method
  ```
- L36 `syntax`

  ```k
  syntax Parent   ::= "root" | parent(Int)
  ```
- L37 `syntax`

  ```k
  syntax Scope    ::= scope(Map, Parent)
  ```
- L38 `syntax`

  ```k
  syntax KResult  ::= Val
  ```
- L39 `syntax`

  ```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
  ```
- L40 `syntax`

  ```k
  syntax Vals     ::= List{Val, ","}
  ```
- L41 `syntax`

  ```k
  syntax Exc      ::= "NoExc" | "AssertionError"
  ```
- L42 `syntax`

  ```k
  syntax RetState ::= "noRet" | retV(Val)
  
    // ==== configuration =======================================================
    // The builtins namespace is a real scope at reserved location -1 (the bottom of every
    // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
    // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
    // resolve to their type objects; any local/global binding shadows them via normal lookup.
  ```
- L49 `configuration`

  ```k
  configuration
      <k>       #loadAll($PGM:Module) </k>
      <env>     0 </env>
      <scopes>   0     |-> scope(.Map, parent(-1))
                -1    |-> builtinsScope </scopes>
      <scopeLoc> 1 </scopeLoc>
      <heap>    .Map </heap>
      <heapLoc> 0 </heapLoc>
      <stack>   .List </stack>
      <ret>     noRet </ret>
      <exc>     NoExc </exc>
      <exit-code exit=""> 0 </exit-code>
  
    // ==== heap allocation (constructed lists become objects) ==================
    // Cons-form emission with a freshness guard (the heap-list-probe discipline:
    // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is
    // monotonic — it does NOT wind back at #pop: returned lists escape by ref.
    // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed);
    // only CONSTRUCTORS in program syntax allocate.
  ```
- L68 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isRefV(Val) [function, total]
  ```
- L69 `rule` [ordinary-rule]

  ```k
  rule isRefV(ref(_:Int)) => true
  ```
- L70 `rule` [owise-rule] attrs=owise

  ```k
  rule isRefV(_:Val)      => false [owise]
  
    // closure cells (Python-faithful capture): the heap holds cellV(V); a
    // cellRef surfacing as the k-redex reads through (lookup is the only use —
    // cellRefs never escape to user-visible values)
  ```
- L75 `syntax`

  ```k
  syntax HeapVal ::= cellV(Val)
  ```
- L76 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isCellRef(Val) [function, total]
  ```
- L77 `rule` [ordinary-rule]

  ```k
  rule isCellRef(cellRef(_:Int)) => true
  ```
- L78 `rule` [owise-rule] attrs=owise

  ```k
  rule isCellRef(_:Val)          => false [owise]
    // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
    // (AugAssign's in-place read and friends). The "$cells" guard keeps this
    // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
    // prover narrow abstract k-top values into cellRef junk (probed on
    // 26-remove-duplicates). Cross-frame reads (a comprehension closure
    // reading the enclosing function's cellvar) deref inside #look instead.
  ```
- L85 `rule` [ordinary-rule]

  ```k
  rule <k> cellRef(H:Int) => V ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         <heap> ... H |-> cellV(V:Val) ... </heap>
  ```
- L89 `requires`
  `requires "$cells" in_keys(M)`
- L95 `syntax`

  ```k
  syntax Val ::= kwV(String, Val)
  ```
- L96 `syntax`

  ```k
  syntax KItem ::= #kwTag(String)
  ```
- L97 `rule` [ordinary-rule]

  ```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
  ```
- L98 `rule` [ordinary-rule]

  ```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
         requires notBool isKwV(V)
  ```
- L100 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isKwV(Val) [function, total]
  ```
- L101 `rule` [ordinary-rule]

  ```k
  rule isKwV(kwV(_:String, _:Val)) => true
  ```
- L102 `rule` [owise-rule] attrs=owise

  ```k
  rule isKwV(_:Val)                => false [owise]
  
    // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
    // decides by pnMember even over an abstract frame rest (no prover branching)
  ```
- L106 `syntax`

  ```k
  syntax Val ::= cellsMark(ParamNames)
  ```
- L107 `syntax` attrs=function

  ```k
  syntax ParamNames ::= cellsOf(Val) [function]
  ```
- L108 `rule` [ordinary-rule]

  ```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
  ```
- L109 `syntax` attrs=function,total

  ```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
  ```
- L110 `rule` [ordinary-rule]

  ```k
  rule pnMember(_:String, .ParamNames) => false
  ```
- L111 `rule` [ordinary-rule]

  ```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
  ```
- L113 `syntax`

  ```k
  syntax KItem ::= #cellW(Val, Val)
  ```
- L114 `rule` [ordinary-rule]

  ```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
         <heap> ... H |-> cellV(_:Val => V) ... </heap>
  ```
- L117 `syntax`

  ```k
  syntax KItem ::= #alloc(Val)
  ```
- L118 `rule` [ordinary-rule]

  ```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
         <heap>    H:Map => (N |-> V) H </heap>
         <heapLoc> N:Int => N +Int 1 </heapLoc>
         requires notBool N in_keys(H)
  
    // ==== module load + statement sequencing ==================================
  ```
- L124 `syntax`

  ```k
  syntax KItem ::= #loadAll(Module)
  ```
- L125 `rule` [ordinary-rule]

  ```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
  ```
- L126 `rule` [ordinary-rule]

  ```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
  ```
- L127 `rule` [ordinary-rule]

  ```k
  rule <k> .Stmts => .K ... </k>
  
    // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
  ```
- L130 `syntax`

  ```k
  syntax KItem ::= #look(String, Int)
  ```
- L131 `rule` [ordinary-rule]

  ```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
  ```
- L132 `rule` [ordinary-rule]

  ```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
         <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
         requires X in_keys(M)
    // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE
    // LOOKUP (higher priority beats the plain return above on concrete cell
    // bindings; abstract claim values take the plain rule unchanged) — this
    // covers cross-frame cell reads (a comprehension closure reading the
    // enclosing function's cellvar) without a narrowing-prone k-top redex
    // guarded on the FOUND frame's DECLARED cellvars (pnMember over the
    // cellsMark): decidable for every concrete frame pin — plain frames and
    // non-cell names prune outright, so an abstract looked-up value never
    // drags a narrowing cellV heap match along (probed on 5-intersperse and
    // Q4's abstract `numbers` in the annotated frame)
  ```
- L145 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #look(X:String, L:Int) => V ... </k>
         <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
         <heap> ... H |-> cellV(V:Val) ... </heap>
         requires X in_keys(M) andBool "$cells" in_keys(M)
          andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
          andBool {M[X]}:>Val ==K cellRef(H)
         [priority(40)]
  ```
- L152 `rule` [ordinary-rule]

  ```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
         <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
         requires notBool (X in_keys(M))
  
    // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
  ```
- L157 `syntax` attrs=function,total

  ```k
  syntax Scope ::= "builtinsScope" [function, total]
  ```
- L158 `rule` [ordinary-rule]

  ```k
  rule builtinsScope
      => scope(.Map [ "len"    <- builtinV("len")    ]
                    [ "set"    <- builtinV("set")    ]
                    [ "sum"    <- builtinV("sum")    ]
                    [ "abs"    <- builtinV("abs")    ]
                    [ "min"    <- builtinV("min")    ]
                    [ "max"    <- builtinV("max")    ]
                    [ "ord"    <- builtinV("ord")    ]
                    [ "chr"    <- builtinV("chr")    ]
                    [ "range"  <- builtinV("range")  ]
                    [ "all"    <- builtinV("all")    ]
                    [ "any"    <- builtinV("any")    ]
                    [ "zip"    <- builtinV("zip")    ]
                    [ "isinstance" <- builtinV("isinstance") ]
                    [ "sorted" <- builtinV("sorted") ]
                    [ "list"   <- builtinV("list")   ]
                    [ "round"  <- builtinV("round")  ]
                    [ "bin"    <- builtinV("bin")    ]
                    [ "enumerate" <- builtinV("enumerate") ]
                    [ "map"    <- builtinV("map")    ]
                    [ "eval"   <- builtinV("eval")   ]
                    [ "int"    <- typeV("int")       ]
                    [ "str"    <- typeV("str")       ]
                    [ "float"  <- typeV("float")     ], root)
  
    // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination ==
    // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)
  ```
- L185 `syntax`

  ```k
  syntax ApplyK ::= toCall(Val)
  ```
- L186 `syntax`

  ```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                    | #evalArgCont(Exprs, Vals, ApplyK)
                    | #applyK(ApplyK, Vals)
  ```
- L189 `rule` [ordinary-rule]

  ```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
  ```
- L190 `rule` [ordinary-rule]

  ```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
  ```
- L191 `rule` [ordinary-rule]

  ```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
  
    // ==== Int / Bool / None literals ==========================================
  ```
- L194 `rule` [ordinary-rule]

  ```k
  rule <k> Int(I:Int)   => I ... </k>
  ```
- L195 `rule` [ordinary-rule]

  ```k
  rule <k> Bool(B:Bool) => B ... </k>
  ```
- L196 `rule` [ordinary-rule]

  ```k
  rule <k> NoneVal      => noneV ... </k>
  
    // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
  ```
- L199 `syntax` attrs=function

  ```k
  syntax Bool ::= truthy(Val) [function]
  ```
- L200 `rule` [ordinary-rule]

  ```k
  rule truthy(B:Bool)          => B
  ```
- L201 `rule` [ordinary-rule]

  ```k
  rule truthy(noneV)           => false
  ```
- L202 `rule` [ordinary-rule]

  ```k
  rule truthy(I:Int)           => I =/=Int 0
  ```
- L203 `rule` [ordinary-rule]

  ```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
  ```
- L204 `rule` [ordinary-rule]

  ```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
  ```
- L205 `rule` [ordinary-rule]

  ```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
  
    // ==== extensible operator dispatch (cases added by the construct modules) ==
  ```
- L208 `syntax` attrs=function

  ```k
  syntax Val  ::= applyUn(String, Val) [function]
  ```
- L209 `syntax` attrs=function

  ```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
  ```
- L210 `syntax` attrs=function

  ```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
  
    // ==== shared list helpers =================================================
  ```
- L213 `syntax` attrs=function,total

  ```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
  ```
- L214 `rule` [ordinary-rule]

  ```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
  ```
- L215 `rule` [ordinary-rule]

  ```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
  ```
- L217 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
  ```
- L218 `rule` [ordinary-rule]

  ```k
  rule vals2valSeq(.Vals)            => .ValSeq
  ```
- L219 `rule` [ordinary-rule]

  ```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
  
    // ==== shared sequence length (len / summaries across many modules) ========
    // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
  ```
- L223 `syntax` attrs=function,total

  ```k
  syntax Int ::= vsLen(ValSeq) [function, total]
  ```
- L224 `rule` [ordinary-rule]

  ```k
  rule vsLen(.ValSeq)                => 0
  ```
- L225 `rule` [ordinary-rule]

  ```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
  ```
- L227 `syntax` attrs=function,total

  ```k
  syntax Int ::= isLen(IntSeq) [function, total]
  ```
- L228 `rule` [ordinary-rule]

  ```k
  rule isLen(.IntSeq)                => 0
  ```
- L229 `rule` [ordinary-rule]

  ```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
  
    // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
    // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
  ```
- L233 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
  ```
- L234 `rule` [ordinary-rule]

  ```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
  ```
- L235 `rule` [ordinary-rule]

  ```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
  ```
- L236 `rule` [ordinary-rule]

  ```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
         requires I >Int 0
  ```
- L238 `rule` [ordinary-rule]

  ```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
         requires I <Int 0
  ```
- L240 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/dict.k

Counts: endmodule=1, imports=4, module=1, rule=28, syntax=12

- L13 `module`
  `module MPY-DICT`
- L14 `imports`
  `imports MPY-CORE`
- L15 `imports`
  `imports MPY-ITER`
- L16 `imports`
  `imports MPY-METHODS`
- L17 `imports`
  `imports MPY-LIST`
- L20 `syntax`

  ```k
  syntax Val ::= dictV(ValSeq, ValSeq)
  
    // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
  ```
- L23 `syntax`

  ```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                   | #dictKey(Expr, Entries, ValSeq, ValSeq)
                   | #dictVal(Val, Entries, ValSeq, ValSeq)
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
  ```
- L27 `rule` [ordinary-rule]

  ```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
  ```
- L28 `rule` [ordinary-rule]

  ```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
          => K ~> #dictKey(V, REST, KS, VS) ... </k>
  ```
- L30 `rule` [ordinary-rule]

  ```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
          => V ~> #dictVal(KV, REST, KS, VS) ... </k>
  ```
- L32 `rule` [ordinary-rule]

  ```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
          => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
  
    // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
    // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
  ```
- L37 `syntax` attrs=function,total

  ```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
  ```
- L38 `rule` [ordinary-rule]

  ```k
  rule dHasKey(.ValSeq, _:Val)                => false
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
  ```
- L40 `rule` [ordinary-rule]

  ```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
  
    // dPutK: KS unchanged if K already present, else append K (keep-first-position).
  ```
- L43 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
  ```
- L44 `rule` [ordinary-rule]

  ```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
  ```
- L45 `rule` [ordinary-rule]

  ```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
  
    // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
    // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
  ```
- L49 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
  ```
- L50 `rule` [ordinary-rule]

  ```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
         requires A ==K K
  ```
- L52 `rule` [ordinary-rule]

  ```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
         requires notBool (A ==K K)
  ```
- L54 `rule` [owise-rule] attrs=owise

  ```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
  
    // ==== dict methods ========================================================
    // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
  ```
- L58 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
          => #alloc(list(KS)) ... </k>
         [priority(40)]
  
    // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
  ```
- L63 `rule` [ordinary-rule]

  ```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
  ```
- L64 `syntax` attrs=function

  ```k
  syntax Val ::= applyIndexD(Val, Val) [function]
  ```
- L65 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
         [priority(45)]
  
    // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
    // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
  ```
- L70 `syntax` attrs=function

  ```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
  ```
- L71 `rule` [ordinary-rule]

  ```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
  
    // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
    // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
    // list — or a heap dict later) writes the heap in place.
  ```
- L76 `syntax`

  ```k
  syntax KItem ::= #dsetK(String, Val)
  ```
- L77 `rule` [ordinary-rule]

  ```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
  ```
- L78 `rule` [ordinary-rule]

  ```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
         requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
  ```
- L82 `rule` [ordinary-rule]

  ```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires X in_keys(M) andBool isRefV({M[X]}:>Val)
  ```
- L86 `syntax`

  ```k
  syntax KItem ::= #dsetV(Val, Val, Val)
  ```
- L87 `rule` [ordinary-rule]

  ```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
         <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
    // negative-index normalization local to the write (subscript.k's is not imported here)
  ```
- L90 `syntax` attrs=function,total

  ```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
  ```
- L91 `rule` [ordinary-rule]

  ```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
  ```
- L92 `rule` [ordinary-rule]

  ```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
  
    // ==== dict == (order-insensitive: same size + same key->value pairs) =======
  ```
- L95 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
      => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
  ```
- L97 `syntax` attrs=function

  ```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
  ```
- L98 `rule` [ordinary-rule]

  ```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
  ```
- L99 `rule` [ordinary-rule]

  ```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
      => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
  ```
- L101 `syntax` attrs=function

  ```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
  ```
- L102 `rule` [ordinary-rule]

  ```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
  ```
- L103 `rule` [ordinary-rule]

  ```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
  ```
- L104 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/float.k

Counts: endmodule=1, imports=3, module=1, rule=121, syntax=34

- L14 `module`
  `module MPY-FLOAT`
- L15 `imports`
  `imports MPY-OPERATORS`
- L16 `imports`
  `imports MPY-BUILTINS`
- L17 `imports`
  `imports FLOAT`
- L20 `syntax`

  ```k
  syntax Val ::= Float
  ```
- L21 `rule` [ordinary-rule]

  ```k
  rule <k> Float(F:Float) => F ... </k>
  
    // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
  ```
- L24 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
  ```
- L25 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
  ```
- L27 `rule` [ordinary-rule]

  ```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
  
    // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
  ```
- L30 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
  ```
- L31 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
  ```
- L32 `rule` [ordinary-rule]

  ```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
  
    // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
    // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
    // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
  ```
- L37 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
  ```
- L38 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
  
    // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
    // concrete floats. kprove proofs return floats structurally and do not compare them.
  ```
- L43 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
  ```
- L44 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
  
    // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
    // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
    // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
    // `abs(a-b) < t` proximity test.)
  ```
- L50 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
  ```
- L51 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
  ```
- L52 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
  ```
- L54 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
  ```
- L55 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule absF(F:Float) => absFloat(F) [concrete]
  ```
- L56 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
  
    // ==== math.ceil ===========================================================
    // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
    // never bound as a value).
  ```
- L61 `rule` [ordinary-rule]

  ```k
  rule <k> Import(_:String) => .K ... </k>
  
    // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
    // priority than the generic Attribute/method dispatch in call.k).
  ```
- L65 `syntax`

  ```k
  syntax KItem ::= "#mathCeil"
  ```
- L66 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
  ```
- L67 `rule` [ordinary-rule]

  ```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
  
    // math.floor(x) — same interception shape as math.ceil
  ```
- L70 `syntax`

  ```k
  syntax KItem ::= "#mathFloor"
  ```
- L71 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
  ```
- L72 `rule` [ordinary-rule]

  ```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
  ```
- L73 `syntax` attrs=function,total,symbol

  ```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
  ```
- L74 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule floorFI(I:Int)   => I                        [concrete]
  ```
- L75 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
  
    // bare floor/ceil (bound by `from math import floor, ceil`)
  ```
- L78 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
  ```
- L79 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
  
    // math.pow(x, y) — a two-arg interception onto powF (ints promote)
  ```
- L82 `syntax`

  ```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
  ```
- L83 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
  ```
- L84 `rule` [ordinary-rule]

  ```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
  ```
- L85 `rule` [ordinary-rule]

  ```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
  ```
- L86 `syntax` attrs=function,total,symbol

  ```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
  ```
- L87 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule toF(F:Float) => F        [concrete]
  ```
- L88 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule toF(I:Int)   => intToF(I) [concrete]
  
    // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
    // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
    // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
  ```
- L93 `syntax` attrs=function,total,symbol

  ```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
  ```
- L94 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule ceilF(I:Int)   => I                       [concrete]
  ```
- L95 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
  
    // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
    // proofs use symbolic elements, never a float literal.
  ```
- L99 `rule` [ordinary-rule]

  ```k
  rule applyUn("-", F:Float) => 0.0 -Float F
  
    // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
    // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
  ```
- L103 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
  ```
- L104 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
  ```
- L105 `rule` [ordinary-rule]

  ```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
  ```
- L107 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
  ```
- L108 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
  ```
- L109 `rule` [ordinary-rule]

  ```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
  ```
- L111 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
  ```
- L112 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
  ```
- L113 `rule` [ordinary-rule]

  ```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
  ```
- L115 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
  ```
- L116 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
  ```
- L117 `rule` [ordinary-rule]

  ```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
  ```
- L119 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
  ```
- L120 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
  ```
- L121 `rule` [ordinary-rule]

  ```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
  
    // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
    //      case-split on the atom; >= / <= derive from the two opaque compares) ----
  ```
- L125 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
  ```
- L126 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
  ```
- L127 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
  ```
- L128 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
  ```
- L129 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
  
    // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
  ```
- L132 `rule` [ordinary-rule]

  ```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
  ```
- L133 `rule` [ordinary-rule]

  ```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
  ```
- L134 `rule` [ordinary-rule]

  ```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
  ```
- L135 `rule` [ordinary-rule]

  ```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
  ```
- L136 `rule` [ordinary-rule]

  ```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
  ```
- L137 `rule` [ordinary-rule]

  ```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
  ```
- L138 `rule` [ordinary-rule]

  ```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
  ```
- L139 `rule` [ordinary-rule]

  ```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
  
    // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
  ```
- L142 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
  ```
- L143 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
  ```
- L144 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
  ```
- L145 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
  ```
- L146 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
  ```
- L147 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
  ```
- L148 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
  ```
- L149 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
  ```
- L150 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
  ```
- L151 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
  
    // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
  ```
- L154 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
  ```
- L155 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
  
    // ---- float(str): decimal parse (promoted from 137's defined chain) ----
    // digits '.' digits, optional leading '-'; concrete evaluation only (the
    // symbolic side stays an opaque decStrToF term a proof case-splits on).
  ```
- L160 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
  ```
- L161 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
  ```
- L162 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule decStrToF(CS:IntSeq)
      => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
         requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
  ```
- L165 `syntax` attrs=function

  ```k
  syntax Int ::= headIS(IntSeq) [function]
  ```
- L166 `rule` [ordinary-rule]

  ```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
  ```
- L167 `syntax` attrs=function,total

  ```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
  ```
- L168 `rule` [ordinary-rule]

  ```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
  ```
- L169 `rule` [ordinary-rule]

  ```k
  rule intPartAcc(.IntSeq, A:Int) => A
  ```
- L170 `rule` [ordinary-rule]

  ```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
  ```
- L171 `rule` [ordinary-rule]

  ```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
         requires C =/=Int 46
  ```
- L173 `syntax` attrs=function,total

  ```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
  ```
- L174 `rule` [ordinary-rule]

  ```k
  rule fracPart(.IntSeq) => 0
  ```
- L175 `rule` [ordinary-rule]

  ```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
  ```
- L176 `rule` [ordinary-rule]

  ```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
  ```
- L177 `rule` [ordinary-rule]

  ```k
  rule fracAcc(.IntSeq, A:Int) => A
  ```
- L178 `rule` [ordinary-rule]

  ```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
  ```
- L179 `syntax` attrs=function,total

  ```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
  ```
- L180 `rule` [ordinary-rule]

  ```k
  rule fracScale(.IntSeq) => 1
  ```
- L181 `rule` [ordinary-rule]

  ```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
  ```
- L182 `rule` [ordinary-rule]

  ```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
  ```
- L183 `rule` [ordinary-rule]

  ```k
  rule fscAcc(.IntSeq, A:Int) => A
  ```
- L184 `rule` [ordinary-rule]

  ```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
  ```
- L185 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
  ```
- L186 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
  ```
- L187 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
  
    // ---- float / int division (promoted from mean_absolute_deviation) ----
  ```
- L190 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
  ```
- L191 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
  ```
- L192 `rule` [ordinary-rule]

  ```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
  
    // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
  ```
- L195 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
  ```
- L196 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
  ```
- L197 `rule` [ordinary-rule]

  ```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
  ```
- L198 `rule` [ordinary-rule]

  ```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
  ```
- L199 `rule` [ordinary-rule]

  ```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
  ```
- L200 `rule` [ordinary-rule]

  ```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
  ```
- L201 `rule` [ordinary-rule]

  ```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
  ```
- L202 `rule` [ordinary-rule]

  ```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
  ```
- L203 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
  ```
- L204 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
  ```
- L205 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
  ```
- L206 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
  
    // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
  ```
- L209 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
  ```
- L210 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
  ```
- L211 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
  ```
- L213 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
  ```
- L214 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("float", F:Float, .Vals) => F
  
    // round: Python half-even (banker's); round(F, N) scales by 10^N
  ```
- L217 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
  ```
- L218 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule roundF(F:Float)
      => #if (F -Float floorFloat(F)) ==Float 0.5
         #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
                #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
         #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
  ```
- L223 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
  ```
- L224 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule roundFN(F:Float, N:Int)
      => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
         /Float Int2Float(10 ^Int N, 53, 11) [concrete]
  ```
- L227 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
  ```
- L228 `rule` [ordinary-rule]

  ```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
  ```
- L230 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
  ```
- L231 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
  ```
- L232 `syntax`

  ```k
  syntax KItem ::= "#mathSqrt"
  ```
- L233 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
  ```
- L234 `rule` [ordinary-rule]

  ```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
  ```
- L235 `rule` [ordinary-rule]

  ```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
  
    // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
    // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
    // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
    // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
    // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
    // the isFloat guard is disjoint from the existing isInt one.
  ```
- L243 `syntax`

  ```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
  ```
- L244 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
  ```
- L245 `rule` [ordinary-rule]

  ```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
  ```
- L246 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
  ```
- L247 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```
- L250 `syntax`

  ```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
  ```
- L251 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
  ```
- L252 `rule` [ordinary-rule]

  ```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
  ```
- L253 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
  ```
- L254 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
         requires isFloat(V)
  
    // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
    // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
    // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
    // with isInt(V) in its path condition refutes this branch without sort reasoning.
  ```
- L261 `syntax`

  ```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
  ```
- L262 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
          => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
         requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
  ```
- L265 `rule` [ordinary-rule]

  ```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
  ```
- L266 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
  ```
- L267 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
          => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```
- L270 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
          => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
         requires isInt(V) orBool isBool(V)
  ```
- L273 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/functions.k

Counts: endmodule=1, imports=1, module=1, requires=1, rule=15, syntax=4

- L3 `module`
  `module MPY-FUNCTIONS`
- L4 `imports`
  `imports MPY-CORE`
- L8 `syntax`

  ```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                   | #bindP(ParamNames, Vals)
                   | "#pop"
                   | "#endcall"
  
    // ==== def / anonymous closure =============================================
  ```
- L14 `rule` [ordinary-rule]

  ```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
  ```
- L18 `syntax`

  ```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
  ```
- L19 `rule` [ordinary-rule]

  ```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
         <env> L:Int </env>
  
    // ==== annotated def/lambda (closure cells; spec 2.3) ======================
    // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
    // enclosing-local reads are freevars (symtable-complete) and go through the
    // captured cells; everything else is global/builtin, so the callee frame's
    // parent is the module scope (0) — sound after the defining frame dies.
  ```
- L27 `syntax`

  ```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
  
    // capture: resolve each freevar to the enclosing frame's cellRef, then bind
    // (FuncDef) or yield (Lambda) the closure value.
  ```
- L31 `syntax`

  ```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                   | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
  ```
- L33 `rule` [ordinary-rule]

  ```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                     FreeVars(FVS:ParamNames), BODY:Stmts)
          => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
  ```
- L36 `rule` [ordinary-rule]

  ```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                        (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
          => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires FV in_keys(M)
  ```
- L42 `rule` [ordinary-rule]

  ```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                        .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
  ```
- L47 `rule` [ordinary-rule]

  ```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
          => closureVal(PNS, Return(E) .Stmts, L) ... </k>
         <env> L:Int </env>
  ```
- L50 `rule` [ordinary-rule]

  ```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                    FreeVars(FVS:ParamNames), E:Expr)
          => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
  ```
- L53 `rule` [ordinary-rule]

  ```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                       (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
          => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires FV in_keys(M)
  ```
- L59 `rule` [ordinary-rule]

  ```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
          => closureValC(PNS, CVS, BODY, CM) ... </k>
  
    // ==== bind params ========================================================
  ```
- L63 `rule` [ordinary-rule]

  ```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
  ```
- L64 `rule` [ordinary-rule]

  ```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
    // a param that is a cellvar was pre-bound to its cell at frame entry
  ```
- L68 `rule` [ordinary-rule]

  ```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
          => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
  ```
- L72 `requires`
  `requires "$cells" in_keys(M)`
- L78 `rule` [ordinary-rule]

  ```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
         <ret> noRet => retV(V) </ret>
  ```
- L80 `rule` [ordinary-rule]

  ```k
  rule <k> #endcall => #pop ... </k>
         <ret> noRet => retV(noneV) </ret>
    // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
    // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
    // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
  ```
- L85 `rule` [ordinary-rule]

  ```k
  rule <k> #pop => V ~> CONT </k>
         <ret>   retV(V) => noRet </ret>
         <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
         <env>   L:Int => CALLERL </env>
         <scopes> SC:Map => SC [ L <- undef ] </scopes>
         <scopeLoc> _ => SAVEDL </scopeLoc>
  ```
- L91 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/int.k

Counts: endmodule=1, imports=1, module=1, rule=16, syntax=1

- L4 `module`
  `module MPY-INT`
- L5 `imports`
  `imports MPY-CORE`
- L7 `rule` [ordinary-rule]

  ```k
  rule applyUn("-", I:Int) => 0 -Int I
  ```
- L9 `rule` [ordinary-rule]

  ```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
    // Bool participates in int arithmetic (x += (a == b))
  ```
- L11 `rule` [ordinary-rule]

  ```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
  ```
- L12 `rule` [ordinary-rule]

  ```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
  ```
- L13 `rule` [ordinary-rule]

  ```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
  ```
- L14 `rule` [ordinary-rule]

  ```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
  ```
- L15 `rule` [ordinary-rule]

  ```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
  ```
- L16 `rule` [ordinary-rule]

  ```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
  ```
- L17 `rule` [ordinary-rule]

  ```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
  ```
- L19 `syntax` attrs=function

  ```k
  syntax Int ::= pyMod(Int, Int) [function]
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
  ```
- L22 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
  ```
- L23 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
  ```
- L24 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
  ```
- L25 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
  ```
- L27 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
  ```
- L28 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/iter.k

Counts: endmodule=1, imports=1, module=1, syntax=1

- L6 `module`
  `module MPY-ITER`
- L7 `imports`
  `imports MPY-CORE`
- L8 `syntax`

  ```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
  ```
- L9 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/list.k

Counts: endmodule=1, imports=3, module=1, rule=27, syntax=5

- L3 `module`
  `module MPY-LIST`
- L4 `imports`
  `imports MPY-CORE`
- L5 `imports`
  `imports MPY-ITER`
- L6 `imports`
  `imports MPY-OPERATORS`
- L9 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
  ```
- L10 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
  
    // ==== ListExpr: [...] literal -> a fresh heap object =======================
  ```
- L13 `syntax`

  ```k
  syntax ApplyK ::= "toList"
  ```
- L14 `rule` [ordinary-rule]

  ```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
  ```
- L15 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
  
    // ==== list ops: + / == / != ===============================================
  ```
- L18 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
  ```
- L19 `rule` [ordinary-rule]

  ```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
  
    // list + list constructs a NEW object (k-cell — it allocates; operands land here
    // already deref'd). priority(45) beats the generic BinOp dispatch.
  ```
- L24 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
         [priority(45)]
  ```
- L27 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
  ```
- L28 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
  
    // ==== deep equality when elements are heap objects (list-of-lists) ========
    // Python == is structural at every depth. Fires ONLY when a ref is present
    // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
  ```
- L33 `syntax` attrs=function,total

  ```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
  ```
- L34 `rule` [ordinary-rule]

  ```k
  rule hasRefVS(.ValSeq)                => false
  ```
- L35 `rule` [ordinary-rule]

  ```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
  ```
- L37 `syntax` attrs=function

  ```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                  | deepEqV(Val, Val, Map)        [function]
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
  ```
- L40 `rule` [ordinary-rule]

  ```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
  ```
- L41 `rule` [ordinary-rule]

  ```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
  ```
- L42 `rule` [ordinary-rule]

  ```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
      => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
  ```
- L45 `rule` [ordinary-rule]

  ```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
         requires H in_keys(HP)
  ```
- L47 `rule` [ordinary-rule]

  ```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
         requires notBool isRefV(A) andBool H in_keys(HP)
  ```
- L49 `rule` [ordinary-rule]

  ```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
  ```
- L50 `rule` [owise-rule] attrs=owise

  ```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
  
    // ==== mutator: xs.append(v) — an in-place heap write ======================
  ```
- L53 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
         <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
         [priority(40)]
  
    // ==== `x in list` — a <k>-cell fold over #iterNext ========================
  ```
- L58 `syntax`

  ```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
  ```
- L59 `rule` [ordinary-rule]

  ```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
  ```
- L60 `rule` [ordinary-rule]

  ```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
  ```
- L61 `rule` [ordinary-rule]

  ```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
  ```
- L62 `rule` [ordinary-rule]

  ```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
  ```
- L63 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
         requires E ==K V
  ```
- L65 `rule` [ordinary-rule]

  ```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
         requires notBool (E ==K V)
  ```
- L67 `rule` [ordinary-rule]

  ```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
  ```
- L68 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/methods.k

Counts: endmodule=1, imports=4, module=1, rule=75, syntax=27

- L3 `module`
  `module MPY-METHODS`
- L4 `imports`
  `imports MPY-CORE`
- L5 `imports`
  `imports K-EQUAL`
- L6 `imports`
  `imports MPY-STR`
- L7 `imports`
  `imports MPY-LIST`
- L10 `syntax` attrs=function

  ```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
  
    // ==== string predicates (Python semantics) =================================
  ```
- L13 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
  ```
- L14 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
  ```
- L15 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
  ```
- L16 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
  
    // ==== case maps ============================================================
  ```
- L19 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
  ```
- L21 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
  
    // ==== join / count / strip / encode ========================================
    // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
    // the call layer; the result str is a value)
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
  ```
- L27 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
  ```
- L28 `rule` [ordinary-rule]

  ```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
  ```
- L29 `rule` [ordinary-rule]

  ```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
  ```
- L30 `rule` [ordinary-rule]

  ```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
      => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
  
    // S.count(sub): non-overlapping window scan (Python str.count)
  ```
- L34 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
  ```
- L35 `syntax` attrs=function

  ```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
  ```
- L36 `rule` [ordinary-rule]

  ```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
  ```
- L37 `rule` [ordinary-rule]

  ```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
         requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
         requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
  ```
- L41 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
  ```
- L42 `rule` [ordinary-rule]

  ```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
  ```
- L43 `rule` [owise-rule] attrs=owise

  ```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
  ```
- L44 `rule` [ordinary-rule]

  ```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
  
    // S.strip(): trim whitespace runs from both ends
  ```
- L47 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
  ```
- L48 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
  ```
- L49 `rule` [ordinary-rule]

  ```k
  rule trimWS(.IntSeq) => .IntSeq
  ```
- L50 `rule` [ordinary-rule]

  ```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
  ```
- L51 `rule` [ordinary-rule]

  ```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
  ```
- L52 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
  ```
- L53 `rule` [ordinary-rule]

  ```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
  ```
- L54 `rule` [ordinary-rule]

  ```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
  ```
- L55 `rule` [ordinary-rule]

  ```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
  
    // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
  ```
- L58 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
  
    // ==== prefix ===============================================================
  ```
- L61 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
  
    // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
  ```
- L64 `rule` [ordinary-rule]

  ```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
  ```
- L65 `syntax` attrs=function,total

  ```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
  ```
- L66 `rule` [ordinary-rule]

  ```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
  ```
- L67 `rule` [ordinary-rule]

  ```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
  ```
- L68 `rule` [ordinary-rule]

  ```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
  
    // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
    // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
  ```
- L72 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
          => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
         [priority(40)]
  ```
- L75 `syntax` attrs=function

  ```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
  ```
- L76 `rule` [ordinary-rule]

  ```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
  ```
- L77 `rule` [ordinary-rule]

  ```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
         requires isWSC(C)
  ```
- L79 `rule` [ordinary-rule]

  ```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
         requires notBool isWSC(C)
    // flush the current token to the result list iff non-empty.
  ```
- L82 `syntax` attrs=function

  ```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
  ```
- L83 `rule` [ordinary-rule]

  ```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
  ```
- L84 `rule` [ordinary-rule]

  ```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
  ```
- L85 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isWSC(Int) [function, total]
  ```
- L86 `rule` [ordinary-rule]

  ```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
  
    // split(sep='x') keyword form delegates to the positional k-cell rule
  ```
- L89 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
          => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
         [priority(39)]
  
    // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
  ```
- L94 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
          => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
         [priority(40)]
  ```
- L97 `syntax` attrs=function

  ```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
  ```
- L98 `rule` [ordinary-rule]

  ```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
  ```
- L99 `rule` [ordinary-rule]

  ```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
         requires C ==Int SEP
  ```
- L101 `rule` [ordinary-rule]

  ```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
         requires notBool (C ==Int SEP)
  ```
- L104 `rule` [ordinary-rule]

  ```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
      => str(replaceC(CS, A, B))
  ```
- L106 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
  ```
- L107 `rule` [ordinary-rule]

  ```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
  ```
- L108 `rule` [ordinary-rule]

  ```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
  ```
- L109 `rule` [ordinary-rule]

  ```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
  
    // ==== char helpers =========================================================
  ```
- L112 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isUpperC(Int) [function, total]
  ```
- L113 `rule` [ordinary-rule]

  ```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
  ```
- L115 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isLowerC(Int) [function, total]
  ```
- L116 `rule` [ordinary-rule]

  ```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
  ```
- L118 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isAlphaC(Int) [function, total]
  ```
- L119 `rule` [ordinary-rule]

  ```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
  ```
- L121 `syntax` attrs=function,total

  ```k
  syntax Bool ::= isDigitC(Int) [function, total]
  ```
- L122 `rule` [ordinary-rule]

  ```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
  ```
- L124 `syntax` attrs=function,total

  ```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
  ```
- L125 `rule` [ordinary-rule]

  ```k
  rule hasUpper(.IntSeq) => false
  ```
- L126 `rule` [ordinary-rule]

  ```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
  ```
- L128 `syntax` attrs=function,total

  ```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
  ```
- L129 `rule` [ordinary-rule]

  ```k
  rule hasLower(.IntSeq) => false
  ```
- L130 `rule` [ordinary-rule]

  ```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
  ```
- L132 `syntax` attrs=function,total

  ```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
  ```
- L133 `rule` [ordinary-rule]

  ```k
  rule allAlpha(.IntSeq) => true
  ```
- L134 `rule` [ordinary-rule]

  ```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
  ```
- L136 `syntax` attrs=function,total

  ```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
  ```
- L137 `rule` [ordinary-rule]

  ```k
  rule allDigit(.IntSeq) => true
  ```
- L138 `rule` [ordinary-rule]

  ```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
  ```
- L140 `syntax` attrs=function,total

  ```k
  syntax Int ::= lowerC(Int) [function, total]
  ```
- L142 `rule` [ordinary-rule]

  ```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
  ```
- L143 `rule` [owise-rule] attrs=owise

  ```k
  rule lowerC(C:Int) => C         [owise]
  ```
- L145 `syntax` attrs=function,total

  ```k
  syntax Int ::= upperC(Int) [function, total]
  ```
- L146 `rule` [ordinary-rule]

  ```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
  ```
- L147 `rule` [owise-rule] attrs=owise

  ```k
  rule upperC(C:Int) => C         [owise]
  ```
- L149 `syntax` attrs=function,total

  ```k
  syntax Int ::= swapC(Int) [function, total]
  ```
- L150 `rule` [ordinary-rule]

  ```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
  ```
- L151 `rule` [ordinary-rule]

  ```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
  ```
- L152 `rule` [owise-rule] attrs=owise

  ```k
  rule swapC(C:Int) => C         [owise]
  ```
- L154 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
  ```
- L155 `rule` [ordinary-rule]

  ```k
  rule mapLower(.IntSeq) => .IntSeq
  ```
- L156 `rule` [ordinary-rule]

  ```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
  ```
- L158 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
  ```
- L159 `rule` [ordinary-rule]

  ```k
  rule mapUpper(.IntSeq) => .IntSeq
  ```
- L160 `rule` [ordinary-rule]

  ```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
  ```
- L162 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
  ```
- L163 `rule` [ordinary-rule]

  ```k
  rule mapSwap(.IntSeq) => .IntSeq
  ```
- L164 `rule` [ordinary-rule]

  ```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
  ```
- L166 `syntax` attrs=function,total

  ```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
  ```
- L167 `rule` [ordinary-rule]

  ```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
  ```
- L168 `rule` [ordinary-rule]

  ```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```
- L169 `rule` [ordinary-rule]

  ```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
  ```
- L170 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/operators.k

Counts: context=2, endmodule=1, imports=2, module=1, rule=10

- L6 `module`
  `module MPY-OPERATORS`
- L7 `imports`
  `imports MPY-CORE`
- L8 `imports`
  `imports MPY-ITER`
- L10 `rule` [ordinary-rule]

  ```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
  ```
- L12 `rule` [ordinary-rule]

  ```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
  
    // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
  ```
- L15 `context`

  ```k
  context Compare(HOLE, _)
  ```
- L16 `context`

  ```k
  context Compare(_:Val, CmpOp(_, HOLE))
  ```
- L17 `rule` [owise-rule] attrs=owise

  ```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
  ```
- L19 `rule` [ordinary-rule]

  ```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
  
    // ==== operand deref: heap objects combine/compare by STRUCTURE ============
    // (Python: list == is structural; identity only via `is`.) priority(40)
    // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
  ```
- L25 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L28 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(L)
         [priority(40)]
  
    // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
  ```
- L34 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires OP =/=String "in" andBool OP =/=String "not in"
         [priority(40)]
  ```
- L38 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(L)
          orBool OP ==String "in" orBool OP ==String "not in"
         [priority(40)]
  ```
- L44 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L47 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/range.k

Counts: endmodule=1, imports=2, module=1, rule=6, syntax=2

- L5 `module`
  `module MPY-RANGE`
- L6 `imports`
  `imports MPY-CORE`
- L7 `imports`
  `imports MPY-ITER`
- L9 `syntax` attrs=function,total

  ```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
  ```
- L10 `rule` [ordinary-rule]

  ```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
  ```
- L12 `syntax` attrs=function

  ```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
  ```
- L13 `rule` [ordinary-rule]

  ```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
         requires ST >Int 0 andBool HI >Int LO
  ```
- L15 `rule` [ordinary-rule]

  ```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
         requires ST <Int 0 andBool HI <Int LO
  ```
- L17 `rule` [ordinary-rule]

  ```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
         requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
          => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
         requires inRange(I, HI, ST)
  ```
- L23 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
         requires notBool inRange(I, HI, ST)
  ```
- L25 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/set.k

Counts: endmodule=1, imports=1, module=1, rule=12, syntax=6

- L3 `module`
  `module MPY-SET`
- L4 `imports`
  `imports MPY-CORE`
- L8 `syntax`

  ```k
  syntax Val ::= setV(IntSeq)
  
    // membership of a code in the accumulated distinct-code sequence
  ```
- L11 `syntax` attrs=function,total

  ```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
  ```
- L12 `rule` [ordinary-rule]

  ```k
  rule codeIn(_:Int, .IntSeq)                => false
  ```
- L13 `rule` [ordinary-rule]

  ```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
  
    // the distinct codes of CS (insert-if-absent fold, first-seen order)
  ```
- L16 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                    | dedupFrom(IntSeq, IntSeq)  [function, total]
  ```
- L18 `rule` [ordinary-rule]

  ```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
  ```
- L19 `rule` [ordinary-rule]

  ```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
         requires codeIn(C, ACC)
  ```
- L22 `rule` [ordinary-rule]

  ```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
         requires notBool codeIn(C, ACC)
  ```
- L25 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
  ```
- L27 `rule` [ordinary-rule]

  ```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
  
    // ==== set equality: two sets are equal iff mutually subsuming ==============
    // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
  ```
- L31 `syntax` attrs=function,total

  ```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
  ```
- L32 `rule` [ordinary-rule]

  ```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
  ```
- L33 `rule` [ordinary-rule]

  ```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
  ```
- L35 `syntax` attrs=function,total

  ```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
  ```
- L36 `rule` [ordinary-rule]

  ```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
  
    // set == set  (the only comparison sets support here)
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
  ```
- L40 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/sort.k

Counts: endmodule=1, imports=2, module=1, rule=19, syntax=6

- L10 `module`
  `module MPY-SORT`
- L11 `imports`
  `imports MPY-BUILTINS`
- L12 `imports`
  `imports MPY-SUBSCRIPT`
- L18 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
  ```
- L19 `syntax` attrs=function

  ```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
  ```
- L20 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
  ```
- L21 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
  ```
- L22 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
  ```
- L23 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
  ```
- L24 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
    // str elements insert by the shared lexicographic strLt (methods.k)
  ```
- L26 `syntax` attrs=function

  ```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
  ```
- L27 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
  ```
- L28 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
  ```
- L29 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
         requires strLt(A, B) orBool A ==K B [concrete]
  ```
- L31 `rule` [concrete-only-rule] attrs=concrete

  ```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
         requires notBool (strLt(A, B) orBool A ==K B) [concrete]
  
    // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
    // applyBuiltin routing in call.k) so the result allocates.
  ```
- L36 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
          => #alloc(list(sortVS(VS))) ... </k>
  
    // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
  ```
- L40 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
         <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
         [priority(40)]
  
    // ==== keyed / reversed sorted() (WP2) =====================================
    // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV
    // (a closure/builtin/type — anything callable). OPAQUE here; the concrete
    // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable-
    // inserts, at priority(40) over these.
  ```
- L49 `syntax` attrs=function,total,symbol,no-evaluators

  ```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
  ```
- L51 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                    | revVSAcc(ValSeq, ValSeq) [function, total]
  ```
- L53 `rule` [ordinary-rule]

  ```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
  ```
- L54 `rule` [ordinary-rule]

  ```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
  ```
- L55 `rule` [ordinary-rule]

  ```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
  ```
- L57 `syntax` attrs=function,total

  ```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
  ```
- L58 `rule` [ordinary-rule]

  ```k
  rule condRev(S:ValSeq, false) => S
  ```
- L59 `rule` [ordinary-rule]

  ```k
  rule condRev(S:ValSeq, true)  => revVS(S)
  ```
- L61 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
          => #alloc(list(sortKeyVS(VS, KV))) ... </k>
  ```
- L63 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
          => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
  ```
- L65 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
          => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
  
    // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
    // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
    // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
    // their postcondition directly as valSeqAt(sortVS(VS), …).
  ```
- L72 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/str.k

Counts: endmodule=1, imports=2, module=1, rule=28, syntax=5

- L3 `module`
  `module MPY-STR`
- L4 `imports`
  `imports MPY-CORE`
- L5 `imports`
  `imports MPY-ITER`
- L8 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
  ```
- L9 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
          => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
  
    // ==== str literal (ASCII-only) ============================================
  ```
- L13 `syntax` attrs=function

  ```k
  syntax IntSeq ::= strToCodes(String) [function]
  ```
- L14 `rule` [ordinary-rule]

  ```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
  ```
- L15 `rule` [ordinary-rule]

  ```k
  rule strToCodes("") => .IntSeq
  ```
- L16 `rule` [ordinary-rule]

  ```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
      requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
  
    // ==== operators: + / == / != / in =========================================
  ```
- L20 `syntax` attrs=function,total

  ```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
  ```
- L21 `rule` [ordinary-rule]

  ```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
  ```
- L22 `rule` [ordinary-rule]

  ```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
  ```
- L24 `rule` [ordinary-rule]

  ```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
  ```
- L25 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
  
    // substring membership: `P in X` iff the code-seq P occurs contiguously in X
  ```
- L29 `rule` [ordinary-rule]

  ```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
  ```
- L30 `rule` [ordinary-rule]

  ```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
  ```
- L32 `syntax` attrs=function,total

  ```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
  ```
- L33 `rule` [ordinary-rule]

  ```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
  ```
- L34 `rule` [ordinary-rule]

  ```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```
- L35 `rule` [ordinary-rule]

  ```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
  ```
- L37 `syntax` attrs=function,total

  ```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
  ```
- L38 `rule` [ordinary-rule]

  ```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
  ```
- L40 `rule` [ordinary-rule]

  ```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
         requires notBool strPrefix(P, iCons(C, Xs))
  
    // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
    // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
    // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
    // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
    // str </<=/>/>= comparisons.
  ```
- L48 `syntax` attrs=function,total

  ```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
  ```
- L49 `rule` [ordinary-rule]

  ```k
  rule strLt(.IntSeq, .IntSeq)                => false
  ```
- L50 `rule` [ordinary-rule]

  ```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
  ```
- L51 `rule` [ordinary-rule]

  ```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```
- L52 `rule` [ordinary-rule]

  ```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
  ```
- L53 `rule` [ordinary-rule]

  ```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
  ```
- L54 `rule` [ordinary-rule]

  ```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
  ```
- L56 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
  ```
- L57 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
  ```
- L58 `rule` [ordinary-rule]

  ```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
  ```
- L59 `rule` [ordinary-rule]

  ```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
  ```
- L60 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/subscript.k

Counts: context=2, endmodule=1, imports=1, module=1, rule=40, syntax=15

- L3 `module`
  `module MPY-SUBSCRIPT`
- L4 `imports`
  `imports MPY-CORE`
- L11 `syntax` attrs=function,total

  ```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
  ```
- L12 `rule` [ordinary-rule]

  ```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
  ```
- L13 `rule` [ordinary-rule]

  ```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
         requires I >Int 0
  ```
- L16 `syntax` attrs=function

  ```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
  ```
- L17 `rule` [ordinary-rule]

  ```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
  ```
- L18 `rule` [ordinary-rule]

  ```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
         requires I >Int 0
  ```
- L21 `syntax` attrs=function,total

  ```k
  syntax Int ::= normIdx(Int, Int) [function, total]
  ```
- L22 `rule` [ordinary-rule]

  ```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
  ```
- L23 `rule` [ordinary-rule]

  ```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
  
    // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
    // contexts (not strict attrs): the Index slot's Slice alternative must never heat
  ```
- L27 `context`

  ```k
  context Subscript(HOLE, _)
  ```
- L28 `context`

  ```k
  context Subscript(_:Val, HOLE:Expr)
  
    // heap-object deref (covers both the index and slice forms via the Index slot)
  ```
- L31 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L35 `rule` [ordinary-rule]

  ```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
  ```
- L37 `syntax` attrs=function

  ```k
  syntax Val ::= applyIndex(Val, Int) [function]
  ```
- L38 `rule` [ordinary-rule]

  ```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
  ```
- L39 `rule` [ordinary-rule]

  ```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
  ```
- L40 `rule` [ordinary-rule]

  ```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
      => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
  
    // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
  ```
- L44 `syntax`

  ```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                   | #slLo(Val, Bound, Bound)
                   | #slHi(Val, OptInt, Bound)
                   | #slStep(Val, OptInt, OptInt)
  ```
- L49 `syntax`

  ```k
  syntax OptInt ::= "noB" | someB(Int)
  ```
- L50 `rule` [ordinary-rule]

  ```k
  rule <k> #evalB(NoBound)  => noB ... </k>
  ```
- L51 `rule` [ordinary-rule]

  ```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
  ```
- L52 `rule` [ordinary-rule]

  ```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
  ```
- L54 `rule` [ordinary-rule]

  ```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
  ```
- L55 `rule` [ordinary-rule]

  ```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
  ```
- L56 `rule` [ordinary-rule]

  ```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
    // a list slice constructs a NEW object; a str slice stays a value
  ```
- L58 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
          => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
         [priority(45)]
  ```
- L61 `rule` [ordinary-rule]

  ```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
  ```
- L63 `syntax` attrs=function

  ```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
  ```
- L64 `rule` [ordinary-rule]

  ```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
  ```
- L66 `rule` [ordinary-rule]

  ```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
  ```
- L68 `rule` [ordinary-rule]

  ```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
  
    // ==== slice.indices: step / start / stop / clamp ==========================
  ```
- L72 `syntax` attrs=function,total

  ```k
  syntax Int ::= slStep(OptInt) [function, total]
  ```
- L73 `rule` [ordinary-rule]

  ```k
  rule slStep(noB)          => 1
  ```
- L74 `rule` [ordinary-rule]

  ```k
  rule slStep(someB(S:Int)) => S
  ```
- L76 `syntax` attrs=function

  ```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
  ```
- L77 `rule` [ordinary-rule]

  ```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
         requires slStep(ST) >Int 0
  ```
- L79 `rule` [ordinary-rule]

  ```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
         requires slStep(ST) <Int 0
  ```
- L81 `rule` [ordinary-rule]

  ```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
  ```
- L83 `syntax` attrs=function

  ```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
  ```
- L84 `rule` [ordinary-rule]

  ```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
         requires slStep(ST) >Int 0
  ```
- L86 `rule` [ordinary-rule]

  ```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
         requires slStep(ST) <Int 0
  ```
- L88 `rule` [ordinary-rule]

  ```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
  ```
- L90 `syntax` attrs=function,total

  ```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
  ```
- L91 `rule` [ordinary-rule]

  ```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
         requires I  <Int 0
  ```
- L93 `rule` [ordinary-rule]

  ```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
         requires I >=Int 0
  ```
- L96 `syntax` attrs=function,total

  ```k
  syntax Int ::= clampLo(Int, Int) [function, total]
  ```
- L97 `rule` [ordinary-rule]

  ```k
  rule clampLo(J:Int, _STEP:Int) => J
         requires J >=Int 0
  ```
- L99 `rule` [ordinary-rule]

  ```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
         requires J <Int 0
  ```
- L102 `syntax` attrs=function,total

  ```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
  ```
- L103 `rule` [ordinary-rule]

  ```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
         requires I  <Int LEN
  ```
- L105 `rule` [ordinary-rule]

  ```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
         requires I >=Int LEN
  
    // ==== build the strided sub-sequence (indices in range by construction) ====
  ```
- L109 `syntax` attrs=function

  ```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
  ```
- L110 `rule` [ordinary-rule]

  ```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
      => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
         requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
  ```
- L113 `rule` [ordinary-rule]

  ```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
         requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
  ```
- L116 `syntax` attrs=function

  ```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
  ```
- L117 `rule` [ordinary-rule]

  ```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
      => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
         requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
  ```
- L120 `rule` [ordinary-rule]

  ```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
         requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
  ```
- L122 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/syntax.k

Counts: endmodule=1, imports=4, module=1, syntax=16

- L3 `module`
  `module MPY-SYNTAX`
- L4 `imports`
  `imports INT-SYNTAX`
- L5 `imports`
  `imports FLOAT-SYNTAX`
- L6 `imports`
  `imports BOOL-SYNTAX`
- L7 `imports`
  `imports STRING-SYNTAX`
- L9 `syntax` attrs=macro

  ```k
  syntax Expr ::= "Int"      "(" Int ")"
                  | "Float"    "(" Float ")"
                  | "Bool"     "(" Bool ")"
                  | "Name"     "(" String ")"
                  | "Str"      "(" String ")"
                  | "UnaryOp"  "(" String "," Expr ")" [strict(2)]
                  | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)]
                  | "BoolOp"    "(" String "," Exprs ")"
                  | "ListExpr"  "(" Exprs ")"
                  | "DictExpr"  "(" Entries ")"
                  | "ListComp"  "(" Expr "," CompFors ")" [macro]
                  | "GenExp"    "(" Expr "," CompFors ")" [macro]
                  | "TupleExpr" "(" Exprs ")"
                  | "Subscript" "(" Expr "," Index ")"
                  | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)]
                  | "Lambda"    "(" Params "," Expr ")"
                  | "KwArg"     "(" String "," Expr ")"
                  | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")"
                  | "NoneVal"
                  | "Call"      "(" Expr "," Exprs ")"
                  | "Attribute" "(" Expr "," String ")" [strict(1)]
                  | "Compare"   "(" Expr "," CmpOp ")"
  ```
- L32 `syntax`

  ```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
  ```
- L33 `syntax`

  ```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
  ```
- L34 `syntax`

  ```k
  syntax Entries  ::= List{Entry, ","}
  ```
- L35 `syntax`

  ```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  ```
- L36 `syntax`

  ```k
  syntax CompFors ::= List{CompFor, ""}
  ```
- L37 `syntax`

  ```k
  syntax Exprs    ::= List{Expr, ","}
  ```
- L38 `syntax`

  ```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
  ```
- L39 `syntax`

  ```k
  syntax Bound    ::= Expr | "NoBound"
  ```
- L41 `syntax`

  ```k
  syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]
                  | "Import"    "(" String ")"
                  | "ImportFrom" "(" String "," ParamNames ")"
                  | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)]
                  | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)]
                  | "While"     "(" Expr "," Stmts ")"
                  | "Break"
                  | "Continue"
                  | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)]
                  | "Return"    "(" Expr ")" [strict]
                  | "Assert"    "(" Expr ")" [strict]
                  | "Expr"      "(" Expr ")" [strict]
                  | "FuncDef"   "(" String "," Params "," Stmts ")"
                  | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
  ```
- L56 `syntax`

  ```k
  syntax Stmts      ::= List{Stmt, ""}
  ```
- L57 `syntax`

  ```k
  syntax Params     ::= "Params" "(" ParamNames ")"
  ```
- L58 `syntax`

  ```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
  ```
- L59 `syntax`

  ```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
  ```
- L60 `syntax`

  ```k
  syntax ParamNames ::= List{String, ","}
  ```
- L61 `syntax`

  ```k
  syntax Module     ::= "Module" "(" Stmts ")"
  ```
- L62 `endmodule`
  `endmodule`

## /reference/reference-semantics/semantics/tuple.k

Counts: endmodule=1, imports=4, module=1, requires=1, rule=21, syntax=4

- L3 `module`
  `module MPY-TUPLE`
- L4 `imports`
  `imports MPY-CORE`
- L5 `imports`
  `imports MPY-ITER`
- L6 `imports`
  `imports MPY-LIST`
- L7 `imports`
  `imports MPY-METHODS`
- L10 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
  ```
- L11 `rule` [ordinary-rule]

  ```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
  
    // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
  ```
- L14 `syntax`

  ```k
  syntax ApplyK ::= "toTuple"
  ```
- L15 `rule` [ordinary-rule]

  ```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
  ```
- L16 `rule` [ordinary-rule]

  ```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
  ```
- L18 `rule` [ordinary-rule]

  ```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
    // membership routes through the same k-cell fold as lists (list.k)
  ```
- L20 `rule` [ordinary-rule]

  ```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
  ```
- L21 `rule` [ordinary-rule]

  ```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
    // t.index(v): first index of v (ValueError out of subset)
  ```
- L23 `rule` [ordinary-rule]

  ```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
  ```
- L24 `syntax` attrs=function

  ```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
  ```
- L25 `rule` [ordinary-rule]

  ```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
  ```
- L26 `rule` [ordinary-rule]

  ```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
         requires notBool (A ==K V)
  ```
- L28 `rule` [ordinary-rule]

  ```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
  
    // ==== target binding: bind a Name or a TupleExpr target to a value ========
  ```
- L31 `syntax`

  ```k
  syntax KItem ::= #bindTgt(Expr, Val)
  ```
- L32 `rule` [ordinary-rule]

  ```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
  ```
- L35 `rule` [ordinary-rule]

  ```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
  ```
- L38 `requires`
  `requires "$cells" in_keys(M)`
- L42 `rule` [ordinary-rule]

  ```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
  ```
- L43 `rule` [ordinary-rule]

  ```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
  ```
- L44 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  
    // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
  ```
- L49 `syntax`

  ```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
  ```
- L50 `rule` [ordinary-rule]

  ```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
  ```
- L51 `rule` [ordinary-rule]

  ```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
  ```
- L52 `rule` [priority-rule] attrs=priority

  ```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```
- L55 `rule` [ordinary-rule]

  ```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
          => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
  ```
- L57 `rule` [ordinary-rule]

  ```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
  ```
- L58 `endmodule`
  `endmodule`

## /candidate/verification.k

Counts: endmodule=1, imports=1, module=1, requires=1, rule=2, syntax=2

- L1 `requires`
  `requires "reference-semantics/semantics.k"`
- L3 `module`
  `module ROUNDED-AVG-VERIFICATION`
- L4 `imports`
  `imports MPY`
- L9 `syntax` attrs=function,total

  ```k
  syntax Stmts ::= "roundedAvgBody" [function, total]
  ```
- L10 `rule` [ordinary-rule]

  ```k
  rule roundedAvgBody
      => If(Compare(Name("n"), CmpOp(">", Name("m"))),
           Return(UnaryOp("-", Int(1))),
           .Stmts)
         Assign(Name("total"), BinOp("+", Name("n"), Name("m")))
         Assign(Name("average"), BinOp("//", Name("total"), Int(2)))
         If(Compare(BinOp("%", Name("total"), Int(2)),
                    CmpOp("==", Int(1))),
            If(Compare(BinOp("%", Name("average"), Int(2)),
                       CmpOp("==", Int(1))),
               Assign(Name("average"),
                      BinOp("+", Name("average"), Int(1))),
               .Stmts),
            .Stmts)
         Return(Call(Name("bin"), Name("average"), .Exprs))
         .Stmts
  
    // A direct entry-point call. Its closure has the module scope as parent,
    // just as the closure produced by the module-level FuncDef in solution.mpy.
  ```
- L29 `syntax` attrs=function,total

  ```k
  syntax Expr ::= roundedAvgCall(Int, Int) [function, total]
  ```
- L30 `rule` [ordinary-rule]

  ```k
  rule roundedAvgCall(N:Int, M:Int)
      => Call(closureVal(("n", "m", .ParamNames), roundedAvgBody, 0),
              (N, M, .Exprs))
  ```
- L33 `endmodule`
  `endmodule`

## /candidate/spec.k

Counts: claim=4, endmodule=1, imports=1, module=1, requires=1

- L1 `requires`
  `requires "verification.k"`
- L3 `module`
  `module ROUNDED-AVG-SPEC`
- L4 `imports`
  `imports ROUNDED-AVG-VERIFICATION`
- L7 `claim`

  ```k
  claim
      <k> roundedAvgCall(N:Int, M:Int) => -1 </k>
      <env> 0 </env>
      <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      </scopes>
      <scopeLoc> 1 </scopeLoc>
      <heap> .Map </heap>
      <heapLoc> 0 </heapLoc>
      <stack> .List </stack>
      <ret> noRet </ret>
      <exc> NoExc </exc>
      requires N >Int 0 andBool M >Int 0 andBool N >Int M
  
    // Valid interval, integral mean: no rounding adjustment is needed.
  ```
- L23 `claim`

  ```k
  claim
      <k> roundedAvgCall(N:Int, M:Int)
        => str(iCons(48, iCons(98, binCodes((N +Int M) /Int 2))))
      </k>
      <env> 0 </env>
      <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      </scopes>
      <scopeLoc> 1 </scopeLoc>
      <heap> .Map </heap>
      <heapLoc> 0 </heapLoc>
      <stack> .List </stack>
      <ret> noRet </ret>
      <exc> NoExc </exc>
      requires N >Int 0 andBool M >Int 0 andBool N <=Int M
        andBool pyMod(N +Int M, 2) ==Int 0
  
    // Exact x.5 mean whose lower neighbor is even: half-even rounds down.
  ```
- L42 `claim`

  ```k
  claim
      <k> roundedAvgCall(N:Int, M:Int)
        => str(iCons(48, iCons(98, binCodes((N +Int M -Int 1) /Int 2))))
      </k>
      <env> 0 </env>
      <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      </scopes>
      <scopeLoc> 1 </scopeLoc>
      <heap> .Map </heap>
      <heapLoc> 0 </heapLoc>
      <stack> .List </stack>
      <ret> noRet </ret>
      <exc> NoExc </exc>
      requires N >Int 0 andBool M >Int 0 andBool N <=Int M
        andBool pyMod(N +Int M, 2) ==Int 1
        andBool pyMod((N +Int M -Int 1) /Int 2, 2) ==Int 0
  
    // Exact x.5 mean whose lower neighbor is odd: half-even rounds up.
  ```
- L62 `claim`

  ```k
  claim
      <k> roundedAvgCall(N:Int, M:Int)
        => str(iCons(48, iCons(98,
             binCodes(((N +Int M -Int 1) /Int 2) +Int 1))))
      </k>
      <env> 0 </env>
      <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      </scopes>
      <scopeLoc> 1 </scopeLoc>
      <heap> .Map </heap>
      <heapLoc> 0 </heapLoc>
      <stack> .List </stack>
      <ret> noRet </ret>
      <exc> NoExc </exc>
      requires N >Int 0 andBool M >Int 0 andBool N <=Int M
        andBool pyMod(N +Int M, 2) ==Int 1
        andBool pyMod((N +Int M -Int 1) /Int 2, 2) ==Int 1
  ```
- L81 `endmodule`
  `endmodule`

# Totals

- claim: 4
- configuration: 1
- context: 5
- endmodule: 27
- imports: 88
- module: 27
- requires: 29
- rule: 697
- syntax: 229

# Attribute-bearing statement counts

- function: 147
- total: 109
- functional: 0
- symbol: 25
- no-evaluators: 22
- concrete: 35
- simplification: 0
- simplify: 0
- priority: 41
- owise: 26
- anywhere: 0
- macro: 4

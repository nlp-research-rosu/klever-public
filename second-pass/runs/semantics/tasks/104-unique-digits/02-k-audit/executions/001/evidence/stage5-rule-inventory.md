# Exhaustive K declaration/rule inventory

Each item records the complete source block beginning at every `syntax`, `rule`, `claim`, `configuration`, or `context` declaration.

## reference-semantics/semantics.k

Count: 0; 

## reference-semantics/semantics/assert.k

Count: 3; rule=3

### reference-semantics/semantics/assert.k:6-6 [1] rule; attributes: none

```k
  rule <k> Assert(V:Val) => .K ... </k>
```

### reference-semantics/semantics/assert.k:8-10 [2] rule; attributes: none

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
```

### reference-semantics/semantics/assert.k:13-15 [3] rule; attributes: priority(40)

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## reference-semantics/semantics/bool.k

Count: 14; context=1, rule=13

### reference-semantics/semantics/bool.k:8-8 [1] rule; attributes: none

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### reference-semantics/semantics/bool.k:10-10 [2] rule; attributes: none

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### reference-semantics/semantics/bool.k:11-15 [3] rule; attributes: none

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### reference-semantics/semantics/bool.k:16-16 [4] context; attributes: none

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### reference-semantics/semantics/bool.k:17-17 [5] rule; attributes: none

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### reference-semantics/semantics/bool.k:18-18 [6] rule; attributes: none

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
```

### reference-semantics/semantics/bool.k:20-20 [7] rule; attributes: none

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### reference-semantics/semantics/bool.k:22-22 [8] rule; attributes: none

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### reference-semantics/semantics/bool.k:24-24 [9] rule; attributes: none

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
```

### reference-semantics/semantics/bool.k:29-30 [10] rule; attributes: priority(40)

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/bool.k:31-32 [11] rule; attributes: none

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/bool.k:35-36 [12] rule; attributes: none

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/bool.k:39-40 [13] rule; attributes: none

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/bool.k:43-44 [14] rule; attributes: none

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

## reference-semantics/semantics/builtins.k

Count: 175; rule=137, syntax=38

### reference-semantics/semantics/builtins.k:17-19 [1] syntax; attributes: function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### reference-semantics/semantics/builtins.k:20-20 [2] syntax; attributes: function

```k
  syntax Int ::= seqLen(Val) [function]
```

### reference-semantics/semantics/builtins.k:21-21 [3] rule; attributes: none

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### reference-semantics/semantics/builtins.k:22-22 [4] rule; attributes: none

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### reference-semantics/semantics/builtins.k:23-23 [5] rule; attributes: none

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### reference-semantics/semantics/builtins.k:24-24 [6] rule; attributes: none

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### reference-semantics/semantics/builtins.k:25-25 [7] rule; attributes: none

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### reference-semantics/semantics/builtins.k:26-31 [8] rule; attributes: none

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### reference-semantics/semantics/builtins.k:32-32 [9] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### reference-semantics/semantics/builtins.k:33-33 [10] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### reference-semantics/semantics/builtins.k:34-34 [11] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### reference-semantics/semantics/builtins.k:35-35 [12] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### reference-semantics/semantics/builtins.k:36-36 [13] syntax; attributes: function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:37-37 [14] rule; attributes: none

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### reference-semantics/semantics/builtins.k:38-40 [15] rule; attributes: none

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### reference-semantics/semantics/builtins.k:41-43 [16] rule; attributes: none

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### reference-semantics/semantics/builtins.k:44-46 [17] rule; attributes: none

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### reference-semantics/semantics/builtins.k:47-47 [18] syntax; attributes: none

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### reference-semantics/semantics/builtins.k:48-48 [19] rule; attributes: none

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### reference-semantics/semantics/builtins.k:49-49 [20] rule; attributes: none

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### reference-semantics/semantics/builtins.k:50-51 [21] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
```

### reference-semantics/semantics/builtins.k:54-54 [22] syntax; attributes: function

```k
  syntax Int ::= intOf(Val) [function]
```

### reference-semantics/semantics/builtins.k:55-55 [23] rule; attributes: none

```k
  rule intOf(I:Int)  => I
```

### reference-semantics/semantics/builtins.k:56-58 [24] rule; attributes: none

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### reference-semantics/semantics/builtins.k:59-59 [25] syntax; attributes: none

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### reference-semantics/semantics/builtins.k:60-60 [26] rule; attributes: none

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### reference-semantics/semantics/builtins.k:61-61 [27] rule; attributes: none

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### reference-semantics/semantics/builtins.k:62-62 [28] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
```

### reference-semantics/semantics/builtins.k:64-64 [29] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
```

### reference-semantics/semantics/builtins.k:67-67 [30] syntax; attributes: none

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### reference-semantics/semantics/builtins.k:68-68 [31] rule; attributes: none

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### reference-semantics/semantics/builtins.k:69-69 [32] rule; attributes: none

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### reference-semantics/semantics/builtins.k:70-70 [33] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
```

### reference-semantics/semantics/builtins.k:72-72 [34] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
```

### reference-semantics/semantics/builtins.k:76-76 [35] syntax; attributes: none

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### reference-semantics/semantics/builtins.k:77-77 [36] rule; attributes: none

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### reference-semantics/semantics/builtins.k:78-78 [37] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
```

### reference-semantics/semantics/builtins.k:80-80 [38] rule; attributes: none

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### reference-semantics/semantics/builtins.k:81-81 [39] rule; attributes: none

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### reference-semantics/semantics/builtins.k:82-83 [40] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
```

### reference-semantics/semantics/builtins.k:86-86 [41] syntax; attributes: none

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### reference-semantics/semantics/builtins.k:87-87 [42] rule; attributes: none

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### reference-semantics/semantics/builtins.k:88-88 [43] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
```

### reference-semantics/semantics/builtins.k:90-90 [44] rule; attributes: none

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### reference-semantics/semantics/builtins.k:91-91 [45] rule; attributes: none

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### reference-semantics/semantics/builtins.k:92-93 [46] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
```

### reference-semantics/semantics/builtins.k:97-97 [47] syntax; attributes: function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### reference-semantics/semantics/builtins.k:98-98 [48] rule; attributes: none

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### reference-semantics/semantics/builtins.k:99-99 [49] rule; attributes: none

```k
  rule maxVals(M:Int, .Vals)           => M
```

### reference-semantics/semantics/builtins.k:100-100 [50] rule; attributes: none

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### reference-semantics/semantics/builtins.k:102-102 [51] syntax; attributes: function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### reference-semantics/semantics/builtins.k:103-103 [52] rule; attributes: none

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### reference-semantics/semantics/builtins.k:104-104 [53] rule; attributes: none

```k
  rule minVals(M:Int, .Vals)           => M
```

### reference-semantics/semantics/builtins.k:105-107 [54] rule; attributes: none

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### reference-semantics/semantics/builtins.k:108-108 [55] rule; attributes: none

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
```

### reference-semantics/semantics/builtins.k:111-112 [56] rule; attributes: none

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
```

### reference-semantics/semantics/builtins.k:114-114 [57] syntax; attributes: function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### reference-semantics/semantics/builtins.k:115-115 [58] rule; attributes: none

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### reference-semantics/semantics/builtins.k:116-116 [59] rule; attributes: none

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### reference-semantics/semantics/builtins.k:117-117 [60] syntax; attributes: function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:118-118 [61] rule; attributes: none

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### reference-semantics/semantics/builtins.k:119-120 [62] rule; attributes: none

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
```

### reference-semantics/semantics/builtins.k:124-125 [63] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### reference-semantics/semantics/builtins.k:126-126 [64] syntax; attributes: function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:127-127 [65] rule; attributes: none

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### reference-semantics/semantics/builtins.k:128-131 [66] rule; attributes: none

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### reference-semantics/semantics/builtins.k:132-133 [67] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### reference-semantics/semantics/builtins.k:134-134 [68] syntax; attributes: function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:135-135 [69] rule; attributes: none

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### reference-semantics/semantics/builtins.k:136-136 [70] rule; attributes: none

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### reference-semantics/semantics/builtins.k:137-139 [71] rule; attributes: none

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### reference-semantics/semantics/builtins.k:140-142 [72] rule; attributes: none

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### reference-semantics/semantics/builtins.k:143-143 [73] rule; attributes: none

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### reference-semantics/semantics/builtins.k:144-144 [74] rule; attributes: none

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
```

### reference-semantics/semantics/builtins.k:148-148 [75] rule; attributes: none

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### reference-semantics/semantics/builtins.k:149-151 [76] rule; attributes: none

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### reference-semantics/semantics/builtins.k:152-152 [77] rule; attributes: none

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
```

### reference-semantics/semantics/builtins.k:156-156 [78] rule; attributes: none

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
```

### reference-semantics/semantics/builtins.k:158-158 [79] syntax; attributes: function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:159-159 [80] rule; attributes: none

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### reference-semantics/semantics/builtins.k:160-162 [81] rule; attributes: none

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### reference-semantics/semantics/builtins.k:163-163 [82] rule; attributes: none

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### reference-semantics/semantics/builtins.k:164-166 [83] rule; attributes: none

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### reference-semantics/semantics/builtins.k:167-168 [84] rule; attributes: none

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### reference-semantics/semantics/builtins.k:169-169 [85] rule; attributes: none

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:170-170 [86] rule; attributes: none

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:171-172 [87] rule; attributes: none

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### reference-semantics/semantics/builtins.k:173-173 [88] rule; attributes: none

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:174-176 [89] rule; attributes: none

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### reference-semantics/semantics/builtins.k:177-177 [90] rule; attributes: none

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### reference-semantics/semantics/builtins.k:178-178 [91] rule; attributes: none

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### reference-semantics/semantics/builtins.k:179-179 [92] rule; attributes: none

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
```

### reference-semantics/semantics/builtins.k:187-187 [93] rule; attributes: none

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### reference-semantics/semantics/builtins.k:188-188 [94] syntax; attributes: function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### reference-semantics/semantics/builtins.k:189-190 [95] rule; attributes: none

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### reference-semantics/semantics/builtins.k:192-192 [96] syntax; attributes: none

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### reference-semantics/semantics/builtins.k:194-194 [97] syntax; attributes: function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### reference-semantics/semantics/builtins.k:195-195 [98] rule; attributes: none

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### reference-semantics/semantics/builtins.k:196-196 [99] syntax; attributes: function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:197-197 [100] rule; attributes: none

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:198-198 [101] rule; attributes: owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### reference-semantics/semantics/builtins.k:199-199 [102] syntax; attributes: function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:200-200 [103] rule; attributes: none

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:201-201 [104] rule; attributes: owise

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### reference-semantics/semantics/builtins.k:203-203 [105] syntax; attributes: function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:204-204 [106] rule; attributes: none

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### reference-semantics/semantics/builtins.k:205-205 [107] rule; attributes: none

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### reference-semantics/semantics/builtins.k:206-206 [108] rule; attributes: none

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### reference-semantics/semantics/builtins.k:207-207 [109] rule; attributes: none

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### reference-semantics/semantics/builtins.k:208-208 [110] rule; attributes: none

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### reference-semantics/semantics/builtins.k:209-209 [111] rule; attributes: none

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### reference-semantics/semantics/builtins.k:210-210 [112] rule; attributes: none

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### reference-semantics/semantics/builtins.k:211-211 [113] rule; attributes: none

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### reference-semantics/semantics/builtins.k:212-212 [114] rule; attributes: none

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### reference-semantics/semantics/builtins.k:214-215 [115] syntax; attributes: function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:216-216 [116] rule; attributes: none

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### reference-semantics/semantics/builtins.k:217-217 [117] rule; attributes: none

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### reference-semantics/semantics/builtins.k:218-218 [118] rule; attributes: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### reference-semantics/semantics/builtins.k:219-219 [119] rule; attributes: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
```

### reference-semantics/semantics/builtins.k:221-221 [120] rule; attributes: none

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
```

### reference-semantics/semantics/builtins.k:223-223 [121] rule; attributes: owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### reference-semantics/semantics/builtins.k:225-225 [122] syntax; attributes: none

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### reference-semantics/semantics/builtins.k:226-226 [123] syntax; attributes: function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:227-227 [124] rule; attributes: none

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### reference-semantics/semantics/builtins.k:228-228 [125] rule; attributes: owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### reference-semantics/semantics/builtins.k:230-230 [126] syntax; attributes: function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:231-231 [127] rule; attributes: none

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### reference-semantics/semantics/builtins.k:232-232 [128] rule; attributes: none

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### reference-semantics/semantics/builtins.k:233-233 [129] rule; attributes: none

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### reference-semantics/semantics/builtins.k:234-234 [130] rule; attributes: none

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### reference-semantics/semantics/builtins.k:235-235 [131] rule; attributes: none

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### reference-semantics/semantics/builtins.k:236-236 [132] rule; attributes: owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### reference-semantics/semantics/builtins.k:238-238 [133] syntax; attributes: function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:239-239 [134] rule; attributes: none

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### reference-semantics/semantics/builtins.k:240-240 [135] rule; attributes: none

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### reference-semantics/semantics/builtins.k:241-241 [136] rule; attributes: none

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
```

### reference-semantics/semantics/builtins.k:243-243 [137] rule; attributes: owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### reference-semantics/semantics/builtins.k:244-244 [138] syntax; attributes: function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:245-245 [139] rule; attributes: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### reference-semantics/semantics/builtins.k:246-246 [140] rule; attributes: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### reference-semantics/semantics/builtins.k:247-247 [141] syntax; attributes: function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:248-248 [142] rule; attributes: none

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### reference-semantics/semantics/builtins.k:250-250 [143] syntax; attributes: function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:251-251 [144] rule; attributes: none

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### reference-semantics/semantics/builtins.k:252-252 [145] rule; attributes: none

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### reference-semantics/semantics/builtins.k:253-253 [146] rule; attributes: none

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### reference-semantics/semantics/builtins.k:254-254 [147] rule; attributes: none

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### reference-semantics/semantics/builtins.k:255-255 [148] syntax; attributes: function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:256-256 [149] rule; attributes: none

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### reference-semantics/semantics/builtins.k:257-258 [150] rule; attributes: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
```

### reference-semantics/semantics/builtins.k:260-261 [151] rule; attributes: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
```

### reference-semantics/semantics/builtins.k:263-264 [152] rule; attributes: owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### reference-semantics/semantics/builtins.k:265-265 [153] syntax; attributes: function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### reference-semantics/semantics/builtins.k:266-266 [154] rule; attributes: none

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### reference-semantics/semantics/builtins.k:267-267 [155] rule; attributes: none

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### reference-semantics/semantics/builtins.k:268-268 [156] rule; attributes: owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### reference-semantics/semantics/builtins.k:269-269 [157] syntax; attributes: function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### reference-semantics/semantics/builtins.k:270-270 [158] rule; attributes: none

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### reference-semantics/semantics/builtins.k:271-271 [159] rule; attributes: none

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### reference-semantics/semantics/builtins.k:272-272 [160] syntax; attributes: function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:273-273 [161] rule; attributes: none

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### reference-semantics/semantics/builtins.k:274-278 [162] rule; attributes: none

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### reference-semantics/semantics/builtins.k:279-279 [163] syntax; attributes: none

```k
  syntax KItem ::= "#md5"
```

### reference-semantics/semantics/builtins.k:280-281 [164] rule; attributes: priority(40)

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### reference-semantics/semantics/builtins.k:282-282 [165] rule; attributes: none

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### reference-semantics/semantics/builtins.k:283-283 [166] syntax; attributes: none

```k
  syntax Val ::= md5Obj(IntSeq)
```

### reference-semantics/semantics/builtins.k:284-284 [167] rule; attributes: none

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### reference-semantics/semantics/builtins.k:285-290 [168] syntax; attributes: function, total, symbol, no-evaluators, owise

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### reference-semantics/semantics/builtins.k:291-291 [169] rule; attributes: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### reference-semantics/semantics/builtins.k:292-292 [170] rule; attributes: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### reference-semantics/semantics/builtins.k:293-293 [171] syntax; attributes: function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### reference-semantics/semantics/builtins.k:294-294 [172] rule; attributes: none

```k
  rule isIntV(_:Int)         => true
```

### reference-semantics/semantics/builtins.k:295-295 [173] rule; attributes: owise

```k
  rule isIntV(_:Val)         => false [owise]
```

### reference-semantics/semantics/builtins.k:296-296 [174] rule; attributes: none

```k
  rule isStrV(str(_:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:297-297 [175] rule; attributes: owise

```k
  rule isStrV(_:Val)         => false [owise]
```

## reference-semantics/semantics/call.k

Count: 24; rule=21, syntax=3

### reference-semantics/semantics/call.k:16-18 [1] rule; attributes: owise

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### reference-semantics/semantics/call.k:19-19 [2] syntax; attributes: none

```k
  syntax KItem ::= #callee(Exprs)
```

### reference-semantics/semantics/call.k:20-20 [3] rule; attributes: owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### reference-semantics/semantics/call.k:21-23 [4] rule; attributes: none

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### reference-semantics/semantics/call.k:24-24 [5] rule; attributes: none

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### reference-semantics/semantics/call.k:26-26 [6] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### reference-semantics/semantics/call.k:27-27 [7] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### reference-semantics/semantics/call.k:28-28 [8] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### reference-semantics/semantics/call.k:29-29 [9] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### reference-semantics/semantics/call.k:30-30 [10] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### reference-semantics/semantics/call.k:31-31 [11] rule; attributes: owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### reference-semantics/semantics/call.k:32-37 [12] rule; attributes: none

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### reference-semantics/semantics/call.k:38-41 [13] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/call.k:42-44 [14] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/call.k:47-50 [15] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/call.k:52-52 [16] syntax; attributes: function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### reference-semantics/semantics/call.k:53-55 [17] rule; attributes: none

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### reference-semantics/semantics/call.k:56-58 [18] rule; attributes: none

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/call.k:63-65 [19] rule; attributes: none

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/call.k:69-79 [20] rule; attributes: none

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

### reference-semantics/semantics/call.k:80-85 [21] rule; attributes: none

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### reference-semantics/semantics/call.k:87-87 [22] syntax; attributes: none

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### reference-semantics/semantics/call.k:88-88 [23] rule; attributes: none

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### reference-semantics/semantics/call.k:89-93 [24] rule; attributes: none

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

## reference-semantics/semantics/comprehension.k

Count: 10; rule=7, syntax=3

### reference-semantics/semantics/comprehension.k:11-11 [1] rule; attributes: none

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### reference-semantics/semantics/comprehension.k:12-12 [2] rule; attributes: none

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### reference-semantics/semantics/comprehension.k:14-14 [3] syntax; attributes: macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### reference-semantics/semantics/comprehension.k:15-16 [4] rule; attributes: none

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### reference-semantics/semantics/comprehension.k:18-18 [5] syntax; attributes: macro

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### reference-semantics/semantics/comprehension.k:19-20 [6] rule; attributes: none

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### reference-semantics/semantics/comprehension.k:21-22 [7] rule; attributes: none

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### reference-semantics/semantics/comprehension.k:24-24 [8] syntax; attributes: macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### reference-semantics/semantics/comprehension.k:25-25 [9] rule; attributes: none

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### reference-semantics/semantics/comprehension.k:26-26 [10] rule; attributes: none

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## reference-semantics/semantics/concrete.k

Count: 21; rule=16, syntax=5

### reference-semantics/semantics/concrete.k:13-14 [1] rule; attributes: none

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### reference-semantics/semantics/concrete.k:16-17 [2] rule; attributes: none

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### reference-semantics/semantics/concrete.k:25-25 [3] syntax; attributes: none

```k
  syntax Val ::= kvP(Val, Val)
```

### reference-semantics/semantics/concrete.k:26-27 [4] syntax; attributes: none

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### reference-semantics/semantics/concrete.k:28-30 [5] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/concrete.k:31-33 [6] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/concrete.k:34-35 [7] rule; attributes: none

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### reference-semantics/semantics/concrete.k:36-37 [8] rule; attributes: none

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### reference-semantics/semantics/concrete.k:38-39 [9] rule; attributes: none

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
```

### reference-semantics/semantics/concrete.k:42-42 [10] syntax; attributes: function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### reference-semantics/semantics/concrete.k:43-43 [11] rule; attributes: none

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### reference-semantics/semantics/concrete.k:44-45 [12] rule; attributes: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
```

### reference-semantics/semantics/concrete.k:47-48 [13] rule; attributes: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
```

### reference-semantics/semantics/concrete.k:51-51 [14] syntax; attributes: function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### reference-semantics/semantics/concrete.k:52-52 [15] rule; attributes: none

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### reference-semantics/semantics/concrete.k:53-53 [16] rule; attributes: none

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### reference-semantics/semantics/concrete.k:54-54 [17] rule; attributes: none

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### reference-semantics/semantics/concrete.k:56-56 [18] syntax; attributes: function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### reference-semantics/semantics/concrete.k:57-57 [19] rule; attributes: none

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### reference-semantics/semantics/concrete.k:58-58 [20] rule; attributes: none

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### reference-semantics/semantics/concrete.k:59-59 [21] rule; attributes: owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## reference-semantics/semantics/controls.k

Count: 37; rule=34, syntax=3

### reference-semantics/semantics/controls.k:9-11 [1] rule; attributes: none

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### reference-semantics/semantics/controls.k:12-14 [2] rule; attributes: none

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/controls.k:20-22 [3] rule; attributes: none

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
```

### reference-semantics/semantics/controls.k:27-29 [4] rule; attributes: none

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/controls.k:35-35 [5] rule; attributes: none

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### reference-semantics/semantics/controls.k:36-36 [6] rule; attributes: owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### reference-semantics/semantics/controls.k:37-37 [7] syntax; attributes: none

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### reference-semantics/semantics/controls.k:38-38 [8] rule; attributes: none

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### reference-semantics/semantics/controls.k:39-41 [9] rule; attributes: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
```

### reference-semantics/semantics/controls.k:43-43 [10] rule; attributes: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
```

### reference-semantics/semantics/controls.k:48-50 [11] rule; attributes: none

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### reference-semantics/semantics/controls.k:51-51 [12] syntax; attributes: none

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### reference-semantics/semantics/controls.k:52-52 [13] rule; attributes: none

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### reference-semantics/semantics/controls.k:53-53 [14] rule; attributes: none

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### reference-semantics/semantics/controls.k:54-56 [15] rule; attributes: none

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### reference-semantics/semantics/controls.k:57-57 [16] rule; attributes: none

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
```

### reference-semantics/semantics/controls.k:59-59 [17] rule; attributes: none

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
```

### reference-semantics/semantics/controls.k:65-67 [18] syntax; attributes: none

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### reference-semantics/semantics/controls.k:69-69 [19] rule; attributes: none

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### reference-semantics/semantics/controls.k:71-71 [20] rule; attributes: none

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### reference-semantics/semantics/controls.k:72-72 [21] rule; attributes: none

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### reference-semantics/semantics/controls.k:73-76 [22] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### reference-semantics/semantics/controls.k:77-77 [23] rule; attributes: none

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### reference-semantics/semantics/controls.k:78-78 [24] rule; attributes: none

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### reference-semantics/semantics/controls.k:79-79 [25] rule; attributes: none

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
```

### reference-semantics/semantics/controls.k:81-81 [26] rule; attributes: none

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
```

### reference-semantics/semantics/controls.k:85-85 [27] rule; attributes: none

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### reference-semantics/semantics/controls.k:86-86 [28] rule; attributes: none

```k
  rule <k> Continue => #cont ... </k>
```

### reference-semantics/semantics/controls.k:87-87 [29] rule; attributes: none

```k
  rule <k> Break => #brk ... </k>
```

### reference-semantics/semantics/controls.k:88-88 [30] rule; attributes: none

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### reference-semantics/semantics/controls.k:89-89 [31] rule; attributes: owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### reference-semantics/semantics/controls.k:90-90 [32] rule; attributes: none

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### reference-semantics/semantics/controls.k:91-94 [33] rule; attributes: owise, priority(40)

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### reference-semantics/semantics/controls.k:95-97 [34] rule; attributes: priority(40)

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:98-100 [35] rule; attributes: priority(40)

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:101-105 [36] rule; attributes: priority(40)

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### reference-semantics/semantics/controls.k:106-108 [37] rule; attributes: priority(40)

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## reference-semantics/semantics/core.k

Count: 84; configuration=1, rule=46, syntax=37

### reference-semantics/semantics/core.k:13-13 [1] syntax; attributes: none

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### reference-semantics/semantics/core.k:14-14 [2] syntax; attributes: none

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### reference-semantics/semantics/core.k:15-17 [3] syntax; attributes: none

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### reference-semantics/semantics/core.k:18-23 [4] syntax; attributes: none

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### reference-semantics/semantics/core.k:25-34 [5] syntax; attributes: function

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

### reference-semantics/semantics/core.k:36-36 [6] syntax; attributes: none

```k
  syntax Parent   ::= "root" | parent(Int)
```

### reference-semantics/semantics/core.k:37-37 [7] syntax; attributes: none

```k
  syntax Scope    ::= scope(Map, Parent)
```

### reference-semantics/semantics/core.k:38-38 [8] syntax; attributes: none

```k
  syntax KResult  ::= Val
```

### reference-semantics/semantics/core.k:39-39 [9] syntax; attributes: none

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### reference-semantics/semantics/core.k:40-40 [10] syntax; attributes: none

```k
  syntax Vals     ::= List{Val, ","}
```

### reference-semantics/semantics/core.k:41-41 [11] syntax; attributes: none

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### reference-semantics/semantics/core.k:42-48 [12] syntax; attributes: none

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### reference-semantics/semantics/core.k:49-67 [13] configuration; attributes: none

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

### reference-semantics/semantics/core.k:68-68 [14] syntax; attributes: function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### reference-semantics/semantics/core.k:69-69 [15] rule; attributes: none

```k
  rule isRefV(ref(_:Int)) => true
```

### reference-semantics/semantics/core.k:70-74 [16] rule; attributes: owise

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### reference-semantics/semantics/core.k:75-75 [17] syntax; attributes: none

```k
  syntax HeapVal ::= cellV(Val)
```

### reference-semantics/semantics/core.k:76-76 [18] syntax; attributes: function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### reference-semantics/semantics/core.k:77-77 [19] rule; attributes: none

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### reference-semantics/semantics/core.k:78-84 [20] rule; attributes: function, owise

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### reference-semantics/semantics/core.k:85-88 [21] rule; attributes: none

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### reference-semantics/semantics/core.k:95-95 [22] syntax; attributes: none

```k
  syntax Val ::= kwV(String, Val)
```

### reference-semantics/semantics/core.k:96-96 [23] syntax; attributes: none

```k
  syntax KItem ::= #kwTag(String)
```

### reference-semantics/semantics/core.k:97-97 [24] rule; attributes: none

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### reference-semantics/semantics/core.k:98-98 [25] rule; attributes: none

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
```

### reference-semantics/semantics/core.k:100-100 [26] syntax; attributes: function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### reference-semantics/semantics/core.k:101-101 [27] rule; attributes: none

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### reference-semantics/semantics/core.k:102-105 [28] rule; attributes: owise

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### reference-semantics/semantics/core.k:106-106 [29] syntax; attributes: none

```k
  syntax Val ::= cellsMark(ParamNames)
```

### reference-semantics/semantics/core.k:107-107 [30] syntax; attributes: function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### reference-semantics/semantics/core.k:108-108 [31] rule; attributes: none

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### reference-semantics/semantics/core.k:109-109 [32] syntax; attributes: function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### reference-semantics/semantics/core.k:110-110 [33] rule; attributes: none

```k
  rule pnMember(_:String, .ParamNames) => false
```

### reference-semantics/semantics/core.k:111-111 [34] rule; attributes: none

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### reference-semantics/semantics/core.k:113-113 [35] syntax; attributes: none

```k
  syntax KItem ::= #cellW(Val, Val)
```

### reference-semantics/semantics/core.k:114-115 [36] rule; attributes: none

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### reference-semantics/semantics/core.k:117-117 [37] syntax; attributes: none

```k
  syntax KItem ::= #alloc(Val)
```

### reference-semantics/semantics/core.k:118-120 [38] rule; attributes: none

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

### reference-semantics/semantics/core.k:124-124 [39] syntax; attributes: none

```k
  syntax KItem ::= #loadAll(Module)
```

### reference-semantics/semantics/core.k:125-125 [40] rule; attributes: none

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### reference-semantics/semantics/core.k:126-126 [41] rule; attributes: none

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### reference-semantics/semantics/core.k:127-129 [42] rule; attributes: none

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### reference-semantics/semantics/core.k:130-130 [43] syntax; attributes: none

```k
  syntax KItem ::= #look(String, Int)
```

### reference-semantics/semantics/core.k:131-131 [44] rule; attributes: none

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### reference-semantics/semantics/core.k:132-133 [45] rule; attributes: none

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
```

### reference-semantics/semantics/core.k:145-147 [46] rule; attributes: none

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### reference-semantics/semantics/core.k:152-153 [47] rule; attributes: none

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
```

### reference-semantics/semantics/core.k:157-157 [48] syntax; attributes: function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### reference-semantics/semantics/core.k:158-184 [49] rule; attributes: none

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

### reference-semantics/semantics/core.k:185-185 [50] syntax; attributes: none

```k
  syntax ApplyK ::= toCall(Val)
```

### reference-semantics/semantics/core.k:186-188 [51] syntax; attributes: none

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### reference-semantics/semantics/core.k:189-189 [52] rule; attributes: none

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### reference-semantics/semantics/core.k:190-190 [53] rule; attributes: none

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### reference-semantics/semantics/core.k:191-193 [54] rule; attributes: none

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### reference-semantics/semantics/core.k:194-194 [55] rule; attributes: none

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### reference-semantics/semantics/core.k:195-195 [56] rule; attributes: none

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### reference-semantics/semantics/core.k:196-198 [57] rule; attributes: none

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### reference-semantics/semantics/core.k:199-199 [58] syntax; attributes: function

```k
  syntax Bool ::= truthy(Val) [function]
```

### reference-semantics/semantics/core.k:200-200 [59] rule; attributes: none

```k
  rule truthy(B:Bool)          => B
```

### reference-semantics/semantics/core.k:201-201 [60] rule; attributes: none

```k
  rule truthy(noneV)           => false
```

### reference-semantics/semantics/core.k:202-202 [61] rule; attributes: none

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### reference-semantics/semantics/core.k:203-203 [62] rule; attributes: none

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### reference-semantics/semantics/core.k:204-204 [63] rule; attributes: none

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### reference-semantics/semantics/core.k:205-207 [64] rule; attributes: none

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### reference-semantics/semantics/core.k:208-208 [65] syntax; attributes: function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### reference-semantics/semantics/core.k:209-209 [66] syntax; attributes: function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### reference-semantics/semantics/core.k:210-212 [67] syntax; attributes: function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### reference-semantics/semantics/core.k:213-213 [68] syntax; attributes: function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### reference-semantics/semantics/core.k:214-214 [69] rule; attributes: none

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### reference-semantics/semantics/core.k:215-215 [70] rule; attributes: none

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### reference-semantics/semantics/core.k:217-217 [71] syntax; attributes: function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### reference-semantics/semantics/core.k:218-218 [72] rule; attributes: none

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### reference-semantics/semantics/core.k:219-222 [73] rule; attributes: none

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### reference-semantics/semantics/core.k:223-223 [74] syntax; attributes: function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### reference-semantics/semantics/core.k:224-224 [75] rule; attributes: none

```k
  rule vsLen(.ValSeq)                => 0
```

### reference-semantics/semantics/core.k:225-225 [76] rule; attributes: none

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### reference-semantics/semantics/core.k:227-227 [77] syntax; attributes: function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### reference-semantics/semantics/core.k:228-228 [78] rule; attributes: none

```k
  rule isLen(.IntSeq)                => 0
```

### reference-semantics/semantics/core.k:229-232 [79] rule; attributes: total

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### reference-semantics/semantics/core.k:233-233 [80] syntax; attributes: function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### reference-semantics/semantics/core.k:234-234 [81] rule; attributes: none

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### reference-semantics/semantics/core.k:235-235 [82] rule; attributes: none

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### reference-semantics/semantics/core.k:236-236 [83] rule; attributes: none

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
```

### reference-semantics/semantics/core.k:238-238 [84] rule; attributes: none

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
```

## reference-semantics/semantics/dict.k

Count: 40; rule=28, syntax=12

### reference-semantics/semantics/dict.k:20-22 [1] syntax; attributes: none

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### reference-semantics/semantics/dict.k:23-25 [2] syntax; attributes: none

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### reference-semantics/semantics/dict.k:26-26 [3] rule; attributes: none

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### reference-semantics/semantics/dict.k:27-27 [4] rule; attributes: none

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:28-29 [5] rule; attributes: none

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:30-31 [6] rule; attributes: none

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:32-36 [7] rule; attributes: total

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### reference-semantics/semantics/dict.k:37-37 [8] syntax; attributes: function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/dict.k:38-38 [9] rule; attributes: none

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### reference-semantics/semantics/dict.k:39-39 [10] rule; attributes: none

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### reference-semantics/semantics/dict.k:40-42 [11] rule; attributes: none

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### reference-semantics/semantics/dict.k:43-43 [12] syntax; attributes: function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/dict.k:44-44 [13] rule; attributes: none

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### reference-semantics/semantics/dict.k:45-48 [14] rule; attributes: owise

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### reference-semantics/semantics/dict.k:49-49 [15] syntax; attributes: function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### reference-semantics/semantics/dict.k:50-50 [16] rule; attributes: none

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
```

### reference-semantics/semantics/dict.k:52-52 [17] rule; attributes: none

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
```

### reference-semantics/semantics/dict.k:54-57 [18] rule; attributes: owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### reference-semantics/semantics/dict.k:58-62 [19] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### reference-semantics/semantics/dict.k:63-63 [20] rule; attributes: none

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### reference-semantics/semantics/dict.k:64-64 [21] syntax; attributes: function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### reference-semantics/semantics/dict.k:65-69 [22] rule; attributes: priority(45)

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### reference-semantics/semantics/dict.k:70-70 [23] syntax; attributes: function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### reference-semantics/semantics/dict.k:71-75 [24] rule; attributes: none

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### reference-semantics/semantics/dict.k:76-76 [25] syntax; attributes: none

```k
  syntax KItem ::= #dsetK(String, Val)
```

### reference-semantics/semantics/dict.k:77-77 [26] rule; attributes: none

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### reference-semantics/semantics/dict.k:78-80 [27] rule; attributes: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
```

### reference-semantics/semantics/dict.k:82-84 [28] rule; attributes: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/dict.k:86-86 [29] syntax; attributes: none

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### reference-semantics/semantics/dict.k:87-89 [30] rule; attributes: none

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### reference-semantics/semantics/dict.k:90-90 [31] syntax; attributes: function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### reference-semantics/semantics/dict.k:91-91 [32] rule; attributes: none

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### reference-semantics/semantics/dict.k:92-94 [33] rule; attributes: none

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### reference-semantics/semantics/dict.k:95-96 [34] rule; attributes: none

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### reference-semantics/semantics/dict.k:97-97 [35] syntax; attributes: function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### reference-semantics/semantics/dict.k:98-98 [36] rule; attributes: none

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### reference-semantics/semantics/dict.k:99-100 [37] rule; attributes: none

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### reference-semantics/semantics/dict.k:101-101 [38] syntax; attributes: function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### reference-semantics/semantics/dict.k:102-102 [39] rule; attributes: none

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### reference-semantics/semantics/dict.k:103-103 [40] rule; attributes: none

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## reference-semantics/semantics/float.k

Count: 155; rule=121, syntax=34

### reference-semantics/semantics/float.k:20-20 [1] syntax; attributes: none

```k
  syntax Val ::= Float
```

### reference-semantics/semantics/float.k:21-23 [2] rule; attributes: no-evaluators

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### reference-semantics/semantics/float.k:24-24 [3] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### reference-semantics/semantics/float.k:25-25 [4] rule; attributes: none

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### reference-semantics/semantics/float.k:27-29 [5] rule; attributes: none

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### reference-semantics/semantics/float.k:30-30 [6] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### reference-semantics/semantics/float.k:31-31 [7] rule; attributes: none

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:32-36 [8] rule; attributes: none

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### reference-semantics/semantics/float.k:37-37 [9] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### reference-semantics/semantics/float.k:38-38 [10] rule; attributes: none

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### reference-semantics/semantics/float.k:39-42 [11] rule; attributes: none

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### reference-semantics/semantics/float.k:43-43 [12] rule; attributes: none

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### reference-semantics/semantics/float.k:44-49 [13] rule; attributes: no-evaluators

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### reference-semantics/semantics/float.k:50-50 [14] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### reference-semantics/semantics/float.k:51-51 [15] rule; attributes: none

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### reference-semantics/semantics/float.k:52-52 [16] rule; attributes: none

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### reference-semantics/semantics/float.k:54-54 [17] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### reference-semantics/semantics/float.k:55-55 [18] rule; attributes: none

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### reference-semantics/semantics/float.k:56-60 [19] rule; attributes: none

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### reference-semantics/semantics/float.k:61-64 [20] rule; attributes: none

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### reference-semantics/semantics/float.k:65-65 [21] syntax; attributes: none

```k
  syntax KItem ::= "#mathCeil"
```

### reference-semantics/semantics/float.k:66-66 [22] rule; attributes: priority(40)

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:67-69 [23] rule; attributes: none

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### reference-semantics/semantics/float.k:70-70 [24] syntax; attributes: none

```k
  syntax KItem ::= "#mathFloor"
```

### reference-semantics/semantics/float.k:71-71 [25] rule; attributes: priority(40)

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:72-72 [26] rule; attributes: none

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### reference-semantics/semantics/float.k:73-73 [27] syntax; attributes: function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### reference-semantics/semantics/float.k:74-74 [28] rule; attributes: none

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### reference-semantics/semantics/float.k:75-77 [29] rule; attributes: none

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### reference-semantics/semantics/float.k:78-78 [30] rule; attributes: none

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### reference-semantics/semantics/float.k:79-81 [31] rule; attributes: none

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### reference-semantics/semantics/float.k:82-82 [32] syntax; attributes: none

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### reference-semantics/semantics/float.k:83-83 [33] rule; attributes: priority(40)

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:84-84 [34] rule; attributes: none

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### reference-semantics/semantics/float.k:85-85 [35] rule; attributes: none

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### reference-semantics/semantics/float.k:86-86 [36] syntax; attributes: function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### reference-semantics/semantics/float.k:87-87 [37] rule; attributes: none

```k
  rule toF(F:Float) => F        [concrete]
```

### reference-semantics/semantics/float.k:88-92 [38] rule; attributes: none

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### reference-semantics/semantics/float.k:93-93 [39] syntax; attributes: function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### reference-semantics/semantics/float.k:94-94 [40] rule; attributes: none

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### reference-semantics/semantics/float.k:95-98 [41] rule; attributes: none

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### reference-semantics/semantics/float.k:99-102 [42] rule; attributes: no-evaluators

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### reference-semantics/semantics/float.k:103-103 [43] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### reference-semantics/semantics/float.k:104-104 [44] rule; attributes: none

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### reference-semantics/semantics/float.k:105-105 [45] rule; attributes: none

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### reference-semantics/semantics/float.k:107-107 [46] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### reference-semantics/semantics/float.k:108-108 [47] rule; attributes: none

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### reference-semantics/semantics/float.k:109-109 [48] rule; attributes: none

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### reference-semantics/semantics/float.k:111-111 [49] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### reference-semantics/semantics/float.k:112-112 [50] rule; attributes: none

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### reference-semantics/semantics/float.k:113-113 [51] rule; attributes: none

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### reference-semantics/semantics/float.k:115-115 [52] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### reference-semantics/semantics/float.k:116-116 [53] rule; attributes: none

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### reference-semantics/semantics/float.k:117-117 [54] rule; attributes: none

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### reference-semantics/semantics/float.k:119-119 [55] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### reference-semantics/semantics/float.k:120-120 [56] rule; attributes: none

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### reference-semantics/semantics/float.k:121-124 [57] rule; attributes: none

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### reference-semantics/semantics/float.k:125-125 [58] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### reference-semantics/semantics/float.k:126-126 [59] rule; attributes: none

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### reference-semantics/semantics/float.k:127-127 [60] rule; attributes: none

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### reference-semantics/semantics/float.k:128-128 [61] rule; attributes: none

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### reference-semantics/semantics/float.k:129-131 [62] rule; attributes: none

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### reference-semantics/semantics/float.k:132-132 [63] rule; attributes: none

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### reference-semantics/semantics/float.k:133-133 [64] rule; attributes: none

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### reference-semantics/semantics/float.k:134-134 [65] rule; attributes: none

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### reference-semantics/semantics/float.k:135-135 [66] rule; attributes: none

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### reference-semantics/semantics/float.k:136-136 [67] rule; attributes: none

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### reference-semantics/semantics/float.k:137-137 [68] rule; attributes: none

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### reference-semantics/semantics/float.k:138-138 [69] rule; attributes: none

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### reference-semantics/semantics/float.k:139-141 [70] rule; attributes: none

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### reference-semantics/semantics/float.k:142-142 [71] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### reference-semantics/semantics/float.k:143-143 [72] rule; attributes: none

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### reference-semantics/semantics/float.k:144-144 [73] rule; attributes: none

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### reference-semantics/semantics/float.k:145-145 [74] rule; attributes: none

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### reference-semantics/semantics/float.k:146-146 [75] rule; attributes: none

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### reference-semantics/semantics/float.k:147-147 [76] rule; attributes: none

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### reference-semantics/semantics/float.k:148-148 [77] rule; attributes: none

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### reference-semantics/semantics/float.k:149-149 [78] rule; attributes: none

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### reference-semantics/semantics/float.k:150-150 [79] rule; attributes: none

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### reference-semantics/semantics/float.k:151-153 [80] rule; attributes: none

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### reference-semantics/semantics/float.k:154-154 [81] rule; attributes: none

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### reference-semantics/semantics/float.k:155-159 [82] rule; attributes: none

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### reference-semantics/semantics/float.k:160-160 [83] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### reference-semantics/semantics/float.k:161-161 [84] rule; attributes: none

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### reference-semantics/semantics/float.k:162-163 [85] rule; attributes: none

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
```

### reference-semantics/semantics/float.k:165-165 [86] syntax; attributes: function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### reference-semantics/semantics/float.k:166-166 [87] rule; attributes: none

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### reference-semantics/semantics/float.k:167-167 [88] syntax; attributes: function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:168-168 [89] rule; attributes: none

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### reference-semantics/semantics/float.k:169-169 [90] rule; attributes: none

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:170-170 [91] rule; attributes: none

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### reference-semantics/semantics/float.k:171-171 [92] rule; attributes: none

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
```

### reference-semantics/semantics/float.k:173-173 [93] syntax; attributes: function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:174-174 [94] rule; attributes: none

```k
  rule fracPart(.IntSeq) => 0
```

### reference-semantics/semantics/float.k:175-175 [95] rule; attributes: none

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### reference-semantics/semantics/float.k:176-176 [96] rule; attributes: none

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### reference-semantics/semantics/float.k:177-177 [97] rule; attributes: none

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:178-178 [98] rule; attributes: none

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### reference-semantics/semantics/float.k:179-179 [99] syntax; attributes: function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:180-180 [100] rule; attributes: none

```k
  rule fracScale(.IntSeq) => 1
```

### reference-semantics/semantics/float.k:181-181 [101] rule; attributes: none

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### reference-semantics/semantics/float.k:182-182 [102] rule; attributes: none

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### reference-semantics/semantics/float.k:183-183 [103] rule; attributes: none

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:184-184 [104] rule; attributes: none

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### reference-semantics/semantics/float.k:185-185 [105] rule; attributes: none

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### reference-semantics/semantics/float.k:186-186 [106] rule; attributes: none

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### reference-semantics/semantics/float.k:187-189 [107] rule; attributes: none

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### reference-semantics/semantics/float.k:190-190 [108] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### reference-semantics/semantics/float.k:191-191 [109] rule; attributes: none

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:192-194 [110] rule; attributes: none

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### reference-semantics/semantics/float.k:195-195 [111] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### reference-semantics/semantics/float.k:196-196 [112] rule; attributes: none

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:197-197 [113] rule; attributes: none

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### reference-semantics/semantics/float.k:198-198 [114] rule; attributes: none

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### reference-semantics/semantics/float.k:199-199 [115] rule; attributes: none

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### reference-semantics/semantics/float.k:200-200 [116] rule; attributes: none

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### reference-semantics/semantics/float.k:201-201 [117] rule; attributes: none

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### reference-semantics/semantics/float.k:202-202 [118] rule; attributes: none

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### reference-semantics/semantics/float.k:203-203 [119] rule; attributes: none

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### reference-semantics/semantics/float.k:204-204 [120] rule; attributes: none

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### reference-semantics/semantics/float.k:205-205 [121] rule; attributes: none

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### reference-semantics/semantics/float.k:206-208 [122] rule; attributes: none

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### reference-semantics/semantics/float.k:209-209 [123] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### reference-semantics/semantics/float.k:210-210 [124] rule; attributes: none

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### reference-semantics/semantics/float.k:211-211 [125] rule; attributes: none

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### reference-semantics/semantics/float.k:213-213 [126] rule; attributes: none

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### reference-semantics/semantics/float.k:214-216 [127] rule; attributes: none

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### reference-semantics/semantics/float.k:217-217 [128] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### reference-semantics/semantics/float.k:218-222 [129] rule; attributes: none

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### reference-semantics/semantics/float.k:223-223 [130] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### reference-semantics/semantics/float.k:224-226 [131] rule; attributes: none

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:227-227 [132] rule; attributes: none

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### reference-semantics/semantics/float.k:228-228 [133] rule; attributes: none

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### reference-semantics/semantics/float.k:230-230 [134] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### reference-semantics/semantics/float.k:231-231 [135] rule; attributes: none

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### reference-semantics/semantics/float.k:232-232 [136] syntax; attributes: none

```k
  syntax KItem ::= "#mathSqrt"
```

### reference-semantics/semantics/float.k:233-233 [137] rule; attributes: priority(40)

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:234-234 [138] rule; attributes: none

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### reference-semantics/semantics/float.k:235-242 [139] rule; attributes: none

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### reference-semantics/semantics/float.k:243-243 [140] syntax; attributes: none

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### reference-semantics/semantics/float.k:244-244 [141] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### reference-semantics/semantics/float.k:245-245 [142] rule; attributes: none

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### reference-semantics/semantics/float.k:246-246 [143] rule; attributes: none

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### reference-semantics/semantics/float.k:247-247 [144] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:250-250 [145] syntax; attributes: none

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### reference-semantics/semantics/float.k:251-251 [146] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### reference-semantics/semantics/float.k:252-252 [147] rule; attributes: none

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### reference-semantics/semantics/float.k:253-253 [148] rule; attributes: none

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### reference-semantics/semantics/float.k:254-254 [149] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:261-261 [150] syntax; attributes: none

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### reference-semantics/semantics/float.k:262-263 [151] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:265-265 [152] rule; attributes: none

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### reference-semantics/semantics/float.k:266-266 [153] rule; attributes: none

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### reference-semantics/semantics/float.k:267-268 [154] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:270-271 [155] rule; attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
```

## reference-semantics/semantics/functions.k

Count: 19; rule=15, syntax=4

### reference-semantics/semantics/functions.k:8-13 [1] syntax; attributes: none

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### reference-semantics/semantics/functions.k:14-16 [2] rule; attributes: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### reference-semantics/semantics/functions.k:18-18 [3] syntax; attributes: none

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### reference-semantics/semantics/functions.k:19-26 [4] rule; attributes: none

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### reference-semantics/semantics/functions.k:27-30 [5] syntax; attributes: none

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### reference-semantics/semantics/functions.k:31-32 [6] syntax; attributes: none

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### reference-semantics/semantics/functions.k:33-35 [7] rule; attributes: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### reference-semantics/semantics/functions.k:36-40 [8] rule; attributes: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/functions.k:42-45 [9] rule; attributes: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### reference-semantics/semantics/functions.k:47-49 [10] rule; attributes: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### reference-semantics/semantics/functions.k:50-52 [11] rule; attributes: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### reference-semantics/semantics/functions.k:53-57 [12] rule; attributes: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/functions.k:59-62 [13] rule; attributes: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### reference-semantics/semantics/functions.k:63-63 [14] rule; attributes: none

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### reference-semantics/semantics/functions.k:64-67 [15] rule; attributes: none

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### reference-semantics/semantics/functions.k:68-71 [16] rule; attributes: none

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/functions.k:78-79 [17] rule; attributes: none

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### reference-semantics/semantics/functions.k:80-84 [18] rule; attributes: none

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### reference-semantics/semantics/functions.k:85-90 [19] rule; attributes: none

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## reference-semantics/semantics/int.k

Count: 17; rule=16, syntax=1

### reference-semantics/semantics/int.k:7-7 [1] rule; attributes: none

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### reference-semantics/semantics/int.k:9-10 [2] rule; attributes: none

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### reference-semantics/semantics/int.k:11-11 [3] rule; attributes: none

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### reference-semantics/semantics/int.k:12-12 [4] rule; attributes: none

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### reference-semantics/semantics/int.k:13-13 [5] rule; attributes: none

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### reference-semantics/semantics/int.k:14-14 [6] rule; attributes: none

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### reference-semantics/semantics/int.k:15-15 [7] rule; attributes: none

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### reference-semantics/semantics/int.k:16-16 [8] rule; attributes: none

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### reference-semantics/semantics/int.k:17-17 [9] rule; attributes: none

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### reference-semantics/semantics/int.k:19-19 [10] syntax; attributes: function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### reference-semantics/semantics/int.k:20-20 [11] rule; attributes: none

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### reference-semantics/semantics/int.k:22-22 [12] rule; attributes: none

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### reference-semantics/semantics/int.k:23-23 [13] rule; attributes: none

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### reference-semantics/semantics/int.k:24-24 [14] rule; attributes: none

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### reference-semantics/semantics/int.k:25-25 [15] rule; attributes: none

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### reference-semantics/semantics/int.k:26-26 [16] rule; attributes: none

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### reference-semantics/semantics/int.k:27-27 [17] rule; attributes: none

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## reference-semantics/semantics/iter.k

Count: 1; syntax=1

### reference-semantics/semantics/iter.k:8-8 [1] syntax; attributes: none

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## reference-semantics/semantics/list.k

Count: 32; rule=27, syntax=5

### reference-semantics/semantics/list.k:9-9 [1] rule; attributes: none

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### reference-semantics/semantics/list.k:10-12 [2] rule; attributes: none

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### reference-semantics/semantics/list.k:13-13 [3] syntax; attributes: none

```k
  syntax ApplyK ::= "toList"
```

### reference-semantics/semantics/list.k:14-14 [4] rule; attributes: none

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### reference-semantics/semantics/list.k:15-17 [5] rule; attributes: none

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### reference-semantics/semantics/list.k:18-18 [6] syntax; attributes: function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/list.k:19-19 [7] rule; attributes: none

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### reference-semantics/semantics/list.k:20-23 [8] rule; attributes: priority(45)

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### reference-semantics/semantics/list.k:24-25 [9] rule; attributes: priority(45)

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### reference-semantics/semantics/list.k:27-27 [10] rule; attributes: none

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### reference-semantics/semantics/list.k:28-32 [11] rule; attributes: none

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### reference-semantics/semantics/list.k:33-33 [12] syntax; attributes: function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### reference-semantics/semantics/list.k:34-34 [13] rule; attributes: none

```k
  rule hasRefVS(.ValSeq)                => false
```

### reference-semantics/semantics/list.k:35-35 [14] rule; attributes: none

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### reference-semantics/semantics/list.k:37-38 [15] syntax; attributes: function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### reference-semantics/semantics/list.k:39-39 [16] rule; attributes: none

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### reference-semantics/semantics/list.k:40-40 [17] rule; attributes: none

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### reference-semantics/semantics/list.k:41-41 [18] rule; attributes: none

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### reference-semantics/semantics/list.k:42-43 [19] rule; attributes: none

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### reference-semantics/semantics/list.k:45-45 [20] rule; attributes: none

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
```

### reference-semantics/semantics/list.k:47-47 [21] rule; attributes: none

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
```

### reference-semantics/semantics/list.k:49-49 [22] rule; attributes: none

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### reference-semantics/semantics/list.k:50-52 [23] rule; attributes: owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### reference-semantics/semantics/list.k:53-57 [24] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### reference-semantics/semantics/list.k:58-58 [25] syntax; attributes: none

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### reference-semantics/semantics/list.k:59-59 [26] rule; attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### reference-semantics/semantics/list.k:60-60 [27] rule; attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### reference-semantics/semantics/list.k:61-61 [28] rule; attributes: none

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### reference-semantics/semantics/list.k:62-62 [29] rule; attributes: none

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### reference-semantics/semantics/list.k:63-63 [30] rule; attributes: none

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
```

### reference-semantics/semantics/list.k:65-65 [31] rule; attributes: none

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
```

### reference-semantics/semantics/list.k:67-67 [32] rule; attributes: none

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## reference-semantics/semantics/methods.k

Count: 102; rule=75, syntax=27

### reference-semantics/semantics/methods.k:10-12 [1] syntax; attributes: function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### reference-semantics/semantics/methods.k:13-13 [2] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### reference-semantics/semantics/methods.k:14-14 [3] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### reference-semantics/semantics/methods.k:15-15 [4] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### reference-semantics/semantics/methods.k:16-18 [5] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### reference-semantics/semantics/methods.k:19-19 [6] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### reference-semantics/semantics/methods.k:20-20 [7] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### reference-semantics/semantics/methods.k:21-25 [8] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### reference-semantics/semantics/methods.k:26-26 [9] rule; attributes: none

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### reference-semantics/semantics/methods.k:27-27 [10] syntax; attributes: function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/methods.k:28-28 [11] rule; attributes: none

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:29-29 [12] rule; attributes: none

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### reference-semantics/semantics/methods.k:30-33 [13] rule; attributes: none

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### reference-semantics/semantics/methods.k:34-34 [14] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### reference-semantics/semantics/methods.k:35-35 [15] syntax; attributes: function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### reference-semantics/semantics/methods.k:36-36 [16] rule; attributes: none

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### reference-semantics/semantics/methods.k:37-37 [17] rule; attributes: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
```

### reference-semantics/semantics/methods.k:39-39 [18] rule; attributes: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
```

### reference-semantics/semantics/methods.k:41-41 [19] syntax; attributes: function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/methods.k:42-42 [20] rule; attributes: none

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### reference-semantics/semantics/methods.k:43-43 [21] rule; attributes: owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### reference-semantics/semantics/methods.k:44-46 [22] rule; attributes: none

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### reference-semantics/semantics/methods.k:47-47 [23] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### reference-semantics/semantics/methods.k:48-48 [24] syntax; attributes: function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:49-49 [25] rule; attributes: none

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:50-50 [26] rule; attributes: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### reference-semantics/semantics/methods.k:51-51 [27] rule; attributes: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### reference-semantics/semantics/methods.k:52-52 [28] syntax; attributes: function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:53-53 [29] rule; attributes: none

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### reference-semantics/semantics/methods.k:54-54 [30] rule; attributes: none

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### reference-semantics/semantics/methods.k:55-57 [31] rule; attributes: none

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### reference-semantics/semantics/methods.k:58-60 [32] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### reference-semantics/semantics/methods.k:61-63 [33] rule; attributes: none

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### reference-semantics/semantics/methods.k:64-64 [34] rule; attributes: none

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### reference-semantics/semantics/methods.k:65-65 [35] syntax; attributes: function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/methods.k:66-66 [36] rule; attributes: none

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### reference-semantics/semantics/methods.k:67-67 [37] rule; attributes: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### reference-semantics/semantics/methods.k:68-71 [38] rule; attributes: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### reference-semantics/semantics/methods.k:72-74 [39] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/methods.k:75-75 [40] syntax; attributes: function

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### reference-semantics/semantics/methods.k:76-76 [41] rule; attributes: none

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### reference-semantics/semantics/methods.k:77-77 [42] rule; attributes: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
```

### reference-semantics/semantics/methods.k:79-79 [43] rule; attributes: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
```

### reference-semantics/semantics/methods.k:82-82 [44] syntax; attributes: function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### reference-semantics/semantics/methods.k:83-83 [45] rule; attributes: none

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### reference-semantics/semantics/methods.k:84-84 [46] rule; attributes: none

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### reference-semantics/semantics/methods.k:85-85 [47] syntax; attributes: function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:86-88 [48] rule; attributes: none

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### reference-semantics/semantics/methods.k:89-93 [49] rule; attributes: priority(39)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### reference-semantics/semantics/methods.k:94-96 [50] rule; attributes: priority(40)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/methods.k:97-97 [51] syntax; attributes: function

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### reference-semantics/semantics/methods.k:98-98 [52] rule; attributes: none

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### reference-semantics/semantics/methods.k:99-99 [53] rule; attributes: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
```

### reference-semantics/semantics/methods.k:101-101 [54] rule; attributes: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
```

### reference-semantics/semantics/methods.k:104-105 [55] rule; attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### reference-semantics/semantics/methods.k:106-106 [56] syntax; attributes: function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### reference-semantics/semantics/methods.k:107-107 [57] rule; attributes: none

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### reference-semantics/semantics/methods.k:108-108 [58] rule; attributes: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### reference-semantics/semantics/methods.k:109-111 [59] rule; attributes: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### reference-semantics/semantics/methods.k:112-112 [60] syntax; attributes: function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:113-113 [61] rule; attributes: none

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### reference-semantics/semantics/methods.k:115-115 [62] syntax; attributes: function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:116-116 [63] rule; attributes: none

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### reference-semantics/semantics/methods.k:118-118 [64] syntax; attributes: function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:119-119 [65] rule; attributes: none

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### reference-semantics/semantics/methods.k:121-121 [66] syntax; attributes: function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:122-122 [67] rule; attributes: none

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### reference-semantics/semantics/methods.k:124-124 [68] syntax; attributes: function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:125-125 [69] rule; attributes: none

```k
  rule hasUpper(.IntSeq) => false
```

### reference-semantics/semantics/methods.k:126-126 [70] rule; attributes: none

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### reference-semantics/semantics/methods.k:128-128 [71] syntax; attributes: function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:129-129 [72] rule; attributes: none

```k
  rule hasLower(.IntSeq) => false
```

### reference-semantics/semantics/methods.k:130-130 [73] rule; attributes: none

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### reference-semantics/semantics/methods.k:132-132 [74] syntax; attributes: function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:133-133 [75] rule; attributes: none

```k
  rule allAlpha(.IntSeq) => true
```

### reference-semantics/semantics/methods.k:134-134 [76] rule; attributes: none

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### reference-semantics/semantics/methods.k:136-136 [77] syntax; attributes: function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:137-137 [78] rule; attributes: none

```k
  rule allDigit(.IntSeq) => true
```

### reference-semantics/semantics/methods.k:138-138 [79] rule; attributes: none

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### reference-semantics/semantics/methods.k:140-140 [80] syntax; attributes: function, total

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:142-142 [81] rule; attributes: none

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### reference-semantics/semantics/methods.k:143-143 [82] rule; attributes: owise

```k
  rule lowerC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:145-145 [83] syntax; attributes: function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:146-146 [84] rule; attributes: none

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### reference-semantics/semantics/methods.k:147-147 [85] rule; attributes: owise

```k
  rule upperC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:149-149 [86] syntax; attributes: function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:150-150 [87] rule; attributes: none

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### reference-semantics/semantics/methods.k:151-151 [88] rule; attributes: none

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### reference-semantics/semantics/methods.k:152-152 [89] rule; attributes: owise

```k
  rule swapC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:154-154 [90] syntax; attributes: function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:155-155 [91] rule; attributes: none

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:156-156 [92] rule; attributes: none

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### reference-semantics/semantics/methods.k:158-158 [93] syntax; attributes: function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:159-159 [94] rule; attributes: none

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:160-160 [95] rule; attributes: none

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### reference-semantics/semantics/methods.k:162-162 [96] syntax; attributes: function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:163-163 [97] rule; attributes: none

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:164-164 [98] rule; attributes: none

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### reference-semantics/semantics/methods.k:166-166 [99] syntax; attributes: function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:167-167 [100] rule; attributes: none

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### reference-semantics/semantics/methods.k:168-168 [101] rule; attributes: none

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/methods.k:169-169 [102] rule; attributes: none

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## reference-semantics/semantics/operators.k

Count: 12; context=2, rule=10

### reference-semantics/semantics/operators.k:10-10 [1] rule; attributes: none

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### reference-semantics/semantics/operators.k:12-14 [2] rule; attributes: none

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### reference-semantics/semantics/operators.k:15-15 [3] context; attributes: none

```k
  context Compare(HOLE, _)
```

### reference-semantics/semantics/operators.k:16-16 [4] context; attributes: none

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### reference-semantics/semantics/operators.k:17-17 [5] rule; attributes: owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### reference-semantics/semantics/operators.k:19-19 [6] rule; attributes: none

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### reference-semantics/semantics/operators.k:20-24 [7] rule; attributes: priority(40)

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### reference-semantics/semantics/operators.k:25-27 [8] rule; attributes: priority(40)

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/operators.k:28-29 [9] rule; attributes: none

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/operators.k:34-35 [10] rule; attributes: none

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/operators.k:38-39 [11] rule; attributes: none

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/operators.k:44-46 [12] rule; attributes: priority(40)

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## reference-semantics/semantics/range.k

Count: 8; rule=6, syntax=2

### reference-semantics/semantics/range.k:9-9 [1] syntax; attributes: function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/range.k:10-10 [2] rule; attributes: none

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### reference-semantics/semantics/range.k:12-12 [3] syntax; attributes: function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### reference-semantics/semantics/range.k:13-13 [4] rule; attributes: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
```

### reference-semantics/semantics/range.k:15-15 [5] rule; attributes: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
```

### reference-semantics/semantics/range.k:17-17 [6] rule; attributes: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
```

### reference-semantics/semantics/range.k:20-21 [7] rule; attributes: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
```

### reference-semantics/semantics/range.k:23-23 [8] rule; attributes: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
```

## reference-semantics/semantics/set.k

Count: 18; rule=12, syntax=6

### reference-semantics/semantics/set.k:8-10 [1] syntax; attributes: none

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### reference-semantics/semantics/set.k:11-11 [2] syntax; attributes: function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:12-12 [3] rule; attributes: none

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### reference-semantics/semantics/set.k:13-15 [4] rule; attributes: none

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### reference-semantics/semantics/set.k:16-17 [5] syntax; attributes: function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### reference-semantics/semantics/set.k:18-18 [6] rule; attributes: none

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### reference-semantics/semantics/set.k:19-19 [7] rule; attributes: none

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### reference-semantics/semantics/set.k:20-20 [8] rule; attributes: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
```

### reference-semantics/semantics/set.k:22-22 [9] rule; attributes: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
```

### reference-semantics/semantics/set.k:25-25 [10] syntax; attributes: function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/set.k:26-26 [11] rule; attributes: none

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### reference-semantics/semantics/set.k:27-30 [12] rule; attributes: none

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### reference-semantics/semantics/set.k:31-31 [13] syntax; attributes: function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:32-32 [14] rule; attributes: none

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### reference-semantics/semantics/set.k:33-33 [15] rule; attributes: none

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### reference-semantics/semantics/set.k:35-35 [16] syntax; attributes: function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:36-38 [17] rule; attributes: none

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### reference-semantics/semantics/set.k:39-39 [18] rule; attributes: none

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## reference-semantics/semantics/sort.k

Count: 25; rule=19, syntax=6

### reference-semantics/semantics/sort.k:18-18 [1] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### reference-semantics/semantics/sort.k:19-19 [2] syntax; attributes: function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### reference-semantics/semantics/sort.k:20-20 [3] rule; attributes: none

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### reference-semantics/semantics/sort.k:21-21 [4] rule; attributes: none

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### reference-semantics/semantics/sort.k:22-22 [5] rule; attributes: none

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### reference-semantics/semantics/sort.k:23-23 [6] rule; attributes: none

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### reference-semantics/semantics/sort.k:24-25 [7] rule; attributes: none

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### reference-semantics/semantics/sort.k:26-26 [8] syntax; attributes: function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### reference-semantics/semantics/sort.k:27-27 [9] rule; attributes: none

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### reference-semantics/semantics/sort.k:28-28 [10] rule; attributes: none

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### reference-semantics/semantics/sort.k:29-29 [11] rule; attributes: none

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
```

### reference-semantics/semantics/sort.k:31-31 [12] rule; attributes: none

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
```

### reference-semantics/semantics/sort.k:36-39 [13] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### reference-semantics/semantics/sort.k:40-48 [14] rule; attributes: priority(40)

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

### reference-semantics/semantics/sort.k:49-49 [15] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### reference-semantics/semantics/sort.k:51-52 [16] syntax; attributes: function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/sort.k:53-53 [17] rule; attributes: none

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### reference-semantics/semantics/sort.k:54-54 [18] rule; attributes: none

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### reference-semantics/semantics/sort.k:55-55 [19] rule; attributes: none

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### reference-semantics/semantics/sort.k:57-57 [20] syntax; attributes: function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### reference-semantics/semantics/sort.k:58-58 [21] rule; attributes: none

```k
  rule condRev(S:ValSeq, false) => S
```

### reference-semantics/semantics/sort.k:59-59 [22] rule; attributes: none

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### reference-semantics/semantics/sort.k:61-62 [23] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### reference-semantics/semantics/sort.k:63-64 [24] rule; attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### reference-semantics/semantics/sort.k:65-71 [25] rule; attributes: total

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

## reference-semantics/semantics/str.k

Count: 33; rule=28, syntax=5

### reference-semantics/semantics/str.k:8-8 [1] rule; attributes: none

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### reference-semantics/semantics/str.k:9-12 [2] rule; attributes: none

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### reference-semantics/semantics/str.k:13-13 [3] syntax; attributes: function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### reference-semantics/semantics/str.k:14-14 [4] rule; attributes: none

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### reference-semantics/semantics/str.k:15-15 [5] rule; attributes: none

```k
  rule strToCodes("") => .IntSeq
```

### reference-semantics/semantics/str.k:16-16 [6] rule; attributes: none

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
```

### reference-semantics/semantics/str.k:20-20 [7] syntax; attributes: function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:21-21 [8] rule; attributes: none

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### reference-semantics/semantics/str.k:22-22 [9] rule; attributes: none

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### reference-semantics/semantics/str.k:24-24 [10] rule; attributes: none

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### reference-semantics/semantics/str.k:25-25 [11] rule; attributes: none

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### reference-semantics/semantics/str.k:26-28 [12] rule; attributes: none

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### reference-semantics/semantics/str.k:29-29 [13] rule; attributes: none

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### reference-semantics/semantics/str.k:30-30 [14] rule; attributes: none

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### reference-semantics/semantics/str.k:32-32 [15] syntax; attributes: function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:33-33 [16] rule; attributes: none

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### reference-semantics/semantics/str.k:34-34 [17] rule; attributes: none

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/str.k:35-35 [18] rule; attributes: none

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### reference-semantics/semantics/str.k:37-37 [19] syntax; attributes: function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:38-38 [20] rule; attributes: none

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### reference-semantics/semantics/str.k:39-39 [21] rule; attributes: none

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### reference-semantics/semantics/str.k:40-40 [22] rule; attributes: none

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
```

### reference-semantics/semantics/str.k:48-48 [23] syntax; attributes: function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:49-49 [24] rule; attributes: none

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### reference-semantics/semantics/str.k:50-50 [25] rule; attributes: none

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### reference-semantics/semantics/str.k:51-51 [26] rule; attributes: none

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/str.k:52-52 [27] rule; attributes: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### reference-semantics/semantics/str.k:53-53 [28] rule; attributes: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### reference-semantics/semantics/str.k:54-54 [29] rule; attributes: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### reference-semantics/semantics/str.k:56-56 [30] rule; attributes: none

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### reference-semantics/semantics/str.k:57-57 [31] rule; attributes: none

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### reference-semantics/semantics/str.k:58-58 [32] rule; attributes: none

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### reference-semantics/semantics/str.k:59-59 [33] rule; attributes: none

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## reference-semantics/semantics/subscript.k

Count: 57; context=2, rule=40, syntax=15

### reference-semantics/semantics/subscript.k:11-11 [1] syntax; attributes: function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:12-12 [2] rule; attributes: none

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### reference-semantics/semantics/subscript.k:13-13 [3] rule; attributes: none

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
```

### reference-semantics/semantics/subscript.k:16-16 [4] syntax; attributes: function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### reference-semantics/semantics/subscript.k:17-17 [5] rule; attributes: none

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### reference-semantics/semantics/subscript.k:18-18 [6] rule; attributes: none

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
```

### reference-semantics/semantics/subscript.k:21-21 [7] syntax; attributes: function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:22-22 [8] rule; attributes: none

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### reference-semantics/semantics/subscript.k:23-26 [9] rule; attributes: none

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### reference-semantics/semantics/subscript.k:27-27 [10] context; attributes: none

```k
  context Subscript(HOLE, _)
```

### reference-semantics/semantics/subscript.k:28-30 [11] context; attributes: none

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### reference-semantics/semantics/subscript.k:31-33 [12] rule; attributes: priority(40)

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/subscript.k:35-35 [13] rule; attributes: none

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### reference-semantics/semantics/subscript.k:37-37 [14] syntax; attributes: function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### reference-semantics/semantics/subscript.k:38-38 [15] rule; attributes: none

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### reference-semantics/semantics/subscript.k:39-39 [16] rule; attributes: none

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### reference-semantics/semantics/subscript.k:40-43 [17] rule; attributes: none

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### reference-semantics/semantics/subscript.k:44-47 [18] syntax; attributes: none

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### reference-semantics/semantics/subscript.k:49-49 [19] syntax; attributes: none

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### reference-semantics/semantics/subscript.k:50-50 [20] rule; attributes: none

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### reference-semantics/semantics/subscript.k:51-51 [21] rule; attributes: none

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### reference-semantics/semantics/subscript.k:52-52 [22] rule; attributes: none

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### reference-semantics/semantics/subscript.k:54-54 [23] rule; attributes: none

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:55-55 [24] rule; attributes: none

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:56-57 [25] rule; attributes: none

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### reference-semantics/semantics/subscript.k:58-60 [26] rule; attributes: priority(45)

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### reference-semantics/semantics/subscript.k:61-61 [27] rule; attributes: none

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:63-63 [28] syntax; attributes: function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### reference-semantics/semantics/subscript.k:64-65 [29] rule; attributes: none

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### reference-semantics/semantics/subscript.k:66-67 [30] rule; attributes: none

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### reference-semantics/semantics/subscript.k:68-71 [31] rule; attributes: none

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### reference-semantics/semantics/subscript.k:72-72 [32] syntax; attributes: function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### reference-semantics/semantics/subscript.k:73-73 [33] rule; attributes: none

```k
  rule slStep(noB)          => 1
```

### reference-semantics/semantics/subscript.k:74-74 [34] rule; attributes: none

```k
  rule slStep(someB(S:Int)) => S
```

### reference-semantics/semantics/subscript.k:76-76 [35] syntax; attributes: function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### reference-semantics/semantics/subscript.k:77-77 [36] rule; attributes: none

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
```

### reference-semantics/semantics/subscript.k:79-79 [37] rule; attributes: none

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
```

### reference-semantics/semantics/subscript.k:81-81 [38] rule; attributes: none

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### reference-semantics/semantics/subscript.k:83-83 [39] syntax; attributes: function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### reference-semantics/semantics/subscript.k:84-84 [40] rule; attributes: none

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
```

### reference-semantics/semantics/subscript.k:86-86 [41] rule; attributes: none

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
```

### reference-semantics/semantics/subscript.k:88-88 [42] rule; attributes: none

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### reference-semantics/semantics/subscript.k:90-90 [43] syntax; attributes: function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:91-91 [44] rule; attributes: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
```

### reference-semantics/semantics/subscript.k:93-93 [45] rule; attributes: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
```

### reference-semantics/semantics/subscript.k:96-96 [46] syntax; attributes: function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:97-97 [47] rule; attributes: none

```k
  rule clampLo(J:Int, _STEP:Int) => J
```

### reference-semantics/semantics/subscript.k:99-99 [48] rule; attributes: none

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
```

### reference-semantics/semantics/subscript.k:102-102 [49] syntax; attributes: function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:103-103 [50] rule; attributes: none

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
```

### reference-semantics/semantics/subscript.k:105-105 [51] rule; attributes: none

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
```

### reference-semantics/semantics/subscript.k:109-109 [52] syntax; attributes: function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### reference-semantics/semantics/subscript.k:110-111 [53] rule; attributes: none

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
```

### reference-semantics/semantics/subscript.k:113-113 [54] rule; attributes: none

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
```

### reference-semantics/semantics/subscript.k:116-116 [55] syntax; attributes: function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### reference-semantics/semantics/subscript.k:117-118 [56] rule; attributes: none

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
```

### reference-semantics/semantics/subscript.k:120-120 [57] rule; attributes: none

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
```

## reference-semantics/semantics/syntax.k

Count: 16; syntax=16

### reference-semantics/semantics/syntax.k:9-30 [1] syntax; attributes: macro

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

### reference-semantics/semantics/syntax.k:32-32 [2] syntax; attributes: none

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### reference-semantics/semantics/syntax.k:33-33 [3] syntax; attributes: none

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### reference-semantics/semantics/syntax.k:34-34 [4] syntax; attributes: none

```k
  syntax Entries  ::= List{Entry, ","}
```

### reference-semantics/semantics/syntax.k:35-35 [5] syntax; attributes: none

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### reference-semantics/semantics/syntax.k:36-36 [6] syntax; attributes: none

```k
  syntax CompFors ::= List{CompFor, ""}
```

### reference-semantics/semantics/syntax.k:37-37 [7] syntax; attributes: none

```k
  syntax Exprs    ::= List{Expr, ","}
```

### reference-semantics/semantics/syntax.k:38-38 [8] syntax; attributes: none

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### reference-semantics/semantics/syntax.k:39-39 [9] syntax; attributes: none

```k
  syntax Bound    ::= Expr | "NoBound"
```

### reference-semantics/semantics/syntax.k:41-54 [10] syntax; attributes: none

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

### reference-semantics/semantics/syntax.k:56-56 [11] syntax; attributes: none

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### reference-semantics/semantics/syntax.k:57-57 [12] syntax; attributes: none

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:58-58 [13] syntax; attributes: none

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:59-59 [14] syntax; attributes: none

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:60-60 [15] syntax; attributes: none

```k
  syntax ParamNames ::= List{String, ","}
```

### reference-semantics/semantics/syntax.k:61-61 [16] syntax; attributes: none

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## reference-semantics/semantics/tuple.k

Count: 25; rule=21, syntax=4

### reference-semantics/semantics/tuple.k:10-10 [1] rule; attributes: none

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### reference-semantics/semantics/tuple.k:11-13 [2] rule; attributes: none

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### reference-semantics/semantics/tuple.k:14-14 [3] syntax; attributes: none

```k
  syntax ApplyK ::= "toTuple"
```

### reference-semantics/semantics/tuple.k:15-15 [4] rule; attributes: none

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### reference-semantics/semantics/tuple.k:16-16 [5] rule; attributes: none

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### reference-semantics/semantics/tuple.k:18-19 [6] rule; attributes: none

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### reference-semantics/semantics/tuple.k:20-20 [7] rule; attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### reference-semantics/semantics/tuple.k:21-22 [8] rule; attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### reference-semantics/semantics/tuple.k:23-23 [9] rule; attributes: none

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### reference-semantics/semantics/tuple.k:24-24 [10] syntax; attributes: function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### reference-semantics/semantics/tuple.k:25-25 [11] rule; attributes: none

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### reference-semantics/semantics/tuple.k:26-26 [12] rule; attributes: none

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
```

### reference-semantics/semantics/tuple.k:28-30 [13] rule; attributes: none

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### reference-semantics/semantics/tuple.k:31-31 [14] syntax; attributes: none

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### reference-semantics/semantics/tuple.k:32-34 [15] rule; attributes: none

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### reference-semantics/semantics/tuple.k:35-37 [16] rule; attributes: none

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/tuple.k:42-42 [17] rule; attributes: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:43-43 [18] rule; attributes: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:44-48 [19] rule; attributes: priority(40)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### reference-semantics/semantics/tuple.k:49-49 [20] syntax; attributes: none

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### reference-semantics/semantics/tuple.k:50-50 [21] rule; attributes: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:51-51 [22] rule; attributes: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:52-54 [23] rule; attributes: priority(40)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/tuple.k:55-56 [24] rule; attributes: none

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:57-57 [25] rule; attributes: none

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## verification.k

Count: 22; rule=14, syntax=8

### verification.k:9-13 [1] syntax; attributes: function, total, symbol, no-evaluators

```k
  syntax Bool ::= oddDigits(Int)
    [function, total, symbol(oddDigits), no-evaluators]

  // Append precisely the all-odd-digit members of the remaining input to ACC.
  // This accumulator form is the invariant of the source-level for loop.
```

### verification.k:14-14 [2] syntax; attributes: function

```k
  syntax ValSeq ::= filterOddAcc(ValSeq, ValSeq) [function]
```

### verification.k:15-15 [3] rule; attributes: none

```k
  rule filterOddAcc(ACC:ValSeq, .ValSeq) => ACC
```

### verification.k:16-19 [4] rule; attributes: none

```k
  rule filterOddAcc(ACC:ValSeq, vCons(N:Int, REST:ValSeq))
    => filterOddAcc(
         valSeqConcat(ACC, vCons(N, .ValSeq)),
         REST)
```

### verification.k:21-22 [5] rule; attributes: none

```k
  rule filterOddAcc(ACC:ValSeq, vCons(N:Int, REST:ValSeq))
    => filterOddAcc(ACC, REST)
```

### verification.k:25-25 [6] syntax; attributes: function, total

```k
  syntax Val ::= lastInput(Val, ValSeq) [function, total]
```

### verification.k:26-26 [7] rule; attributes: none

```k
  rule lastInput(OLD:Val, .ValSeq) => OLD
```

### verification.k:27-28 [8] rule; attributes: none

```k
  rule lastInput(_:Val, vCons(V:Val, REST:ValSeq))
    => lastInput(V, REST)
```

### verification.k:30-30 [9] syntax; attributes: function, total

```k
  syntax Bool ::= positiveInts(ValSeq) [function, total]
```

### verification.k:31-31 [10] rule; attributes: none

```k
  rule positiveInts(.ValSeq) => true
```

### verification.k:32-33 [11] rule; attributes: none

```k
  rule positiveInts(vCons(N:Int, REST:ValSeq))
    => N >Int 0 andBool positiveInts(REST)
```

### verification.k:34-34 [12] rule; attributes: none

```k
  rule positiveInts(vCons(V:Val, _:ValSeq)) => false
```

### verification.k:37-37 [13] syntax; attributes: macro

```k
  syntax Stmts ::= "digitLoopBody" [macro]
```

### verification.k:38-44 [14] rule; attributes: none

```k
  rule digitLoopBody
    => If(Compare(BinOp("%", Name("n"), Int(2)),
                  CmpOp("==", Int(0))),
          Assign(Name("result"), Bool(false))
          Break,
          .Stmts)
       AugAssign(Name("n"), "//", Int(10))
```

### verification.k:46-46 [15] syntax; attributes: macro

```k
  syntax Stmts ::= "oddDigitsBody" [macro]
```

### verification.k:47-51 [16] rule; attributes: none

```k
  rule oddDigitsBody
    => Assign(Name("result"), Bool(true))
       While(Compare(Name("n"), CmpOp(">", Int(0))),
             digitLoopBody)
       Return(Name("result"))
```

### verification.k:53-53 [17] syntax; attributes: macro

```k
  syntax Stmts ::= "filterLoopBody" [macro]
```

### verification.k:54-57 [18] rule; attributes: none

```k
  rule filterLoopBody
    => If(Call(Name("_all_digits_odd"), Name("n")),
          Expr(Call(Attribute(Name("result"), "append"), Name("n"))),
          .Stmts)
```

### verification.k:59-59 [19] syntax; attributes: macro

```k
  syntax Stmts ::= "uniqueDigitsBody" [macro]
```

### verification.k:60-64 [20] rule; attributes: none

```k
  rule uniqueDigitsBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("n"), Int(0))
       For(Name("n"), Name("x"), filterLoopBody)
       Return(Call(Name("sorted"), Name("result")))
```

### verification.k:76-82 [21] rule; attributes: priority(40)

```k
  rule <k>
         #applyK(
           toCall(closureVal(("n", .ParamNames), oddDigitsBody, 0)),
           (N:Int, .Vals))
         => oddDigits(N)
       ... </k>
    [priority(40)]
```

### verification.k:90-109 [22] rule; attributes: priority(40)

```k
  rule <k>
         #loop(list(INPUT:ValSeq), Name("n"), filterLoopBody)
         => .K
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> OLD:Val
            "result" |-> ref(H:Int)
            "x" |-> X:Val)
           =>
           ("n" |-> lastInput(OLD, INPUT)
            "result" |-> ref(H)
            "x" |-> X),
           P:Parent) ...
       </scopes>
       <heap>
         ... H |-> list(ACC:ValSeq => filterOddAcc(ACC, INPUT)) ...
       </heap>
    [priority(40)]
```

## spec.k

Count: 1; claim=1

### spec.k:9-49 [1] claim; attributes: none

```k
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "_all_digits_odd",
            Params("n"),
            oddDigitsBody)
          FuncDef(
            "unique_digits",
            Params("x"),
            uniqueDigitsBody)))
      ~> Call(Name("unique_digits"), list(INPUT:ValSeq))
    =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(
        "_all_digits_odd" |->
          closureVal(("n", .ParamNames), oddDigitsBody, 0)
        "unique_digits" |->
          closureVal(("x", .ParamNames), uniqueDigitsBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(filterOddAcc(.ValSeq, INPUT))
      1 |-> list(sortVS(filterOddAcc(.ValSeq, INPUT)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
```

# Totals

claim=1, configuration=1, context=5, rule=709, syntax=235

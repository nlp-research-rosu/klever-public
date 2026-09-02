# Exhaustive K declaration inventory

Each numbered entry is one top-level local declaration. Continuation
lines, guards, cells, and attributes are included in its code block.

## Per-file counts

| File | Syntax | Rules | Claims | Configs | Contexts | Attributes |
|---|---:|---:|---:|---:|---:|---|
| `/candidate/reference-semantics/semantics/assert.k` | 0 | 3 | 0 | 0 | 0 | priority=1 |
| `/candidate/reference-semantics/semantics/bool.k` | 0 | 13 | 0 | 0 | 1 | priority=5 |
| `/candidate/reference-semantics/semantics/builtins.k` | 38 | 137 | 0 | 0 | 0 | function=32, total=24, concrete=3, priority=1, owise=12, symbol=1, no-evaluators=1 |
| `/candidate/reference-semantics/semantics/call.k` | 3 | 21 | 0 | 0 | 0 | function=2, total=1, priority=5, owise=3 |
| `/candidate/reference-semantics/semantics/comprehension.k` | 3 | 7 | 0 | 0 | 0 | macro=3, macro-rec=1 |
| `/candidate/reference-semantics/semantics/concrete.k` | 5 | 16 | 0 | 0 | 0 | function=3, total=1, concrete=3, priority=3, owise=1 |
| `/candidate/reference-semantics/semantics/controls.k` | 3 | 34 | 0 | 0 | 0 | priority=7, owise=3 |
| `/candidate/reference-semantics/semantics/core.k` | 37 | 46 | 0 | 1 | 0 | function=18, total=11, concrete=2, priority=3, owise=3 |
| `/candidate/reference-semantics/semantics/dict.k` | 12 | 28 | 0 | 0 | 0 | function=8, total=6, concrete=1, priority=2, owise=2 |
| `/candidate/reference-semantics/semantics/float.k` | 34 | 121 | 0 | 0 | 0 | function=29, total=28, concrete=39, priority=6, symbol=22, no-evaluators=23 |
| `/candidate/reference-semantics/semantics/functions.k` | 4 | 15 | 0 | 0 | 0 | priority=1 |
| `/candidate/reference-semantics/semantics/int.k` | 1 | 16 | 0 | 0 | 0 | function=1 |
| `/candidate/reference-semantics/semantics/iter.k` | 1 | 0 | 0 | 0 | 0 | none |
| `/candidate/reference-semantics/semantics/list.k` | 5 | 27 | 0 | 0 | 0 | function=4, total=2, concrete=1, priority=3, owise=1 |
| `/candidate/reference-semantics/semantics/methods.k` | 27 | 75 | 0 | 0 | 0 | function=28, total=23, concrete=1, priority=3, owise=4 |
| `/candidate/reference-semantics/semantics/operators.k` | 0 | 10 | 0 | 0 | 2 | priority=6, owise=1 |
| `/candidate/reference-semantics/semantics/range.k` | 2 | 6 | 0 | 0 | 0 | function=2, total=1 |
| `/candidate/reference-semantics/semantics/set.k` | 6 | 12 | 0 | 0 | 0 | function=6, total=6 |
| `/candidate/reference-semantics/semantics/sort.k` | 6 | 19 | 0 | 0 | 0 | function=7, total=7, concrete=13, priority=2, owise=1, symbol=2, no-evaluators=3 |
| `/candidate/reference-semantics/semantics/str.k` | 5 | 28 | 0 | 0 | 0 | function=5, total=4 |
| `/candidate/reference-semantics/semantics/subscript.k` | 15 | 40 | 0 | 0 | 2 | function=13, total=10, priority=2 |
| `/candidate/reference-semantics/semantics/syntax.k` | 16 | 0 | 0 | 0 | 0 | macro=2 |
| `/candidate/reference-semantics/semantics/tuple.k` | 4 | 21 | 0 | 0 | 0 | function=1, priority=3 |
| `/candidate/reference-semantics/semantics.k` | 0 | 0 | 0 | 0 | 0 | concrete=5 |
| `/candidate/spec.k` | 0 | 0 | 2 | 0 | 0 | none |
| `/candidate/verification.k` | 1 | 2 | 0 | 0 | 0 | none |

## Grand declaration counts

- syntax: 228
- rule: 697
- claim: 2
- configuration: 1
- context: 5
- alias: 0

## /candidate/reference-semantics/semantics/assert.k

### INV-0001 — rule at `/candidate/reference-semantics/semantics/assert.k:6`

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### INV-0002 — rule at `/candidate/reference-semantics/semantics/assert.k:8`

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)

```

### INV-0003 — rule at `/candidate/reference-semantics/semantics/assert.k:13` — attributes: priority

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

## /candidate/reference-semantics/semantics/bool.k

### INV-0004 — rule at `/candidate/reference-semantics/semantics/bool.k:8`

```k
  rule applyUn("not", V:Val) => notBool truthy(V)

```

### INV-0005 — rule at `/candidate/reference-semantics/semantics/bool.k:10`

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### INV-0006 — rule at `/candidate/reference-semantics/semantics/bool.k:11`

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### INV-0007 — context at `/candidate/reference-semantics/semantics/bool.k:16`

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### INV-0008 — rule at `/candidate/reference-semantics/semantics/bool.k:17`

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### INV-0009 — rule at `/candidate/reference-semantics/semantics/bool.k:18`

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### INV-0010 — rule at `/candidate/reference-semantics/semantics/bool.k:20`

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### INV-0011 — rule at `/candidate/reference-semantics/semantics/bool.k:22`

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### INV-0012 — rule at `/candidate/reference-semantics/semantics/bool.k:24`

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### INV-0013 — rule at `/candidate/reference-semantics/semantics/bool.k:29` — attributes: priority

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### INV-0014 — rule at `/candidate/reference-semantics/semantics/bool.k:31` — attributes: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### INV-0015 — rule at `/candidate/reference-semantics/semantics/bool.k:35` — attributes: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### INV-0016 — rule at `/candidate/reference-semantics/semantics/bool.k:39` — attributes: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### INV-0017 — rule at `/candidate/reference-semantics/semantics/bool.k:43` — attributes: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
endmodule
```

## /candidate/reference-semantics/semantics/builtins.k

### INV-0018 — syntax at `/candidate/reference-semantics/semantics/builtins.k:17` — attributes: function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### INV-0019 — syntax at `/candidate/reference-semantics/semantics/builtins.k:20` — attributes: function

```k
  syntax Int ::= seqLen(Val) [function]
```

### INV-0020 — rule at `/candidate/reference-semantics/semantics/builtins.k:21`

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### INV-0021 — rule at `/candidate/reference-semantics/semantics/builtins.k:22`

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### INV-0022 — rule at `/candidate/reference-semantics/semantics/builtins.k:23`

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### INV-0023 — rule at `/candidate/reference-semantics/semantics/builtins.k:24`

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### INV-0024 — rule at `/candidate/reference-semantics/semantics/builtins.k:25`

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### INV-0025 — rule at `/candidate/reference-semantics/semantics/builtins.k:26`

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### INV-0026 — rule at `/candidate/reference-semantics/semantics/builtins.k:32`

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### INV-0027 — rule at `/candidate/reference-semantics/semantics/builtins.k:33`

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### INV-0028 — rule at `/candidate/reference-semantics/semantics/builtins.k:34`

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### INV-0029 — rule at `/candidate/reference-semantics/semantics/builtins.k:35`

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### INV-0030 — syntax at `/candidate/reference-semantics/semantics/builtins.k:36` — attributes: function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### INV-0031 — rule at `/candidate/reference-semantics/semantics/builtins.k:37`

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### INV-0032 — rule at `/candidate/reference-semantics/semantics/builtins.k:38`

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### INV-0033 — rule at `/candidate/reference-semantics/semantics/builtins.k:41`

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### INV-0034 — rule at `/candidate/reference-semantics/semantics/builtins.k:44`

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### INV-0035 — syntax at `/candidate/reference-semantics/semantics/builtins.k:47`

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### INV-0036 — rule at `/candidate/reference-semantics/semantics/builtins.k:48`

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### INV-0037 — rule at `/candidate/reference-semantics/semantics/builtins.k:49`

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### INV-0038 — rule at `/candidate/reference-semantics/semantics/builtins.k:50`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)

```

### INV-0039 — syntax at `/candidate/reference-semantics/semantics/builtins.k:54` — attributes: function

```k
  syntax Int ::= intOf(Val) [function]
```

### INV-0040 — rule at `/candidate/reference-semantics/semantics/builtins.k:55`

```k
  rule intOf(I:Int)  => I
```

### INV-0041 — rule at `/candidate/reference-semantics/semantics/builtins.k:56`

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### INV-0042 — syntax at `/candidate/reference-semantics/semantics/builtins.k:59`

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### INV-0043 — rule at `/candidate/reference-semantics/semantics/builtins.k:60`

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### INV-0044 — rule at `/candidate/reference-semantics/semantics/builtins.k:61`

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### INV-0045 — rule at `/candidate/reference-semantics/semantics/builtins.k:62`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### INV-0046 — rule at `/candidate/reference-semantics/semantics/builtins.k:64`

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)

```

### INV-0047 — syntax at `/candidate/reference-semantics/semantics/builtins.k:67`

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### INV-0048 — rule at `/candidate/reference-semantics/semantics/builtins.k:68`

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### INV-0049 — rule at `/candidate/reference-semantics/semantics/builtins.k:69`

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### INV-0050 — rule at `/candidate/reference-semantics/semantics/builtins.k:70`

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### INV-0051 — rule at `/candidate/reference-semantics/semantics/builtins.k:72`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### INV-0052 — syntax at `/candidate/reference-semantics/semantics/builtins.k:76`

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### INV-0053 — rule at `/candidate/reference-semantics/semantics/builtins.k:77`

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### INV-0054 — rule at `/candidate/reference-semantics/semantics/builtins.k:78`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### INV-0055 — rule at `/candidate/reference-semantics/semantics/builtins.k:80`

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### INV-0056 — rule at `/candidate/reference-semantics/semantics/builtins.k:81`

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### INV-0057 — rule at `/candidate/reference-semantics/semantics/builtins.k:82`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

```

### INV-0058 — syntax at `/candidate/reference-semantics/semantics/builtins.k:86`

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### INV-0059 — rule at `/candidate/reference-semantics/semantics/builtins.k:87`

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### INV-0060 — rule at `/candidate/reference-semantics/semantics/builtins.k:88`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### INV-0061 — rule at `/candidate/reference-semantics/semantics/builtins.k:90`

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### INV-0062 — rule at `/candidate/reference-semantics/semantics/builtins.k:91`

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### INV-0063 — rule at `/candidate/reference-semantics/semantics/builtins.k:92`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### INV-0064 — syntax at `/candidate/reference-semantics/semantics/builtins.k:97` — attributes: function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### INV-0065 — rule at `/candidate/reference-semantics/semantics/builtins.k:98`

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### INV-0066 — rule at `/candidate/reference-semantics/semantics/builtins.k:99`

```k
  rule maxVals(M:Int, .Vals)           => M
```

### INV-0067 — rule at `/candidate/reference-semantics/semantics/builtins.k:100`

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)

```

### INV-0068 — syntax at `/candidate/reference-semantics/semantics/builtins.k:102` — attributes: function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### INV-0069 — rule at `/candidate/reference-semantics/semantics/builtins.k:103`

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### INV-0070 — rule at `/candidate/reference-semantics/semantics/builtins.k:104`

```k
  rule minVals(M:Int, .Vals)           => M
```

### INV-0071 — rule at `/candidate/reference-semantics/semantics/builtins.k:105`

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### INV-0072 — rule at `/candidate/reference-semantics/semantics/builtins.k:108`

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### INV-0073 — rule at `/candidate/reference-semantics/semantics/builtins.k:111`

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### INV-0074 — syntax at `/candidate/reference-semantics/semantics/builtins.k:114` — attributes: function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### INV-0075 — rule at `/candidate/reference-semantics/semantics/builtins.k:115`

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### INV-0076 — rule at `/candidate/reference-semantics/semantics/builtins.k:116`

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### INV-0077 — syntax at `/candidate/reference-semantics/semantics/builtins.k:117` — attributes: function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### INV-0078 — rule at `/candidate/reference-semantics/semantics/builtins.k:118`

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### INV-0079 — rule at `/candidate/reference-semantics/semantics/builtins.k:119`

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### INV-0080 — rule at `/candidate/reference-semantics/semantics/builtins.k:124`

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### INV-0081 — syntax at `/candidate/reference-semantics/semantics/builtins.k:126` — attributes: function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### INV-0082 — rule at `/candidate/reference-semantics/semantics/builtins.k:127`

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### INV-0083 — rule at `/candidate/reference-semantics/semantics/builtins.k:128`

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### INV-0084 — rule at `/candidate/reference-semantics/semantics/builtins.k:132`

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### INV-0085 — syntax at `/candidate/reference-semantics/semantics/builtins.k:134` — attributes: function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### INV-0086 — rule at `/candidate/reference-semantics/semantics/builtins.k:135`

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### INV-0087 — rule at `/candidate/reference-semantics/semantics/builtins.k:136`

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### INV-0088 — rule at `/candidate/reference-semantics/semantics/builtins.k:137`

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### INV-0089 — rule at `/candidate/reference-semantics/semantics/builtins.k:140`

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### INV-0090 — rule at `/candidate/reference-semantics/semantics/builtins.k:143`

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### INV-0091 — rule at `/candidate/reference-semantics/semantics/builtins.k:144`

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### INV-0092 — rule at `/candidate/reference-semantics/semantics/builtins.k:148`

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### INV-0093 — rule at `/candidate/reference-semantics/semantics/builtins.k:149`

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### INV-0094 — rule at `/candidate/reference-semantics/semantics/builtins.k:152`

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### INV-0095 — rule at `/candidate/reference-semantics/semantics/builtins.k:156`

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### INV-0096 — syntax at `/candidate/reference-semantics/semantics/builtins.k:158` — attributes: function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### INV-0097 — rule at `/candidate/reference-semantics/semantics/builtins.k:159`

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### INV-0098 — rule at `/candidate/reference-semantics/semantics/builtins.k:160`

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### INV-0099 — rule at `/candidate/reference-semantics/semantics/builtins.k:163`

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### INV-0100 — rule at `/candidate/reference-semantics/semantics/builtins.k:164`

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### INV-0101 — rule at `/candidate/reference-semantics/semantics/builtins.k:167`

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### INV-0102 — rule at `/candidate/reference-semantics/semantics/builtins.k:169`

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### INV-0103 — rule at `/candidate/reference-semantics/semantics/builtins.k:170`

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### INV-0104 — rule at `/candidate/reference-semantics/semantics/builtins.k:171`

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### INV-0105 — rule at `/candidate/reference-semantics/semantics/builtins.k:173`

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### INV-0106 — rule at `/candidate/reference-semantics/semantics/builtins.k:174`

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### INV-0107 — rule at `/candidate/reference-semantics/semantics/builtins.k:177`

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### INV-0108 — rule at `/candidate/reference-semantics/semantics/builtins.k:178`

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### INV-0109 — rule at `/candidate/reference-semantics/semantics/builtins.k:179` — attributes: concrete

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### INV-0110 — rule at `/candidate/reference-semantics/semantics/builtins.k:187`

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### INV-0111 — syntax at `/candidate/reference-semantics/semantics/builtins.k:188` — attributes: function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### INV-0112 — rule at `/candidate/reference-semantics/semantics/builtins.k:189`

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))

```

### INV-0113 — syntax at `/candidate/reference-semantics/semantics/builtins.k:192`

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)

```

### INV-0114 — syntax at `/candidate/reference-semantics/semantics/builtins.k:194` — attributes: function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### INV-0115 — rule at `/candidate/reference-semantics/semantics/builtins.k:195`

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### INV-0116 — syntax at `/candidate/reference-semantics/semantics/builtins.k:196` — attributes: function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### INV-0117 — rule at `/candidate/reference-semantics/semantics/builtins.k:197`

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### INV-0118 — rule at `/candidate/reference-semantics/semantics/builtins.k:198` — attributes: owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### INV-0119 — syntax at `/candidate/reference-semantics/semantics/builtins.k:199` — attributes: function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### INV-0120 — rule at `/candidate/reference-semantics/semantics/builtins.k:200`

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### INV-0121 — rule at `/candidate/reference-semantics/semantics/builtins.k:201` — attributes: owise

```k
  rule evHead47(_:IntSeq)            => false [owise]

```

### INV-0122 — syntax at `/candidate/reference-semantics/semantics/builtins.k:203` — attributes: function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### INV-0123 — rule at `/candidate/reference-semantics/semantics/builtins.k:204`

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### INV-0124 — rule at `/candidate/reference-semantics/semantics/builtins.k:205`

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### INV-0125 — rule at `/candidate/reference-semantics/semantics/builtins.k:206`

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### INV-0126 — rule at `/candidate/reference-semantics/semantics/builtins.k:207`

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### INV-0127 — rule at `/candidate/reference-semantics/semantics/builtins.k:208`

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### INV-0128 — rule at `/candidate/reference-semantics/semantics/builtins.k:209`

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### INV-0129 — rule at `/candidate/reference-semantics/semantics/builtins.k:210`

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### INV-0130 — rule at `/candidate/reference-semantics/semantics/builtins.k:211`

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### INV-0131 — rule at `/candidate/reference-semantics/semantics/builtins.k:212`

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))

```

### INV-0132 — syntax at `/candidate/reference-semantics/semantics/builtins.k:214` — attributes: function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### INV-0133 — rule at `/candidate/reference-semantics/semantics/builtins.k:216`

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### INV-0134 — rule at `/candidate/reference-semantics/semantics/builtins.k:217`

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### INV-0135 — rule at `/candidate/reference-semantics/semantics/builtins.k:218`

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### INV-0136 — rule at `/candidate/reference-semantics/semantics/builtins.k:219`

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### INV-0137 — rule at `/candidate/reference-semantics/semantics/builtins.k:221`

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### INV-0138 — rule at `/candidate/reference-semantics/semantics/builtins.k:223` — attributes: owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]

```

### INV-0139 — syntax at `/candidate/reference-semantics/semantics/builtins.k:225`

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### INV-0140 — syntax at `/candidate/reference-semantics/semantics/builtins.k:226` — attributes: function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### INV-0141 — rule at `/candidate/reference-semantics/semantics/builtins.k:227`

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### INV-0142 — rule at `/candidate/reference-semantics/semantics/builtins.k:228` — attributes: owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]

```

### INV-0143 — syntax at `/candidate/reference-semantics/semantics/builtins.k:230` — attributes: function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### INV-0144 — rule at `/candidate/reference-semantics/semantics/builtins.k:231`

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### INV-0145 — rule at `/candidate/reference-semantics/semantics/builtins.k:232`

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### INV-0146 — rule at `/candidate/reference-semantics/semantics/builtins.k:233`

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### INV-0147 — rule at `/candidate/reference-semantics/semantics/builtins.k:234`

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### INV-0148 — rule at `/candidate/reference-semantics/semantics/builtins.k:235`

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### INV-0149 — rule at `/candidate/reference-semantics/semantics/builtins.k:236` — attributes: owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]

```

### INV-0150 — syntax at `/candidate/reference-semantics/semantics/builtins.k:238` — attributes: function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### INV-0151 — rule at `/candidate/reference-semantics/semantics/builtins.k:239`

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### INV-0152 — rule at `/candidate/reference-semantics/semantics/builtins.k:240`

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### INV-0153 — rule at `/candidate/reference-semantics/semantics/builtins.k:241`

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### INV-0154 — rule at `/candidate/reference-semantics/semantics/builtins.k:243` — attributes: owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### INV-0155 — syntax at `/candidate/reference-semantics/semantics/builtins.k:244` — attributes: function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### INV-0156 — rule at `/candidate/reference-semantics/semantics/builtins.k:245`

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### INV-0157 — rule at `/candidate/reference-semantics/semantics/builtins.k:246`

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### INV-0158 — syntax at `/candidate/reference-semantics/semantics/builtins.k:247` — attributes: function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### INV-0159 — rule at `/candidate/reference-semantics/semantics/builtins.k:248`

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))

```

### INV-0160 — syntax at `/candidate/reference-semantics/semantics/builtins.k:250` — attributes: function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### INV-0161 — rule at `/candidate/reference-semantics/semantics/builtins.k:251`

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### INV-0162 — rule at `/candidate/reference-semantics/semantics/builtins.k:252`

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### INV-0163 — rule at `/candidate/reference-semantics/semantics/builtins.k:253`

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### INV-0164 — rule at `/candidate/reference-semantics/semantics/builtins.k:254`

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### INV-0165 — syntax at `/candidate/reference-semantics/semantics/builtins.k:255` — attributes: function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### INV-0166 — rule at `/candidate/reference-semantics/semantics/builtins.k:256`

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### INV-0167 — rule at `/candidate/reference-semantics/semantics/builtins.k:257`

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### INV-0168 — rule at `/candidate/reference-semantics/semantics/builtins.k:260`

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### INV-0169 — rule at `/candidate/reference-semantics/semantics/builtins.k:263` — attributes: owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### INV-0170 — syntax at `/candidate/reference-semantics/semantics/builtins.k:265` — attributes: function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### INV-0171 — rule at `/candidate/reference-semantics/semantics/builtins.k:266`

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### INV-0172 — rule at `/candidate/reference-semantics/semantics/builtins.k:267`

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### INV-0173 — rule at `/candidate/reference-semantics/semantics/builtins.k:268` — attributes: owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### INV-0174 — syntax at `/candidate/reference-semantics/semantics/builtins.k:269` — attributes: function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### INV-0175 — rule at `/candidate/reference-semantics/semantics/builtins.k:270`

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### INV-0176 — rule at `/candidate/reference-semantics/semantics/builtins.k:271`

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### INV-0177 — syntax at `/candidate/reference-semantics/semantics/builtins.k:272` — attributes: function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### INV-0178 — rule at `/candidate/reference-semantics/semantics/builtins.k:273`

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### INV-0179 — rule at `/candidate/reference-semantics/semantics/builtins.k:274` — attributes: concrete

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### INV-0180 — syntax at `/candidate/reference-semantics/semantics/builtins.k:279`

```k
  syntax KItem ::= "#md5"
```

### INV-0181 — rule at `/candidate/reference-semantics/semantics/builtins.k:280` — attributes: priority

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### INV-0182 — rule at `/candidate/reference-semantics/semantics/builtins.k:282`

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### INV-0183 — syntax at `/candidate/reference-semantics/semantics/builtins.k:283`

```k
  syntax Val ::= md5Obj(IntSeq)
```

### INV-0184 — rule at `/candidate/reference-semantics/semantics/builtins.k:284`

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### INV-0185 — syntax at `/candidate/reference-semantics/semantics/builtins.k:285` — attributes: function, total, concrete, owise, symbol, no-evaluators

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### INV-0186 — rule at `/candidate/reference-semantics/semantics/builtins.k:291`

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### INV-0187 — rule at `/candidate/reference-semantics/semantics/builtins.k:292`

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### INV-0188 — syntax at `/candidate/reference-semantics/semantics/builtins.k:293` — attributes: function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### INV-0189 — rule at `/candidate/reference-semantics/semantics/builtins.k:294`

```k
  rule isIntV(_:Int)         => true
```

### INV-0190 — rule at `/candidate/reference-semantics/semantics/builtins.k:295` — attributes: owise

```k
  rule isIntV(_:Val)         => false [owise]
```

### INV-0191 — rule at `/candidate/reference-semantics/semantics/builtins.k:296`

```k
  rule isStrV(str(_:IntSeq)) => true
```

### INV-0192 — rule at `/candidate/reference-semantics/semantics/builtins.k:297` — attributes: owise

```k
  rule isStrV(_:Val)         => false [owise]
endmodule
```

## /candidate/reference-semantics/semantics/call.k

### INV-0193 — rule at `/candidate/reference-semantics/semantics/call.k:16` — attributes: owise

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### INV-0194 — syntax at `/candidate/reference-semantics/semantics/call.k:19`

```k
  syntax KItem ::= #callee(Exprs)
```

### INV-0195 — rule at `/candidate/reference-semantics/semantics/call.k:20` — attributes: owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### INV-0196 — rule at `/candidate/reference-semantics/semantics/call.k:21`

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### INV-0197 — rule at `/candidate/reference-semantics/semantics/call.k:24`

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>

```

### INV-0198 — rule at `/candidate/reference-semantics/semantics/call.k:26`

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### INV-0199 — rule at `/candidate/reference-semantics/semantics/call.k:27`

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### INV-0200 — rule at `/candidate/reference-semantics/semantics/call.k:28`

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### INV-0201 — rule at `/candidate/reference-semantics/semantics/call.k:29`

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### INV-0202 — rule at `/candidate/reference-semantics/semantics/call.k:30`

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### INV-0203 — rule at `/candidate/reference-semantics/semantics/call.k:31` — attributes: owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### INV-0204 — rule at `/candidate/reference-semantics/semantics/call.k:32`

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### INV-0205 — rule at `/candidate/reference-semantics/semantics/call.k:38` — attributes: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### INV-0206 — rule at `/candidate/reference-semantics/semantics/call.k:42` — attributes: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### INV-0207 — rule at `/candidate/reference-semantics/semantics/call.k:47` — attributes: priority

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

```

### INV-0208 — syntax at `/candidate/reference-semantics/semantics/call.k:52` — attributes: function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### INV-0209 — rule at `/candidate/reference-semantics/semantics/call.k:53`

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### INV-0210 — rule at `/candidate/reference-semantics/semantics/call.k:56` — attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### INV-0211 — rule at `/candidate/reference-semantics/semantics/call.k:63` — attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]

```

### INV-0212 — rule at `/candidate/reference-semantics/semantics/call.k:69`

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

### INV-0213 — rule at `/candidate/reference-semantics/semantics/call.k:80`

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>

```

### INV-0214 — syntax at `/candidate/reference-semantics/semantics/call.k:87`

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### INV-0215 — rule at `/candidate/reference-semantics/semantics/call.k:88`

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### INV-0216 — rule at `/candidate/reference-semantics/semantics/call.k:89`

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
endmodule
```

## /candidate/reference-semantics/semantics/comprehension.k

### INV-0217 — rule at `/candidate/reference-semantics/semantics/comprehension.k:11`

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### INV-0218 — rule at `/candidate/reference-semantics/semantics/comprehension.k:12`

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)

```

### INV-0219 — syntax at `/candidate/reference-semantics/semantics/comprehension.k:14` — attributes: macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### INV-0220 — rule at `/candidate/reference-semantics/semantics/comprehension.k:15`

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))

```

### INV-0221 — syntax at `/candidate/reference-semantics/semantics/comprehension.k:18` — attributes: macro, macro-rec

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### INV-0222 — rule at `/candidate/reference-semantics/semantics/comprehension.k:19`

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### INV-0223 — rule at `/candidate/reference-semantics/semantics/comprehension.k:21`

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))

```

### INV-0224 — syntax at `/candidate/reference-semantics/semantics/comprehension.k:24` — attributes: macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### INV-0225 — rule at `/candidate/reference-semantics/semantics/comprehension.k:25`

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### INV-0226 — rule at `/candidate/reference-semantics/semantics/comprehension.k:26`

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
endmodule
```

## /candidate/reference-semantics/semantics/concrete.k

### INV-0227 — rule at `/candidate/reference-semantics/semantics/concrete.k:13`

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### INV-0228 — rule at `/candidate/reference-semantics/semantics/concrete.k:16` — attributes: concrete, priority

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

### INV-0229 — syntax at `/candidate/reference-semantics/semantics/concrete.k:25`

```k
  syntax Val ::= kvP(Val, Val)
```

### INV-0230 — syntax at `/candidate/reference-semantics/semantics/concrete.k:26`

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### INV-0231 — rule at `/candidate/reference-semantics/semantics/concrete.k:28` — attributes: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### INV-0232 — rule at `/candidate/reference-semantics/semantics/concrete.k:31` — attributes: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### INV-0233 — rule at `/candidate/reference-semantics/semantics/concrete.k:34`

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### INV-0234 — rule at `/candidate/reference-semantics/semantics/concrete.k:36`

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### INV-0235 — rule at `/candidate/reference-semantics/semantics/concrete.k:38`

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)

```

### INV-0236 — syntax at `/candidate/reference-semantics/semantics/concrete.k:42` — attributes: function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### INV-0237 — rule at `/candidate/reference-semantics/semantics/concrete.k:43`

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### INV-0238 — rule at `/candidate/reference-semantics/semantics/concrete.k:44`

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### INV-0239 — rule at `/candidate/reference-semantics/semantics/concrete.k:47`

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)

```

### INV-0240 — syntax at `/candidate/reference-semantics/semantics/concrete.k:51` — attributes: function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### INV-0241 — rule at `/candidate/reference-semantics/semantics/concrete.k:52`

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### INV-0242 — rule at `/candidate/reference-semantics/semantics/concrete.k:53`

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### INV-0243 — rule at `/candidate/reference-semantics/semantics/concrete.k:54`

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)

```

### INV-0244 — syntax at `/candidate/reference-semantics/semantics/concrete.k:56` — attributes: function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### INV-0245 — rule at `/candidate/reference-semantics/semantics/concrete.k:57`

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### INV-0246 — rule at `/candidate/reference-semantics/semantics/concrete.k:58`

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### INV-0247 — rule at `/candidate/reference-semantics/semantics/concrete.k:59` — attributes: owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
endmodule
```

## /candidate/reference-semantics/semantics/controls.k

### INV-0248 — rule at `/candidate/reference-semantics/semantics/controls.k:9`

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### INV-0249 — rule at `/candidate/reference-semantics/semantics/controls.k:12` — attributes: priority

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]

```

### INV-0250 — rule at `/candidate/reference-semantics/semantics/controls.k:20`

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### INV-0251 — rule at `/candidate/reference-semantics/semantics/controls.k:27` — attributes: priority

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### INV-0252 — rule at `/candidate/reference-semantics/semantics/controls.k:35`

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### INV-0253 — rule at `/candidate/reference-semantics/semantics/controls.k:36` — attributes: owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### INV-0254 — syntax at `/candidate/reference-semantics/semantics/controls.k:37`

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### INV-0255 — rule at `/candidate/reference-semantics/semantics/controls.k:38`

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### INV-0256 — rule at `/candidate/reference-semantics/semantics/controls.k:39`

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### INV-0257 — rule at `/candidate/reference-semantics/semantics/controls.k:43`

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### INV-0258 — rule at `/candidate/reference-semantics/semantics/controls.k:48`

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### INV-0259 — syntax at `/candidate/reference-semantics/semantics/controls.k:51`

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### INV-0260 — rule at `/candidate/reference-semantics/semantics/controls.k:52`

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### INV-0261 — rule at `/candidate/reference-semantics/semantics/controls.k:53`

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### INV-0262 — rule at `/candidate/reference-semantics/semantics/controls.k:54`

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### INV-0263 — rule at `/candidate/reference-semantics/semantics/controls.k:57`

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### INV-0264 — rule at `/candidate/reference-semantics/semantics/controls.k:59`

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### INV-0265 — syntax at `/candidate/reference-semantics/semantics/controls.k:65`

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"

```

### INV-0266 — rule at `/candidate/reference-semantics/semantics/controls.k:69`

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>

```

### INV-0267 — rule at `/candidate/reference-semantics/semantics/controls.k:71`

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### INV-0268 — rule at `/candidate/reference-semantics/semantics/controls.k:72`

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### INV-0269 — rule at `/candidate/reference-semantics/semantics/controls.k:73`

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### INV-0270 — rule at `/candidate/reference-semantics/semantics/controls.k:77`

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### INV-0271 — rule at `/candidate/reference-semantics/semantics/controls.k:78`

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### INV-0272 — rule at `/candidate/reference-semantics/semantics/controls.k:79`

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### INV-0273 — rule at `/candidate/reference-semantics/semantics/controls.k:81`

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### INV-0274 — rule at `/candidate/reference-semantics/semantics/controls.k:85`

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### INV-0275 — rule at `/candidate/reference-semantics/semantics/controls.k:86`

```k
  rule <k> Continue => #cont ... </k>
```

### INV-0276 — rule at `/candidate/reference-semantics/semantics/controls.k:87`

```k
  rule <k> Break => #brk ... </k>
```

### INV-0277 — rule at `/candidate/reference-semantics/semantics/controls.k:88`

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### INV-0278 — rule at `/candidate/reference-semantics/semantics/controls.k:89` — attributes: owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### INV-0279 — rule at `/candidate/reference-semantics/semantics/controls.k:90`

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### INV-0280 — rule at `/candidate/reference-semantics/semantics/controls.k:91` — attributes: priority, owise

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### INV-0281 — rule at `/candidate/reference-semantics/semantics/controls.k:95` — attributes: priority

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### INV-0282 — rule at `/candidate/reference-semantics/semantics/controls.k:98` — attributes: priority

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### INV-0283 — rule at `/candidate/reference-semantics/semantics/controls.k:101` — attributes: priority

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### INV-0284 — rule at `/candidate/reference-semantics/semantics/controls.k:106` — attributes: priority

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

## /candidate/reference-semantics/semantics/core.k

### INV-0285 — syntax at `/candidate/reference-semantics/semantics/core.k:13`

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### INV-0286 — syntax at `/candidate/reference-semantics/semantics/core.k:14`

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### INV-0287 — syntax at `/candidate/reference-semantics/semantics/core.k:15`

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### INV-0288 — syntax at `/candidate/reference-semantics/semantics/core.k:18`

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)

```

### INV-0289 — syntax at `/candidate/reference-semantics/semantics/core.k:25` — attributes: function

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

### INV-0290 — syntax at `/candidate/reference-semantics/semantics/core.k:36`

```k
  syntax Parent   ::= "root" | parent(Int)
```

### INV-0291 — syntax at `/candidate/reference-semantics/semantics/core.k:37`

```k
  syntax Scope    ::= scope(Map, Parent)
```

### INV-0292 — syntax at `/candidate/reference-semantics/semantics/core.k:38`

```k
  syntax KResult  ::= Val
```

### INV-0293 — syntax at `/candidate/reference-semantics/semantics/core.k:39`

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### INV-0294 — syntax at `/candidate/reference-semantics/semantics/core.k:40`

```k
  syntax Vals     ::= List{Val, ","}
```

### INV-0295 — syntax at `/candidate/reference-semantics/semantics/core.k:41`

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### INV-0296 — syntax at `/candidate/reference-semantics/semantics/core.k:42`

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### INV-0297 — configuration at `/candidate/reference-semantics/semantics/core.k:49`

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

### INV-0298 — syntax at `/candidate/reference-semantics/semantics/core.k:68` — attributes: function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### INV-0299 — rule at `/candidate/reference-semantics/semantics/core.k:69`

```k
  rule isRefV(ref(_:Int)) => true
```

### INV-0300 — rule at `/candidate/reference-semantics/semantics/core.k:70` — attributes: owise

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### INV-0301 — syntax at `/candidate/reference-semantics/semantics/core.k:75`

```k
  syntax HeapVal ::= cellV(Val)
```

### INV-0302 — syntax at `/candidate/reference-semantics/semantics/core.k:76` — attributes: function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### INV-0303 — rule at `/candidate/reference-semantics/semantics/core.k:77`

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### INV-0304 — rule at `/candidate/reference-semantics/semantics/core.k:78` — attributes: function, owise

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### INV-0305 — rule at `/candidate/reference-semantics/semantics/core.k:85` — attributes: priority

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]

  // write through a cell (Assign / #bindP / #bindTgt dispatch here on
  // cell-bound names)
  // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)
```

### INV-0306 — syntax at `/candidate/reference-semantics/semantics/core.k:95`

```k
  syntax Val ::= kwV(String, Val)
```

### INV-0307 — syntax at `/candidate/reference-semantics/semantics/core.k:96`

```k
  syntax KItem ::= #kwTag(String)
```

### INV-0308 — rule at `/candidate/reference-semantics/semantics/core.k:97`

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### INV-0309 — rule at `/candidate/reference-semantics/semantics/core.k:98`

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### INV-0310 — syntax at `/candidate/reference-semantics/semantics/core.k:100` — attributes: function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### INV-0311 — rule at `/candidate/reference-semantics/semantics/core.k:101`

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### INV-0312 — rule at `/candidate/reference-semantics/semantics/core.k:102` — attributes: owise

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### INV-0313 — syntax at `/candidate/reference-semantics/semantics/core.k:106`

```k
  syntax Val ::= cellsMark(ParamNames)
```

### INV-0314 — syntax at `/candidate/reference-semantics/semantics/core.k:107` — attributes: function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### INV-0315 — rule at `/candidate/reference-semantics/semantics/core.k:108`

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### INV-0316 — syntax at `/candidate/reference-semantics/semantics/core.k:109` — attributes: function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### INV-0317 — rule at `/candidate/reference-semantics/semantics/core.k:110`

```k
  rule pnMember(_:String, .ParamNames) => false
```

### INV-0318 — rule at `/candidate/reference-semantics/semantics/core.k:111`

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)

```

### INV-0319 — syntax at `/candidate/reference-semantics/semantics/core.k:113`

```k
  syntax KItem ::= #cellW(Val, Val)
```

### INV-0320 — rule at `/candidate/reference-semantics/semantics/core.k:114`

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>

```

### INV-0321 — syntax at `/candidate/reference-semantics/semantics/core.k:117`

```k
  syntax KItem ::= #alloc(Val)
```

### INV-0322 — rule at `/candidate/reference-semantics/semantics/core.k:118`

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### INV-0323 — syntax at `/candidate/reference-semantics/semantics/core.k:124`

```k
  syntax KItem ::= #loadAll(Module)
```

### INV-0324 — rule at `/candidate/reference-semantics/semantics/core.k:125`

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### INV-0325 — rule at `/candidate/reference-semantics/semantics/core.k:126`

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### INV-0326 — rule at `/candidate/reference-semantics/semantics/core.k:127`

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### INV-0327 — syntax at `/candidate/reference-semantics/semantics/core.k:130`

```k
  syntax KItem ::= #look(String, Int)
```

### INV-0328 — rule at `/candidate/reference-semantics/semantics/core.k:131`

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### INV-0329 — rule at `/candidate/reference-semantics/semantics/core.k:132` — attributes: function, concrete, priority

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

### INV-0330 — rule at `/candidate/reference-semantics/semantics/core.k:145` — attributes: priority

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### INV-0331 — rule at `/candidate/reference-semantics/semantics/core.k:152`

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### INV-0332 — syntax at `/candidate/reference-semantics/semantics/core.k:157` — attributes: function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### INV-0333 — rule at `/candidate/reference-semantics/semantics/core.k:158`

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

### INV-0334 — syntax at `/candidate/reference-semantics/semantics/core.k:185`

```k
  syntax ApplyK ::= toCall(Val)
```

### INV-0335 — syntax at `/candidate/reference-semantics/semantics/core.k:186`

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### INV-0336 — rule at `/candidate/reference-semantics/semantics/core.k:189`

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### INV-0337 — rule at `/candidate/reference-semantics/semantics/core.k:190`

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### INV-0338 — rule at `/candidate/reference-semantics/semantics/core.k:191`

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### INV-0339 — rule at `/candidate/reference-semantics/semantics/core.k:194`

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### INV-0340 — rule at `/candidate/reference-semantics/semantics/core.k:195`

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### INV-0341 — rule at `/candidate/reference-semantics/semantics/core.k:196`

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### INV-0342 — syntax at `/candidate/reference-semantics/semantics/core.k:199` — attributes: function

```k
  syntax Bool ::= truthy(Val) [function]
```

### INV-0343 — rule at `/candidate/reference-semantics/semantics/core.k:200`

```k
  rule truthy(B:Bool)          => B
```

### INV-0344 — rule at `/candidate/reference-semantics/semantics/core.k:201`

```k
  rule truthy(noneV)           => false
```

### INV-0345 — rule at `/candidate/reference-semantics/semantics/core.k:202`

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### INV-0346 — rule at `/candidate/reference-semantics/semantics/core.k:203`

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### INV-0347 — rule at `/candidate/reference-semantics/semantics/core.k:204`

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### INV-0348 — rule at `/candidate/reference-semantics/semantics/core.k:205`

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### INV-0349 — syntax at `/candidate/reference-semantics/semantics/core.k:208` — attributes: function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### INV-0350 — syntax at `/candidate/reference-semantics/semantics/core.k:209` — attributes: function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### INV-0351 — syntax at `/candidate/reference-semantics/semantics/core.k:210` — attributes: function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### INV-0352 — syntax at `/candidate/reference-semantics/semantics/core.k:213` — attributes: function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### INV-0353 — rule at `/candidate/reference-semantics/semantics/core.k:214`

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### INV-0354 — rule at `/candidate/reference-semantics/semantics/core.k:215`

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)

```

### INV-0355 — syntax at `/candidate/reference-semantics/semantics/core.k:217` — attributes: function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### INV-0356 — rule at `/candidate/reference-semantics/semantics/core.k:218`

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### INV-0357 — rule at `/candidate/reference-semantics/semantics/core.k:219`

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### INV-0358 — syntax at `/candidate/reference-semantics/semantics/core.k:223` — attributes: function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### INV-0359 — rule at `/candidate/reference-semantics/semantics/core.k:224`

```k
  rule vsLen(.ValSeq)                => 0
```

### INV-0360 — rule at `/candidate/reference-semantics/semantics/core.k:225`

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)

```

### INV-0361 — syntax at `/candidate/reference-semantics/semantics/core.k:227` — attributes: function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### INV-0362 — rule at `/candidate/reference-semantics/semantics/core.k:228`

```k
  rule isLen(.IntSeq)                => 0
```

### INV-0363 — rule at `/candidate/reference-semantics/semantics/core.k:229` — attributes: total

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### INV-0364 — syntax at `/candidate/reference-semantics/semantics/core.k:233` — attributes: function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### INV-0365 — rule at `/candidate/reference-semantics/semantics/core.k:234`

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### INV-0366 — rule at `/candidate/reference-semantics/semantics/core.k:235`

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### INV-0367 — rule at `/candidate/reference-semantics/semantics/core.k:236`

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### INV-0368 — rule at `/candidate/reference-semantics/semantics/core.k:238`

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
endmodule
```

## /candidate/reference-semantics/semantics/dict.k

### INV-0369 — syntax at `/candidate/reference-semantics/semantics/dict.k:20`

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### INV-0370 — syntax at `/candidate/reference-semantics/semantics/dict.k:23`

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### INV-0371 — rule at `/candidate/reference-semantics/semantics/dict.k:26`

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### INV-0372 — rule at `/candidate/reference-semantics/semantics/dict.k:27`

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### INV-0373 — rule at `/candidate/reference-semantics/semantics/dict.k:28`

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### INV-0374 — rule at `/candidate/reference-semantics/semantics/dict.k:30`

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### INV-0375 — rule at `/candidate/reference-semantics/semantics/dict.k:32` — attributes: total, concrete

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### INV-0376 — syntax at `/candidate/reference-semantics/semantics/dict.k:37` — attributes: function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### INV-0377 — rule at `/candidate/reference-semantics/semantics/dict.k:38`

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### INV-0378 — rule at `/candidate/reference-semantics/semantics/dict.k:39`

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### INV-0379 — rule at `/candidate/reference-semantics/semantics/dict.k:40`

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### INV-0380 — syntax at `/candidate/reference-semantics/semantics/dict.k:43` — attributes: function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### INV-0381 — rule at `/candidate/reference-semantics/semantics/dict.k:44`

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### INV-0382 — rule at `/candidate/reference-semantics/semantics/dict.k:45` — attributes: owise

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### INV-0383 — syntax at `/candidate/reference-semantics/semantics/dict.k:49` — attributes: function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### INV-0384 — rule at `/candidate/reference-semantics/semantics/dict.k:50`

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### INV-0385 — rule at `/candidate/reference-semantics/semantics/dict.k:52`

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### INV-0386 — rule at `/candidate/reference-semantics/semantics/dict.k:54` — attributes: owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### INV-0387 — rule at `/candidate/reference-semantics/semantics/dict.k:58` — attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### INV-0388 — rule at `/candidate/reference-semantics/semantics/dict.k:63`

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### INV-0389 — syntax at `/candidate/reference-semantics/semantics/dict.k:64` — attributes: function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### INV-0390 — rule at `/candidate/reference-semantics/semantics/dict.k:65` — attributes: priority

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### INV-0391 — syntax at `/candidate/reference-semantics/semantics/dict.k:70` — attributes: function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### INV-0392 — rule at `/candidate/reference-semantics/semantics/dict.k:71`

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### INV-0393 — syntax at `/candidate/reference-semantics/semantics/dict.k:76`

```k
  syntax KItem ::= #dsetK(String, Val)
```

### INV-0394 — rule at `/candidate/reference-semantics/semantics/dict.k:77`

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### INV-0395 — rule at `/candidate/reference-semantics/semantics/dict.k:78`

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### INV-0396 — rule at `/candidate/reference-semantics/semantics/dict.k:82`

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### INV-0397 — syntax at `/candidate/reference-semantics/semantics/dict.k:86`

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### INV-0398 — rule at `/candidate/reference-semantics/semantics/dict.k:87`

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### INV-0399 — syntax at `/candidate/reference-semantics/semantics/dict.k:90` — attributes: function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### INV-0400 — rule at `/candidate/reference-semantics/semantics/dict.k:91`

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### INV-0401 — rule at `/candidate/reference-semantics/semantics/dict.k:92`

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### INV-0402 — rule at `/candidate/reference-semantics/semantics/dict.k:95`

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### INV-0403 — syntax at `/candidate/reference-semantics/semantics/dict.k:97` — attributes: function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### INV-0404 — rule at `/candidate/reference-semantics/semantics/dict.k:98`

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### INV-0405 — rule at `/candidate/reference-semantics/semantics/dict.k:99`

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### INV-0406 — syntax at `/candidate/reference-semantics/semantics/dict.k:101` — attributes: function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### INV-0407 — rule at `/candidate/reference-semantics/semantics/dict.k:102`

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### INV-0408 — rule at `/candidate/reference-semantics/semantics/dict.k:103`

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
endmodule
```

## /candidate/reference-semantics/semantics/float.k

### INV-0409 — syntax at `/candidate/reference-semantics/semantics/float.k:20`

```k
  syntax Val ::= Float
```

### INV-0410 — rule at `/candidate/reference-semantics/semantics/float.k:21` — attributes: concrete, no-evaluators

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### INV-0411 — syntax at `/candidate/reference-semantics/semantics/float.k:24` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### INV-0412 — rule at `/candidate/reference-semantics/semantics/float.k:25` — attributes: concrete

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]

```

### INV-0413 — rule at `/candidate/reference-semantics/semantics/float.k:27` — attributes: concrete

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### INV-0414 — syntax at `/candidate/reference-semantics/semantics/float.k:30` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### INV-0415 — rule at `/candidate/reference-semantics/semantics/float.k:31` — attributes: concrete

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### INV-0416 — rule at `/candidate/reference-semantics/semantics/float.k:32` — attributes: concrete

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### INV-0417 — syntax at `/candidate/reference-semantics/semantics/float.k:37` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### INV-0418 — rule at `/candidate/reference-semantics/semantics/float.k:38` — attributes: concrete

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### INV-0419 — rule at `/candidate/reference-semantics/semantics/float.k:39` — attributes: concrete

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### INV-0420 — rule at `/candidate/reference-semantics/semantics/float.k:43`

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### INV-0421 — rule at `/candidate/reference-semantics/semantics/float.k:44` — attributes: concrete, no-evaluators

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### INV-0422 — syntax at `/candidate/reference-semantics/semantics/float.k:50` — attributes: function, total, symbol, no-evaluators

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### INV-0423 — rule at `/candidate/reference-semantics/semantics/float.k:51` — attributes: concrete

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### INV-0424 — rule at `/candidate/reference-semantics/semantics/float.k:52`

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)

```

### INV-0425 — syntax at `/candidate/reference-semantics/semantics/float.k:54` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### INV-0426 — rule at `/candidate/reference-semantics/semantics/float.k:55` — attributes: concrete

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### INV-0427 — rule at `/candidate/reference-semantics/semantics/float.k:56`

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### INV-0428 — rule at `/candidate/reference-semantics/semantics/float.k:61` — attributes: priority

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### INV-0429 — syntax at `/candidate/reference-semantics/semantics/float.k:65`

```k
  syntax KItem ::= "#mathCeil"
```

### INV-0430 — rule at `/candidate/reference-semantics/semantics/float.k:66` — attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### INV-0431 — rule at `/candidate/reference-semantics/semantics/float.k:67`

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### INV-0432 — syntax at `/candidate/reference-semantics/semantics/float.k:70`

```k
  syntax KItem ::= "#mathFloor"
```

### INV-0433 — rule at `/candidate/reference-semantics/semantics/float.k:71` — attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### INV-0434 — rule at `/candidate/reference-semantics/semantics/float.k:72`

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### INV-0435 — syntax at `/candidate/reference-semantics/semantics/float.k:73` — attributes: function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### INV-0436 — rule at `/candidate/reference-semantics/semantics/float.k:74` — attributes: concrete

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### INV-0437 — rule at `/candidate/reference-semantics/semantics/float.k:75` — attributes: concrete

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### INV-0438 — rule at `/candidate/reference-semantics/semantics/float.k:78`

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### INV-0439 — rule at `/candidate/reference-semantics/semantics/float.k:79`

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### INV-0440 — syntax at `/candidate/reference-semantics/semantics/float.k:82`

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### INV-0441 — rule at `/candidate/reference-semantics/semantics/float.k:83` — attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### INV-0442 — rule at `/candidate/reference-semantics/semantics/float.k:84`

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### INV-0443 — rule at `/candidate/reference-semantics/semantics/float.k:85`

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### INV-0444 — syntax at `/candidate/reference-semantics/semantics/float.k:86` — attributes: function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### INV-0445 — rule at `/candidate/reference-semantics/semantics/float.k:87` — attributes: concrete

```k
  rule toF(F:Float) => F        [concrete]
```

### INV-0446 — rule at `/candidate/reference-semantics/semantics/float.k:88` — attributes: concrete

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### INV-0447 — syntax at `/candidate/reference-semantics/semantics/float.k:93` — attributes: function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### INV-0448 — rule at `/candidate/reference-semantics/semantics/float.k:94` — attributes: concrete

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### INV-0449 — rule at `/candidate/reference-semantics/semantics/float.k:95` — attributes: concrete

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### INV-0450 — rule at `/candidate/reference-semantics/semantics/float.k:99` — attributes: concrete, no-evaluators

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### INV-0451 — syntax at `/candidate/reference-semantics/semantics/float.k:103` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### INV-0452 — rule at `/candidate/reference-semantics/semantics/float.k:104` — attributes: concrete

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### INV-0453 — rule at `/candidate/reference-semantics/semantics/float.k:105`

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)

```

### INV-0454 — syntax at `/candidate/reference-semantics/semantics/float.k:107` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### INV-0455 — rule at `/candidate/reference-semantics/semantics/float.k:108` — attributes: concrete

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### INV-0456 — rule at `/candidate/reference-semantics/semantics/float.k:109`

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)

```

### INV-0457 — syntax at `/candidate/reference-semantics/semantics/float.k:111` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### INV-0458 — rule at `/candidate/reference-semantics/semantics/float.k:112` — attributes: concrete

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### INV-0459 — rule at `/candidate/reference-semantics/semantics/float.k:113`

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)

```

### INV-0460 — syntax at `/candidate/reference-semantics/semantics/float.k:115` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### INV-0461 — rule at `/candidate/reference-semantics/semantics/float.k:116` — attributes: concrete

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### INV-0462 — rule at `/candidate/reference-semantics/semantics/float.k:117`

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)

```

### INV-0463 — syntax at `/candidate/reference-semantics/semantics/float.k:119` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### INV-0464 — rule at `/candidate/reference-semantics/semantics/float.k:120` — attributes: concrete

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### INV-0465 — rule at `/candidate/reference-semantics/semantics/float.k:121`

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### INV-0466 — syntax at `/candidate/reference-semantics/semantics/float.k:125` — attributes: function, total, symbol, no-evaluators

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### INV-0467 — rule at `/candidate/reference-semantics/semantics/float.k:126` — attributes: concrete

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### INV-0468 — rule at `/candidate/reference-semantics/semantics/float.k:127`

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### INV-0469 — rule at `/candidate/reference-semantics/semantics/float.k:128`

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### INV-0470 — rule at `/candidate/reference-semantics/semantics/float.k:129`

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### INV-0471 — rule at `/candidate/reference-semantics/semantics/float.k:132`

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### INV-0472 — rule at `/candidate/reference-semantics/semantics/float.k:133`

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### INV-0473 — rule at `/candidate/reference-semantics/semantics/float.k:134`

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### INV-0474 — rule at `/candidate/reference-semantics/semantics/float.k:135`

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### INV-0475 — rule at `/candidate/reference-semantics/semantics/float.k:136`

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### INV-0476 — rule at `/candidate/reference-semantics/semantics/float.k:137`

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### INV-0477 — rule at `/candidate/reference-semantics/semantics/float.k:138`

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### INV-0478 — rule at `/candidate/reference-semantics/semantics/float.k:139` — attributes: concrete

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### INV-0479 — syntax at `/candidate/reference-semantics/semantics/float.k:142` — attributes: function, total, symbol, no-evaluators

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### INV-0480 — rule at `/candidate/reference-semantics/semantics/float.k:143` — attributes: concrete

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### INV-0481 — rule at `/candidate/reference-semantics/semantics/float.k:144`

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### INV-0482 — rule at `/candidate/reference-semantics/semantics/float.k:145`

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### INV-0483 — rule at `/candidate/reference-semantics/semantics/float.k:146`

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### INV-0484 — rule at `/candidate/reference-semantics/semantics/float.k:147`

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### INV-0485 — rule at `/candidate/reference-semantics/semantics/float.k:148`

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### INV-0486 — rule at `/candidate/reference-semantics/semantics/float.k:149`

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### INV-0487 — rule at `/candidate/reference-semantics/semantics/float.k:150`

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### INV-0488 — rule at `/candidate/reference-semantics/semantics/float.k:151`

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### INV-0489 — rule at `/candidate/reference-semantics/semantics/float.k:154`

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### INV-0490 — rule at `/candidate/reference-semantics/semantics/float.k:155` — attributes: concrete

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### INV-0491 — syntax at `/candidate/reference-semantics/semantics/float.k:160` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### INV-0492 — rule at `/candidate/reference-semantics/semantics/float.k:161` — attributes: concrete

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### INV-0493 — rule at `/candidate/reference-semantics/semantics/float.k:162` — attributes: concrete

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### INV-0494 — syntax at `/candidate/reference-semantics/semantics/float.k:165` — attributes: function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### INV-0495 — rule at `/candidate/reference-semantics/semantics/float.k:166`

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### INV-0496 — syntax at `/candidate/reference-semantics/semantics/float.k:167` — attributes: function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### INV-0497 — rule at `/candidate/reference-semantics/semantics/float.k:168`

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### INV-0498 — rule at `/candidate/reference-semantics/semantics/float.k:169`

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### INV-0499 — rule at `/candidate/reference-semantics/semantics/float.k:170`

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### INV-0500 — rule at `/candidate/reference-semantics/semantics/float.k:171`

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### INV-0501 — syntax at `/candidate/reference-semantics/semantics/float.k:173` — attributes: function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### INV-0502 — rule at `/candidate/reference-semantics/semantics/float.k:174`

```k
  rule fracPart(.IntSeq) => 0
```

### INV-0503 — rule at `/candidate/reference-semantics/semantics/float.k:175`

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### INV-0504 — rule at `/candidate/reference-semantics/semantics/float.k:176`

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### INV-0505 — rule at `/candidate/reference-semantics/semantics/float.k:177`

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### INV-0506 — rule at `/candidate/reference-semantics/semantics/float.k:178`

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### INV-0507 — syntax at `/candidate/reference-semantics/semantics/float.k:179` — attributes: function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### INV-0508 — rule at `/candidate/reference-semantics/semantics/float.k:180`

```k
  rule fracScale(.IntSeq) => 1
```

### INV-0509 — rule at `/candidate/reference-semantics/semantics/float.k:181`

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### INV-0510 — rule at `/candidate/reference-semantics/semantics/float.k:182`

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### INV-0511 — rule at `/candidate/reference-semantics/semantics/float.k:183`

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### INV-0512 — rule at `/candidate/reference-semantics/semantics/float.k:184`

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### INV-0513 — rule at `/candidate/reference-semantics/semantics/float.k:185`

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### INV-0514 — rule at `/candidate/reference-semantics/semantics/float.k:186`

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### INV-0515 — rule at `/candidate/reference-semantics/semantics/float.k:187`

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### INV-0516 — syntax at `/candidate/reference-semantics/semantics/float.k:190` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### INV-0517 — rule at `/candidate/reference-semantics/semantics/float.k:191` — attributes: concrete

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### INV-0518 — rule at `/candidate/reference-semantics/semantics/float.k:192`

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### INV-0519 — syntax at `/candidate/reference-semantics/semantics/float.k:195` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### INV-0520 — rule at `/candidate/reference-semantics/semantics/float.k:196` — attributes: concrete

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### INV-0521 — rule at `/candidate/reference-semantics/semantics/float.k:197`

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### INV-0522 — rule at `/candidate/reference-semantics/semantics/float.k:198`

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### INV-0523 — rule at `/candidate/reference-semantics/semantics/float.k:199`

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### INV-0524 — rule at `/candidate/reference-semantics/semantics/float.k:200`

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### INV-0525 — rule at `/candidate/reference-semantics/semantics/float.k:201`

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### INV-0526 — rule at `/candidate/reference-semantics/semantics/float.k:202`

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### INV-0527 — rule at `/candidate/reference-semantics/semantics/float.k:203`

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### INV-0528 — rule at `/candidate/reference-semantics/semantics/float.k:204`

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### INV-0529 — rule at `/candidate/reference-semantics/semantics/float.k:205`

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### INV-0530 — rule at `/candidate/reference-semantics/semantics/float.k:206`

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### INV-0531 — syntax at `/candidate/reference-semantics/semantics/float.k:209` — attributes: function, total, symbol, no-evaluators

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### INV-0532 — rule at `/candidate/reference-semantics/semantics/float.k:210` — attributes: concrete

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### INV-0533 — rule at `/candidate/reference-semantics/semantics/float.k:211`

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)

```

### INV-0534 — rule at `/candidate/reference-semantics/semantics/float.k:213`

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### INV-0535 — rule at `/candidate/reference-semantics/semantics/float.k:214`

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### INV-0536 — syntax at `/candidate/reference-semantics/semantics/float.k:217` — attributes: function, total, symbol, no-evaluators

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### INV-0537 — rule at `/candidate/reference-semantics/semantics/float.k:218` — attributes: concrete

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### INV-0538 — syntax at `/candidate/reference-semantics/semantics/float.k:223` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### INV-0539 — rule at `/candidate/reference-semantics/semantics/float.k:224` — attributes: concrete

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### INV-0540 — rule at `/candidate/reference-semantics/semantics/float.k:227`

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### INV-0541 — rule at `/candidate/reference-semantics/semantics/float.k:228`

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)

```

### INV-0542 — syntax at `/candidate/reference-semantics/semantics/float.k:230` — attributes: function, total, symbol, no-evaluators

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### INV-0543 — rule at `/candidate/reference-semantics/semantics/float.k:231` — attributes: concrete

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### INV-0544 — syntax at `/candidate/reference-semantics/semantics/float.k:232`

```k
  syntax KItem ::= "#mathSqrt"
```

### INV-0545 — rule at `/candidate/reference-semantics/semantics/float.k:233` — attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### INV-0546 — rule at `/candidate/reference-semantics/semantics/float.k:234`

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### INV-0547 — rule at `/candidate/reference-semantics/semantics/float.k:235` — attributes: concrete, priority

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### INV-0548 — syntax at `/candidate/reference-semantics/semantics/float.k:243`

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### INV-0549 — rule at `/candidate/reference-semantics/semantics/float.k:244`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### INV-0550 — rule at `/candidate/reference-semantics/semantics/float.k:245`

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### INV-0551 — rule at `/candidate/reference-semantics/semantics/float.k:246`

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### INV-0552 — rule at `/candidate/reference-semantics/semantics/float.k:247`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

```

### INV-0553 — syntax at `/candidate/reference-semantics/semantics/float.k:250`

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### INV-0554 — rule at `/candidate/reference-semantics/semantics/float.k:251`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### INV-0555 — rule at `/candidate/reference-semantics/semantics/float.k:252`

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### INV-0556 — rule at `/candidate/reference-semantics/semantics/float.k:253`

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### INV-0557 — rule at `/candidate/reference-semantics/semantics/float.k:254` — attributes: concrete

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### INV-0558 — syntax at `/candidate/reference-semantics/semantics/float.k:261`

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### INV-0559 — rule at `/candidate/reference-semantics/semantics/float.k:262`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### INV-0560 — rule at `/candidate/reference-semantics/semantics/float.k:265`

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### INV-0561 — rule at `/candidate/reference-semantics/semantics/float.k:266`

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### INV-0562 — rule at `/candidate/reference-semantics/semantics/float.k:267`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### INV-0563 — rule at `/candidate/reference-semantics/semantics/float.k:270`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
endmodule
```

## /candidate/reference-semantics/semantics/functions.k

### INV-0564 — syntax at `/candidate/reference-semantics/semantics/functions.k:8`

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### INV-0565 — rule at `/candidate/reference-semantics/semantics/functions.k:14`

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>

```

### INV-0566 — syntax at `/candidate/reference-semantics/semantics/functions.k:18`

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### INV-0567 — rule at `/candidate/reference-semantics/semantics/functions.k:19`

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### INV-0568 — syntax at `/candidate/reference-semantics/semantics/functions.k:27`

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### INV-0569 — syntax at `/candidate/reference-semantics/semantics/functions.k:31`

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### INV-0570 — rule at `/candidate/reference-semantics/semantics/functions.k:33`

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### INV-0571 — rule at `/candidate/reference-semantics/semantics/functions.k:36`

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### INV-0572 — rule at `/candidate/reference-semantics/semantics/functions.k:42`

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>

```

### INV-0573 — rule at `/candidate/reference-semantics/semantics/functions.k:47`

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### INV-0574 — rule at `/candidate/reference-semantics/semantics/functions.k:50`

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### INV-0575 — rule at `/candidate/reference-semantics/semantics/functions.k:53`

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### INV-0576 — rule at `/candidate/reference-semantics/semantics/functions.k:59`

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### INV-0577 — rule at `/candidate/reference-semantics/semantics/functions.k:63`

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### INV-0578 — rule at `/candidate/reference-semantics/semantics/functions.k:64`

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### INV-0579 — rule at `/candidate/reference-semantics/semantics/functions.k:68` — attributes: priority

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
        andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
       [priority(40)]

  // ==== return / pop the frame (the returned expr evaluates by strictness) ==
```

### INV-0580 — rule at `/candidate/reference-semantics/semantics/functions.k:78`

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### INV-0581 — rule at `/candidate/reference-semantics/semantics/functions.k:80`

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### INV-0582 — rule at `/candidate/reference-semantics/semantics/functions.k:85`

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
endmodule
```

## /candidate/reference-semantics/semantics/int.k

### INV-0583 — rule at `/candidate/reference-semantics/semantics/int.k:7`

```k
  rule applyUn("-", I:Int) => 0 -Int I

```

### INV-0584 — rule at `/candidate/reference-semantics/semantics/int.k:9`

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### INV-0585 — rule at `/candidate/reference-semantics/semantics/int.k:11`

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### INV-0586 — rule at `/candidate/reference-semantics/semantics/int.k:12`

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### INV-0587 — rule at `/candidate/reference-semantics/semantics/int.k:13`

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### INV-0588 — rule at `/candidate/reference-semantics/semantics/int.k:14`

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### INV-0589 — rule at `/candidate/reference-semantics/semantics/int.k:15`

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### INV-0590 — rule at `/candidate/reference-semantics/semantics/int.k:16`

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### INV-0591 — rule at `/candidate/reference-semantics/semantics/int.k:17`

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0

```

### INV-0592 — syntax at `/candidate/reference-semantics/semantics/int.k:19` — attributes: function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### INV-0593 — rule at `/candidate/reference-semantics/semantics/int.k:20`

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2

```

### INV-0594 — rule at `/candidate/reference-semantics/semantics/int.k:22`

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### INV-0595 — rule at `/candidate/reference-semantics/semantics/int.k:23`

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### INV-0596 — rule at `/candidate/reference-semantics/semantics/int.k:24`

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### INV-0597 — rule at `/candidate/reference-semantics/semantics/int.k:25`

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### INV-0598 — rule at `/candidate/reference-semantics/semantics/int.k:26`

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### INV-0599 — rule at `/candidate/reference-semantics/semantics/int.k:27`

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
endmodule
```

## /candidate/reference-semantics/semantics/iter.k

### INV-0600 — syntax at `/candidate/reference-semantics/semantics/iter.k:8`

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
endmodule
```

## /candidate/reference-semantics/semantics/list.k

### INV-0601 — rule at `/candidate/reference-semantics/semantics/list.k:9`

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### INV-0602 — rule at `/candidate/reference-semantics/semantics/list.k:10`

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### INV-0603 — syntax at `/candidate/reference-semantics/semantics/list.k:13`

```k
  syntax ApplyK ::= "toList"
```

### INV-0604 — rule at `/candidate/reference-semantics/semantics/list.k:14`

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### INV-0605 — rule at `/candidate/reference-semantics/semantics/list.k:15`

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### INV-0606 — syntax at `/candidate/reference-semantics/semantics/list.k:18` — attributes: function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### INV-0607 — rule at `/candidate/reference-semantics/semantics/list.k:19`

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### INV-0608 — rule at `/candidate/reference-semantics/semantics/list.k:20` — attributes: priority

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### INV-0609 — rule at `/candidate/reference-semantics/semantics/list.k:24` — attributes: priority

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]

```

### INV-0610 — rule at `/candidate/reference-semantics/semantics/list.k:27`

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### INV-0611 — rule at `/candidate/reference-semantics/semantics/list.k:28` — attributes: concrete

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### INV-0612 — syntax at `/candidate/reference-semantics/semantics/list.k:33` — attributes: function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### INV-0613 — rule at `/candidate/reference-semantics/semantics/list.k:34`

```k
  rule hasRefVS(.ValSeq)                => false
```

### INV-0614 — rule at `/candidate/reference-semantics/semantics/list.k:35`

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)

```

### INV-0615 — syntax at `/candidate/reference-semantics/semantics/list.k:37` — attributes: function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### INV-0616 — rule at `/candidate/reference-semantics/semantics/list.k:39`

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### INV-0617 — rule at `/candidate/reference-semantics/semantics/list.k:40`

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### INV-0618 — rule at `/candidate/reference-semantics/semantics/list.k:41`

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### INV-0619 — rule at `/candidate/reference-semantics/semantics/list.k:42`

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)

```

### INV-0620 — rule at `/candidate/reference-semantics/semantics/list.k:45`

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### INV-0621 — rule at `/candidate/reference-semantics/semantics/list.k:47`

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### INV-0622 — rule at `/candidate/reference-semantics/semantics/list.k:49`

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### INV-0623 — rule at `/candidate/reference-semantics/semantics/list.k:50` — attributes: owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### INV-0624 — rule at `/candidate/reference-semantics/semantics/list.k:53` — attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### INV-0625 — syntax at `/candidate/reference-semantics/semantics/list.k:58`

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### INV-0626 — rule at `/candidate/reference-semantics/semantics/list.k:59`

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### INV-0627 — rule at `/candidate/reference-semantics/semantics/list.k:60`

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### INV-0628 — rule at `/candidate/reference-semantics/semantics/list.k:61`

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### INV-0629 — rule at `/candidate/reference-semantics/semantics/list.k:62`

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### INV-0630 — rule at `/candidate/reference-semantics/semantics/list.k:63`

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### INV-0631 — rule at `/candidate/reference-semantics/semantics/list.k:65`

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### INV-0632 — rule at `/candidate/reference-semantics/semantics/list.k:67`

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
endmodule
```

## /candidate/reference-semantics/semantics/methods.k

### INV-0633 — syntax at `/candidate/reference-semantics/semantics/methods.k:10` — attributes: function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### INV-0634 — rule at `/candidate/reference-semantics/semantics/methods.k:13`

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### INV-0635 — rule at `/candidate/reference-semantics/semantics/methods.k:14`

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### INV-0636 — rule at `/candidate/reference-semantics/semantics/methods.k:15`

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### INV-0637 — rule at `/candidate/reference-semantics/semantics/methods.k:16`

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### INV-0638 — rule at `/candidate/reference-semantics/semantics/methods.k:19`

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### INV-0639 — rule at `/candidate/reference-semantics/semantics/methods.k:20`

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### INV-0640 — rule at `/candidate/reference-semantics/semantics/methods.k:21`

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### INV-0641 — rule at `/candidate/reference-semantics/semantics/methods.k:26`

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### INV-0642 — syntax at `/candidate/reference-semantics/semantics/methods.k:27` — attributes: function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### INV-0643 — rule at `/candidate/reference-semantics/semantics/methods.k:28`

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### INV-0644 — rule at `/candidate/reference-semantics/semantics/methods.k:29`

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### INV-0645 — rule at `/candidate/reference-semantics/semantics/methods.k:30`

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### INV-0646 — rule at `/candidate/reference-semantics/semantics/methods.k:34`

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### INV-0647 — syntax at `/candidate/reference-semantics/semantics/methods.k:35` — attributes: function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### INV-0648 — rule at `/candidate/reference-semantics/semantics/methods.k:36`

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### INV-0649 — rule at `/candidate/reference-semantics/semantics/methods.k:37`

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### INV-0650 — rule at `/candidate/reference-semantics/semantics/methods.k:39`

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### INV-0651 — syntax at `/candidate/reference-semantics/semantics/methods.k:41` — attributes: function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### INV-0652 — rule at `/candidate/reference-semantics/semantics/methods.k:42`

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### INV-0653 — rule at `/candidate/reference-semantics/semantics/methods.k:43` — attributes: owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### INV-0654 — rule at `/candidate/reference-semantics/semantics/methods.k:44`

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### INV-0655 — rule at `/candidate/reference-semantics/semantics/methods.k:47`

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### INV-0656 — syntax at `/candidate/reference-semantics/semantics/methods.k:48` — attributes: function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### INV-0657 — rule at `/candidate/reference-semantics/semantics/methods.k:49`

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### INV-0658 — rule at `/candidate/reference-semantics/semantics/methods.k:50`

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### INV-0659 — rule at `/candidate/reference-semantics/semantics/methods.k:51`

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### INV-0660 — syntax at `/candidate/reference-semantics/semantics/methods.k:52` — attributes: function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### INV-0661 — rule at `/candidate/reference-semantics/semantics/methods.k:53`

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### INV-0662 — rule at `/candidate/reference-semantics/semantics/methods.k:54`

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### INV-0663 — rule at `/candidate/reference-semantics/semantics/methods.k:55`

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### INV-0664 — rule at `/candidate/reference-semantics/semantics/methods.k:58`

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### INV-0665 — rule at `/candidate/reference-semantics/semantics/methods.k:61` — attributes: concrete

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### INV-0666 — rule at `/candidate/reference-semantics/semantics/methods.k:64`

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### INV-0667 — syntax at `/candidate/reference-semantics/semantics/methods.k:65` — attributes: function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### INV-0668 — rule at `/candidate/reference-semantics/semantics/methods.k:66`

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### INV-0669 — rule at `/candidate/reference-semantics/semantics/methods.k:67`

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### INV-0670 — rule at `/candidate/reference-semantics/semantics/methods.k:68`

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### INV-0671 — rule at `/candidate/reference-semantics/semantics/methods.k:72` — attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### INV-0672 — syntax at `/candidate/reference-semantics/semantics/methods.k:75` — attributes: function

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### INV-0673 — rule at `/candidate/reference-semantics/semantics/methods.k:76`

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### INV-0674 — rule at `/candidate/reference-semantics/semantics/methods.k:77`

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### INV-0675 — rule at `/candidate/reference-semantics/semantics/methods.k:79`

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### INV-0676 — syntax at `/candidate/reference-semantics/semantics/methods.k:82` — attributes: function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### INV-0677 — rule at `/candidate/reference-semantics/semantics/methods.k:83`

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### INV-0678 — rule at `/candidate/reference-semantics/semantics/methods.k:84`

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### INV-0679 — syntax at `/candidate/reference-semantics/semantics/methods.k:85` — attributes: function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### INV-0680 — rule at `/candidate/reference-semantics/semantics/methods.k:86`

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### INV-0681 — rule at `/candidate/reference-semantics/semantics/methods.k:89` — attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### INV-0682 — rule at `/candidate/reference-semantics/semantics/methods.k:94` — attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### INV-0683 — syntax at `/candidate/reference-semantics/semantics/methods.k:97` — attributes: function

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### INV-0684 — rule at `/candidate/reference-semantics/semantics/methods.k:98`

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### INV-0685 — rule at `/candidate/reference-semantics/semantics/methods.k:99`

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### INV-0686 — rule at `/candidate/reference-semantics/semantics/methods.k:101`

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)

```

### INV-0687 — rule at `/candidate/reference-semantics/semantics/methods.k:104`

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### INV-0688 — syntax at `/candidate/reference-semantics/semantics/methods.k:106` — attributes: function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### INV-0689 — rule at `/candidate/reference-semantics/semantics/methods.k:107`

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### INV-0690 — rule at `/candidate/reference-semantics/semantics/methods.k:108`

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### INV-0691 — rule at `/candidate/reference-semantics/semantics/methods.k:109`

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### INV-0692 — syntax at `/candidate/reference-semantics/semantics/methods.k:112` — attributes: function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### INV-0693 — rule at `/candidate/reference-semantics/semantics/methods.k:113`

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90

```

### INV-0694 — syntax at `/candidate/reference-semantics/semantics/methods.k:115` — attributes: function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### INV-0695 — rule at `/candidate/reference-semantics/semantics/methods.k:116`

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122

```

### INV-0696 — syntax at `/candidate/reference-semantics/semantics/methods.k:118` — attributes: function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### INV-0697 — rule at `/candidate/reference-semantics/semantics/methods.k:119`

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)

```

### INV-0698 — syntax at `/candidate/reference-semantics/semantics/methods.k:121` — attributes: function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### INV-0699 — rule at `/candidate/reference-semantics/semantics/methods.k:122`

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57

```

### INV-0700 — syntax at `/candidate/reference-semantics/semantics/methods.k:124` — attributes: function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### INV-0701 — rule at `/candidate/reference-semantics/semantics/methods.k:125`

```k
  rule hasUpper(.IntSeq) => false
```

### INV-0702 — rule at `/candidate/reference-semantics/semantics/methods.k:126`

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)

```

### INV-0703 — syntax at `/candidate/reference-semantics/semantics/methods.k:128` — attributes: function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### INV-0704 — rule at `/candidate/reference-semantics/semantics/methods.k:129`

```k
  rule hasLower(.IntSeq) => false
```

### INV-0705 — rule at `/candidate/reference-semantics/semantics/methods.k:130`

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)

```

### INV-0706 — syntax at `/candidate/reference-semantics/semantics/methods.k:132` — attributes: function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### INV-0707 — rule at `/candidate/reference-semantics/semantics/methods.k:133`

```k
  rule allAlpha(.IntSeq) => true
```

### INV-0708 — rule at `/candidate/reference-semantics/semantics/methods.k:134`

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)

```

### INV-0709 — syntax at `/candidate/reference-semantics/semantics/methods.k:136` — attributes: function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### INV-0710 — rule at `/candidate/reference-semantics/semantics/methods.k:137`

```k
  rule allDigit(.IntSeq) => true
```

### INV-0711 — rule at `/candidate/reference-semantics/semantics/methods.k:138`

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)

```

### INV-0712 — syntax at `/candidate/reference-semantics/semantics/methods.k:140` — attributes: function, total

```k
  syntax Int ::= lowerC(Int) [function, total]

```

### INV-0713 — rule at `/candidate/reference-semantics/semantics/methods.k:142`

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### INV-0714 — rule at `/candidate/reference-semantics/semantics/methods.k:143` — attributes: owise

```k
  rule lowerC(C:Int) => C         [owise]

```

### INV-0715 — syntax at `/candidate/reference-semantics/semantics/methods.k:145` — attributes: function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

### INV-0716 — rule at `/candidate/reference-semantics/semantics/methods.k:146`

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### INV-0717 — rule at `/candidate/reference-semantics/semantics/methods.k:147` — attributes: owise

```k
  rule upperC(C:Int) => C         [owise]

```

### INV-0718 — syntax at `/candidate/reference-semantics/semantics/methods.k:149` — attributes: function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

### INV-0719 — rule at `/candidate/reference-semantics/semantics/methods.k:150`

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### INV-0720 — rule at `/candidate/reference-semantics/semantics/methods.k:151`

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### INV-0721 — rule at `/candidate/reference-semantics/semantics/methods.k:152` — attributes: owise

```k
  rule swapC(C:Int) => C         [owise]

```

### INV-0722 — syntax at `/candidate/reference-semantics/semantics/methods.k:154` — attributes: function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### INV-0723 — rule at `/candidate/reference-semantics/semantics/methods.k:155`

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### INV-0724 — rule at `/candidate/reference-semantics/semantics/methods.k:156`

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))

```

### INV-0725 — syntax at `/candidate/reference-semantics/semantics/methods.k:158` — attributes: function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### INV-0726 — rule at `/candidate/reference-semantics/semantics/methods.k:159`

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### INV-0727 — rule at `/candidate/reference-semantics/semantics/methods.k:160`

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))

```

### INV-0728 — syntax at `/candidate/reference-semantics/semantics/methods.k:162` — attributes: function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### INV-0729 — rule at `/candidate/reference-semantics/semantics/methods.k:163`

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### INV-0730 — rule at `/candidate/reference-semantics/semantics/methods.k:164`

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))

```

### INV-0731 — syntax at `/candidate/reference-semantics/semantics/methods.k:166` — attributes: function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### INV-0732 — rule at `/candidate/reference-semantics/semantics/methods.k:167`

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### INV-0733 — rule at `/candidate/reference-semantics/semantics/methods.k:168`

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### INV-0734 — rule at `/candidate/reference-semantics/semantics/methods.k:169`

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
endmodule
```

## /candidate/reference-semantics/semantics/operators.k

### INV-0735 — rule at `/candidate/reference-semantics/semantics/operators.k:10`

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>

```

### INV-0736 — rule at `/candidate/reference-semantics/semantics/operators.k:12`

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### INV-0737 — context at `/candidate/reference-semantics/semantics/operators.k:15`

```k
  context Compare(HOLE, _)
```

### INV-0738 — context at `/candidate/reference-semantics/semantics/operators.k:16`

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### INV-0739 — rule at `/candidate/reference-semantics/semantics/operators.k:17` — attributes: owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]

```

### INV-0740 — rule at `/candidate/reference-semantics/semantics/operators.k:19`

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### INV-0741 — rule at `/candidate/reference-semantics/semantics/operators.k:20` — attributes: priority

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### INV-0742 — rule at `/candidate/reference-semantics/semantics/operators.k:25` — attributes: priority

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### INV-0743 — rule at `/candidate/reference-semantics/semantics/operators.k:28` — attributes: priority

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### INV-0744 — rule at `/candidate/reference-semantics/semantics/operators.k:34` — attributes: priority

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### INV-0745 — rule at `/candidate/reference-semantics/semantics/operators.k:38` — attributes: priority

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]

```

### INV-0746 — rule at `/candidate/reference-semantics/semantics/operators.k:44` — attributes: priority

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

## /candidate/reference-semantics/semantics/range.k

### INV-0747 — syntax at `/candidate/reference-semantics/semantics/range.k:9` — attributes: function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### INV-0748 — rule at `/candidate/reference-semantics/semantics/range.k:10`

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)

```

### INV-0749 — syntax at `/candidate/reference-semantics/semantics/range.k:12` — attributes: function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### INV-0750 — rule at `/candidate/reference-semantics/semantics/range.k:13`

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### INV-0751 — rule at `/candidate/reference-semantics/semantics/range.k:15`

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### INV-0752 — rule at `/candidate/reference-semantics/semantics/range.k:17`

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)

```

### INV-0753 — rule at `/candidate/reference-semantics/semantics/range.k:20`

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### INV-0754 — rule at `/candidate/reference-semantics/semantics/range.k:23`

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
endmodule
```

## /candidate/reference-semantics/semantics/set.k

### INV-0755 — syntax at `/candidate/reference-semantics/semantics/set.k:8`

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### INV-0756 — syntax at `/candidate/reference-semantics/semantics/set.k:11` — attributes: function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### INV-0757 — rule at `/candidate/reference-semantics/semantics/set.k:12`

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### INV-0758 — rule at `/candidate/reference-semantics/semantics/set.k:13`

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### INV-0759 — syntax at `/candidate/reference-semantics/semantics/set.k:16` — attributes: function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### INV-0760 — rule at `/candidate/reference-semantics/semantics/set.k:18`

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### INV-0761 — rule at `/candidate/reference-semantics/semantics/set.k:19`

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### INV-0762 — rule at `/candidate/reference-semantics/semantics/set.k:20`

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### INV-0763 — rule at `/candidate/reference-semantics/semantics/set.k:22`

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)

```

### INV-0764 — syntax at `/candidate/reference-semantics/semantics/set.k:25` — attributes: function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### INV-0765 — rule at `/candidate/reference-semantics/semantics/set.k:26`

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### INV-0766 — rule at `/candidate/reference-semantics/semantics/set.k:27`

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### INV-0767 — syntax at `/candidate/reference-semantics/semantics/set.k:31` — attributes: function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### INV-0768 — rule at `/candidate/reference-semantics/semantics/set.k:32`

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### INV-0769 — rule at `/candidate/reference-semantics/semantics/set.k:33`

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)

```

### INV-0770 — syntax at `/candidate/reference-semantics/semantics/set.k:35` — attributes: function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### INV-0771 — rule at `/candidate/reference-semantics/semantics/set.k:36`

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### INV-0772 — rule at `/candidate/reference-semantics/semantics/set.k:39`

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
endmodule
```

## /candidate/reference-semantics/semantics/sort.k

### INV-0773 — syntax at `/candidate/reference-semantics/semantics/sort.k:18` — attributes: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### INV-0774 — syntax at `/candidate/reference-semantics/semantics/sort.k:19` — attributes: function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### INV-0775 — rule at `/candidate/reference-semantics/semantics/sort.k:20` — attributes: concrete

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### INV-0776 — rule at `/candidate/reference-semantics/semantics/sort.k:21` — attributes: concrete

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### INV-0777 — rule at `/candidate/reference-semantics/semantics/sort.k:22` — attributes: concrete

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### INV-0778 — rule at `/candidate/reference-semantics/semantics/sort.k:23` — attributes: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### INV-0779 — rule at `/candidate/reference-semantics/semantics/sort.k:24` — attributes: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### INV-0780 — syntax at `/candidate/reference-semantics/semantics/sort.k:26` — attributes: function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### INV-0781 — rule at `/candidate/reference-semantics/semantics/sort.k:27` — attributes: concrete

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### INV-0782 — rule at `/candidate/reference-semantics/semantics/sort.k:28` — attributes: concrete

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### INV-0783 — rule at `/candidate/reference-semantics/semantics/sort.k:29` — attributes: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### INV-0784 — rule at `/candidate/reference-semantics/semantics/sort.k:31` — attributes: concrete, owise

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### INV-0785 — rule at `/candidate/reference-semantics/semantics/sort.k:36`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### INV-0786 — rule at `/candidate/reference-semantics/semantics/sort.k:40` — attributes: concrete, priority

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

### INV-0787 — syntax at `/candidate/reference-semantics/semantics/sort.k:49` — attributes: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]

```

### INV-0788 — syntax at `/candidate/reference-semantics/semantics/sort.k:51` — attributes: function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### INV-0789 — rule at `/candidate/reference-semantics/semantics/sort.k:53`

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### INV-0790 — rule at `/candidate/reference-semantics/semantics/sort.k:54`

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### INV-0791 — rule at `/candidate/reference-semantics/semantics/sort.k:55`

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))

```

### INV-0792 — syntax at `/candidate/reference-semantics/semantics/sort.k:57` — attributes: function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### INV-0793 — rule at `/candidate/reference-semantics/semantics/sort.k:58`

```k
  rule condRev(S:ValSeq, false) => S
```

### INV-0794 — rule at `/candidate/reference-semantics/semantics/sort.k:59`

```k
  rule condRev(S:ValSeq, true)  => revVS(S)

```

### INV-0795 — rule at `/candidate/reference-semantics/semantics/sort.k:61`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### INV-0796 — rule at `/candidate/reference-semantics/semantics/sort.k:63`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### INV-0797 — rule at `/candidate/reference-semantics/semantics/sort.k:65` — attributes: total, concrete

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
endmodule
```

## /candidate/reference-semantics/semantics/str.k

### INV-0798 — rule at `/candidate/reference-semantics/semantics/str.k:8`

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### INV-0799 — rule at `/candidate/reference-semantics/semantics/str.k:9`

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### INV-0800 — syntax at `/candidate/reference-semantics/semantics/str.k:13` — attributes: function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### INV-0801 — rule at `/candidate/reference-semantics/semantics/str.k:14`

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### INV-0802 — rule at `/candidate/reference-semantics/semantics/str.k:15`

```k
  rule strToCodes("") => .IntSeq
```

### INV-0803 — rule at `/candidate/reference-semantics/semantics/str.k:16`

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### INV-0804 — syntax at `/candidate/reference-semantics/semantics/str.k:20` — attributes: function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### INV-0805 — rule at `/candidate/reference-semantics/semantics/str.k:21`

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### INV-0806 — rule at `/candidate/reference-semantics/semantics/str.k:22`

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))

```

### INV-0807 — rule at `/candidate/reference-semantics/semantics/str.k:24`

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### INV-0808 — rule at `/candidate/reference-semantics/semantics/str.k:25`

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### INV-0809 — rule at `/candidate/reference-semantics/semantics/str.k:26`

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### INV-0810 — rule at `/candidate/reference-semantics/semantics/str.k:29`

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### INV-0811 — rule at `/candidate/reference-semantics/semantics/str.k:30`

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)

```

### INV-0812 — syntax at `/candidate/reference-semantics/semantics/str.k:32` — attributes: function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### INV-0813 — rule at `/candidate/reference-semantics/semantics/str.k:33`

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### INV-0814 — rule at `/candidate/reference-semantics/semantics/str.k:34`

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### INV-0815 — rule at `/candidate/reference-semantics/semantics/str.k:35`

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)

```

### INV-0816 — syntax at `/candidate/reference-semantics/semantics/str.k:37` — attributes: function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### INV-0817 — rule at `/candidate/reference-semantics/semantics/str.k:38`

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### INV-0818 — rule at `/candidate/reference-semantics/semantics/str.k:39`

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### INV-0819 — rule at `/candidate/reference-semantics/semantics/str.k:40`

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### INV-0820 — syntax at `/candidate/reference-semantics/semantics/str.k:48` — attributes: function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### INV-0821 — rule at `/candidate/reference-semantics/semantics/str.k:49`

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### INV-0822 — rule at `/candidate/reference-semantics/semantics/str.k:50`

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### INV-0823 — rule at `/candidate/reference-semantics/semantics/str.k:51`

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### INV-0824 — rule at `/candidate/reference-semantics/semantics/str.k:52`

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### INV-0825 — rule at `/candidate/reference-semantics/semantics/str.k:53`

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### INV-0826 — rule at `/candidate/reference-semantics/semantics/str.k:54`

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B

```

### INV-0827 — rule at `/candidate/reference-semantics/semantics/str.k:56`

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### INV-0828 — rule at `/candidate/reference-semantics/semantics/str.k:57`

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### INV-0829 — rule at `/candidate/reference-semantics/semantics/str.k:58`

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### INV-0830 — rule at `/candidate/reference-semantics/semantics/str.k:59`

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
endmodule
```

## /candidate/reference-semantics/semantics/subscript.k

### INV-0831 — syntax at `/candidate/reference-semantics/semantics/subscript.k:11` — attributes: function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### INV-0832 — rule at `/candidate/reference-semantics/semantics/subscript.k:12`

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### INV-0833 — rule at `/candidate/reference-semantics/semantics/subscript.k:13`

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0

```

### INV-0834 — syntax at `/candidate/reference-semantics/semantics/subscript.k:16` — attributes: function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### INV-0835 — rule at `/candidate/reference-semantics/semantics/subscript.k:17`

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### INV-0836 — rule at `/candidate/reference-semantics/semantics/subscript.k:18`

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0

```

### INV-0837 — syntax at `/candidate/reference-semantics/semantics/subscript.k:21` — attributes: function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### INV-0838 — rule at `/candidate/reference-semantics/semantics/subscript.k:22`

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### INV-0839 — rule at `/candidate/reference-semantics/semantics/subscript.k:23`

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### INV-0840 — context at `/candidate/reference-semantics/semantics/subscript.k:27`

```k
  context Subscript(HOLE, _)
```

### INV-0841 — context at `/candidate/reference-semantics/semantics/subscript.k:28`

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### INV-0842 — rule at `/candidate/reference-semantics/semantics/subscript.k:31` — attributes: priority

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

```

### INV-0843 — rule at `/candidate/reference-semantics/semantics/subscript.k:35`

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>

```

### INV-0844 — syntax at `/candidate/reference-semantics/semantics/subscript.k:37` — attributes: function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### INV-0845 — rule at `/candidate/reference-semantics/semantics/subscript.k:38`

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### INV-0846 — rule at `/candidate/reference-semantics/semantics/subscript.k:39`

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### INV-0847 — rule at `/candidate/reference-semantics/semantics/subscript.k:40`

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### INV-0848 — syntax at `/candidate/reference-semantics/semantics/subscript.k:44`

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)

```

### INV-0849 — syntax at `/candidate/reference-semantics/semantics/subscript.k:49`

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### INV-0850 — rule at `/candidate/reference-semantics/semantics/subscript.k:50`

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### INV-0851 — rule at `/candidate/reference-semantics/semantics/subscript.k:51`

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### INV-0852 — rule at `/candidate/reference-semantics/semantics/subscript.k:52`

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>

```

### INV-0853 — rule at `/candidate/reference-semantics/semantics/subscript.k:54`

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### INV-0854 — rule at `/candidate/reference-semantics/semantics/subscript.k:55`

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### INV-0855 — rule at `/candidate/reference-semantics/semantics/subscript.k:56`

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### INV-0856 — rule at `/candidate/reference-semantics/semantics/subscript.k:58` — attributes: priority

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### INV-0857 — rule at `/candidate/reference-semantics/semantics/subscript.k:61`

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>

```

### INV-0858 — syntax at `/candidate/reference-semantics/semantics/subscript.k:63` — attributes: function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### INV-0859 — rule at `/candidate/reference-semantics/semantics/subscript.k:64`

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### INV-0860 — rule at `/candidate/reference-semantics/semantics/subscript.k:66`

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### INV-0861 — rule at `/candidate/reference-semantics/semantics/subscript.k:68`

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### INV-0862 — syntax at `/candidate/reference-semantics/semantics/subscript.k:72` — attributes: function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### INV-0863 — rule at `/candidate/reference-semantics/semantics/subscript.k:73`

```k
  rule slStep(noB)          => 1
```

### INV-0864 — rule at `/candidate/reference-semantics/semantics/subscript.k:74`

```k
  rule slStep(someB(S:Int)) => S

```

### INV-0865 — syntax at `/candidate/reference-semantics/semantics/subscript.k:76` — attributes: function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### INV-0866 — rule at `/candidate/reference-semantics/semantics/subscript.k:77`

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### INV-0867 — rule at `/candidate/reference-semantics/semantics/subscript.k:79`

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### INV-0868 — rule at `/candidate/reference-semantics/semantics/subscript.k:81`

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))

```

### INV-0869 — syntax at `/candidate/reference-semantics/semantics/subscript.k:83` — attributes: function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### INV-0870 — rule at `/candidate/reference-semantics/semantics/subscript.k:84`

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### INV-0871 — rule at `/candidate/reference-semantics/semantics/subscript.k:86`

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### INV-0872 — rule at `/candidate/reference-semantics/semantics/subscript.k:88`

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))

```

### INV-0873 — syntax at `/candidate/reference-semantics/semantics/subscript.k:90` — attributes: function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### INV-0874 — rule at `/candidate/reference-semantics/semantics/subscript.k:91`

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### INV-0875 — rule at `/candidate/reference-semantics/semantics/subscript.k:93`

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0

```

### INV-0876 — syntax at `/candidate/reference-semantics/semantics/subscript.k:96` — attributes: function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### INV-0877 — rule at `/candidate/reference-semantics/semantics/subscript.k:97`

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### INV-0878 — rule at `/candidate/reference-semantics/semantics/subscript.k:99`

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0

```

### INV-0879 — syntax at `/candidate/reference-semantics/semantics/subscript.k:102` — attributes: function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### INV-0880 — rule at `/candidate/reference-semantics/semantics/subscript.k:103`

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### INV-0881 — rule at `/candidate/reference-semantics/semantics/subscript.k:105`

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### INV-0882 — syntax at `/candidate/reference-semantics/semantics/subscript.k:109` — attributes: function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### INV-0883 — rule at `/candidate/reference-semantics/semantics/subscript.k:110`

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### INV-0884 — rule at `/candidate/reference-semantics/semantics/subscript.k:113`

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))

```

### INV-0885 — syntax at `/candidate/reference-semantics/semantics/subscript.k:116` — attributes: function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### INV-0886 — rule at `/candidate/reference-semantics/semantics/subscript.k:117`

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### INV-0887 — rule at `/candidate/reference-semantics/semantics/subscript.k:120`

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
endmodule
```

## /candidate/reference-semantics/semantics/syntax.k

### INV-0888 — syntax at `/candidate/reference-semantics/semantics/syntax.k:9` — attributes: macro

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

### INV-0889 — syntax at `/candidate/reference-semantics/semantics/syntax.k:32`

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### INV-0890 — syntax at `/candidate/reference-semantics/semantics/syntax.k:33`

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### INV-0891 — syntax at `/candidate/reference-semantics/semantics/syntax.k:34`

```k
  syntax Entries  ::= List{Entry, ","}
```

### INV-0892 — syntax at `/candidate/reference-semantics/semantics/syntax.k:35`

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### INV-0893 — syntax at `/candidate/reference-semantics/semantics/syntax.k:36`

```k
  syntax CompFors ::= List{CompFor, ""}
```

### INV-0894 — syntax at `/candidate/reference-semantics/semantics/syntax.k:37`

```k
  syntax Exprs    ::= List{Expr, ","}
```

### INV-0895 — syntax at `/candidate/reference-semantics/semantics/syntax.k:38`

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### INV-0896 — syntax at `/candidate/reference-semantics/semantics/syntax.k:39`

```k
  syntax Bound    ::= Expr | "NoBound"

```

### INV-0897 — syntax at `/candidate/reference-semantics/semantics/syntax.k:41`

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

### INV-0898 — syntax at `/candidate/reference-semantics/semantics/syntax.k:56`

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### INV-0899 — syntax at `/candidate/reference-semantics/semantics/syntax.k:57`

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### INV-0900 — syntax at `/candidate/reference-semantics/semantics/syntax.k:58`

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### INV-0901 — syntax at `/candidate/reference-semantics/semantics/syntax.k:59`

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### INV-0902 — syntax at `/candidate/reference-semantics/semantics/syntax.k:60`

```k
  syntax ParamNames ::= List{String, ","}
```

### INV-0903 — syntax at `/candidate/reference-semantics/semantics/syntax.k:61`

```k
  syntax Module     ::= "Module" "(" Stmts ")"
endmodule
```

## /candidate/reference-semantics/semantics/tuple.k

### INV-0904 — rule at `/candidate/reference-semantics/semantics/tuple.k:10`

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### INV-0905 — rule at `/candidate/reference-semantics/semantics/tuple.k:11`

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### INV-0906 — syntax at `/candidate/reference-semantics/semantics/tuple.k:14`

```k
  syntax ApplyK ::= "toTuple"
```

### INV-0907 — rule at `/candidate/reference-semantics/semantics/tuple.k:15`

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### INV-0908 — rule at `/candidate/reference-semantics/semantics/tuple.k:16`

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>

```

### INV-0909 — rule at `/candidate/reference-semantics/semantics/tuple.k:18`

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### INV-0910 — rule at `/candidate/reference-semantics/semantics/tuple.k:20`

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### INV-0911 — rule at `/candidate/reference-semantics/semantics/tuple.k:21`

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### INV-0912 — rule at `/candidate/reference-semantics/semantics/tuple.k:23`

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### INV-0913 — syntax at `/candidate/reference-semantics/semantics/tuple.k:24` — attributes: function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### INV-0914 — rule at `/candidate/reference-semantics/semantics/tuple.k:25`

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### INV-0915 — rule at `/candidate/reference-semantics/semantics/tuple.k:26`

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### INV-0916 — rule at `/candidate/reference-semantics/semantics/tuple.k:28`

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### INV-0917 — syntax at `/candidate/reference-semantics/semantics/tuple.k:31`

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### INV-0918 — rule at `/candidate/reference-semantics/semantics/tuple.k:32`

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### INV-0919 — rule at `/candidate/reference-semantics/semantics/tuple.k:35` — attributes: priority

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### INV-0920 — rule at `/candidate/reference-semantics/semantics/tuple.k:42`

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### INV-0921 — rule at `/candidate/reference-semantics/semantics/tuple.k:43`

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### INV-0922 — rule at `/candidate/reference-semantics/semantics/tuple.k:44` — attributes: priority

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### INV-0923 — syntax at `/candidate/reference-semantics/semantics/tuple.k:49`

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### INV-0924 — rule at `/candidate/reference-semantics/semantics/tuple.k:50`

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### INV-0925 — rule at `/candidate/reference-semantics/semantics/tuple.k:51`

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### INV-0926 — rule at `/candidate/reference-semantics/semantics/tuple.k:52` — attributes: priority

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### INV-0927 — rule at `/candidate/reference-semantics/semantics/tuple.k:55`

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### INV-0928 — rule at `/candidate/reference-semantics/semantics/tuple.k:57`

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
endmodule
```

## /candidate/reference-semantics/semantics.k

## /candidate/spec.k

### INV-0929 — claim at `/candidate/spec.k:7`

```k
  claim
    <k> #loadCountDistinct => .K </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(
        ("count_distinct_characters"
          |-> closureVal(
            ("string", .ParamNames),
            Return(
              Call(
                Name("len"),
                Call(
                  Name("set"),
                  Call(Attribute(Name("string"), "lower"), .Exprs))))
            .Stmts,
            0)),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // For every semantic string, the implementation returns the number of
  // distinct codes after applying the supplied Python-lowercase model.
```

### INV-0930 — claim at `/candidate/spec.k:39`

```k
  claim
    <k>
      #callCountDistinct(CS:IntSeq)
      =>
      isLen(dedupCodes(mapLower(CS)))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
```

## /candidate/verification.k

### INV-0931 — syntax at `/candidate/verification.k:8`

```k
  syntax KItem ::= "#loadCountDistinct"
                 | "#callCountDistinct" "(" IntSeq ")"

```

### INV-0932 — rule at `/candidate/verification.k:11`

```k
  rule #loadCountDistinct
    => FuncDef(
         "count_distinct_characters",
         Params("string"),
         Return(
           Call(
             Name("len"),
             Call(
               Name("set"),
               Call(Attribute(Name("string"), "lower"), .Exprs)))))

```

### INV-0933 — rule at `/candidate/verification.k:22`

```k
  rule #callCountDistinct(CS:IntSeq)
    => #applyK(
         toCall(
           closureVal(
             ("string", .ParamNames),
             Return(
               Call(
                 Name("len"),
                 Call(
                   Name("set"),
                   Call(Attribute(Name("string"), "lower"), .Exprs))))
             .Stmts,
             0)),
         (str(CS), .Vals))
endmodule
```

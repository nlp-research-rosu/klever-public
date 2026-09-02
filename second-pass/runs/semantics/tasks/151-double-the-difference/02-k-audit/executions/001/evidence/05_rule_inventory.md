# Exhaustive K source inventory

Generated from every mounted supplied-semantics K source plus candidate
`verification.k` and `spec.k`. Each item preserves its complete source
block through the next top-level K declaration.

## Summary

- Files: 26
- Top-level inventory entries: 1112
- `claim`: 2
- `configuration`: 1
- `context`: 5
- `endmodule`: 27
- `equational-rule`: 419
- `function-syntax`: 148
- `imports`: 88
- `module`: 27
- `operational-rule`: 241
- `priority-rule`: 45
- `requires`: 25
- `syntax`: 84

| File | Entries | Rules/claims |
|---|---:|---:|
| `reference-semantics/semantics.k` | 50 | 0 |
| `reference-semantics/semantics/assert.k` | 6 | 3 |
| `reference-semantics/semantics/bool.k` | 17 | 13 |
| `reference-semantics/semantics/builtins.k` | 184 | 137 |
| `reference-semantics/semantics/call.k` | 29 | 21 |
| `reference-semantics/semantics/comprehension.k` | 17 | 7 |
| `reference-semantics/semantics/concrete.k` | 24 | 16 |
| `reference-semantics/semantics/controls.k` | 42 | 34 |
| `reference-semantics/semantics/core.k` | 93 | 46 |
| `reference-semantics/semantics/dict.k` | 46 | 28 |
| `reference-semantics/semantics/float.k` | 160 | 121 |
| `reference-semantics/semantics/functions.k` | 22 | 15 |
| `reference-semantics/semantics/int.k` | 20 | 16 |
| `reference-semantics/semantics/iter.k` | 4 | 0 |
| `reference-semantics/semantics/list.k` | 37 | 27 |
| `reference-semantics/semantics/methods.k` | 108 | 75 |
| `reference-semantics/semantics/operators.k` | 16 | 10 |
| `reference-semantics/semantics/range.k` | 12 | 6 |
| `reference-semantics/semantics/set.k` | 21 | 12 |
| `reference-semantics/semantics/sort.k` | 29 | 19 |
| `reference-semantics/semantics/str.k` | 37 | 28 |
| `reference-semantics/semantics/subscript.k` | 60 | 40 |
| `reference-semantics/semantics/syntax.k` | 22 | 0 |
| `reference-semantics/semantics/tuple.k` | 31 | 21 |
| `spec.k` | 6 | 2 |
| `verification.k` | 19 | 10 |

## Entries

### I0001 — `reference-semantics/semantics.k:34` (requires; attributes: `none`)

```k
requires "semantics/syntax.k"
```

### I0002 — `reference-semantics/semantics.k:35` (requires; attributes: `none`)

```k
requires "semantics/core.k"
```

### I0003 — `reference-semantics/semantics.k:36` (requires; attributes: `none`)

```k
requires "semantics/iter.k"
```

### I0004 — `reference-semantics/semantics.k:37` (requires; attributes: `none`)

```k
requires "semantics/range.k"
```

### I0005 — `reference-semantics/semantics.k:38` (requires; attributes: `none`)

```k
requires "semantics/operators.k"
```

### I0006 — `reference-semantics/semantics.k:39` (requires; attributes: `none`)

```k
requires "semantics/int.k"
```

### I0007 — `reference-semantics/semantics.k:40` (requires; attributes: `none`)

```k
requires "semantics/bool.k"
```

### I0008 — `reference-semantics/semantics.k:41` (requires; attributes: `none`)

```k
requires "semantics/float.k"
```

### I0009 — `reference-semantics/semantics.k:42` (requires; attributes: `none`)

```k
requires "semantics/str.k"
```

### I0010 — `reference-semantics/semantics.k:43` (requires; attributes: `none`)

```k
requires "semantics/set.k"
```

### I0011 — `reference-semantics/semantics.k:44` (requires; attributes: `none`)

```k
requires "semantics/list.k"
```

### I0012 — `reference-semantics/semantics.k:45` (requires; attributes: `none`)

```k
requires "semantics/tuple.k"
```

### I0013 — `reference-semantics/semantics.k:46` (requires; attributes: `none`)

```k
requires "semantics/subscript.k"
```

### I0014 — `reference-semantics/semantics.k:47` (requires; attributes: `none`)

```k
requires "semantics/comprehension.k"
```

### I0015 — `reference-semantics/semantics.k:48` (requires; attributes: `none`)

```k
requires "semantics/methods.k"
```

### I0016 — `reference-semantics/semantics.k:49` (requires; attributes: `none`)

```k
requires "semantics/controls.k"
```

### I0017 — `reference-semantics/semantics.k:50` (requires; attributes: `none`)

```k
requires "semantics/functions.k"
```

### I0018 — `reference-semantics/semantics.k:51` (requires; attributes: `none`)

```k
requires "semantics/builtins.k"
```

### I0019 — `reference-semantics/semantics.k:52` (requires; attributes: `none`)

```k
requires "semantics/call.k"
```

### I0020 — `reference-semantics/semantics.k:53` (requires; attributes: `none`)

```k
requires "semantics/sort.k"
```

### I0021 — `reference-semantics/semantics.k:54` (requires; attributes: `none`)

```k
requires "semantics/assert.k"
```

### I0022 — `reference-semantics/semantics.k:55` (requires; attributes: `none`)

```k
requires "semantics/dict.k"
```

### I0023 — `reference-semantics/semantics.k:56` (requires; attributes: `none`)

```k
requires "semantics/concrete.k"
```

### I0024 — `reference-semantics/semantics.k:58` (module; attributes: `none`)

```k
module MPY
```

### I0025 — `reference-semantics/semantics.k:59` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0026 — `reference-semantics/semantics.k:60` (imports; attributes: `none`)

```k
  imports MPY-ITER
```

### I0027 — `reference-semantics/semantics.k:61` (imports; attributes: `none`)

```k
  imports MPY-RANGE
```

### I0028 — `reference-semantics/semantics.k:62` (imports; attributes: `none`)

```k
  imports MPY-OPERATORS
```

### I0029 — `reference-semantics/semantics.k:63` (imports; attributes: `none`)

```k
  imports MPY-INT
```

### I0030 — `reference-semantics/semantics.k:64` (imports; attributes: `none`)

```k
  imports MPY-BOOL
```

### I0031 — `reference-semantics/semantics.k:65` (imports; attributes: `none`)

```k
  imports MPY-FLOAT
```

### I0032 — `reference-semantics/semantics.k:66` (imports; attributes: `none`)

```k
  imports MPY-STR
```

### I0033 — `reference-semantics/semantics.k:67` (imports; attributes: `none`)

```k
  imports MPY-SET
```

### I0034 — `reference-semantics/semantics.k:68` (imports; attributes: `none`)

```k
  imports MPY-LIST
```

### I0035 — `reference-semantics/semantics.k:69` (imports; attributes: `none`)

```k
  imports MPY-TUPLE
```

### I0036 — `reference-semantics/semantics.k:70` (imports; attributes: `none`)

```k
  imports MPY-SUBSCRIPT
```

### I0037 — `reference-semantics/semantics.k:71` (imports; attributes: `none`)

```k
  imports MPY-COMPREHENSION
```

### I0038 — `reference-semantics/semantics.k:72` (imports; attributes: `none`)

```k
  imports MPY-METHODS
```

### I0039 — `reference-semantics/semantics.k:73` (imports; attributes: `none`)

```k
  imports MPY-CONTROLS
```

### I0040 — `reference-semantics/semantics.k:74` (imports; attributes: `none`)

```k
  imports MPY-FUNCTIONS
```

### I0041 — `reference-semantics/semantics.k:75` (imports; attributes: `none`)

```k
  imports MPY-BUILTINS
```

### I0042 — `reference-semantics/semantics.k:76` (imports; attributes: `none`)

```k
  imports MPY-CALL
```

### I0043 — `reference-semantics/semantics.k:77` (imports; attributes: `none`)

```k
  imports MPY-SORT
```

### I0044 — `reference-semantics/semantics.k:78` (imports; attributes: `none`)

```k
  imports MPY-ASSERT
```

### I0045 — `reference-semantics/semantics.k:79` (imports; attributes: `none`)

```k
  imports MPY-DICT
```

### I0046 — `reference-semantics/semantics.k:80` (endmodule; attributes: `none`)

```k
endmodule

// The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's
// real key calls, deep list equality). Verification builds import MPY and
// never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN —
// with plain MPY the concrete legs are silently absent (this was live for a
// while: sorted-key stuck and comprehension asserted wrong under krun).
```

### I0047 — `reference-semantics/semantics.k:87` (module; attributes: `none`)

```k
module MPY-KRUN
```

### I0048 — `reference-semantics/semantics.k:88` (imports; attributes: `none`)

```k
  imports MPY
```

### I0049 — `reference-semantics/semantics.k:89` (imports; attributes: `none`)

```k
  imports MPY-CONCRETE
```

### I0050 — `reference-semantics/semantics.k:90` (endmodule; attributes: `none`)

```k
endmodule
```

### I0051 — `reference-semantics/semantics/assert.k:3` (module; attributes: `none`)

```k
module MPY-ASSERT
```

### I0052 — `reference-semantics/semantics/assert.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0053 — `reference-semantics/semantics/assert.k:6` (operational-rule; attributes: `none`)

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### I0054 — `reference-semantics/semantics/assert.k:8` (operational-rule; attributes: `none`)

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### I0055 — `reference-semantics/semantics/assert.k:13` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0056 — `reference-semantics/semantics/assert.k:16` (endmodule; attributes: `none`)

```k
endmodule
```

### I0057 — `reference-semantics/semantics/bool.k:5` (module; attributes: `none`)

```k
module MPY-BOOL
```

### I0058 — `reference-semantics/semantics/bool.k:6` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0059 — `reference-semantics/semantics/bool.k:8` (equational-rule; attributes: `none`)

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### I0060 — `reference-semantics/semantics/bool.k:10` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### I0061 — `reference-semantics/semantics/bool.k:11` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### I0062 — `reference-semantics/semantics/bool.k:16` (context; attributes: `none`)

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### I0063 — `reference-semantics/semantics/bool.k:17` (operational-rule; attributes: `none`)

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### I0064 — `reference-semantics/semantics/bool.k:18` (operational-rule; attributes: `none`)

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### I0065 — `reference-semantics/semantics/bool.k:20` (operational-rule; attributes: `none`)

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### I0066 — `reference-semantics/semantics/bool.k:22` (operational-rule; attributes: `none`)

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### I0067 — `reference-semantics/semantics/bool.k:24` (operational-rule; attributes: `none`)

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### I0068 — `reference-semantics/semantics/bool.k:29` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### I0069 — `reference-semantics/semantics/bool.k:31` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### I0070 — `reference-semantics/semantics/bool.k:35` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### I0071 — `reference-semantics/semantics/bool.k:39` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### I0072 — `reference-semantics/semantics/bool.k:43` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### I0073 — `reference-semantics/semantics/bool.k:47` (endmodule; attributes: `none`)

```k
endmodule
```

### I0074 — `reference-semantics/semantics/builtins.k:3` (module; attributes: `none`)

```k
module MPY-BUILTINS
```

### I0075 — `reference-semantics/semantics/builtins.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0076 — `reference-semantics/semantics/builtins.k:5` (imports; attributes: `none`)

```k
  imports MPY-STR
```

### I0077 — `reference-semantics/semantics/builtins.k:6` (imports; attributes: `none`)

```k
  imports MPY-SET
```

### I0078 — `reference-semantics/semantics/builtins.k:7` (imports; attributes: `none`)

```k
  imports MPY-ITER
```

### I0079 — `reference-semantics/semantics/builtins.k:8` (imports; attributes: `none`)

```k
  imports MPY-RANGE
```

### I0080 — `reference-semantics/semantics/builtins.k:9` (imports; attributes: `none`)

```k
  imports MPY-INT
```

### I0081 — `reference-semantics/semantics/builtins.k:10` (imports; attributes: `none`)

```k
  imports MPY-METHODS

  // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup

  // Call routing + argument evaluation live in call.k, which also routes the fold
  // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to
  // applyBuiltin. This module owns applyBuiltin + the fold implementations.
```

### I0082 — `reference-semantics/semantics/builtins.k:17` (function-syntax; attributes: `function`)

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### I0083 — `reference-semantics/semantics/builtins.k:20` (function-syntax; attributes: `function`)

```k
  syntax Int ::= seqLen(Val) [function]
```

### I0084 — `reference-semantics/semantics/builtins.k:21` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### I0085 — `reference-semantics/semantics/builtins.k:22` (equational-rule; attributes: `none`)

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### I0086 — `reference-semantics/semantics/builtins.k:23` (equational-rule; attributes: `none`)

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### I0087 — `reference-semantics/semantics/builtins.k:24` (equational-rule; attributes: `none`)

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### I0088 — `reference-semantics/semantics/builtins.k:25` (equational-rule; attributes: `none`)

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### I0089 — `reference-semantics/semantics/builtins.k:26` (equational-rule; attributes: `none`)

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### I0090 — `reference-semantics/semantics/builtins.k:32` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### I0091 — `reference-semantics/semantics/builtins.k:33` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### I0092 — `reference-semantics/semantics/builtins.k:34` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### I0093 — `reference-semantics/semantics/builtins.k:35` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### I0094 — `reference-semantics/semantics/builtins.k:36` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### I0095 — `reference-semantics/semantics/builtins.k:37` (equational-rule; attributes: `none`)

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### I0096 — `reference-semantics/semantics/builtins.k:38` (equational-rule; attributes: `none`)

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### I0097 — `reference-semantics/semantics/builtins.k:41` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### I0098 — `reference-semantics/semantics/builtins.k:44` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### I0099 — `reference-semantics/semantics/builtins.k:47` (syntax; attributes: `none`)

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### I0100 — `reference-semantics/semantics/builtins.k:48` (operational-rule; attributes: `none`)

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### I0101 — `reference-semantics/semantics/builtins.k:49` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### I0102 — `reference-semantics/semantics/builtins.k:50` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### I0103 — `reference-semantics/semantics/builtins.k:54` (function-syntax; attributes: `function`)

```k
  syntax Int ::= intOf(Val) [function]
```

### I0104 — `reference-semantics/semantics/builtins.k:55` (equational-rule; attributes: `none`)

```k
  rule intOf(I:Int)  => I
```

### I0105 — `reference-semantics/semantics/builtins.k:56` (equational-rule; attributes: `none`)

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### I0106 — `reference-semantics/semantics/builtins.k:59` (syntax; attributes: `none`)

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### I0107 — `reference-semantics/semantics/builtins.k:60` (operational-rule; attributes: `none`)

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### I0108 — `reference-semantics/semantics/builtins.k:61` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### I0109 — `reference-semantics/semantics/builtins.k:62` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### I0110 — `reference-semantics/semantics/builtins.k:64` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### I0111 — `reference-semantics/semantics/builtins.k:67` (syntax; attributes: `none`)

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### I0112 — `reference-semantics/semantics/builtins.k:68` (operational-rule; attributes: `none`)

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### I0113 — `reference-semantics/semantics/builtins.k:69` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### I0114 — `reference-semantics/semantics/builtins.k:70` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### I0115 — `reference-semantics/semantics/builtins.k:72` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### I0116 — `reference-semantics/semantics/builtins.k:76` (syntax; attributes: `none`)

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### I0117 — `reference-semantics/semantics/builtins.k:77` (operational-rule; attributes: `none`)

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### I0118 — `reference-semantics/semantics/builtins.k:78` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### I0119 — `reference-semantics/semantics/builtins.k:80` (operational-rule; attributes: `none`)

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### I0120 — `reference-semantics/semantics/builtins.k:81` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### I0121 — `reference-semantics/semantics/builtins.k:82` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### I0122 — `reference-semantics/semantics/builtins.k:86` (syntax; attributes: `none`)

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### I0123 — `reference-semantics/semantics/builtins.k:87` (operational-rule; attributes: `none`)

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### I0124 — `reference-semantics/semantics/builtins.k:88` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### I0125 — `reference-semantics/semantics/builtins.k:90` (operational-rule; attributes: `none`)

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### I0126 — `reference-semantics/semantics/builtins.k:91` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### I0127 — `reference-semantics/semantics/builtins.k:92` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### I0128 — `reference-semantics/semantics/builtins.k:97` (function-syntax; attributes: `function`)

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### I0129 — `reference-semantics/semantics/builtins.k:98` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### I0130 — `reference-semantics/semantics/builtins.k:99` (equational-rule; attributes: `none`)

```k
  rule maxVals(M:Int, .Vals)           => M
```

### I0131 — `reference-semantics/semantics/builtins.k:100` (equational-rule; attributes: `none`)

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### I0132 — `reference-semantics/semantics/builtins.k:102` (function-syntax; attributes: `function`)

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### I0133 — `reference-semantics/semantics/builtins.k:103` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### I0134 — `reference-semantics/semantics/builtins.k:104` (equational-rule; attributes: `none`)

```k
  rule minVals(M:Int, .Vals)           => M
```

### I0135 — `reference-semantics/semantics/builtins.k:105` (equational-rule; attributes: `none`)

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### I0136 — `reference-semantics/semantics/builtins.k:108` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### I0137 — `reference-semantics/semantics/builtins.k:111` (operational-rule; attributes: `none`)

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### I0138 — `reference-semantics/semantics/builtins.k:114` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### I0139 — `reference-semantics/semantics/builtins.k:115` (equational-rule; attributes: `none`)

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### I0140 — `reference-semantics/semantics/builtins.k:116` (equational-rule; attributes: `none`)

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### I0141 — `reference-semantics/semantics/builtins.k:117` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### I0142 — `reference-semantics/semantics/builtins.k:118` (equational-rule; attributes: `none`)

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### I0143 — `reference-semantics/semantics/builtins.k:119` (equational-rule; attributes: `none`)

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### I0144 — `reference-semantics/semantics/builtins.k:124` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### I0145 — `reference-semantics/semantics/builtins.k:126` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### I0146 — `reference-semantics/semantics/builtins.k:127` (equational-rule; attributes: `none`)

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### I0147 — `reference-semantics/semantics/builtins.k:128` (equational-rule; attributes: `none`)

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### I0148 — `reference-semantics/semantics/builtins.k:132` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### I0149 — `reference-semantics/semantics/builtins.k:134` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### I0150 — `reference-semantics/semantics/builtins.k:135` (equational-rule; attributes: `none`)

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### I0151 — `reference-semantics/semantics/builtins.k:136` (equational-rule; attributes: `none`)

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### I0152 — `reference-semantics/semantics/builtins.k:137` (equational-rule; attributes: `none`)

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### I0153 — `reference-semantics/semantics/builtins.k:140` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### I0154 — `reference-semantics/semantics/builtins.k:143` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### I0155 — `reference-semantics/semantics/builtins.k:144` (operational-rule; attributes: `none`)

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### I0156 — `reference-semantics/semantics/builtins.k:148` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### I0157 — `reference-semantics/semantics/builtins.k:149` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### I0158 — `reference-semantics/semantics/builtins.k:152` (operational-rule; attributes: `none`)

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### I0159 — `reference-semantics/semantics/builtins.k:156` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### I0160 — `reference-semantics/semantics/builtins.k:158` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### I0161 — `reference-semantics/semantics/builtins.k:159` (equational-rule; attributes: `none`)

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### I0162 — `reference-semantics/semantics/builtins.k:160` (equational-rule; attributes: `none`)

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### I0163 — `reference-semantics/semantics/builtins.k:163` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### I0164 — `reference-semantics/semantics/builtins.k:164` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### I0165 — `reference-semantics/semantics/builtins.k:167` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### I0166 — `reference-semantics/semantics/builtins.k:169` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### I0167 — `reference-semantics/semantics/builtins.k:170` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### I0168 — `reference-semantics/semantics/builtins.k:171` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### I0169 — `reference-semantics/semantics/builtins.k:173` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### I0170 — `reference-semantics/semantics/builtins.k:174` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### I0171 — `reference-semantics/semantics/builtins.k:177` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### I0172 — `reference-semantics/semantics/builtins.k:178` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### I0173 — `reference-semantics/semantics/builtins.k:179` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### I0174 — `reference-semantics/semantics/builtins.k:187` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### I0175 — `reference-semantics/semantics/builtins.k:188` (function-syntax; attributes: `function`)

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### I0176 — `reference-semantics/semantics/builtins.k:189` (equational-rule; attributes: `none`)

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### I0177 — `reference-semantics/semantics/builtins.k:192` (syntax; attributes: `none`)

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### I0178 — `reference-semantics/semantics/builtins.k:194` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### I0179 — `reference-semantics/semantics/builtins.k:195` (operational-rule; attributes: `none`)

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### I0180 — `reference-semantics/semantics/builtins.k:196` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### I0181 — `reference-semantics/semantics/builtins.k:197` (equational-rule; attributes: `none`)

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### I0182 — `reference-semantics/semantics/builtins.k:198` (equational-rule; attributes: `owise`)

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### I0183 — `reference-semantics/semantics/builtins.k:199` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### I0184 — `reference-semantics/semantics/builtins.k:200` (equational-rule; attributes: `none`)

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### I0185 — `reference-semantics/semantics/builtins.k:201` (equational-rule; attributes: `owise`)

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### I0186 — `reference-semantics/semantics/builtins.k:203` (function-syntax; attributes: `function, total`)

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### I0187 — `reference-semantics/semantics/builtins.k:204` (equational-rule; attributes: `none`)

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### I0188 — `reference-semantics/semantics/builtins.k:205` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### I0189 — `reference-semantics/semantics/builtins.k:206` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### I0190 — `reference-semantics/semantics/builtins.k:207` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### I0191 — `reference-semantics/semantics/builtins.k:208` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### I0192 — `reference-semantics/semantics/builtins.k:209` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### I0193 — `reference-semantics/semantics/builtins.k:210` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### I0194 — `reference-semantics/semantics/builtins.k:211` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### I0195 — `reference-semantics/semantics/builtins.k:212` (equational-rule; attributes: `none`)

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### I0196 — `reference-semantics/semantics/builtins.k:214` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### I0197 — `reference-semantics/semantics/builtins.k:216` (equational-rule; attributes: `none`)

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### I0198 — `reference-semantics/semantics/builtins.k:217` (equational-rule; attributes: `none`)

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### I0199 — `reference-semantics/semantics/builtins.k:218` (equational-rule; attributes: `none`)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### I0200 — `reference-semantics/semantics/builtins.k:219` (equational-rule; attributes: `none`)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### I0201 — `reference-semantics/semantics/builtins.k:221` (equational-rule; attributes: `none`)

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### I0202 — `reference-semantics/semantics/builtins.k:223` (equational-rule; attributes: `owise`)

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### I0203 — `reference-semantics/semantics/builtins.k:225` (syntax; attributes: `none`)

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### I0204 — `reference-semantics/semantics/builtins.k:226` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### I0205 — `reference-semantics/semantics/builtins.k:227` (equational-rule; attributes: `none`)

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### I0206 — `reference-semantics/semantics/builtins.k:228` (equational-rule; attributes: `owise`)

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### I0207 — `reference-semantics/semantics/builtins.k:230` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### I0208 — `reference-semantics/semantics/builtins.k:231` (equational-rule; attributes: `none`)

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### I0209 — `reference-semantics/semantics/builtins.k:232` (equational-rule; attributes: `none`)

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### I0210 — `reference-semantics/semantics/builtins.k:233` (equational-rule; attributes: `none`)

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### I0211 — `reference-semantics/semantics/builtins.k:234` (equational-rule; attributes: `none`)

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### I0212 — `reference-semantics/semantics/builtins.k:235` (equational-rule; attributes: `none`)

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### I0213 — `reference-semantics/semantics/builtins.k:236` (equational-rule; attributes: `owise`)

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### I0214 — `reference-semantics/semantics/builtins.k:238` (function-syntax; attributes: `function, total`)

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### I0215 — `reference-semantics/semantics/builtins.k:239` (equational-rule; attributes: `none`)

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### I0216 — `reference-semantics/semantics/builtins.k:240` (equational-rule; attributes: `none`)

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### I0217 — `reference-semantics/semantics/builtins.k:241` (equational-rule; attributes: `none`)

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### I0218 — `reference-semantics/semantics/builtins.k:243` (equational-rule; attributes: `owise`)

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### I0219 — `reference-semantics/semantics/builtins.k:244` (function-syntax; attributes: `function, total`)

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### I0220 — `reference-semantics/semantics/builtins.k:245` (equational-rule; attributes: `none`)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### I0221 — `reference-semantics/semantics/builtins.k:246` (equational-rule; attributes: `none`)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### I0222 — `reference-semantics/semantics/builtins.k:247` (function-syntax; attributes: `function, total`)

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### I0223 — `reference-semantics/semantics/builtins.k:248` (equational-rule; attributes: `none`)

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### I0224 — `reference-semantics/semantics/builtins.k:250` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### I0225 — `reference-semantics/semantics/builtins.k:251` (equational-rule; attributes: `none`)

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### I0226 — `reference-semantics/semantics/builtins.k:252` (equational-rule; attributes: `none`)

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### I0227 — `reference-semantics/semantics/builtins.k:253` (equational-rule; attributes: `none`)

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### I0228 — `reference-semantics/semantics/builtins.k:254` (equational-rule; attributes: `none`)

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### I0229 — `reference-semantics/semantics/builtins.k:255` (function-syntax; attributes: `function, total`)

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### I0230 — `reference-semantics/semantics/builtins.k:256` (equational-rule; attributes: `none`)

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### I0231 — `reference-semantics/semantics/builtins.k:257` (equational-rule; attributes: `none`)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### I0232 — `reference-semantics/semantics/builtins.k:260` (equational-rule; attributes: `none`)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### I0233 — `reference-semantics/semantics/builtins.k:263` (equational-rule; attributes: `owise`)

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### I0234 — `reference-semantics/semantics/builtins.k:265` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### I0235 — `reference-semantics/semantics/builtins.k:266` (equational-rule; attributes: `none`)

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### I0236 — `reference-semantics/semantics/builtins.k:267` (equational-rule; attributes: `none`)

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### I0237 — `reference-semantics/semantics/builtins.k:268` (equational-rule; attributes: `owise`)

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### I0238 — `reference-semantics/semantics/builtins.k:269` (function-syntax; attributes: `function, total`)

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### I0239 — `reference-semantics/semantics/builtins.k:270` (equational-rule; attributes: `none`)

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### I0240 — `reference-semantics/semantics/builtins.k:271` (equational-rule; attributes: `none`)

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### I0241 — `reference-semantics/semantics/builtins.k:272` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### I0242 — `reference-semantics/semantics/builtins.k:273` (equational-rule; attributes: `none`)

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### I0243 — `reference-semantics/semantics/builtins.k:274` (equational-rule; attributes: `none`)

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### I0244 — `reference-semantics/semantics/builtins.k:279` (syntax; attributes: `none`)

```k
  syntax KItem ::= "#md5"
```

### I0245 — `reference-semantics/semantics/builtins.k:280` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### I0246 — `reference-semantics/semantics/builtins.k:282` (operational-rule; attributes: `none`)

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### I0247 — `reference-semantics/semantics/builtins.k:283` (syntax; attributes: `none`)

```k
  syntax Val ::= md5Obj(IntSeq)
```

### I0248 — `reference-semantics/semantics/builtins.k:284` (equational-rule; attributes: `none`)

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### I0249 — `reference-semantics/semantics/builtins.k:285` (function-syntax; attributes: `function, total, symbol(md5hexCodes), no-evaluators`)

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### I0250 — `reference-semantics/semantics/builtins.k:291` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### I0251 — `reference-semantics/semantics/builtins.k:292` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### I0252 — `reference-semantics/semantics/builtins.k:293` (function-syntax; attributes: `function,function`)

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### I0253 — `reference-semantics/semantics/builtins.k:294` (equational-rule; attributes: `none`)

```k
  rule isIntV(_:Int)         => true
```

### I0254 — `reference-semantics/semantics/builtins.k:295` (equational-rule; attributes: `owise`)

```k
  rule isIntV(_:Val)         => false [owise]
```

### I0255 — `reference-semantics/semantics/builtins.k:296` (equational-rule; attributes: `none`)

```k
  rule isStrV(str(_:IntSeq)) => true
```

### I0256 — `reference-semantics/semantics/builtins.k:297` (equational-rule; attributes: `owise`)

```k
  rule isStrV(_:Val)         => false [owise]
```

### I0257 — `reference-semantics/semantics/builtins.k:298` (endmodule; attributes: `none`)

```k
endmodule
```

### I0258 — `reference-semantics/semantics/call.k:10` (module; attributes: `none`)

```k
module MPY-CALL
```

### I0259 — `reference-semantics/semantics/call.k:11` (imports; attributes: `none`)

```k
  imports MPY-METHODS
```

### I0260 — `reference-semantics/semantics/call.k:12` (imports; attributes: `none`)

```k
  imports MPY-BUILTINS
```

### I0261 — `reference-semantics/semantics/call.k:13` (imports; attributes: `none`)

```k
  imports MPY-FUNCTIONS

  // a cooled attribute is a bound method value
```

### I0262 — `reference-semantics/semantics/call.k:16` (operational-rule; attributes: `owise`)

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### I0263 — `reference-semantics/semantics/call.k:19` (syntax; attributes: `none`)

```k
  syntax KItem ::= #callee(Exprs)
```

### I0264 — `reference-semantics/semantics/call.k:20` (operational-rule; attributes: `owise`)

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### I0265 — `reference-semantics/semantics/call.k:21` (operational-rule; attributes: `none`)

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### I0266 — `reference-semantics/semantics/call.k:24` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### I0267 — `reference-semantics/semantics/call.k:26` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### I0268 — `reference-semantics/semantics/call.k:27` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### I0269 — `reference-semantics/semantics/call.k:28` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### I0270 — `reference-semantics/semantics/call.k:29` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### I0271 — `reference-semantics/semantics/call.k:30` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### I0272 — `reference-semantics/semantics/call.k:31` (operational-rule; attributes: `owise`)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### I0273 — `reference-semantics/semantics/call.k:32` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### I0274 — `reference-semantics/semantics/call.k:38` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0275 — `reference-semantics/semantics/call.k:42` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### I0276 — `reference-semantics/semantics/call.k:47` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0277 — `reference-semantics/semantics/call.k:52` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### I0278 — `reference-semantics/semantics/call.k:53` (equational-rule; attributes: `none`)

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### I0279 — `reference-semantics/semantics/call.k:56` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### I0280 — `reference-semantics/semantics/call.k:63` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### I0281 — `reference-semantics/semantics/call.k:69` (operational-rule; attributes: ` NEWL <- scope(.Map, parent(DEFL)) `)

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

### I0282 — `reference-semantics/semantics/call.k:80` (operational-rule; attributes: ` NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) `)

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### I0283 — `reference-semantics/semantics/call.k:87` (syntax; attributes: `none`)

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### I0284 — `reference-semantics/semantics/call.k:88` (operational-rule; attributes: `none`)

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### I0285 — `reference-semantics/semantics/call.k:89` (operational-rule; attributes: ` CV <- cellRef(N) `)

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### I0286 — `reference-semantics/semantics/call.k:95` (endmodule; attributes: `none`)

```k
endmodule
```

### I0287 — `reference-semantics/semantics/comprehension.k:3` (module; attributes: `none`)

```k
module MPY-COMPREHENSION
```

### I0288 — `reference-semantics/semantics/comprehension.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0289 — `reference-semantics/semantics/comprehension.k:5` (imports; attributes: `none`)

```k
  imports MPY-OPERATORS
```

### I0290 — `reference-semantics/semantics/comprehension.k:6` (imports; attributes: `none`)

```k
  imports MPY-LIST
```

### I0291 — `reference-semantics/semantics/comprehension.k:7` (imports; attributes: `none`)

```k
  imports MPY-CONTROLS
```

### I0292 — `reference-semantics/semantics/comprehension.k:8` (imports; attributes: `none`)

```k
  imports MPY-FUNCTIONS

  // A comprehension is pure syntactic sugar
```

### I0293 — `reference-semantics/semantics/comprehension.k:11` (equational-rule; attributes: `none`)

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### I0294 — `reference-semantics/semantics/comprehension.k:12` (equational-rule; attributes: `none`)

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### I0295 — `reference-semantics/semantics/comprehension.k:14` (syntax; attributes: `macro`)

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### I0296 — `reference-semantics/semantics/comprehension.k:15` (equational-rule; attributes: `none`)

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### I0297 — `reference-semantics/semantics/comprehension.k:18` (syntax; attributes: `macro-rec`)

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### I0298 — `reference-semantics/semantics/comprehension.k:19` (equational-rule; attributes: `none`)

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### I0299 — `reference-semantics/semantics/comprehension.k:21` (equational-rule; attributes: `none`)

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### I0300 — `reference-semantics/semantics/comprehension.k:24` (syntax; attributes: `macro`)

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### I0301 — `reference-semantics/semantics/comprehension.k:25` (equational-rule; attributes: `none`)

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### I0302 — `reference-semantics/semantics/comprehension.k:26` (equational-rule; attributes: `none`)

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### I0303 — `reference-semantics/semantics/comprehension.k:27` (endmodule; attributes: `none`)

```k
endmodule
```

### I0304 — `reference-semantics/semantics/concrete.k:8` (module; attributes: `none`)

```k
module MPY-CONCRETE
```

### I0305 — `reference-semantics/semantics/concrete.k:9` (imports; attributes: `none`)

```k
  imports MPY

  // deep equality for list compares whose elements are heap objects
  // (list-of-lists): Python == is structural at every depth.
```

### I0306 — `reference-semantics/semantics/concrete.k:13` (operational-rule; attributes: `none`)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### I0307 — `reference-semantics/semantics/concrete.k:16` (operational-rule; attributes: `none`)

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

### I0308 — `reference-semantics/semantics/concrete.k:25` (syntax; attributes: `none`)

```k
  syntax Val ::= kvP(Val, Val)
```

### I0309 — `reference-semantics/semantics/concrete.k:26` (syntax; attributes: `none`)

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### I0310 — `reference-semantics/semantics/concrete.k:28` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### I0311 — `reference-semantics/semantics/concrete.k:31` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### I0312 — `reference-semantics/semantics/concrete.k:34` (operational-rule; attributes: `none`)

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### I0313 — `reference-semantics/semantics/concrete.k:36` (operational-rule; attributes: `none`)

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### I0314 — `reference-semantics/semantics/concrete.k:38` (operational-rule; attributes: `none`)

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### I0315 — `reference-semantics/semantics/concrete.k:42` (function-syntax; attributes: `function`)

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### I0316 — `reference-semantics/semantics/concrete.k:43` (equational-rule; attributes: `none`)

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### I0317 — `reference-semantics/semantics/concrete.k:44` (equational-rule; attributes: `none`)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### I0318 — `reference-semantics/semantics/concrete.k:47` (equational-rule; attributes: `none`)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### I0319 — `reference-semantics/semantics/concrete.k:51` (function-syntax; attributes: `function`)

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### I0320 — `reference-semantics/semantics/concrete.k:52` (operational-rule; attributes: `none`)

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### I0321 — `reference-semantics/semantics/concrete.k:53` (operational-rule; attributes: `none`)

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### I0322 — `reference-semantics/semantics/concrete.k:54` (equational-rule; attributes: `none`)

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### I0323 — `reference-semantics/semantics/concrete.k:56` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### I0324 — `reference-semantics/semantics/concrete.k:57` (equational-rule; attributes: `none`)

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### I0325 — `reference-semantics/semantics/concrete.k:58` (equational-rule; attributes: `none`)

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### I0326 — `reference-semantics/semantics/concrete.k:59` (equational-rule; attributes: `owise`)

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### I0327 — `reference-semantics/semantics/concrete.k:60` (endmodule; attributes: `none`)

```k
endmodule
```

### I0328 — `reference-semantics/semantics/controls.k:3` (module; attributes: `none`)

```k
module MPY-CONTROLS
```

### I0329 — `reference-semantics/semantics/controls.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0330 — `reference-semantics/semantics/controls.k:5` (imports; attributes: `none`)

```k
  imports MPY-TUPLE
```

### I0331 — `reference-semantics/semantics/controls.k:6` (imports; attributes: `none`)

```k
  imports MPY-ITER

  // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==
```

### I0332 — `reference-semantics/semantics/controls.k:9` (operational-rule; attributes: ` X <- V `)

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### I0333 — `reference-semantics/semantics/controls.k:12` (priority-rule; attributes: `X,"$cells",X,priority(40)`)

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### I0334 — `reference-semantics/semantics/controls.k:20` (operational-rule; attributes: ` X <- applyBin(OP, {M[X,..`)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### I0335 — `reference-semantics/semantics/controls.k:27` (priority-rule; attributes: `X,priority(40)`)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### I0336 — `reference-semantics/semantics/controls.k:35` (operational-rule; attributes: `none`)

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### I0337 — `reference-semantics/semantics/controls.k:36` (operational-rule; attributes: `owise`)

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### I0338 — `reference-semantics/semantics/controls.k:37` (syntax; attributes: `none`)

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### I0339 — `reference-semantics/semantics/controls.k:38` (operational-rule; attributes: `none`)

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### I0340 — `reference-semantics/semantics/controls.k:39` (operational-rule; attributes: ` N <- builtinV(N) `)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### I0341 — `reference-semantics/semantics/controls.k:43` (operational-rule; attributes: `none`)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### I0342 — `reference-semantics/semantics/controls.k:48` (operational-rule; attributes: `none`)

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### I0343 — `reference-semantics/semantics/controls.k:51` (syntax; attributes: `none`)

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### I0344 — `reference-semantics/semantics/controls.k:52` (operational-rule; attributes: `none`)

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### I0345 — `reference-semantics/semantics/controls.k:53` (operational-rule; attributes: `none`)

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### I0346 — `reference-semantics/semantics/controls.k:54` (operational-rule; attributes: `none`)

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### I0347 — `reference-semantics/semantics/controls.k:57` (operational-rule; attributes: `none`)

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### I0348 — `reference-semantics/semantics/controls.k:59` (operational-rule; attributes: `none`)

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### I0349 — `reference-semantics/semantics/controls.k:65` (syntax; attributes: `none`)

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### I0350 — `reference-semantics/semantics/controls.k:69` (operational-rule; attributes: `none`)

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### I0351 — `reference-semantics/semantics/controls.k:71` (operational-rule; attributes: `none`)

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### I0352 — `reference-semantics/semantics/controls.k:72` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### I0353 — `reference-semantics/semantics/controls.k:73` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### I0354 — `reference-semantics/semantics/controls.k:77` (operational-rule; attributes: `none`)

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### I0355 — `reference-semantics/semantics/controls.k:78` (operational-rule; attributes: `none`)

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### I0356 — `reference-semantics/semantics/controls.k:79` (operational-rule; attributes: `none`)

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### I0357 — `reference-semantics/semantics/controls.k:81` (operational-rule; attributes: `none`)

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### I0358 — `reference-semantics/semantics/controls.k:85` (operational-rule; attributes: `none`)

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### I0359 — `reference-semantics/semantics/controls.k:86` (operational-rule; attributes: `none`)

```k
  rule <k> Continue => #cont ... </k>
```

### I0360 — `reference-semantics/semantics/controls.k:87` (operational-rule; attributes: `none`)

```k
  rule <k> Break => #brk ... </k>
```

### I0361 — `reference-semantics/semantics/controls.k:88` (operational-rule; attributes: `none`)

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### I0362 — `reference-semantics/semantics/controls.k:89` (operational-rule; attributes: `owise`)

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### I0363 — `reference-semantics/semantics/controls.k:90` (operational-rule; attributes: `none`)

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### I0364 — `reference-semantics/semantics/controls.k:91` (operational-rule; attributes: `owise`)

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### I0365 — `reference-semantics/semantics/controls.k:95` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0366 — `reference-semantics/semantics/controls.k:98` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0367 — `reference-semantics/semantics/controls.k:101` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### I0368 — `reference-semantics/semantics/controls.k:106` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0369 — `reference-semantics/semantics/controls.k:109` (endmodule; attributes: `none`)

```k
endmodule
```

### I0370 — `reference-semantics/semantics/core.k:3` (module; attributes: `none`)

```k
module MPY-CORE
```

### I0371 — `reference-semantics/semantics/core.k:4` (imports; attributes: `none`)

```k
  imports MPY-SYNTAX
```

### I0372 — `reference-semantics/semantics/core.k:5` (imports; attributes: `none`)

```k
  imports INT
```

### I0373 — `reference-semantics/semantics/core.k:6` (imports; attributes: `none`)

```k
  imports BOOL
```

### I0374 — `reference-semantics/semantics/core.k:7` (imports; attributes: `none`)

```k
  imports STRING
```

### I0375 — `reference-semantics/semantics/core.k:8` (imports; attributes: `none`)

```k
  imports MAP
```

### I0376 — `reference-semantics/semantics/core.k:9` (imports; attributes: `none`)

```k
  imports LIST
```

### I0377 — `reference-semantics/semantics/core.k:10` (imports; attributes: `none`)

```k
  imports K-EQUAL

  // ==== values, the algebraic lists, and the scope heap =====================
```

### I0378 — `reference-semantics/semantics/core.k:13` (syntax; attributes: `none`)

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### I0379 — `reference-semantics/semantics/core.k:14` (syntax; attributes: `none`)

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### I0380 — `reference-semantics/semantics/core.k:15` (syntax; attributes: `none`)

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### I0381 — `reference-semantics/semantics/core.k:18` (syntax; attributes: `none`)

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### I0382 — `reference-semantics/semantics/core.k:25` (syntax; attributes: `none`)

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

### I0383 — `reference-semantics/semantics/core.k:36` (syntax; attributes: `none`)

```k
  syntax Parent   ::= "root" | parent(Int)
```

### I0384 — `reference-semantics/semantics/core.k:37` (syntax; attributes: `none`)

```k
  syntax Scope    ::= scope(Map, Parent)
```

### I0385 — `reference-semantics/semantics/core.k:38` (syntax; attributes: `none`)

```k
  syntax KResult  ::= Val
```

### I0386 — `reference-semantics/semantics/core.k:39` (syntax; attributes: `none`)

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### I0387 — `reference-semantics/semantics/core.k:40` (syntax; attributes: `none`)

```k
  syntax Vals     ::= List{Val, ","}
```

### I0388 — `reference-semantics/semantics/core.k:41` (syntax; attributes: `none`)

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### I0389 — `reference-semantics/semantics/core.k:42` (syntax; attributes: `none`)

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### I0390 — `reference-semantics/semantics/core.k:49` (configuration; attributes: `N <- _`)

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

### I0391 — `reference-semantics/semantics/core.k:68` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### I0392 — `reference-semantics/semantics/core.k:69` (equational-rule; attributes: `none`)

```k
  rule isRefV(ref(_:Int)) => true
```

### I0393 — `reference-semantics/semantics/core.k:70` (equational-rule; attributes: `owise`)

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### I0394 — `reference-semantics/semantics/core.k:75` (syntax; attributes: `none`)

```k
  syntax HeapVal ::= cellV(Val)
```

### I0395 — `reference-semantics/semantics/core.k:76` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### I0396 — `reference-semantics/semantics/core.k:77` (equational-rule; attributes: `none`)

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### I0397 — `reference-semantics/semantics/core.k:78` (equational-rule; attributes: `owise`)

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### I0398 — `reference-semantics/semantics/core.k:85` (priority-rule; attributes: `priority(40)`)

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

### I0399 — `reference-semantics/semantics/core.k:95` (syntax; attributes: `none`)

```k
  syntax Val ::= kwV(String, Val)
```

### I0400 — `reference-semantics/semantics/core.k:96` (syntax; attributes: `none`)

```k
  syntax KItem ::= #kwTag(String)
```

### I0401 — `reference-semantics/semantics/core.k:97` (operational-rule; attributes: `none`)

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### I0402 — `reference-semantics/semantics/core.k:98` (operational-rule; attributes: `none`)

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### I0403 — `reference-semantics/semantics/core.k:100` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### I0404 — `reference-semantics/semantics/core.k:101` (equational-rule; attributes: `none`)

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### I0405 — `reference-semantics/semantics/core.k:102` (equational-rule; attributes: `owise`)

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### I0406 — `reference-semantics/semantics/core.k:106` (syntax; attributes: `none`)

```k
  syntax Val ::= cellsMark(ParamNames)
```

### I0407 — `reference-semantics/semantics/core.k:107` (function-syntax; attributes: `function`)

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### I0408 — `reference-semantics/semantics/core.k:108` (equational-rule; attributes: `none`)

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### I0409 — `reference-semantics/semantics/core.k:109` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### I0410 — `reference-semantics/semantics/core.k:110` (equational-rule; attributes: `none`)

```k
  rule pnMember(_:String, .ParamNames) => false
```

### I0411 — `reference-semantics/semantics/core.k:111` (equational-rule; attributes: `none`)

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### I0412 — `reference-semantics/semantics/core.k:113` (syntax; attributes: `none`)

```k
  syntax KItem ::= #cellW(Val, Val)
```

### I0413 — `reference-semantics/semantics/core.k:114` (operational-rule; attributes: `none`)

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### I0414 — `reference-semantics/semantics/core.k:117` (syntax; attributes: `none`)

```k
  syntax KItem ::= #alloc(Val)
```

### I0415 — `reference-semantics/semantics/core.k:118` (operational-rule; attributes: `none`)

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### I0416 — `reference-semantics/semantics/core.k:124` (syntax; attributes: `none`)

```k
  syntax KItem ::= #loadAll(Module)
```

### I0417 — `reference-semantics/semantics/core.k:125` (operational-rule; attributes: `none`)

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### I0418 — `reference-semantics/semantics/core.k:126` (operational-rule; attributes: `none`)

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### I0419 — `reference-semantics/semantics/core.k:127` (operational-rule; attributes: `none`)

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### I0420 — `reference-semantics/semantics/core.k:130` (syntax; attributes: `none`)

```k
  syntax KItem ::= #look(String, Int)
```

### I0421 — `reference-semantics/semantics/core.k:131` (operational-rule; attributes: `none`)

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### I0422 — `reference-semantics/semantics/core.k:132` (operational-rule; attributes: `X`)

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

### I0423 — `reference-semantics/semantics/core.k:145` (priority-rule; attributes: `"$cells",X,priority(40)`)

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### I0424 — `reference-semantics/semantics/core.k:152` (operational-rule; attributes: `none`)

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### I0425 — `reference-semantics/semantics/core.k:157` (function-syntax; attributes: `function, total`)

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### I0426 — `reference-semantics/semantics/core.k:158` (operational-rule; attributes: ` "len"    <- builtinV("len")    , "set"    <- builtinV("set")    , "sum"    <- builtinV("sum")    , "abs"    <- builtinV("abs")    , "min"    <- builtinV("min")    , "max"    <- builtinV("max")    , "ord"    <- builtinV("ord")    , "chr"    <- builtinV("chr")    , "range"  <- builtinV("range")  , "all"    <- builtinV("all")    , "any"    <- builtinV("any")    , "zip"    <- builtinV("zip")    , "isinstance" <- builtinV("isinstance") , "sorted" <- builtinV("sorted") , "list"   <- builtinV("list")   , "round"  <- builtinV("round")  , "bin"    <- builtinV("bin")    , "enumerate" <- builtinV("enumerate") , "map"    <- builtinV("map")    , "eval"   <- builtinV("eval")   , "int"    <- typeV("int")       , "str"    <- typeV("str")       , "float"  <- typeV("float")     `)

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

### I0427 — `reference-semantics/semantics/core.k:185` (syntax; attributes: `none`)

```k
  syntax ApplyK ::= toCall(Val)
```

### I0428 — `reference-semantics/semantics/core.k:186` (syntax; attributes: `none`)

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### I0429 — `reference-semantics/semantics/core.k:189` (operational-rule; attributes: `none`)

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### I0430 — `reference-semantics/semantics/core.k:190` (operational-rule; attributes: `none`)

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### I0431 — `reference-semantics/semantics/core.k:191` (operational-rule; attributes: `none`)

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### I0432 — `reference-semantics/semantics/core.k:194` (operational-rule; attributes: `none`)

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### I0433 — `reference-semantics/semantics/core.k:195` (operational-rule; attributes: `none`)

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### I0434 — `reference-semantics/semantics/core.k:196` (operational-rule; attributes: `none`)

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### I0435 — `reference-semantics/semantics/core.k:199` (function-syntax; attributes: `function`)

```k
  syntax Bool ::= truthy(Val) [function]
```

### I0436 — `reference-semantics/semantics/core.k:200` (equational-rule; attributes: `none`)

```k
  rule truthy(B:Bool)          => B
```

### I0437 — `reference-semantics/semantics/core.k:201` (equational-rule; attributes: `none`)

```k
  rule truthy(noneV)           => false
```

### I0438 — `reference-semantics/semantics/core.k:202` (equational-rule; attributes: `none`)

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### I0439 — `reference-semantics/semantics/core.k:203` (equational-rule; attributes: `none`)

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### I0440 — `reference-semantics/semantics/core.k:204` (equational-rule; attributes: `none`)

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### I0441 — `reference-semantics/semantics/core.k:205` (equational-rule; attributes: `none`)

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### I0442 — `reference-semantics/semantics/core.k:208` (function-syntax; attributes: `function`)

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### I0443 — `reference-semantics/semantics/core.k:209` (function-syntax; attributes: `function`)

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### I0444 — `reference-semantics/semantics/core.k:210` (function-syntax; attributes: `function`)

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### I0445 — `reference-semantics/semantics/core.k:213` (function-syntax; attributes: `function, total`)

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### I0446 — `reference-semantics/semantics/core.k:214` (equational-rule; attributes: `none`)

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### I0447 — `reference-semantics/semantics/core.k:215` (equational-rule; attributes: `none`)

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### I0448 — `reference-semantics/semantics/core.k:217` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### I0449 — `reference-semantics/semantics/core.k:218` (equational-rule; attributes: `none`)

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### I0450 — `reference-semantics/semantics/core.k:219` (equational-rule; attributes: `none`)

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### I0451 — `reference-semantics/semantics/core.k:223` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### I0452 — `reference-semantics/semantics/core.k:224` (equational-rule; attributes: `none`)

```k
  rule vsLen(.ValSeq)                => 0
```

### I0453 — `reference-semantics/semantics/core.k:225` (equational-rule; attributes: `none`)

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### I0454 — `reference-semantics/semantics/core.k:227` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### I0455 — `reference-semantics/semantics/core.k:228` (equational-rule; attributes: `none`)

```k
  rule isLen(.IntSeq)                => 0
```

### I0456 — `reference-semantics/semantics/core.k:229` (equational-rule; attributes: `none`)

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### I0457 — `reference-semantics/semantics/core.k:233` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### I0458 — `reference-semantics/semantics/core.k:234` (equational-rule; attributes: `none`)

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### I0459 — `reference-semantics/semantics/core.k:235` (equational-rule; attributes: `none`)

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### I0460 — `reference-semantics/semantics/core.k:236` (equational-rule; attributes: `none`)

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### I0461 — `reference-semantics/semantics/core.k:238` (operational-rule; attributes: `none`)

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### I0462 — `reference-semantics/semantics/core.k:240` (endmodule; attributes: `none`)

```k
endmodule
```

### I0463 — `reference-semantics/semantics/dict.k:13` (module; attributes: `none`)

```k
module MPY-DICT
```

### I0464 — `reference-semantics/semantics/dict.k:14` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0465 — `reference-semantics/semantics/dict.k:15` (imports; attributes: `none`)

```k
  imports MPY-ITER
```

### I0466 — `reference-semantics/semantics/dict.k:16` (imports; attributes: `none`)

```k
  imports MPY-METHODS
```

### I0467 — `reference-semantics/semantics/dict.k:17` (imports; attributes: `none`)

```k
  imports MPY-LIST

  // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).
```

### I0468 — `reference-semantics/semantics/dict.k:20` (syntax; attributes: `none`)

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### I0469 — `reference-semantics/semantics/dict.k:23` (syntax; attributes: `none`)

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### I0470 — `reference-semantics/semantics/dict.k:26` (operational-rule; attributes: `none`)

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### I0471 — `reference-semantics/semantics/dict.k:27` (operational-rule; attributes: `none`)

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### I0472 — `reference-semantics/semantics/dict.k:28` (operational-rule; attributes: `none`)

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### I0473 — `reference-semantics/semantics/dict.k:30` (operational-rule; attributes: `none`)

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### I0474 — `reference-semantics/semantics/dict.k:32` (operational-rule; attributes: `total`)

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### I0475 — `reference-semantics/semantics/dict.k:37` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### I0476 — `reference-semantics/semantics/dict.k:38` (equational-rule; attributes: `none`)

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### I0477 — `reference-semantics/semantics/dict.k:39` (equational-rule; attributes: `none`)

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### I0478 — `reference-semantics/semantics/dict.k:40` (equational-rule; attributes: `none`)

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### I0479 — `reference-semantics/semantics/dict.k:43` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### I0480 — `reference-semantics/semantics/dict.k:44` (equational-rule; attributes: `none`)

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### I0481 — `reference-semantics/semantics/dict.k:45` (equational-rule; attributes: `owise`)

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### I0482 — `reference-semantics/semantics/dict.k:49` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### I0483 — `reference-semantics/semantics/dict.k:50` (equational-rule; attributes: `none`)

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### I0484 — `reference-semantics/semantics/dict.k:52` (equational-rule; attributes: `none`)

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### I0485 — `reference-semantics/semantics/dict.k:54` (equational-rule; attributes: `owise`)

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### I0486 — `reference-semantics/semantics/dict.k:58` (priority-rule; attributes: `priority(40),k`)

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### I0487 — `reference-semantics/semantics/dict.k:63` (equational-rule; attributes: `none`)

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### I0488 — `reference-semantics/semantics/dict.k:64` (function-syntax; attributes: `function`)

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### I0489 — `reference-semantics/semantics/dict.k:65` (priority-rule; attributes: `priority(45),k`)

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### I0490 — `reference-semantics/semantics/dict.k:70` (function-syntax; attributes: `function`)

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### I0491 — `reference-semantics/semantics/dict.k:71` (equational-rule; attributes: `none`)

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### I0492 — `reference-semantics/semantics/dict.k:76` (syntax; attributes: `none`)

```k
  syntax KItem ::= #dsetK(String, Val)
```

### I0493 — `reference-semantics/semantics/dict.k:77` (operational-rule; attributes: `none`)

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### I0494 — `reference-semantics/semantics/dict.k:78` (operational-rule; attributes: ` X <- dictSet({M[X,X`)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### I0495 — `reference-semantics/semantics/dict.k:82` (operational-rule; attributes: `X,X`)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### I0496 — `reference-semantics/semantics/dict.k:86` (syntax; attributes: `none`)

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### I0497 — `reference-semantics/semantics/dict.k:87` (operational-rule; attributes: `none`)

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### I0498 — `reference-semantics/semantics/dict.k:90` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### I0499 — `reference-semantics/semantics/dict.k:91` (operational-rule; attributes: `none`)

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### I0500 — `reference-semantics/semantics/dict.k:92` (equational-rule; attributes: `none`)

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### I0501 — `reference-semantics/semantics/dict.k:95` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### I0502 — `reference-semantics/semantics/dict.k:97` (function-syntax; attributes: `function`)

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### I0503 — `reference-semantics/semantics/dict.k:98` (equational-rule; attributes: `none`)

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### I0504 — `reference-semantics/semantics/dict.k:99` (equational-rule; attributes: `none`)

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### I0505 — `reference-semantics/semantics/dict.k:101` (function-syntax; attributes: `function`)

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### I0506 — `reference-semantics/semantics/dict.k:102` (equational-rule; attributes: `none`)

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### I0507 — `reference-semantics/semantics/dict.k:103` (equational-rule; attributes: `none`)

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### I0508 — `reference-semantics/semantics/dict.k:104` (endmodule; attributes: `none`)

```k
endmodule
```

### I0509 — `reference-semantics/semantics/float.k:14` (module; attributes: `none`)

```k
module MPY-FLOAT
```

### I0510 — `reference-semantics/semantics/float.k:15` (imports; attributes: `none`)

```k
  imports MPY-OPERATORS
```

### I0511 — `reference-semantics/semantics/float.k:16` (imports; attributes: `none`)

```k
  imports MPY-BUILTINS
```

### I0512 — `reference-semantics/semantics/float.k:17` (imports; attributes: `none`)

```k
  imports FLOAT

  // Float is a value; the float literal evaluates to the K Float.
```

### I0513 — `reference-semantics/semantics/float.k:20` (syntax; attributes: `none`)

```k
  syntax Val ::= Float
```

### I0514 — `reference-semantics/semantics/float.k:21` (operational-rule; attributes: `none`)

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### I0515 — `reference-semantics/semantics/float.k:24` (function-syntax; attributes: `function, total, symbol(intFloatDiv), no-evaluators`)

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### I0516 — `reference-semantics/semantics/float.k:25` (equational-rule; attributes: `concrete`)

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### I0517 — `reference-semantics/semantics/float.k:27` (equational-rule; attributes: `none`)

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### I0518 — `reference-semantics/semantics/float.k:30` (function-syntax; attributes: `function, total, symbol(divII), no-evaluators`)

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### I0519 — `reference-semantics/semantics/float.k:31` (equational-rule; attributes: `concrete`)

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### I0520 — `reference-semantics/semantics/float.k:32` (equational-rule; attributes: `none`)

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### I0521 — `reference-semantics/semantics/float.k:37` (function-syntax; attributes: `function, total, symbol(floatMod), no-evaluators`)

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### I0522 — `reference-semantics/semantics/float.k:38` (equational-rule; attributes: `concrete`)

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### I0523 — `reference-semantics/semantics/float.k:39` (equational-rule; attributes: `none`)

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### I0524 — `reference-semantics/semantics/float.k:43` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### I0525 — `reference-semantics/semantics/float.k:44` (operational-rule; attributes: `no-evaluators,concrete`)

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### I0526 — `reference-semantics/semantics/float.k:50` (function-syntax; attributes: `function, total, symbol(floatLt), no-evaluators`)

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### I0527 — `reference-semantics/semantics/float.k:51` (operational-rule; attributes: `concrete`)

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### I0528 — `reference-semantics/semantics/float.k:52` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### I0529 — `reference-semantics/semantics/float.k:54` (function-syntax; attributes: `function, total, symbol(absF), no-evaluators`)

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### I0530 — `reference-semantics/semantics/float.k:55` (equational-rule; attributes: `concrete`)

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### I0531 — `reference-semantics/semantics/float.k:56` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### I0532 — `reference-semantics/semantics/float.k:61` (operational-rule; attributes: `none`)

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### I0533 — `reference-semantics/semantics/float.k:65` (syntax; attributes: `none`)

```k
  syntax KItem ::= "#mathCeil"
```

### I0534 — `reference-semantics/semantics/float.k:66` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### I0535 — `reference-semantics/semantics/float.k:67` (operational-rule; attributes: `none`)

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### I0536 — `reference-semantics/semantics/float.k:70` (syntax; attributes: `none`)

```k
  syntax KItem ::= "#mathFloor"
```

### I0537 — `reference-semantics/semantics/float.k:71` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### I0538 — `reference-semantics/semantics/float.k:72` (operational-rule; attributes: `none`)

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### I0539 — `reference-semantics/semantics/float.k:73` (function-syntax; attributes: `function, total, symbol(floorFI)`)

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### I0540 — `reference-semantics/semantics/float.k:74` (equational-rule; attributes: `concrete`)

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### I0541 — `reference-semantics/semantics/float.k:75` (equational-rule; attributes: `concrete`)

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### I0542 — `reference-semantics/semantics/float.k:78` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### I0543 — `reference-semantics/semantics/float.k:79` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### I0544 — `reference-semantics/semantics/float.k:82` (syntax; attributes: `none`)

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### I0545 — `reference-semantics/semantics/float.k:83` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### I0546 — `reference-semantics/semantics/float.k:84` (operational-rule; attributes: `none`)

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### I0547 — `reference-semantics/semantics/float.k:85` (operational-rule; attributes: `none`)

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### I0548 — `reference-semantics/semantics/float.k:86` (function-syntax; attributes: `function, total, symbol(toF)`)

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### I0549 — `reference-semantics/semantics/float.k:87` (equational-rule; attributes: `concrete`)

```k
  rule toF(F:Float) => F        [concrete]
```

### I0550 — `reference-semantics/semantics/float.k:88` (equational-rule; attributes: `concrete,concrete`)

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### I0551 — `reference-semantics/semantics/float.k:93` (function-syntax; attributes: `function, total, symbol(ceilF)`)

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### I0552 — `reference-semantics/semantics/float.k:94` (equational-rule; attributes: `concrete`)

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### I0553 — `reference-semantics/semantics/float.k:95` (equational-rule; attributes: `concrete`)

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### I0554 — `reference-semantics/semantics/float.k:99` (equational-rule; attributes: `no-evaluators`)

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### I0555 — `reference-semantics/semantics/float.k:103` (function-syntax; attributes: `function, total, symbol(subF), no-evaluators`)

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### I0556 — `reference-semantics/semantics/float.k:104` (equational-rule; attributes: `concrete`)

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### I0557 — `reference-semantics/semantics/float.k:105` (equational-rule; attributes: `none`)

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### I0558 — `reference-semantics/semantics/float.k:107` (function-syntax; attributes: `function, total, symbol(divF), no-evaluators`)

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### I0559 — `reference-semantics/semantics/float.k:108` (equational-rule; attributes: `concrete`)

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### I0560 — `reference-semantics/semantics/float.k:109` (equational-rule; attributes: `none`)

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### I0561 — `reference-semantics/semantics/float.k:111` (function-syntax; attributes: `function, total, symbol(addF), no-evaluators`)

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### I0562 — `reference-semantics/semantics/float.k:112` (equational-rule; attributes: `concrete`)

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### I0563 — `reference-semantics/semantics/float.k:113` (equational-rule; attributes: `none`)

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### I0564 — `reference-semantics/semantics/float.k:115` (function-syntax; attributes: `function, total, symbol(mulF), no-evaluators`)

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### I0565 — `reference-semantics/semantics/float.k:116` (equational-rule; attributes: `concrete`)

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### I0566 — `reference-semantics/semantics/float.k:117` (equational-rule; attributes: `none`)

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### I0567 — `reference-semantics/semantics/float.k:119` (function-syntax; attributes: `function, total, symbol(powF), no-evaluators`)

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### I0568 — `reference-semantics/semantics/float.k:120` (equational-rule; attributes: `concrete`)

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### I0569 — `reference-semantics/semantics/float.k:121` (operational-rule; attributes: `none`)

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### I0570 — `reference-semantics/semantics/float.k:125` (function-syntax; attributes: `function, total, symbol(gtF), no-evaluators`)

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### I0571 — `reference-semantics/semantics/float.k:126` (equational-rule; attributes: `concrete`)

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### I0572 — `reference-semantics/semantics/float.k:127` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### I0573 — `reference-semantics/semantics/float.k:128` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### I0574 — `reference-semantics/semantics/float.k:129` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### I0575 — `reference-semantics/semantics/float.k:132` (equational-rule; attributes: `none`)

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### I0576 — `reference-semantics/semantics/float.k:133` (equational-rule; attributes: `none`)

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### I0577 — `reference-semantics/semantics/float.k:134` (equational-rule; attributes: `none`)

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### I0578 — `reference-semantics/semantics/float.k:135` (equational-rule; attributes: `none`)

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### I0579 — `reference-semantics/semantics/float.k:136` (equational-rule; attributes: `none`)

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### I0580 — `reference-semantics/semantics/float.k:137` (equational-rule; attributes: `none`)

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### I0581 — `reference-semantics/semantics/float.k:138` (equational-rule; attributes: `none`)

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### I0582 — `reference-semantics/semantics/float.k:139` (equational-rule; attributes: `none`)

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### I0583 — `reference-semantics/semantics/float.k:142` (function-syntax; attributes: `function, total, symbol(eqF), no-evaluators`)

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### I0584 — `reference-semantics/semantics/float.k:143` (equational-rule; attributes: `concrete`)

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### I0585 — `reference-semantics/semantics/float.k:144` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### I0586 — `reference-semantics/semantics/float.k:145` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### I0587 — `reference-semantics/semantics/float.k:146` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### I0588 — `reference-semantics/semantics/float.k:147` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### I0589 — `reference-semantics/semantics/float.k:148` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### I0590 — `reference-semantics/semantics/float.k:149` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### I0591 — `reference-semantics/semantics/float.k:150` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### I0592 — `reference-semantics/semantics/float.k:151` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### I0593 — `reference-semantics/semantics/float.k:154` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### I0594 — `reference-semantics/semantics/float.k:155` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### I0595 — `reference-semantics/semantics/float.k:160` (function-syntax; attributes: `function, total, symbol(decStrToF), no-evaluators`)

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### I0596 — `reference-semantics/semantics/float.k:161` (equational-rule; attributes: `concrete`)

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### I0597 — `reference-semantics/semantics/float.k:162` (equational-rule; attributes: `concrete`)

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### I0598 — `reference-semantics/semantics/float.k:165` (function-syntax; attributes: `function`)

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### I0599 — `reference-semantics/semantics/float.k:166` (equational-rule; attributes: `none`)

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### I0600 — `reference-semantics/semantics/float.k:167` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### I0601 — `reference-semantics/semantics/float.k:168` (equational-rule; attributes: `none`)

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### I0602 — `reference-semantics/semantics/float.k:169` (equational-rule; attributes: `none`)

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### I0603 — `reference-semantics/semantics/float.k:170` (equational-rule; attributes: `none`)

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### I0604 — `reference-semantics/semantics/float.k:171` (equational-rule; attributes: `none`)

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### I0605 — `reference-semantics/semantics/float.k:173` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### I0606 — `reference-semantics/semantics/float.k:174` (equational-rule; attributes: `none`)

```k
  rule fracPart(.IntSeq) => 0
```

### I0607 — `reference-semantics/semantics/float.k:175` (equational-rule; attributes: `none`)

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### I0608 — `reference-semantics/semantics/float.k:176` (equational-rule; attributes: `none`)

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### I0609 — `reference-semantics/semantics/float.k:177` (equational-rule; attributes: `none`)

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### I0610 — `reference-semantics/semantics/float.k:178` (equational-rule; attributes: `none`)

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### I0611 — `reference-semantics/semantics/float.k:179` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### I0612 — `reference-semantics/semantics/float.k:180` (equational-rule; attributes: `none`)

```k
  rule fracScale(.IntSeq) => 1
```

### I0613 — `reference-semantics/semantics/float.k:181` (equational-rule; attributes: `none`)

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### I0614 — `reference-semantics/semantics/float.k:182` (equational-rule; attributes: `none`)

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### I0615 — `reference-semantics/semantics/float.k:183` (equational-rule; attributes: `none`)

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### I0616 — `reference-semantics/semantics/float.k:184` (equational-rule; attributes: `none`)

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### I0617 — `reference-semantics/semantics/float.k:185` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### I0618 — `reference-semantics/semantics/float.k:186` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### I0619 — `reference-semantics/semantics/float.k:187` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### I0620 — `reference-semantics/semantics/float.k:190` (function-syntax; attributes: `function, total, symbol(divFloatIntV), no-evaluators`)

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### I0621 — `reference-semantics/semantics/float.k:191` (equational-rule; attributes: `concrete`)

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### I0622 — `reference-semantics/semantics/float.k:192` (equational-rule; attributes: `none`)

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### I0623 — `reference-semantics/semantics/float.k:195` (function-syntax; attributes: `function, total, symbol(intToF), no-evaluators`)

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### I0624 — `reference-semantics/semantics/float.k:196` (equational-rule; attributes: `concrete`)

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### I0625 — `reference-semantics/semantics/float.k:197` (equational-rule; attributes: `none`)

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### I0626 — `reference-semantics/semantics/float.k:198` (equational-rule; attributes: `none`)

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### I0627 — `reference-semantics/semantics/float.k:199` (equational-rule; attributes: `none`)

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### I0628 — `reference-semantics/semantics/float.k:200` (equational-rule; attributes: `none`)

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### I0629 — `reference-semantics/semantics/float.k:201` (equational-rule; attributes: `none`)

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### I0630 — `reference-semantics/semantics/float.k:202` (equational-rule; attributes: `none`)

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### I0631 — `reference-semantics/semantics/float.k:203` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### I0632 — `reference-semantics/semantics/float.k:204` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### I0633 — `reference-semantics/semantics/float.k:205` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### I0634 — `reference-semantics/semantics/float.k:206` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### I0635 — `reference-semantics/semantics/float.k:209` (function-syntax; attributes: `function, total, symbol(truncF), no-evaluators`)

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### I0636 — `reference-semantics/semantics/float.k:210` (equational-rule; attributes: `concrete`)

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### I0637 — `reference-semantics/semantics/float.k:211` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### I0638 — `reference-semantics/semantics/float.k:213` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### I0639 — `reference-semantics/semantics/float.k:214` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### I0640 — `reference-semantics/semantics/float.k:217` (function-syntax; attributes: `function, total, symbol(roundF), no-evaluators`)

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### I0641 — `reference-semantics/semantics/float.k:218` (equational-rule; attributes: `concrete`)

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### I0642 — `reference-semantics/semantics/float.k:223` (function-syntax; attributes: `function, total, symbol(roundFN), no-evaluators`)

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### I0643 — `reference-semantics/semantics/float.k:224` (equational-rule; attributes: `concrete`)

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### I0644 — `reference-semantics/semantics/float.k:227` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### I0645 — `reference-semantics/semantics/float.k:228` (equational-rule; attributes: `none`)

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### I0646 — `reference-semantics/semantics/float.k:230` (function-syntax; attributes: `function, total, symbol(sqrtF), no-evaluators`)

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### I0647 — `reference-semantics/semantics/float.k:231` (equational-rule; attributes: `concrete`)

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### I0648 — `reference-semantics/semantics/float.k:232` (syntax; attributes: `none`)

```k
  syntax KItem ::= "#mathSqrt"
```

### I0649 — `reference-semantics/semantics/float.k:233` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### I0650 — `reference-semantics/semantics/float.k:234` (operational-rule; attributes: `none`)

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### I0651 — `reference-semantics/semantics/float.k:235` (operational-rule; attributes: `none`)

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### I0652 — `reference-semantics/semantics/float.k:243` (syntax; attributes: `none`)

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### I0653 — `reference-semantics/semantics/float.k:244` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### I0654 — `reference-semantics/semantics/float.k:245` (operational-rule; attributes: `none`)

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### I0655 — `reference-semantics/semantics/float.k:246` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### I0656 — `reference-semantics/semantics/float.k:247` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### I0657 — `reference-semantics/semantics/float.k:250` (syntax; attributes: `none`)

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### I0658 — `reference-semantics/semantics/float.k:251` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### I0659 — `reference-semantics/semantics/float.k:252` (operational-rule; attributes: `none`)

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### I0660 — `reference-semantics/semantics/float.k:253` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### I0661 — `reference-semantics/semantics/float.k:254` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### I0662 — `reference-semantics/semantics/float.k:261` (syntax; attributes: `none`)

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### I0663 — `reference-semantics/semantics/float.k:262` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### I0664 — `reference-semantics/semantics/float.k:265` (operational-rule; attributes: `none`)

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### I0665 — `reference-semantics/semantics/float.k:266` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### I0666 — `reference-semantics/semantics/float.k:267` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### I0667 — `reference-semantics/semantics/float.k:270` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### I0668 — `reference-semantics/semantics/float.k:273` (endmodule; attributes: `none`)

```k
endmodule
```

### I0669 — `reference-semantics/semantics/functions.k:3` (module; attributes: `none`)

```k
module MPY-FUNCTIONS
```

### I0670 — `reference-semantics/semantics/functions.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE

  // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k;
  // this module owns the frame lifecycle (bind params, return, pop).
```

### I0671 — `reference-semantics/semantics/functions.k:8` (syntax; attributes: `none`)

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### I0672 — `reference-semantics/semantics/functions.k:14` (operational-rule; attributes: ` F <- closureVal(PNS, BODY, L) `)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### I0673 — `reference-semantics/semantics/functions.k:18` (syntax; attributes: `none`)

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### I0674 — `reference-semantics/semantics/functions.k:19` (operational-rule; attributes: `none`)

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### I0675 — `reference-semantics/semantics/functions.k:27` (syntax; attributes: `none`)

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### I0676 — `reference-semantics/semantics/functions.k:31` (syntax; attributes: `none`)

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### I0677 — `reference-semantics/semantics/functions.k:33` (operational-rule; attributes: `none`)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### I0678 — `reference-semantics/semantics/functions.k:36` (operational-rule; attributes: ` FV <- {M[FV`)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### I0679 — `reference-semantics/semantics/functions.k:42` (operational-rule; attributes: ` F <- closureValC(PNS, CVS, BODY, CM) `)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### I0680 — `reference-semantics/semantics/functions.k:47` (operational-rule; attributes: `none`)

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### I0681 — `reference-semantics/semantics/functions.k:50` (operational-rule; attributes: `none`)

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### I0682 — `reference-semantics/semantics/functions.k:53` (operational-rule; attributes: ` FV <- {M[FV`)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### I0683 — `reference-semantics/semantics/functions.k:59` (operational-rule; attributes: `none`)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### I0684 — `reference-semantics/semantics/functions.k:63` (operational-rule; attributes: `none`)

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### I0685 — `reference-semantics/semantics/functions.k:64` (operational-rule; attributes: ` P <- V `)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### I0686 — `reference-semantics/semantics/functions.k:68` (priority-rule; attributes: `P,"$cells",P,priority(40)`)

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

### I0687 — `reference-semantics/semantics/functions.k:78` (operational-rule; attributes: `none`)

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### I0688 — `reference-semantics/semantics/functions.k:80` (operational-rule; attributes: `none`)

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### I0689 — `reference-semantics/semantics/functions.k:85` (operational-rule; attributes: ` L <- undef `)

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### I0690 — `reference-semantics/semantics/functions.k:91` (endmodule; attributes: `none`)

```k
endmodule
```

### I0691 — `reference-semantics/semantics/int.k:4` (module; attributes: `none`)

```k
module MPY-INT
```

### I0692 — `reference-semantics/semantics/int.k:5` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0693 — `reference-semantics/semantics/int.k:7` (equational-rule; attributes: `none`)

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### I0694 — `reference-semantics/semantics/int.k:9` (equational-rule; attributes: `none`)

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### I0695 — `reference-semantics/semantics/int.k:11` (equational-rule; attributes: `none`)

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### I0696 — `reference-semantics/semantics/int.k:12` (equational-rule; attributes: `none`)

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### I0697 — `reference-semantics/semantics/int.k:13` (equational-rule; attributes: `none`)

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### I0698 — `reference-semantics/semantics/int.k:14` (equational-rule; attributes: `none`)

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### I0699 — `reference-semantics/semantics/int.k:15` (equational-rule; attributes: `none`)

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### I0700 — `reference-semantics/semantics/int.k:16` (equational-rule; attributes: `none`)

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### I0701 — `reference-semantics/semantics/int.k:17` (equational-rule; attributes: `none`)

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### I0702 — `reference-semantics/semantics/int.k:19` (function-syntax; attributes: `function`)

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### I0703 — `reference-semantics/semantics/int.k:20` (equational-rule; attributes: `none`)

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### I0704 — `reference-semantics/semantics/int.k:22` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### I0705 — `reference-semantics/semantics/int.k:23` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### I0706 — `reference-semantics/semantics/int.k:24` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### I0707 — `reference-semantics/semantics/int.k:25` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### I0708 — `reference-semantics/semantics/int.k:26` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### I0709 — `reference-semantics/semantics/int.k:27` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### I0710 — `reference-semantics/semantics/int.k:28` (endmodule; attributes: `none`)

```k
endmodule
```

### I0711 — `reference-semantics/semantics/iter.k:6` (module; attributes: `none`)

```k
module MPY-ITER
```

### I0712 — `reference-semantics/semantics/iter.k:7` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0713 — `reference-semantics/semantics/iter.k:8` (syntax; attributes: `none`)

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### I0714 — `reference-semantics/semantics/iter.k:9` (endmodule; attributes: `none`)

```k
endmodule
```

### I0715 — `reference-semantics/semantics/list.k:3` (module; attributes: `none`)

```k
module MPY-LIST
```

### I0716 — `reference-semantics/semantics/list.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0717 — `reference-semantics/semantics/list.k:5` (imports; attributes: `none`)

```k
  imports MPY-ITER
```

### I0718 — `reference-semantics/semantics/list.k:6` (imports; attributes: `none`)

```k
  imports MPY-OPERATORS

  // ==== iteration (the iterator protocol's list case) =======================
```

### I0719 — `reference-semantics/semantics/list.k:9` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### I0720 — `reference-semantics/semantics/list.k:10` (operational-rule; attributes: `...`)

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### I0721 — `reference-semantics/semantics/list.k:13` (syntax; attributes: `none`)

```k
  syntax ApplyK ::= "toList"
```

### I0722 — `reference-semantics/semantics/list.k:14` (operational-rule; attributes: `none`)

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### I0723 — `reference-semantics/semantics/list.k:15` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### I0724 — `reference-semantics/semantics/list.k:18` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### I0725 — `reference-semantics/semantics/list.k:19` (equational-rule; attributes: `none`)

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### I0726 — `reference-semantics/semantics/list.k:20` (equational-rule; attributes: `none`)

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### I0727 — `reference-semantics/semantics/list.k:24` (priority-rule; attributes: `priority(45)`)

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### I0728 — `reference-semantics/semantics/list.k:27` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### I0729 — `reference-semantics/semantics/list.k:28` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### I0730 — `reference-semantics/semantics/list.k:33` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### I0731 — `reference-semantics/semantics/list.k:34` (equational-rule; attributes: `none`)

```k
  rule hasRefVS(.ValSeq)                => false
```

### I0732 — `reference-semantics/semantics/list.k:35` (equational-rule; attributes: `none`)

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### I0733 — `reference-semantics/semantics/list.k:37` (function-syntax; attributes: `function,function`)

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### I0734 — `reference-semantics/semantics/list.k:39` (equational-rule; attributes: `none`)

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### I0735 — `reference-semantics/semantics/list.k:40` (equational-rule; attributes: `none`)

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### I0736 — `reference-semantics/semantics/list.k:41` (equational-rule; attributes: `none`)

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### I0737 — `reference-semantics/semantics/list.k:42` (equational-rule; attributes: `none`)

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### I0738 — `reference-semantics/semantics/list.k:45` (equational-rule; attributes: `H`)

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### I0739 — `reference-semantics/semantics/list.k:47` (equational-rule; attributes: `H`)

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### I0740 — `reference-semantics/semantics/list.k:49` (equational-rule; attributes: `none`)

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### I0741 — `reference-semantics/semantics/list.k:50` (equational-rule; attributes: `owise`)

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### I0742 — `reference-semantics/semantics/list.k:53` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### I0743 — `reference-semantics/semantics/list.k:58` (syntax; attributes: `none`)

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### I0744 — `reference-semantics/semantics/list.k:59` (operational-rule; attributes: `none`)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### I0745 — `reference-semantics/semantics/list.k:60` (operational-rule; attributes: `none`)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### I0746 — `reference-semantics/semantics/list.k:61` (operational-rule; attributes: `none`)

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### I0747 — `reference-semantics/semantics/list.k:62` (operational-rule; attributes: `none`)

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### I0748 — `reference-semantics/semantics/list.k:63` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### I0749 — `reference-semantics/semantics/list.k:65` (operational-rule; attributes: `none`)

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### I0750 — `reference-semantics/semantics/list.k:67` (operational-rule; attributes: `none`)

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### I0751 — `reference-semantics/semantics/list.k:68` (endmodule; attributes: `none`)

```k
endmodule
```

### I0752 — `reference-semantics/semantics/methods.k:3` (module; attributes: `none`)

```k
module MPY-METHODS
```

### I0753 — `reference-semantics/semantics/methods.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0754 — `reference-semantics/semantics/methods.k:5` (imports; attributes: `none`)

```k
  imports K-EQUAL
```

### I0755 — `reference-semantics/semantics/methods.k:6` (imports; attributes: `none`)

```k
  imports MPY-STR
```

### I0756 — `reference-semantics/semantics/methods.k:7` (imports; attributes: `none`)

```k
  imports MPY-LIST

  // method-call routing + arg-eval live in call.k; this module owns applyMethod.
```

### I0757 — `reference-semantics/semantics/methods.k:10` (function-syntax; attributes: `function`)

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### I0758 — `reference-semantics/semantics/methods.k:13` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### I0759 — `reference-semantics/semantics/methods.k:14` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### I0760 — `reference-semantics/semantics/methods.k:15` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### I0761 — `reference-semantics/semantics/methods.k:16` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### I0762 — `reference-semantics/semantics/methods.k:19` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### I0763 — `reference-semantics/semantics/methods.k:20` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### I0764 — `reference-semantics/semantics/methods.k:21` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### I0765 — `reference-semantics/semantics/methods.k:26` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### I0766 — `reference-semantics/semantics/methods.k:27` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### I0767 — `reference-semantics/semantics/methods.k:28` (equational-rule; attributes: `none`)

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### I0768 — `reference-semantics/semantics/methods.k:29` (equational-rule; attributes: `none`)

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### I0769 — `reference-semantics/semantics/methods.k:30` (equational-rule; attributes: `none`)

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### I0770 — `reference-semantics/semantics/methods.k:34` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### I0771 — `reference-semantics/semantics/methods.k:35` (function-syntax; attributes: `function`)

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### I0772 — `reference-semantics/semantics/methods.k:36` (equational-rule; attributes: `none`)

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### I0773 — `reference-semantics/semantics/methods.k:37` (equational-rule; attributes: `none`)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### I0774 — `reference-semantics/semantics/methods.k:39` (operational-rule; attributes: `none`)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### I0775 — `reference-semantics/semantics/methods.k:41` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### I0776 — `reference-semantics/semantics/methods.k:42` (operational-rule; attributes: `none`)

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### I0777 — `reference-semantics/semantics/methods.k:43` (equational-rule; attributes: `owise`)

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### I0778 — `reference-semantics/semantics/methods.k:44` (equational-rule; attributes: `none`)

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### I0779 — `reference-semantics/semantics/methods.k:47` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### I0780 — `reference-semantics/semantics/methods.k:48` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### I0781 — `reference-semantics/semantics/methods.k:49` (equational-rule; attributes: `none`)

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### I0782 — `reference-semantics/semantics/methods.k:50` (equational-rule; attributes: `none`)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### I0783 — `reference-semantics/semantics/methods.k:51` (equational-rule; attributes: `none`)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### I0784 — `reference-semantics/semantics/methods.k:52` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### I0785 — `reference-semantics/semantics/methods.k:53` (equational-rule; attributes: `none`)

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### I0786 — `reference-semantics/semantics/methods.k:54` (equational-rule; attributes: `none`)

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### I0787 — `reference-semantics/semantics/methods.k:55` (equational-rule; attributes: `none`)

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### I0788 — `reference-semantics/semantics/methods.k:58` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### I0789 — `reference-semantics/semantics/methods.k:61` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### I0790 — `reference-semantics/semantics/methods.k:64` (equational-rule; attributes: `none`)

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### I0791 — `reference-semantics/semantics/methods.k:65` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### I0792 — `reference-semantics/semantics/methods.k:66` (equational-rule; attributes: `none`)

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### I0793 — `reference-semantics/semantics/methods.k:67` (equational-rule; attributes: `none`)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### I0794 — `reference-semantics/semantics/methods.k:68` (equational-rule; attributes: `none`)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### I0795 — `reference-semantics/semantics/methods.k:72` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### I0796 — `reference-semantics/semantics/methods.k:75` (function-syntax; attributes: `function`)

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### I0797 — `reference-semantics/semantics/methods.k:76` (equational-rule; attributes: `none`)

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### I0798 — `reference-semantics/semantics/methods.k:77` (equational-rule; attributes: `none`)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### I0799 — `reference-semantics/semantics/methods.k:79` (equational-rule; attributes: `none`)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### I0800 — `reference-semantics/semantics/methods.k:82` (function-syntax; attributes: `function`)

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### I0801 — `reference-semantics/semantics/methods.k:83` (equational-rule; attributes: `none`)

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### I0802 — `reference-semantics/semantics/methods.k:84` (equational-rule; attributes: `none`)

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### I0803 — `reference-semantics/semantics/methods.k:85` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### I0804 — `reference-semantics/semantics/methods.k:86` (equational-rule; attributes: `none`)

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### I0805 — `reference-semantics/semantics/methods.k:89` (priority-rule; attributes: `priority(39)`)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### I0806 — `reference-semantics/semantics/methods.k:94` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### I0807 — `reference-semantics/semantics/methods.k:97` (function-syntax; attributes: `function`)

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### I0808 — `reference-semantics/semantics/methods.k:98` (equational-rule; attributes: `none`)

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### I0809 — `reference-semantics/semantics/methods.k:99` (equational-rule; attributes: `none`)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### I0810 — `reference-semantics/semantics/methods.k:101` (equational-rule; attributes: `none`)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### I0811 — `reference-semantics/semantics/methods.k:104` (equational-rule; attributes: `none`)

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### I0812 — `reference-semantics/semantics/methods.k:106` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### I0813 — `reference-semantics/semantics/methods.k:107` (equational-rule; attributes: `none`)

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### I0814 — `reference-semantics/semantics/methods.k:108` (equational-rule; attributes: `none`)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### I0815 — `reference-semantics/semantics/methods.k:109` (equational-rule; attributes: `none`)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### I0816 — `reference-semantics/semantics/methods.k:112` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### I0817 — `reference-semantics/semantics/methods.k:113` (operational-rule; attributes: `none`)

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### I0818 — `reference-semantics/semantics/methods.k:115` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### I0819 — `reference-semantics/semantics/methods.k:116` (operational-rule; attributes: `none`)

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### I0820 — `reference-semantics/semantics/methods.k:118` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### I0821 — `reference-semantics/semantics/methods.k:119` (equational-rule; attributes: `none`)

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### I0822 — `reference-semantics/semantics/methods.k:121` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### I0823 — `reference-semantics/semantics/methods.k:122` (operational-rule; attributes: `none`)

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### I0824 — `reference-semantics/semantics/methods.k:124` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### I0825 — `reference-semantics/semantics/methods.k:125` (equational-rule; attributes: `none`)

```k
  rule hasUpper(.IntSeq) => false
```

### I0826 — `reference-semantics/semantics/methods.k:126` (equational-rule; attributes: `none`)

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### I0827 — `reference-semantics/semantics/methods.k:128` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### I0828 — `reference-semantics/semantics/methods.k:129` (equational-rule; attributes: `none`)

```k
  rule hasLower(.IntSeq) => false
```

### I0829 — `reference-semantics/semantics/methods.k:130` (equational-rule; attributes: `none`)

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### I0830 — `reference-semantics/semantics/methods.k:132` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### I0831 — `reference-semantics/semantics/methods.k:133` (equational-rule; attributes: `none`)

```k
  rule allAlpha(.IntSeq) => true
```

### I0832 — `reference-semantics/semantics/methods.k:134` (equational-rule; attributes: `none`)

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### I0833 — `reference-semantics/semantics/methods.k:136` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### I0834 — `reference-semantics/semantics/methods.k:137` (equational-rule; attributes: `none`)

```k
  rule allDigit(.IntSeq) => true
```

### I0835 — `reference-semantics/semantics/methods.k:138` (equational-rule; attributes: `none`)

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### I0836 — `reference-semantics/semantics/methods.k:140` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### I0837 — `reference-semantics/semantics/methods.k:142` (equational-rule; attributes: `none`)

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### I0838 — `reference-semantics/semantics/methods.k:143` (equational-rule; attributes: `owise`)

```k
  rule lowerC(C:Int) => C         [owise]
```

### I0839 — `reference-semantics/semantics/methods.k:145` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= upperC(Int) [function, total]
```

### I0840 — `reference-semantics/semantics/methods.k:146` (equational-rule; attributes: `none`)

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### I0841 — `reference-semantics/semantics/methods.k:147` (equational-rule; attributes: `owise`)

```k
  rule upperC(C:Int) => C         [owise]
```

### I0842 — `reference-semantics/semantics/methods.k:149` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= swapC(Int) [function, total]
```

### I0843 — `reference-semantics/semantics/methods.k:150` (equational-rule; attributes: `none`)

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### I0844 — `reference-semantics/semantics/methods.k:151` (equational-rule; attributes: `none`)

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### I0845 — `reference-semantics/semantics/methods.k:152` (equational-rule; attributes: `owise`)

```k
  rule swapC(C:Int) => C         [owise]
```

### I0846 — `reference-semantics/semantics/methods.k:154` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### I0847 — `reference-semantics/semantics/methods.k:155` (equational-rule; attributes: `none`)

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### I0848 — `reference-semantics/semantics/methods.k:156` (equational-rule; attributes: `none`)

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### I0849 — `reference-semantics/semantics/methods.k:158` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### I0850 — `reference-semantics/semantics/methods.k:159` (equational-rule; attributes: `none`)

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### I0851 — `reference-semantics/semantics/methods.k:160` (equational-rule; attributes: `none`)

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### I0852 — `reference-semantics/semantics/methods.k:162` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### I0853 — `reference-semantics/semantics/methods.k:163` (equational-rule; attributes: `none`)

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### I0854 — `reference-semantics/semantics/methods.k:164` (equational-rule; attributes: `none`)

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### I0855 — `reference-semantics/semantics/methods.k:166` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### I0856 — `reference-semantics/semantics/methods.k:167` (equational-rule; attributes: `none`)

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### I0857 — `reference-semantics/semantics/methods.k:168` (equational-rule; attributes: `none`)

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### I0858 — `reference-semantics/semantics/methods.k:169` (equational-rule; attributes: `none`)

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### I0859 — `reference-semantics/semantics/methods.k:170` (endmodule; attributes: `none`)

```k
endmodule
```

### I0860 — `reference-semantics/semantics/operators.k:6` (module; attributes: `none`)

```k
module MPY-OPERATORS
```

### I0861 — `reference-semantics/semantics/operators.k:7` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0862 — `reference-semantics/semantics/operators.k:8` (imports; attributes: `none`)

```k
  imports MPY-ITER
```

### I0863 — `reference-semantics/semantics/operators.k:10` (operational-rule; attributes: `none`)

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### I0864 — `reference-semantics/semantics/operators.k:12` (operational-rule; attributes: `none`)

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### I0865 — `reference-semantics/semantics/operators.k:15` (context; attributes: `none`)

```k
  context Compare(HOLE, _)
```

### I0866 — `reference-semantics/semantics/operators.k:16` (context; attributes: `none`)

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### I0867 — `reference-semantics/semantics/operators.k:17` (operational-rule; attributes: `owise`)

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### I0868 — `reference-semantics/semantics/operators.k:19` (equational-rule; attributes: `none`)

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### I0869 — `reference-semantics/semantics/operators.k:20` (equational-rule; attributes: `none`)

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### I0870 — `reference-semantics/semantics/operators.k:25` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0871 — `reference-semantics/semantics/operators.k:28` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### I0872 — `reference-semantics/semantics/operators.k:34` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### I0873 — `reference-semantics/semantics/operators.k:38` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### I0874 — `reference-semantics/semantics/operators.k:44` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0875 — `reference-semantics/semantics/operators.k:47` (endmodule; attributes: `none`)

```k
endmodule
```

### I0876 — `reference-semantics/semantics/range.k:5` (module; attributes: `none`)

```k
module MPY-RANGE
```

### I0877 — `reference-semantics/semantics/range.k:6` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0878 — `reference-semantics/semantics/range.k:7` (imports; attributes: `none`)

```k
  imports MPY-ITER
```

### I0879 — `reference-semantics/semantics/range.k:9` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### I0880 — `reference-semantics/semantics/range.k:10` (operational-rule; attributes: `none`)

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### I0881 — `reference-semantics/semantics/range.k:12` (function-syntax; attributes: `function`)

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### I0882 — `reference-semantics/semantics/range.k:13` (equational-rule; attributes: `none`)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### I0883 — `reference-semantics/semantics/range.k:15` (operational-rule; attributes: `none`)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### I0884 — `reference-semantics/semantics/range.k:17` (operational-rule; attributes: `none`)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### I0885 — `reference-semantics/semantics/range.k:20` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### I0886 — `reference-semantics/semantics/range.k:23` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### I0887 — `reference-semantics/semantics/range.k:25` (endmodule; attributes: `none`)

```k
endmodule
```

### I0888 — `reference-semantics/semantics/set.k:3` (module; attributes: `none`)

```k
module MPY-SET
```

### I0889 — `reference-semantics/semantics/set.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE

  // a set value, carried as its distinct codes in first-seen order (order is irrelevant
  // to membership/cardinality — the two observations sets support here).
```

### I0890 — `reference-semantics/semantics/set.k:8` (syntax; attributes: `none`)

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### I0891 — `reference-semantics/semantics/set.k:11` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### I0892 — `reference-semantics/semantics/set.k:12` (equational-rule; attributes: `none`)

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### I0893 — `reference-semantics/semantics/set.k:13` (equational-rule; attributes: `none`)

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### I0894 — `reference-semantics/semantics/set.k:16` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### I0895 — `reference-semantics/semantics/set.k:18` (equational-rule; attributes: `none`)

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### I0896 — `reference-semantics/semantics/set.k:19` (equational-rule; attributes: `none`)

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### I0897 — `reference-semantics/semantics/set.k:20` (equational-rule; attributes: `none`)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### I0898 — `reference-semantics/semantics/set.k:22` (equational-rule; attributes: `none`)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### I0899 — `reference-semantics/semantics/set.k:25` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### I0900 — `reference-semantics/semantics/set.k:26` (equational-rule; attributes: `none`)

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### I0901 — `reference-semantics/semantics/set.k:27` (equational-rule; attributes: `none`)

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### I0902 — `reference-semantics/semantics/set.k:31` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### I0903 — `reference-semantics/semantics/set.k:32` (equational-rule; attributes: `none`)

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### I0904 — `reference-semantics/semantics/set.k:33` (equational-rule; attributes: `none`)

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### I0905 — `reference-semantics/semantics/set.k:35` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### I0906 — `reference-semantics/semantics/set.k:36` (equational-rule; attributes: `none`)

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### I0907 — `reference-semantics/semantics/set.k:39` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### I0908 — `reference-semantics/semantics/set.k:40` (endmodule; attributes: `none`)

```k
endmodule
```

### I0909 — `reference-semantics/semantics/sort.k:10` (module; attributes: `none`)

```k
module MPY-SORT
```

### I0910 — `reference-semantics/semantics/sort.k:11` (imports; attributes: `none`)

```k
  imports MPY-BUILTINS
```

### I0911 — `reference-semantics/semantics/sort.k:12` (imports; attributes: `none`)

```k
  imports MPY-SUBSCRIPT

  // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators);
  // concrete insertion sort for krun.
  // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal
  // (lemmas-only) is not available in the semantics. Int and str lists.
```

### I0912 — `reference-semantics/semantics/sort.k:18` (function-syntax; attributes: `function, total, symbol(sortVS), no-evaluators`)

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### I0913 — `reference-semantics/semantics/sort.k:19` (function-syntax; attributes: `function`)

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### I0914 — `reference-semantics/semantics/sort.k:20` (equational-rule; attributes: `concrete`)

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### I0915 — `reference-semantics/semantics/sort.k:21` (equational-rule; attributes: `concrete`)

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### I0916 — `reference-semantics/semantics/sort.k:22` (equational-rule; attributes: `concrete`)

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### I0917 — `reference-semantics/semantics/sort.k:23` (operational-rule; attributes: `concrete`)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### I0918 — `reference-semantics/semantics/sort.k:24` (equational-rule; attributes: `concrete`)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### I0919 — `reference-semantics/semantics/sort.k:26` (function-syntax; attributes: `function`)

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### I0920 — `reference-semantics/semantics/sort.k:27` (equational-rule; attributes: `concrete`)

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### I0921 — `reference-semantics/semantics/sort.k:28` (equational-rule; attributes: `concrete`)

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### I0922 — `reference-semantics/semantics/sort.k:29` (equational-rule; attributes: `concrete`)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### I0923 — `reference-semantics/semantics/sort.k:31` (equational-rule; attributes: `concrete,owise`)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### I0924 — `reference-semantics/semantics/sort.k:36` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### I0925 — `reference-semantics/semantics/sort.k:40` (priority-rule; attributes: `priority(40)`)

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

### I0926 — `reference-semantics/semantics/sort.k:49` (function-syntax; attributes: `function, total, symbol(sortKeyVS), no-evaluators`)

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### I0927 — `reference-semantics/semantics/sort.k:51` (function-syntax; attributes: `function, total,function, total`)

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### I0928 — `reference-semantics/semantics/sort.k:53` (equational-rule; attributes: `none`)

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### I0929 — `reference-semantics/semantics/sort.k:54` (equational-rule; attributes: `none`)

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### I0930 — `reference-semantics/semantics/sort.k:55` (equational-rule; attributes: `none`)

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### I0931 — `reference-semantics/semantics/sort.k:57` (function-syntax; attributes: `function, total`)

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### I0932 — `reference-semantics/semantics/sort.k:58` (equational-rule; attributes: `none`)

```k
  rule condRev(S:ValSeq, false) => S
```

### I0933 — `reference-semantics/semantics/sort.k:59` (equational-rule; attributes: `none`)

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### I0934 — `reference-semantics/semantics/sort.k:61` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### I0935 — `reference-semantics/semantics/sort.k:63` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### I0936 — `reference-semantics/semantics/sort.k:65` (operational-rule; attributes: `total`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

### I0937 — `reference-semantics/semantics/sort.k:72` (endmodule; attributes: `none`)

```k
endmodule
```

### I0938 — `reference-semantics/semantics/str.k:3` (module; attributes: `none`)

```k
module MPY-STR
```

### I0939 — `reference-semantics/semantics/str.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I0940 — `reference-semantics/semantics/str.k:5` (imports; attributes: `none`)

```k
  imports MPY-ITER

  // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==
```

### I0941 — `reference-semantics/semantics/str.k:8` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### I0942 — `reference-semantics/semantics/str.k:9` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### I0943 — `reference-semantics/semantics/str.k:13` (function-syntax; attributes: `function`)

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### I0944 — `reference-semantics/semantics/str.k:14` (operational-rule; attributes: `none`)

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### I0945 — `reference-semantics/semantics/str.k:15` (equational-rule; attributes: `none`)

```k
  rule strToCodes("") => .IntSeq
```

### I0946 — `reference-semantics/semantics/str.k:16` (operational-rule; attributes: `none`)

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### I0947 — `reference-semantics/semantics/str.k:20` (function-syntax; attributes: `function, total`)

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### I0948 — `reference-semantics/semantics/str.k:21` (equational-rule; attributes: `none`)

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### I0949 — `reference-semantics/semantics/str.k:22` (equational-rule; attributes: `none`)

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### I0950 — `reference-semantics/semantics/str.k:24` (equational-rule; attributes: `none`)

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### I0951 — `reference-semantics/semantics/str.k:25` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### I0952 — `reference-semantics/semantics/str.k:26` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### I0953 — `reference-semantics/semantics/str.k:29` (equational-rule; attributes: `none`)

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### I0954 — `reference-semantics/semantics/str.k:30` (equational-rule; attributes: `none`)

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### I0955 — `reference-semantics/semantics/str.k:32` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### I0956 — `reference-semantics/semantics/str.k:33` (equational-rule; attributes: `none`)

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### I0957 — `reference-semantics/semantics/str.k:34` (equational-rule; attributes: `none`)

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### I0958 — `reference-semantics/semantics/str.k:35` (equational-rule; attributes: `none`)

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### I0959 — `reference-semantics/semantics/str.k:37` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### I0960 — `reference-semantics/semantics/str.k:38` (equational-rule; attributes: `none`)

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### I0961 — `reference-semantics/semantics/str.k:39` (equational-rule; attributes: `none`)

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### I0962 — `reference-semantics/semantics/str.k:40` (operational-rule; attributes: `none`)

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### I0963 — `reference-semantics/semantics/str.k:48` (function-syntax; attributes: `function, total`)

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### I0964 — `reference-semantics/semantics/str.k:49` (equational-rule; attributes: `none`)

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### I0965 — `reference-semantics/semantics/str.k:50` (equational-rule; attributes: `none`)

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### I0966 — `reference-semantics/semantics/str.k:51` (equational-rule; attributes: `none`)

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### I0967 — `reference-semantics/semantics/str.k:52` (operational-rule; attributes: `none`)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### I0968 — `reference-semantics/semantics/str.k:53` (equational-rule; attributes: `none`)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### I0969 — `reference-semantics/semantics/str.k:54` (equational-rule; attributes: `none`)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### I0970 — `reference-semantics/semantics/str.k:56` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### I0971 — `reference-semantics/semantics/str.k:57` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### I0972 — `reference-semantics/semantics/str.k:58` (operational-rule; attributes: `none`)

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### I0973 — `reference-semantics/semantics/str.k:59` (equational-rule; attributes: `none`)

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### I0974 — `reference-semantics/semantics/str.k:60` (endmodule; attributes: `none`)

```k
endmodule
```

### I0975 — `reference-semantics/semantics/subscript.k:3` (module; attributes: `none`)

```k
module MPY-SUBSCRIPT
```

### I0976 — `reference-semantics/semantics/subscript.k:4` (imports; attributes: `total,total`)

```k
  imports MPY-CORE

  // ==== positional access + negative-index normalization (used only here) ===
  // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g.
  // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the
  // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total
  // atK. K trusts the [total] annotation; valid programs index in-bounds.
```

### I0977 — `reference-semantics/semantics/subscript.k:11` (function-syntax; attributes: `function, total`)

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### I0978 — `reference-semantics/semantics/subscript.k:12` (equational-rule; attributes: `none`)

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### I0979 — `reference-semantics/semantics/subscript.k:13` (equational-rule; attributes: `none`)

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### I0980 — `reference-semantics/semantics/subscript.k:16` (function-syntax; attributes: `function`)

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### I0981 — `reference-semantics/semantics/subscript.k:17` (equational-rule; attributes: `none`)

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### I0982 — `reference-semantics/semantics/subscript.k:18` (equational-rule; attributes: `none`)

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### I0983 — `reference-semantics/semantics/subscript.k:21` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### I0984 — `reference-semantics/semantics/subscript.k:22` (operational-rule; attributes: `none`)

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### I0985 — `reference-semantics/semantics/subscript.k:23` (equational-rule; attributes: `i`)

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### I0986 — `reference-semantics/semantics/subscript.k:27` (context; attributes: `none`)

```k
  context Subscript(HOLE, _)
```

### I0987 — `reference-semantics/semantics/subscript.k:28` (context; attributes: `none`)

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### I0988 — `reference-semantics/semantics/subscript.k:31` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0989 — `reference-semantics/semantics/subscript.k:35` (operational-rule; attributes: `none`)

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### I0990 — `reference-semantics/semantics/subscript.k:37` (function-syntax; attributes: `function`)

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### I0991 — `reference-semantics/semantics/subscript.k:38` (equational-rule; attributes: `none`)

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### I0992 — `reference-semantics/semantics/subscript.k:39` (equational-rule; attributes: `none`)

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### I0993 — `reference-semantics/semantics/subscript.k:40` (equational-rule; attributes: `lo:hi:step`)

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### I0994 — `reference-semantics/semantics/subscript.k:44` (syntax; attributes: `none`)

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### I0995 — `reference-semantics/semantics/subscript.k:49` (syntax; attributes: `none`)

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### I0996 — `reference-semantics/semantics/subscript.k:50` (operational-rule; attributes: `none`)

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### I0997 — `reference-semantics/semantics/subscript.k:51` (operational-rule; attributes: `none`)

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### I0998 — `reference-semantics/semantics/subscript.k:52` (operational-rule; attributes: `none`)

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### I0999 — `reference-semantics/semantics/subscript.k:54` (operational-rule; attributes: `none`)

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### I1000 — `reference-semantics/semantics/subscript.k:55` (operational-rule; attributes: `none`)

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### I1001 — `reference-semantics/semantics/subscript.k:56` (operational-rule; attributes: `none`)

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### I1002 — `reference-semantics/semantics/subscript.k:58` (priority-rule; attributes: `priority(45)`)

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### I1003 — `reference-semantics/semantics/subscript.k:61` (operational-rule; attributes: `none`)

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### I1004 — `reference-semantics/semantics/subscript.k:63` (function-syntax; attributes: `function`)

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### I1005 — `reference-semantics/semantics/subscript.k:64` (equational-rule; attributes: `none`)

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### I1006 — `reference-semantics/semantics/subscript.k:66` (equational-rule; attributes: `none`)

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### I1007 — `reference-semantics/semantics/subscript.k:68` (equational-rule; attributes: `none`)

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### I1008 — `reference-semantics/semantics/subscript.k:72` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### I1009 — `reference-semantics/semantics/subscript.k:73` (equational-rule; attributes: `none`)

```k
  rule slStep(noB)          => 1
```

### I1010 — `reference-semantics/semantics/subscript.k:74` (equational-rule; attributes: `none`)

```k
  rule slStep(someB(S:Int)) => S
```

### I1011 — `reference-semantics/semantics/subscript.k:76` (function-syntax; attributes: `function`)

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### I1012 — `reference-semantics/semantics/subscript.k:77` (equational-rule; attributes: `none`)

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### I1013 — `reference-semantics/semantics/subscript.k:79` (operational-rule; attributes: `none`)

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### I1014 — `reference-semantics/semantics/subscript.k:81` (equational-rule; attributes: `none`)

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### I1015 — `reference-semantics/semantics/subscript.k:83` (function-syntax; attributes: `function`)

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### I1016 — `reference-semantics/semantics/subscript.k:84` (equational-rule; attributes: `none`)

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### I1017 — `reference-semantics/semantics/subscript.k:86` (operational-rule; attributes: `none`)

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### I1018 — `reference-semantics/semantics/subscript.k:88` (equational-rule; attributes: `none`)

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### I1019 — `reference-semantics/semantics/subscript.k:90` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### I1020 — `reference-semantics/semantics/subscript.k:91` (operational-rule; attributes: `none`)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### I1021 — `reference-semantics/semantics/subscript.k:93` (equational-rule; attributes: `none`)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### I1022 — `reference-semantics/semantics/subscript.k:96` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### I1023 — `reference-semantics/semantics/subscript.k:97` (equational-rule; attributes: `none`)

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### I1024 — `reference-semantics/semantics/subscript.k:99` (operational-rule; attributes: `none`)

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### I1025 — `reference-semantics/semantics/subscript.k:102` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### I1026 — `reference-semantics/semantics/subscript.k:103` (operational-rule; attributes: `none`)

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### I1027 — `reference-semantics/semantics/subscript.k:105` (operational-rule; attributes: `none`)

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### I1028 — `reference-semantics/semantics/subscript.k:109` (function-syntax; attributes: `function`)

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### I1029 — `reference-semantics/semantics/subscript.k:110` (operational-rule; attributes: `none`)

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### I1030 — `reference-semantics/semantics/subscript.k:113` (operational-rule; attributes: `none`)

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### I1031 — `reference-semantics/semantics/subscript.k:116` (function-syntax; attributes: `function`)

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### I1032 — `reference-semantics/semantics/subscript.k:117` (operational-rule; attributes: `none`)

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### I1033 — `reference-semantics/semantics/subscript.k:120` (operational-rule; attributes: `none`)

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### I1034 — `reference-semantics/semantics/subscript.k:122` (endmodule; attributes: `none`)

```k
endmodule
```

### I1035 — `reference-semantics/semantics/syntax.k:3` (module; attributes: `none`)

```k
module MPY-SYNTAX
```

### I1036 — `reference-semantics/semantics/syntax.k:4` (imports; attributes: `none`)

```k
  imports INT-SYNTAX
```

### I1037 — `reference-semantics/semantics/syntax.k:5` (imports; attributes: `none`)

```k
  imports FLOAT-SYNTAX
```

### I1038 — `reference-semantics/semantics/syntax.k:6` (imports; attributes: `none`)

```k
  imports BOOL-SYNTAX
```

### I1039 — `reference-semantics/semantics/syntax.k:7` (imports; attributes: `none`)

```k
  imports STRING-SYNTAX
```

### I1040 — `reference-semantics/semantics/syntax.k:9` (syntax; attributes: `strict(2),seqstrict(2, 3),macro,macro,strict(1),strict(1)`)

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

### I1041 — `reference-semantics/semantics/syntax.k:32` (syntax; attributes: `none`)

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### I1042 — `reference-semantics/semantics/syntax.k:33` (syntax; attributes: `none`)

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### I1043 — `reference-semantics/semantics/syntax.k:34` (syntax; attributes: `none`)

```k
  syntax Entries  ::= List{Entry, ","}
```

### I1044 — `reference-semantics/semantics/syntax.k:35` (syntax; attributes: `none`)

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### I1045 — `reference-semantics/semantics/syntax.k:36` (syntax; attributes: `none`)

```k
  syntax CompFors ::= List{CompFor, ""}
```

### I1046 — `reference-semantics/semantics/syntax.k:37` (syntax; attributes: `none`)

```k
  syntax Exprs    ::= List{Expr, ","}
```

### I1047 — `reference-semantics/semantics/syntax.k:38` (syntax; attributes: `none`)

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### I1048 — `reference-semantics/semantics/syntax.k:39` (syntax; attributes: `none`)

```k
  syntax Bound    ::= Expr | "NoBound"
```

### I1049 — `reference-semantics/semantics/syntax.k:41` (syntax; attributes: `strict(2),strict(3),strict(2),strict(1),strict,strict,strict`)

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

### I1050 — `reference-semantics/semantics/syntax.k:56` (syntax; attributes: `none`)

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### I1051 — `reference-semantics/semantics/syntax.k:57` (syntax; attributes: `none`)

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### I1052 — `reference-semantics/semantics/syntax.k:58` (syntax; attributes: `none`)

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### I1053 — `reference-semantics/semantics/syntax.k:59` (syntax; attributes: `none`)

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### I1054 — `reference-semantics/semantics/syntax.k:60` (syntax; attributes: `none`)

```k
  syntax ParamNames ::= List{String, ","}
```

### I1055 — `reference-semantics/semantics/syntax.k:61` (syntax; attributes: `none`)

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### I1056 — `reference-semantics/semantics/syntax.k:62` (endmodule; attributes: `none`)

```k
endmodule
```

### I1057 — `reference-semantics/semantics/tuple.k:3` (module; attributes: `none`)

```k
module MPY-TUPLE
```

### I1058 — `reference-semantics/semantics/tuple.k:4` (imports; attributes: `none`)

```k
  imports MPY-CORE
```

### I1059 — `reference-semantics/semantics/tuple.k:5` (imports; attributes: `none`)

```k
  imports MPY-ITER
```

### I1060 — `reference-semantics/semantics/tuple.k:6` (imports; attributes: `none`)

```k
  imports MPY-LIST
```

### I1061 — `reference-semantics/semantics/tuple.k:7` (imports; attributes: `none`)

```k
  imports MPY-METHODS

  // ==== iteration (the iterator protocol's tuple case) ======================
```

### I1062 — `reference-semantics/semantics/tuple.k:10` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### I1063 — `reference-semantics/semantics/tuple.k:11` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### I1064 — `reference-semantics/semantics/tuple.k:14` (syntax; attributes: `none`)

```k
  syntax ApplyK ::= "toTuple"
```

### I1065 — `reference-semantics/semantics/tuple.k:15` (operational-rule; attributes: `none`)

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### I1066 — `reference-semantics/semantics/tuple.k:16` (operational-rule; attributes: `none`)

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### I1067 — `reference-semantics/semantics/tuple.k:18` (equational-rule; attributes: `none`)

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### I1068 — `reference-semantics/semantics/tuple.k:20` (operational-rule; attributes: `none`)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### I1069 — `reference-semantics/semantics/tuple.k:21` (operational-rule; attributes: `none`)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### I1070 — `reference-semantics/semantics/tuple.k:23` (equational-rule; attributes: `none`)

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### I1071 — `reference-semantics/semantics/tuple.k:24` (function-syntax; attributes: `function`)

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### I1072 — `reference-semantics/semantics/tuple.k:25` (equational-rule; attributes: `none`)

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### I1073 — `reference-semantics/semantics/tuple.k:26` (equational-rule; attributes: `none`)

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### I1074 — `reference-semantics/semantics/tuple.k:28` (equational-rule; attributes: `none`)

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### I1075 — `reference-semantics/semantics/tuple.k:31` (syntax; attributes: `none`)

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### I1076 — `reference-semantics/semantics/tuple.k:32` (operational-rule; attributes: ` X <- V `)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### I1077 — `reference-semantics/semantics/tuple.k:35` (priority-rule; attributes: `X,"$cells",X,priority(40)`)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### I1078 — `reference-semantics/semantics/tuple.k:42` (operational-rule; attributes: `none`)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### I1079 — `reference-semantics/semantics/tuple.k:43` (operational-rule; attributes: `none`)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### I1080 — `reference-semantics/semantics/tuple.k:44` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### I1081 — `reference-semantics/semantics/tuple.k:49` (syntax; attributes: `none`)

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### I1082 — `reference-semantics/semantics/tuple.k:50` (operational-rule; attributes: `none`)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### I1083 — `reference-semantics/semantics/tuple.k:51` (operational-rule; attributes: `none`)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### I1084 — `reference-semantics/semantics/tuple.k:52` (priority-rule; attributes: `priority(40)`)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I1085 — `reference-semantics/semantics/tuple.k:55` (operational-rule; attributes: `none`)

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### I1086 — `reference-semantics/semantics/tuple.k:57` (operational-rule; attributes: `none`)

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### I1087 — `reference-semantics/semantics/tuple.k:58` (endmodule; attributes: `none`)

```k
endmodule
```

### I1088 — `verification.k:1` (requires; attributes: `none`)

```k
requires "reference-semantics/semantics.k"
```

### I1089 — `verification.k:3` (module; attributes: `none`)

```k
module DOUBLE-THE-DIFFERENCE-VERIFICATION
```

### I1090 — `verification.k:4` (imports; attributes: `none`)

```k
  imports MPY

  // A symbolic sequence of exactly the numeric values admitted by the prompt.
  // Keeping the Int/Float choice in the constructor lets kprove split the
  // sequence structurally instead of treating an arbitrary Val as non-integer.
```

### I1091 — `verification.k:9` (syntax; attributes: `none`)

```k
  syntax NumSeq ::= ".NumSeq"
                  | iNum(Int, NumSeq)
                  | fNum(Float, NumSeq)

  // numVals is a proof-domain representation of a list's ValSeq.  Its iterator
  // rules expose the NumSeq constructor directly to symbolic narrowing.
```

### I1092 — `verification.k:15` (syntax; attributes: `none`)

```k
  syntax ValSeq ::= numVals(NumSeq)
```

### I1093 — `verification.k:16` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(list(numVals(.NumSeq)))
        => #iterDone ... </k>
```

### I1094 — `verification.k:18` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(list(numVals(iNum(I, REST))))
        => #iterYield(I, list(numVals(REST))) ... </k>
```

### I1095 — `verification.k:20` (operational-rule; attributes: `none`)

```k
  rule <k> #iterNext(list(numVals(fNum(F, REST))))
        => #iterYield(F, list(numVals(REST))) ... </k>
```

### I1096 — `verification.k:23` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= oddSquare(Int) [function, total]
```

### I1097 — `verification.k:24` (equational-rule; attributes: `none`)

```k
  rule oddSquare(I)
    => #if I >Int 0 andBool pyMod(I, 2) ==Int 1
       #then I *Int I
       #else 0
       #fi
```

### I1098 — `verification.k:30` (function-syntax; attributes: `function, total`)

```k
  syntax Int ::= doubleDifferenceSpec(NumSeq) [function, total]
```

### I1099 — `verification.k:31` (equational-rule; attributes: `none`)

```k
  rule doubleDifferenceSpec(.NumSeq)       => 0
```

### I1100 — `verification.k:32` (equational-rule; attributes: `none`)

```k
  rule doubleDifferenceSpec(iNum(I, REST))
    => oddSquare(I) +Int doubleDifferenceSpec(REST)
```

### I1101 — `verification.k:34` (equational-rule; attributes: `none`)

```k
  rule doubleDifferenceSpec(fNum(_F, REST))
    => doubleDifferenceSpec(REST)
```

### I1102 — `verification.k:37` (function-syntax; attributes: `function, total`)

```k
  syntax Val ::= finalNumber(NumSeq, Val) [function, total]
```

### I1103 — `verification.k:38` (equational-rule; attributes: `none`)

```k
  rule finalNumber(.NumSeq, OLD)          => OLD
```

### I1104 — `verification.k:39` (equational-rule; attributes: `none`)

```k
  rule finalNumber(iNum(I, REST), _OLD)   => finalNumber(REST, I)
```

### I1105 — `verification.k:40` (equational-rule; attributes: `none`)

```k
  rule finalNumber(fNum(F, REST), _OLD)   => finalNumber(REST, F)
```

### I1106 — `verification.k:41` (endmodule; attributes: `none`)

```k
endmodule
```

### I1107 — `spec.k:1` (requires; attributes: `none`)

```k
requires "verification.k"
```

### I1108 — `spec.k:3` (module; attributes: `none`)

```k
module DOUBLE-THE-DIFFERENCE-SPEC
```

### I1109 — `spec.k:4` (imports; attributes: `none`)

```k
  imports DOUBLE-THE-DIFFERENCE-VERIFICATION
```

### I1110 — `spec.k:6` (claim; attributes: `loop-invariant`)

```k
  claim [loop-invariant]:
    <k>
      #loop(
        list(numVals(NUMBERS)),
        Name("number"),
        If(
          BoolOp(
            "and",
            Call(
              Name("isinstance"),
              Name("number"),
              Name("int")),
            Compare(
              Name("number"),
              CmpOp(">", Int(0))),
            Compare(
              BinOp("%", Name("number"), Int(2)),
              CmpOp("==", Int(1)))),
          AugAssign(
            Name("total"),
            "+",
            BinOp("**", Name("number"), Int(2))),
          .Stmts))
      ~> CONT
    =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst" |-> _INPUT
        "total" |->
          (ACC => ACC +Int doubleDifferenceSpec(NUMBERS))
        "number" |->
          (OLDNUMBER => finalNumber(NUMBERS, OLDNUMBER)),
        parent(0))
      0 |-> scope(
        "double_the_difference" |-> _FUNCTION,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
```

### I1111 — `spec.k:48` (claim; attributes: `double-the-difference-correct`)

```k
  claim [double-the-difference-correct]:
    <k>
      Call(
        Name("double_the_difference"),
        list(numVals(NUMBERS)))
      => doubleDifferenceSpec(NUMBERS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "double_the_difference" |->
          closureVal(
            "lst",
            Assign(Name("total"), Int(0))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("lst"),
              If(
                BoolOp(
                  "and",
                  Call(
                    Name("isinstance"),
                    Name("number"),
                    Name("int")),
                  Compare(
                    Name("number"),
                    CmpOp(">", Int(0))),
                  Compare(
                    BinOp("%", Name("number"), Int(2)),
                    CmpOp("==", Int(1)))),
                AugAssign(
                  Name("total"),
                  "+",
                  BinOp("**", Name("number"), Int(2))),
                .Stmts))
            Return(Name("total")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
```

### I1112 — `spec.k:96` (endmodule; attributes: `none`)

```k
endmodule
```


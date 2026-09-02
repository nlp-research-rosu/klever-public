# Exhaustive K source sentence inventory

Scope: the recursively identical supplied semantics, candidate `verification.k`, and both candidate claims in `spec.k`.

## Summary

- Files: 26
- Sentences: 934
- `claim` sentences: 2
- `configuration` sentences: 1
- `context` sentences: 5
- `rule` sentences: 698
- `syntax` sentences: 228
- `[priority]` sentences: 45
- `[no-evaluators]` opaque declarations: 22
- `[simplification]` attributes: 0
- `[functional]` attributes: 0

Attribute-token counts: `concrete`=35, `function`=150, `is-happy`=1, `loop-invariant`=1, `macro`=4, `macro-rec`=1, `no-evaluators`=22, `owise`=26, `priority`=45, `seqstrict`=1, `strict`=10, `symbol`=25, `total`=111

Opaque declarations: semantics/builtins.k:285, semantics/float.k:24, semantics/float.k:30, semantics/float.k:37, semantics/float.k:50, semantics/float.k:54, semantics/float.k:103, semantics/float.k:107, semantics/float.k:111, semantics/float.k:115, semantics/float.k:119, semantics/float.k:125, semantics/float.k:142, semantics/float.k:160, semantics/float.k:190, semantics/float.k:195, semantics/float.k:209, semantics/float.k:217, semantics/float.k:223, semantics/float.k:230, semantics/sort.k:18, semantics/sort.k:49

Priority sentences: semantics/assert.k:13, semantics/bool.k:29, semantics/bool.k:31, semantics/bool.k:35, semantics/bool.k:39, semantics/bool.k:43, semantics/builtins.k:280, semantics/call.k:38, semantics/call.k:42, semantics/call.k:47, semantics/call.k:56, semantics/call.k:63, semantics/concrete.k:28, semantics/concrete.k:31, semantics/controls.k:12, semantics/controls.k:27, semantics/controls.k:95, semantics/controls.k:98, semantics/controls.k:101, semantics/controls.k:106, semantics/core.k:85, semantics/core.k:145, semantics/dict.k:58, semantics/dict.k:65, semantics/float.k:66, semantics/float.k:71, semantics/float.k:83, semantics/float.k:233, semantics/functions.k:68, semantics/list.k:24, semantics/list.k:53, semantics/methods.k:72, semantics/methods.k:89, semantics/methods.k:94, semantics/operators.k:25, semantics/operators.k:28, semantics/operators.k:34, semantics/operators.k:38, semantics/operators.k:44, semantics/sort.k:40, semantics/subscript.k:31, semantics/subscript.k:58, semantics/tuple.k:35, semantics/tuple.k:44, semantics/tuple.k:52

## Source hashes

- `semantics.k`: `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`
- `semantics/assert.k`: `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b`
- `semantics/bool.k`: `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd`
- `semantics/builtins.k`: `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd`
- `semantics/call.k`: `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4`
- `semantics/comprehension.k`: `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7`
- `semantics/concrete.k`: `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305`
- `semantics/controls.k`: `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae`
- `semantics/core.k`: `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e`
- `semantics/dict.k`: `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580`
- `semantics/float.k`: `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f`
- `semantics/functions.k`: `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193`
- `semantics/int.k`: `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5`
- `semantics/iter.k`: `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f`
- `semantics/list.k`: `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa`
- `semantics/methods.k`: `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743`
- `semantics/operators.k`: `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b`
- `semantics/range.k`: `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d`
- `semantics/set.k`: `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7`
- `semantics/sort.k`: `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a`
- `semantics/str.k`: `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f`
- `semantics/subscript.k`: `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7`
- `semantics/syntax.k`: `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6`
- `semantics/tuple.k`: `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb`
- `verification.k`: `f1b0f2b550d53e6867df41c4fd2a56752ef0558cb38a709c34a6b93339020738`
- `spec.k`: `4e11e5042d34eeaca62e72e605e50b7d29ba399a5c75b41f2041ad67173e141e`

## Every local sentence

### semantics/assert.k:6 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### semantics/assert.k:8 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### semantics/assert.k:13 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/bool.k:8 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### semantics/bool.k:10 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### semantics/bool.k:11 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### semantics/bool.k:16 — context

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### semantics/bool.k:17 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### semantics/bool.k:18 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### semantics/bool.k:20 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### semantics/bool.k:22 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### semantics/bool.k:24 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### semantics/bool.k:29 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### semantics/bool.k:31 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### semantics/bool.k:35 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### semantics/bool.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### semantics/bool.k:43 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### semantics/builtins.k:17 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### semantics/builtins.k:20 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= seqLen(Val) [function]
```

### semantics/builtins.k:21 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### semantics/builtins.k:22 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### semantics/builtins.k:23 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### semantics/builtins.k:24 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### semantics/builtins.k:25 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### semantics/builtins.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### semantics/builtins.k:32 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### semantics/builtins.k:33 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### semantics/builtins.k:34 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### semantics/builtins.k:35 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### semantics/builtins.k:36 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### semantics/builtins.k:37 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### semantics/builtins.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### semantics/builtins.k:41 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### semantics/builtins.k:44 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### semantics/builtins.k:47 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### semantics/builtins.k:48 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### semantics/builtins.k:49 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### semantics/builtins.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### semantics/builtins.k:54 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= intOf(Val) [function]
```

### semantics/builtins.k:55 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intOf(I:Int)  => I
```

### semantics/builtins.k:56 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### semantics/builtins.k:59 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### semantics/builtins.k:60 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### semantics/builtins.k:61 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### semantics/builtins.k:62 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### semantics/builtins.k:64 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### semantics/builtins.k:67 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### semantics/builtins.k:68 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### semantics/builtins.k:69 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### semantics/builtins.k:70 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### semantics/builtins.k:72 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### semantics/builtins.k:76 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### semantics/builtins.k:77 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### semantics/builtins.k:78 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### semantics/builtins.k:80 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### semantics/builtins.k:81 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### semantics/builtins.k:82 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### semantics/builtins.k:86 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### semantics/builtins.k:87 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### semantics/builtins.k:88 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### semantics/builtins.k:90 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### semantics/builtins.k:91 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### semantics/builtins.k:92 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### semantics/builtins.k:97 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### semantics/builtins.k:98 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### semantics/builtins.k:99 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule maxVals(M:Int, .Vals)           => M
```

### semantics/builtins.k:100 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### semantics/builtins.k:102 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### semantics/builtins.k:103 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### semantics/builtins.k:104 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule minVals(M:Int, .Vals)           => M
```

### semantics/builtins.k:105 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### semantics/builtins.k:108 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### semantics/builtins.k:111 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### semantics/builtins.k:114 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### semantics/builtins.k:115 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### semantics/builtins.k:116 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### semantics/builtins.k:117 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### semantics/builtins.k:118 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### semantics/builtins.k:119 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### semantics/builtins.k:124 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### semantics/builtins.k:126 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### semantics/builtins.k:127 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### semantics/builtins.k:128 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### semantics/builtins.k:132 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### semantics/builtins.k:134 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### semantics/builtins.k:135 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### semantics/builtins.k:136 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### semantics/builtins.k:137 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### semantics/builtins.k:140 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### semantics/builtins.k:143 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### semantics/builtins.k:144 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### semantics/builtins.k:148 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### semantics/builtins.k:149 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### semantics/builtins.k:152 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### semantics/builtins.k:156 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### semantics/builtins.k:158 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### semantics/builtins.k:159 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### semantics/builtins.k:160 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### semantics/builtins.k:163 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### semantics/builtins.k:164 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### semantics/builtins.k:167 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### semantics/builtins.k:169 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### semantics/builtins.k:170 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### semantics/builtins.k:171 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### semantics/builtins.k:173 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### semantics/builtins.k:174 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### semantics/builtins.k:177 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### semantics/builtins.k:178 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### semantics/builtins.k:179 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### semantics/builtins.k:187 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### semantics/builtins.k:188 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### semantics/builtins.k:189 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### semantics/builtins.k:192 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### semantics/builtins.k:194 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### semantics/builtins.k:195 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### semantics/builtins.k:196 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### semantics/builtins.k:197 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### semantics/builtins.k:198 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### semantics/builtins.k:199 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### semantics/builtins.k:200 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### semantics/builtins.k:201 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### semantics/builtins.k:203 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### semantics/builtins.k:204 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### semantics/builtins.k:205 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### semantics/builtins.k:206 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### semantics/builtins.k:207 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### semantics/builtins.k:208 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### semantics/builtins.k:209 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### semantics/builtins.k:210 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### semantics/builtins.k:211 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### semantics/builtins.k:212 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### semantics/builtins.k:214 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`, `function`, `total`

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### semantics/builtins.k:216 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### semantics/builtins.k:217 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### semantics/builtins.k:218 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### semantics/builtins.k:219 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### semantics/builtins.k:221 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### semantics/builtins.k:223 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### semantics/builtins.k:225 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### semantics/builtins.k:226 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### semantics/builtins.k:227 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### semantics/builtins.k:228 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### semantics/builtins.k:230 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### semantics/builtins.k:231 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### semantics/builtins.k:232 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### semantics/builtins.k:233 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### semantics/builtins.k:234 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### semantics/builtins.k:235 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### semantics/builtins.k:236 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### semantics/builtins.k:238 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### semantics/builtins.k:239 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### semantics/builtins.k:240 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### semantics/builtins.k:241 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### semantics/builtins.k:243 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### semantics/builtins.k:244 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### semantics/builtins.k:245 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### semantics/builtins.k:246 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### semantics/builtins.k:247 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### semantics/builtins.k:248 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### semantics/builtins.k:250 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### semantics/builtins.k:251 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### semantics/builtins.k:252 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### semantics/builtins.k:253 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### semantics/builtins.k:254 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### semantics/builtins.k:255 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### semantics/builtins.k:256 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### semantics/builtins.k:257 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### semantics/builtins.k:260 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### semantics/builtins.k:263 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### semantics/builtins.k:265 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### semantics/builtins.k:266 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### semantics/builtins.k:267 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### semantics/builtins.k:268 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### semantics/builtins.k:269 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### semantics/builtins.k:270 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### semantics/builtins.k:271 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### semantics/builtins.k:272 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### semantics/builtins.k:273 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### semantics/builtins.k:274 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### semantics/builtins.k:279 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= "#md5"
```

### semantics/builtins.k:280 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### semantics/builtins.k:282 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### semantics/builtins.k:283 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= md5Obj(IntSeq)
```

### semantics/builtins.k:284 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### semantics/builtins.k:285 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### semantics/builtins.k:291 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### semantics/builtins.k:292 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### semantics/builtins.k:293 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### semantics/builtins.k:294 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isIntV(_:Int)         => true
```

### semantics/builtins.k:295 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule isIntV(_:Val)         => false [owise]
```

### semantics/builtins.k:296 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isStrV(str(_:IntSeq)) => true
```

### semantics/builtins.k:297 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule isStrV(_:Val)         => false [owise]
```

### semantics/call.k:16 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### semantics/call.k:19 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= #callee(Exprs)
```

### semantics/call.k:20 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `owise`

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### semantics/call.k:21 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### semantics/call.k:24 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### semantics/call.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### semantics/call.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### semantics/call.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### semantics/call.k:29 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### semantics/call.k:30 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### semantics/call.k:31 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `owise`

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### semantics/call.k:32 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### semantics/call.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/call.k:42 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### semantics/call.k:47 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/call.k:52 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### semantics/call.k:53 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### semantics/call.k:56 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### semantics/call.k:63 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### semantics/call.k:69 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

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

### semantics/call.k:80 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### semantics/call.k:87 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### semantics/call.k:88 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### semantics/call.k:89 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### semantics/comprehension.k:11 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### semantics/comprehension.k:12 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### semantics/comprehension.k:14 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `macro`

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### semantics/comprehension.k:15 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### semantics/comprehension.k:18 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `macro-rec`

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### semantics/comprehension.k:19 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### semantics/comprehension.k:21 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### semantics/comprehension.k:24 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `macro`

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### semantics/comprehension.k:25 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### semantics/comprehension.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### semantics/concrete.k:13 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### semantics/concrete.k:16 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

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

### semantics/concrete.k:25 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= kvP(Val, Val)
```

### semantics/concrete.k:26 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### semantics/concrete.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### semantics/concrete.k:31 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### semantics/concrete.k:34 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### semantics/concrete.k:36 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### semantics/concrete.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### semantics/concrete.k:42 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### semantics/concrete.k:43 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### semantics/concrete.k:44 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### semantics/concrete.k:47 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### semantics/concrete.k:51 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### semantics/concrete.k:52 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### semantics/concrete.k:53 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### semantics/concrete.k:54 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### semantics/concrete.k:56 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### semantics/concrete.k:57 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### semantics/concrete.k:58 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### semantics/concrete.k:59 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### semantics/controls.k:9 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### semantics/controls.k:12 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### semantics/controls.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### semantics/controls.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### semantics/controls.k:35 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### semantics/controls.k:36 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### semantics/controls.k:37 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### semantics/controls.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### semantics/controls.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### semantics/controls.k:43 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### semantics/controls.k:48 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### semantics/controls.k:51 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### semantics/controls.k:52 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### semantics/controls.k:53 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### semantics/controls.k:54 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### semantics/controls.k:57 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### semantics/controls.k:59 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### semantics/controls.k:65 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### semantics/controls.k:69 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### semantics/controls.k:71 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### semantics/controls.k:72 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### semantics/controls.k:73 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### semantics/controls.k:77 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### semantics/controls.k:78 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### semantics/controls.k:79 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### semantics/controls.k:81 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### semantics/controls.k:85 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### semantics/controls.k:86 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Continue => #cont ... </k>
```

### semantics/controls.k:87 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Break => #brk ... </k>
```

### semantics/controls.k:88 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### semantics/controls.k:89 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### semantics/controls.k:90 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### semantics/controls.k:91 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### semantics/controls.k:95 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/controls.k:98 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/controls.k:101 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### semantics/controls.k:106 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/core.k:13 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### semantics/core.k:14 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### semantics/core.k:15 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### semantics/core.k:18 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### semantics/core.k:25 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

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

### semantics/core.k:36 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Parent   ::= "root" | parent(Int)
```

### semantics/core.k:37 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Scope    ::= scope(Map, Parent)
```

### semantics/core.k:38 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KResult  ::= Val
```

### semantics/core.k:39 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### semantics/core.k:40 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Vals     ::= List{Val, ","}
```

### semantics/core.k:41 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### semantics/core.k:42 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### semantics/core.k:49 — configuration

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

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

### semantics/core.k:68 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### semantics/core.k:69 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isRefV(ref(_:Int)) => true
```

### semantics/core.k:70 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### semantics/core.k:75 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax HeapVal ::= cellV(Val)
```

### semantics/core.k:76 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### semantics/core.k:77 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### semantics/core.k:78 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### semantics/core.k:85 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

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

### semantics/core.k:95 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= kwV(String, Val)
```

### semantics/core.k:96 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #kwTag(String)
```

### semantics/core.k:97 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### semantics/core.k:98 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### semantics/core.k:100 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### semantics/core.k:101 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### semantics/core.k:102 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### semantics/core.k:106 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= cellsMark(ParamNames)
```

### semantics/core.k:107 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### semantics/core.k:108 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### semantics/core.k:109 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### semantics/core.k:110 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule pnMember(_:String, .ParamNames) => false
```

### semantics/core.k:111 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### semantics/core.k:113 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #cellW(Val, Val)
```

### semantics/core.k:114 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### semantics/core.k:117 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #alloc(Val)
```

### semantics/core.k:118 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### semantics/core.k:124 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= #loadAll(Module)
```

### semantics/core.k:125 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### semantics/core.k:126 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### semantics/core.k:127 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### semantics/core.k:130 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= #look(String, Int)
```

### semantics/core.k:131 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### semantics/core.k:132 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

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

### semantics/core.k:145 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### semantics/core.k:152 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### semantics/core.k:157 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`, `total`

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### semantics/core.k:158 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

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

### semantics/core.k:185 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax ApplyK ::= toCall(Val)
```

### semantics/core.k:186 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### semantics/core.k:189 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### semantics/core.k:190 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### semantics/core.k:191 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### semantics/core.k:194 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### semantics/core.k:195 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### semantics/core.k:196 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### semantics/core.k:199 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`

```k
  syntax Bool ::= truthy(Val) [function]
```

### semantics/core.k:200 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule truthy(B:Bool)          => B
```

### semantics/core.k:201 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule truthy(noneV)           => false
```

### semantics/core.k:202 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### semantics/core.k:203 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### semantics/core.k:204 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### semantics/core.k:205 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### semantics/core.k:208 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### semantics/core.k:209 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### semantics/core.k:210 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### semantics/core.k:213 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`, `total`

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### semantics/core.k:214 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### semantics/core.k:215 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### semantics/core.k:217 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### semantics/core.k:218 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### semantics/core.k:219 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### semantics/core.k:223 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### semantics/core.k:224 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule vsLen(.ValSeq)                => 0
```

### semantics/core.k:225 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### semantics/core.k:227 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`, `total`

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### semantics/core.k:228 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule isLen(.IntSeq)                => 0
```

### semantics/core.k:229 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### semantics/core.k:233 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### semantics/core.k:234 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### semantics/core.k:235 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### semantics/core.k:236 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### semantics/core.k:238 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### semantics/dict.k:20 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### semantics/dict.k:23 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### semantics/dict.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### semantics/dict.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### semantics/dict.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### semantics/dict.k:30 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### semantics/dict.k:32 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### semantics/dict.k:37 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### semantics/dict.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### semantics/dict.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### semantics/dict.k:40 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### semantics/dict.k:43 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### semantics/dict.k:44 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### semantics/dict.k:45 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### semantics/dict.k:49 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### semantics/dict.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### semantics/dict.k:52 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### semantics/dict.k:54 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### semantics/dict.k:58 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### semantics/dict.k:63 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### semantics/dict.k:64 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### semantics/dict.k:65 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### semantics/dict.k:70 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### semantics/dict.k:71 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### semantics/dict.k:76 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #dsetK(String, Val)
```

### semantics/dict.k:77 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### semantics/dict.k:78 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### semantics/dict.k:82 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### semantics/dict.k:86 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### semantics/dict.k:87 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### semantics/dict.k:90 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### semantics/dict.k:91 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### semantics/dict.k:92 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### semantics/dict.k:95 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### semantics/dict.k:97 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### semantics/dict.k:98 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### semantics/dict.k:99 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### semantics/dict.k:101 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### semantics/dict.k:102 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### semantics/dict.k:103 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### semantics/float.k:20 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= Float
```

### semantics/float.k:21 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### semantics/float.k:24 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### semantics/float.k:25 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### semantics/float.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### semantics/float.k:30 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### semantics/float.k:31 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### semantics/float.k:32 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### semantics/float.k:37 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### semantics/float.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### semantics/float.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### semantics/float.k:43 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### semantics/float.k:44 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### semantics/float.k:50 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### semantics/float.k:51 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### semantics/float.k:52 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### semantics/float.k:54 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### semantics/float.k:55 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### semantics/float.k:56 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### semantics/float.k:61 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### semantics/float.k:65 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= "#mathCeil"
```

### semantics/float.k:66 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### semantics/float.k:67 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### semantics/float.k:70 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= "#mathFloor"
```

### semantics/float.k:71 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### semantics/float.k:72 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### semantics/float.k:73 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`, `symbol`

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### semantics/float.k:74 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### semantics/float.k:75 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### semantics/float.k:78 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### semantics/float.k:79 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### semantics/float.k:82 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### semantics/float.k:83 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### semantics/float.k:84 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### semantics/float.k:85 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### semantics/float.k:86 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`, `symbol`

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### semantics/float.k:87 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule toF(F:Float) => F        [concrete]
```

### semantics/float.k:88 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### semantics/float.k:93 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`, `symbol`

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### semantics/float.k:94 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### semantics/float.k:95 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### semantics/float.k:99 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### semantics/float.k:103 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### semantics/float.k:104 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### semantics/float.k:105 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### semantics/float.k:107 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### semantics/float.k:108 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### semantics/float.k:109 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### semantics/float.k:111 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### semantics/float.k:112 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### semantics/float.k:113 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### semantics/float.k:115 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### semantics/float.k:116 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### semantics/float.k:117 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### semantics/float.k:119 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### semantics/float.k:120 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### semantics/float.k:121 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### semantics/float.k:125 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### semantics/float.k:126 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### semantics/float.k:127 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### semantics/float.k:128 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### semantics/float.k:129 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### semantics/float.k:132 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### semantics/float.k:133 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### semantics/float.k:134 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### semantics/float.k:135 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### semantics/float.k:136 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### semantics/float.k:137 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### semantics/float.k:138 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### semantics/float.k:139 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### semantics/float.k:142 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### semantics/float.k:143 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### semantics/float.k:144 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### semantics/float.k:145 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### semantics/float.k:146 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### semantics/float.k:147 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### semantics/float.k:148 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### semantics/float.k:149 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### semantics/float.k:150 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### semantics/float.k:151 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### semantics/float.k:154 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### semantics/float.k:155 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### semantics/float.k:160 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### semantics/float.k:161 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### semantics/float.k:162 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### semantics/float.k:165 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### semantics/float.k:166 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### semantics/float.k:167 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### semantics/float.k:168 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### semantics/float.k:169 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### semantics/float.k:170 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### semantics/float.k:171 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### semantics/float.k:173 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### semantics/float.k:174 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracPart(.IntSeq) => 0
```

### semantics/float.k:175 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### semantics/float.k:176 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### semantics/float.k:177 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### semantics/float.k:178 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### semantics/float.k:179 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### semantics/float.k:180 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracScale(.IntSeq) => 1
```

### semantics/float.k:181 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### semantics/float.k:182 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### semantics/float.k:183 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### semantics/float.k:184 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### semantics/float.k:185 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### semantics/float.k:186 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### semantics/float.k:187 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### semantics/float.k:190 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### semantics/float.k:191 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### semantics/float.k:192 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### semantics/float.k:195 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### semantics/float.k:196 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### semantics/float.k:197 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### semantics/float.k:198 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### semantics/float.k:199 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### semantics/float.k:200 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### semantics/float.k:201 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### semantics/float.k:202 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### semantics/float.k:203 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### semantics/float.k:204 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### semantics/float.k:205 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### semantics/float.k:206 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### semantics/float.k:209 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### semantics/float.k:210 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### semantics/float.k:211 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### semantics/float.k:213 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### semantics/float.k:214 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### semantics/float.k:217 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### semantics/float.k:218 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### semantics/float.k:223 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### semantics/float.k:224 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### semantics/float.k:227 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### semantics/float.k:228 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### semantics/float.k:230 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### semantics/float.k:231 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### semantics/float.k:232 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= "#mathSqrt"
```

### semantics/float.k:233 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### semantics/float.k:234 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### semantics/float.k:235 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### semantics/float.k:243 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### semantics/float.k:244 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### semantics/float.k:245 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### semantics/float.k:246 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### semantics/float.k:247 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### semantics/float.k:250 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### semantics/float.k:251 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### semantics/float.k:252 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### semantics/float.k:253 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### semantics/float.k:254 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### semantics/float.k:261 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### semantics/float.k:262 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### semantics/float.k:265 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### semantics/float.k:266 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### semantics/float.k:267 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### semantics/float.k:270 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### semantics/functions.k:8 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### semantics/functions.k:14 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### semantics/functions.k:18 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### semantics/functions.k:19 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### semantics/functions.k:27 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### semantics/functions.k:31 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### semantics/functions.k:33 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### semantics/functions.k:36 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### semantics/functions.k:42 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### semantics/functions.k:47 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### semantics/functions.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### semantics/functions.k:53 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### semantics/functions.k:59 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### semantics/functions.k:63 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### semantics/functions.k:64 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### semantics/functions.k:68 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

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

### semantics/functions.k:78 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### semantics/functions.k:80 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### semantics/functions.k:85 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### semantics/int.k:7 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### semantics/int.k:9 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### semantics/int.k:11 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### semantics/int.k:12 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### semantics/int.k:13 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### semantics/int.k:14 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### semantics/int.k:15 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### semantics/int.k:16 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### semantics/int.k:17 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### semantics/int.k:19 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### semantics/int.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### semantics/int.k:22 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### semantics/int.k:23 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### semantics/int.k:24 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### semantics/int.k:25 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### semantics/int.k:26 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### semantics/int.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### semantics/iter.k:8 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### semantics/list.k:9 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### semantics/list.k:10 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### semantics/list.k:13 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax ApplyK ::= "toList"
```

### semantics/list.k:14 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### semantics/list.k:15 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### semantics/list.k:18 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### semantics/list.k:19 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### semantics/list.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### semantics/list.k:24 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### semantics/list.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### semantics/list.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### semantics/list.k:33 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### semantics/list.k:34 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule hasRefVS(.ValSeq)                => false
```

### semantics/list.k:35 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### semantics/list.k:37 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `function`

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### semantics/list.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### semantics/list.k:40 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### semantics/list.k:41 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### semantics/list.k:42 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### semantics/list.k:45 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### semantics/list.k:47 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### semantics/list.k:49 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### semantics/list.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### semantics/list.k:53 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### semantics/list.k:58 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### semantics/list.k:59 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### semantics/list.k:60 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### semantics/list.k:61 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### semantics/list.k:62 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### semantics/list.k:63 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### semantics/list.k:65 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### semantics/list.k:67 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### semantics/methods.k:10 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### semantics/methods.k:13 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### semantics/methods.k:14 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### semantics/methods.k:15 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### semantics/methods.k:16 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### semantics/methods.k:19 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### semantics/methods.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### semantics/methods.k:21 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### semantics/methods.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### semantics/methods.k:27 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### semantics/methods.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### semantics/methods.k:29 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### semantics/methods.k:30 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### semantics/methods.k:34 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### semantics/methods.k:35 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### semantics/methods.k:36 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### semantics/methods.k:37 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### semantics/methods.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### semantics/methods.k:41 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### semantics/methods.k:42 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### semantics/methods.k:43 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### semantics/methods.k:44 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### semantics/methods.k:47 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### semantics/methods.k:48 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### semantics/methods.k:49 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### semantics/methods.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### semantics/methods.k:51 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### semantics/methods.k:52 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### semantics/methods.k:53 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### semantics/methods.k:54 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### semantics/methods.k:55 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### semantics/methods.k:58 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### semantics/methods.k:61 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### semantics/methods.k:64 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### semantics/methods.k:65 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### semantics/methods.k:66 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### semantics/methods.k:67 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### semantics/methods.k:68 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### semantics/methods.k:72 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### semantics/methods.k:75 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### semantics/methods.k:76 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### semantics/methods.k:77 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### semantics/methods.k:79 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### semantics/methods.k:82 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### semantics/methods.k:83 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### semantics/methods.k:84 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### semantics/methods.k:85 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### semantics/methods.k:86 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### semantics/methods.k:89 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### semantics/methods.k:94 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### semantics/methods.k:97 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### semantics/methods.k:98 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### semantics/methods.k:99 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### semantics/methods.k:101 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### semantics/methods.k:104 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### semantics/methods.k:106 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### semantics/methods.k:107 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### semantics/methods.k:108 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### semantics/methods.k:109 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### semantics/methods.k:112 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### semantics/methods.k:113 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### semantics/methods.k:115 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### semantics/methods.k:116 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### semantics/methods.k:118 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### semantics/methods.k:119 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### semantics/methods.k:121 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### semantics/methods.k:122 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### semantics/methods.k:124 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### semantics/methods.k:125 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule hasUpper(.IntSeq) => false
```

### semantics/methods.k:126 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### semantics/methods.k:128 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### semantics/methods.k:129 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule hasLower(.IntSeq) => false
```

### semantics/methods.k:130 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### semantics/methods.k:132 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### semantics/methods.k:133 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule allAlpha(.IntSeq) => true
```

### semantics/methods.k:134 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### semantics/methods.k:136 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### semantics/methods.k:137 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule allDigit(.IntSeq) => true
```

### semantics/methods.k:138 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### semantics/methods.k:140 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### semantics/methods.k:142 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### semantics/methods.k:143 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule lowerC(C:Int) => C         [owise]
```

### semantics/methods.k:145 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= upperC(Int) [function, total]
```

### semantics/methods.k:146 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### semantics/methods.k:147 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule upperC(C:Int) => C         [owise]
```

### semantics/methods.k:149 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= swapC(Int) [function, total]
```

### semantics/methods.k:150 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### semantics/methods.k:151 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### semantics/methods.k:152 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `owise`

```k
  rule swapC(C:Int) => C         [owise]
```

### semantics/methods.k:154 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### semantics/methods.k:155 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### semantics/methods.k:156 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### semantics/methods.k:158 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### semantics/methods.k:159 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### semantics/methods.k:160 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### semantics/methods.k:162 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### semantics/methods.k:163 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### semantics/methods.k:164 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### semantics/methods.k:166 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### semantics/methods.k:167 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### semantics/methods.k:168 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### semantics/methods.k:169 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### semantics/operators.k:10 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### semantics/operators.k:12 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### semantics/operators.k:15 — context

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  context Compare(HOLE, _)
```

### semantics/operators.k:16 — context

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### semantics/operators.k:17 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `owise`

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### semantics/operators.k:19 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### semantics/operators.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### semantics/operators.k:25 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/operators.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### semantics/operators.k:34 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### semantics/operators.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### semantics/operators.k:44 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/range.k:9 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### semantics/range.k:10 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### semantics/range.k:12 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### semantics/range.k:13 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### semantics/range.k:15 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### semantics/range.k:17 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### semantics/range.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### semantics/range.k:23 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### semantics/set.k:8 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### semantics/set.k:11 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### semantics/set.k:12 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### semantics/set.k:13 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### semantics/set.k:16 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`, `function`, `total`

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### semantics/set.k:18 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### semantics/set.k:19 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### semantics/set.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### semantics/set.k:22 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### semantics/set.k:25 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### semantics/set.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### semantics/set.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### semantics/set.k:31 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### semantics/set.k:32 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### semantics/set.k:33 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### semantics/set.k:35 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### semantics/set.k:36 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### semantics/set.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### semantics/sort.k:18 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### semantics/sort.k:19 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### semantics/sort.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### semantics/sort.k:21 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### semantics/sort.k:22 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### semantics/sort.k:23 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### semantics/sort.k:24 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### semantics/sort.k:26 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### semantics/sort.k:27 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### semantics/sort.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### semantics/sort.k:29 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### semantics/sort.k:31 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `concrete`

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### semantics/sort.k:36 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### semantics/sort.k:40 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

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

### semantics/sort.k:49 — syntax

Disposition: `FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM`

Attributes: `function`, `total`, `symbol`, `no-evaluators`

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### semantics/sort.k:51 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`, `function`, `total`

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### semantics/sort.k:53 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### semantics/sort.k:54 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### semantics/sort.k:55 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### semantics/sort.k:57 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### semantics/sort.k:58 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule condRev(S:ValSeq, false) => S
```

### semantics/sort.k:59 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### semantics/sort.k:61 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### semantics/sort.k:63 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### semantics/sort.k:65 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

### semantics/str.k:8 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### semantics/str.k:9 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### semantics/str.k:13 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `function`

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### semantics/str.k:14 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### semantics/str.k:15 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule strToCodes("") => .IntSeq
```

### semantics/str.k:16 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### semantics/str.k:20 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### semantics/str.k:21 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### semantics/str.k:22 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### semantics/str.k:24 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### semantics/str.k:25 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### semantics/str.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### semantics/str.k:29 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### semantics/str.k:30 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### semantics/str.k:32 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### semantics/str.k:33 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### semantics/str.k:34 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### semantics/str.k:35 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### semantics/str.k:37 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### semantics/str.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### semantics/str.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### semantics/str.k:40 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### semantics/str.k:48 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### semantics/str.k:49 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### semantics/str.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### semantics/str.k:51 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### semantics/str.k:52 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### semantics/str.k:53 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### semantics/str.k:54 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### semantics/str.k:56 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### semantics/str.k:57 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### semantics/str.k:58 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### semantics/str.k:59 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### semantics/subscript.k:11 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### semantics/subscript.k:12 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### semantics/subscript.k:13 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### semantics/subscript.k:16 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### semantics/subscript.k:17 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### semantics/subscript.k:18 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### semantics/subscript.k:21 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### semantics/subscript.k:22 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### semantics/subscript.k:23 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### semantics/subscript.k:27 — context

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  context Subscript(HOLE, _)
```

### semantics/subscript.k:28 — context

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### semantics/subscript.k:31 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/subscript.k:35 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### semantics/subscript.k:37 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### semantics/subscript.k:38 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### semantics/subscript.k:39 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### semantics/subscript.k:40 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### semantics/subscript.k:44 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### semantics/subscript.k:49 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### semantics/subscript.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### semantics/subscript.k:51 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### semantics/subscript.k:52 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### semantics/subscript.k:54 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### semantics/subscript.k:55 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### semantics/subscript.k:56 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### semantics/subscript.k:58 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### semantics/subscript.k:61 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### semantics/subscript.k:63 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### semantics/subscript.k:64 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### semantics/subscript.k:66 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### semantics/subscript.k:68 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### semantics/subscript.k:72 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### semantics/subscript.k:73 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStep(noB)          => 1
```

### semantics/subscript.k:74 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStep(someB(S:Int)) => S
```

### semantics/subscript.k:76 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### semantics/subscript.k:77 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### semantics/subscript.k:79 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### semantics/subscript.k:81 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### semantics/subscript.k:83 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### semantics/subscript.k:84 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### semantics/subscript.k:86 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### semantics/subscript.k:88 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### semantics/subscript.k:90 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### semantics/subscript.k:91 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### semantics/subscript.k:93 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### semantics/subscript.k:96 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### semantics/subscript.k:97 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### semantics/subscript.k:99 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### semantics/subscript.k:102 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`, `total`

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### semantics/subscript.k:103 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### semantics/subscript.k:105 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### semantics/subscript.k:109 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### semantics/subscript.k:110 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### semantics/subscript.k:113 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### semantics/subscript.k:116 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### semantics/subscript.k:117 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### semantics/subscript.k:120 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### semantics/syntax.k:9 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `strict`, `seqstrict`, `macro`, `macro`, `strict`, `strict`

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

### semantics/syntax.k:32 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### semantics/syntax.k:33 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### semantics/syntax.k:34 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Entries  ::= List{Entry, ","}
```

### semantics/syntax.k:35 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### semantics/syntax.k:36 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax CompFors ::= List{CompFor, ""}
```

### semantics/syntax.k:37 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Exprs    ::= List{Expr, ","}
```

### semantics/syntax.k:38 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### semantics/syntax.k:39 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax Bound    ::= Expr | "NoBound"
```

### semantics/syntax.k:41 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: `strict`, `strict`, `strict`, `strict`, `strict`, `strict`, `strict`

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

### semantics/syntax.k:56 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### semantics/syntax.k:57 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### semantics/syntax.k:58 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### semantics/syntax.k:59 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### semantics/syntax.k:60 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax ParamNames ::= List{String, ","}
```

### semantics/syntax.k:61 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### semantics/tuple.k:10 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### semantics/tuple.k:11 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### semantics/tuple.k:14 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax ApplyK ::= "toTuple"
```

### semantics/tuple.k:15 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### semantics/tuple.k:16 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### semantics/tuple.k:18 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### semantics/tuple.k:20 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### semantics/tuple.k:21 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### semantics/tuple.k:23 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### semantics/tuple.k:24 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: `function`

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### semantics/tuple.k:25 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### semantics/tuple.k:26 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### semantics/tuple.k:28 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### semantics/tuple.k:31 — syntax

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### semantics/tuple.k:32 — rule

Disposition: `FIXED_USED_REVIEWED_FAITHFUL`

Attributes: none

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### semantics/tuple.k:35 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### semantics/tuple.k:42 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### semantics/tuple.k:43 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### semantics/tuple.k:44 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### semantics/tuple.k:49 — syntax

Disposition: `FIXED_DECLARATION_OR_CONFIGURATION`

Attributes: none

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### semantics/tuple.k:50 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### semantics/tuple.k:51 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### semantics/tuple.k:52 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: `priority`

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### semantics/tuple.k:55 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### semantics/tuple.k:57 — rule

Disposition: `FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH`

Attributes: none

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### verification.k:8 — syntax

Disposition: `PROOF_LOCAL_DECLARATION`

Attributes: `function`, `total`

```k
  syntax Bool ::= scanHappy(IntSeq, Int, Int, Int) [function, total]
```

### verification.k:9 — rule

Disposition: `PROOF_LOCAL_EXACT_EQUATION`

Attributes: none

```k
  rule scanHappy(.IntSeq, _:Int, _:Int, _:Int) => true
```

### verification.k:10 — rule

Disposition: `PROOF_LOCAL_EXACT_EQUATION`

Attributes: none

```k
  rule scanHappy(iCons(C:Int, REST:IntSeq), I:Int, _:Int, P1:Int)
    => scanHappy(REST, I +Int 1, P1, C)
    requires I <Int 2
```

### verification.k:13 — rule

Disposition: `PROOF_LOCAL_EXACT_EQUATION`

Attributes: none

```k
  rule scanHappy(iCons(C:Int, REST:IntSeq), I:Int, P2:Int, P1:Int)
    => (C =/=Int P1)
       andBool (C =/=Int P2)
       andBool (P1 =/=Int P2)
       andBool scanHappy(REST, I +Int 1, P1, C)
    requires I >=Int 2
```

### spec.k:6 — claim

Disposition: `POSITIVE_PROOF_OBLIGATION`

Attributes: `loop-invariant`

```k
  claim [loop-invariant]:
    <k>
      #loop(
        str(IS:IntSeq),
        Name("ch"),
        Assign(Name("code"), Call(Name("ord"), Name("ch")))
        If(
          BoolOp(
            "and",
            Compare(Name("i"), CmpOp(">=", Int(2))),
            BoolOp(
              "or",
              Compare(Name("code"), CmpOp("==", Name("previous1"))),
              Compare(Name("code"), CmpOp("==", Name("previous2"))),
              Compare(Name("previous1"), CmpOp("==", Name("previous2"))))),
          Assign(Name("happy"), Bool(false)),
          .Stmts)
        Assign(Name("previous2"), Name("previous1"))
        Assign(Name("previous1"), Name("code"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("is_happy" |-> _:Val, parent(-1))
       1 |-> scope(
              "s"         |-> str(_:IntSeq)
              "happy"     |-> (H:Bool => H andBool scanHappy(IS, I, P2, P1))
              "previous2" |-> (P2:Int => ?FINALP2:Int)
              "previous1" |-> (P1:Int => ?FINALP1:Int)
              "i"         |-> (I:Int => I +Int isLen(IS))
              "ch"        |-> (_:Val => ?FINALCH:Val)
              "code"      |-> (_:Int => ?FINALCODE:Int),
              parent(0))
    </scopes>
    requires I >=Int 2
```

### spec.k:45 — claim

Disposition: `POSITIVE_PROOF_OBLIGATION`

Attributes: `is-happy`

```k
  claim [is-happy]:
    <k>
      Call(Name("is_happy"), str(IS:IntSeq))
      => ?R:Bool
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "is_happy" |->
                closureVal(
                  ("s", .ParamNames),
                  Assign(Name("happy"), Bool(true))
                  Assign(Name("previous2"), UnaryOp("-", Int(1)))
                  Assign(Name("previous1"), UnaryOp("-", Int(1)))
                  Assign(Name("i"), Int(0))
                  Assign(Name("ch"), Str(""))
                  Assign(Name("code"), Int(0))
                  For(
                    Name("ch"),
                    Name("s"),
                    Assign(Name("code"), Call(Name("ord"), Name("ch")))
                    If(
                      BoolOp(
                        "and",
                        Compare(Name("i"), CmpOp(">=", Int(2))),
                        BoolOp(
                          "or",
                          Compare(
                            Name("code"),
                            CmpOp("==", Name("previous1"))),
                          Compare(
                            Name("code"),
                            CmpOp("==", Name("previous2"))),
                          Compare(
                            Name("previous1"),
                            CmpOp("==", Name("previous2"))))),
                      Assign(Name("happy"), Bool(false)),
                      .Stmts)
                    Assign(Name("previous2"), Name("previous1"))
                    Assign(Name("previous1"), Name("code"))
                    Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
                  Return(
                    BoolOp(
                      "and",
                      Compare(Name("i"), CmpOp(">=", Int(3))),
                      Name("happy"))),
                  0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    ensures ?R ==Bool
      ((isLen(IS) >=Int 3) andBool scanHappy(IS, 0, -1, -1))
```

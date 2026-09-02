# Exhaustive K source inventory

Generated directly from the fresh scratch source copy. Every local `syntax`,
`configuration`, `context`, `rule`, and `claim` entry is listed with its
complete source block and attributes. Imported K builtins are outside this
local-source inventory.

## Summary

| File | Lines | SHA-256 | Syntax | Config | Context | Rules | Claims | Function | Total | Functional | Opaque | Priority | Simplification | Concrete |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `reference-semantics/semantics.k` | 90 | `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/assert.k` | 16 | `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b` | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| `reference-semantics/semantics/bool.k` | 47 | `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd` | 0 | 0 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 |
| `reference-semantics/semantics/builtins.k` | 298 | `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd` | 38 | 0 | 0 | 137 | 0 | 29 | 22 | 0 | 1 | 1 | 0 | 0 |
| `reference-semantics/semantics/call.k` | 95 | `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4` | 3 | 0 | 0 | 21 | 0 | 1 | 1 | 0 | 0 | 5 | 0 | 0 |
| `reference-semantics/semantics/comprehension.k` | 27 | `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7` | 3 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/concrete.k` | 60 | `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305` | 5 | 0 | 0 | 16 | 0 | 3 | 1 | 0 | 0 | 2 | 0 | 0 |
| `reference-semantics/semantics/controls.k` | 109 | `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae` | 3 | 0 | 0 | 34 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 |
| `reference-semantics/semantics/core.k` | 240 | `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e` | 37 | 1 | 0 | 46 | 0 | 16 | 10 | 0 | 0 | 2 | 0 | 0 |
| `reference-semantics/semantics/dict.k` | 104 | `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580` | 12 | 0 | 0 | 28 | 0 | 8 | 4 | 0 | 0 | 2 | 0 | 0 |
| `reference-semantics/semantics/float.k` | 273 | `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f` | 34 | 0 | 0 | 121 | 0 | 26 | 25 | 0 | 19 | 4 | 0 | 26 |
| `reference-semantics/semantics/functions.k` | 91 | `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193` | 4 | 0 | 0 | 15 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| `reference-semantics/semantics/int.k` | 28 | `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5` | 1 | 0 | 0 | 16 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/iter.k` | 9 | `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/list.k` | 68 | `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa` | 5 | 0 | 0 | 27 | 0 | 3 | 2 | 0 | 0 | 2 | 0 | 0 |
| `reference-semantics/semantics/methods.k` | 170 | `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743` | 27 | 0 | 0 | 75 | 0 | 27 | 22 | 0 | 0 | 3 | 0 | 0 |
| `reference-semantics/semantics/operators.k` | 47 | `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b` | 0 | 0 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 |
| `reference-semantics/semantics/range.k` | 25 | `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d` | 2 | 0 | 0 | 6 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/set.k` | 40 | `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7` | 6 | 0 | 0 | 12 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/sort.k` | 72 | `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a` | 6 | 0 | 0 | 19 | 0 | 6 | 4 | 0 | 2 | 1 | 0 | 9 |
| `reference-semantics/semantics/str.k` | 60 | `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f` | 5 | 0 | 0 | 28 | 0 | 5 | 4 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/subscript.k` | 122 | `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7` | 15 | 0 | 2 | 40 | 0 | 13 | 6 | 0 | 0 | 2 | 0 | 0 |
| `reference-semantics/semantics/syntax.k` | 62 | `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6` | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/tuple.k` | 58 | `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb` | 4 | 0 | 0 | 21 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | 0 |
| `verification.k` | 28 | `2676f2f6309fcfced10755a7fc35578374bdcd7339102663c32f389783f3835e` | 2 | 0 | 0 | 5 | 0 | 2 | 2 | 0 | 1 | 0 | 2 | 0 |
| `spec.k` | 100 | `29241d4f6ece30ac821ac9a14c7f94d78e040b0c9eb7c4feb1c23d416aff25a0` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Aggregate local entries: **937** (229 syntax, 1 configuration, 5 context, 700 rule, 2 claim).

## Complete inventory

### `reference-semantics/semantics.k`

No local declaration or rule entries.

### `reference-semantics/semantics/assert.k`

- **rule at line 6**

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

- **rule at line 8**

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

- **rule at line 13** — tags: priority

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/bool.k`

- **rule at line 8**

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

- **rule at line 10**

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

- **rule at line 11**

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

- **context at line 16**

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

- **rule at line 17**

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

- **rule at line 18**

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

- **rule at line 20**

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

- **rule at line 22**

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

- **rule at line 24**

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

- **rule at line 29** — tags: priority

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

- **rule at line 31** — tags: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

- **rule at line 35** — tags: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

- **rule at line 39** — tags: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

- **rule at line 43** — tags: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### `reference-semantics/semantics/builtins.k`

- **syntax at line 17** — tags: function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

- **syntax at line 20** — tags: function

```k
  syntax Int ::= seqLen(Val) [function]
```

- **rule at line 21**

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

- **rule at line 22**

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

- **rule at line 23**

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

- **rule at line 24**

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

- **rule at line 25**

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

- **rule at line 26**

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

- **rule at line 32**

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

- **rule at line 33**

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

- **rule at line 34**

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

- **rule at line 35**

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

- **syntax at line 36** — tags: function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

- **rule at line 37**

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

- **rule at line 38**

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

- **rule at line 41**

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

- **rule at line 44**

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

- **syntax at line 47**

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

- **rule at line 48**

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

- **rule at line 49**

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

- **rule at line 50**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

- **syntax at line 54** — tags: function

```k
  syntax Int ::= intOf(Val) [function]
```

- **rule at line 55**

```k
  rule intOf(I:Int)  => I
```

- **rule at line 56**

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

- **syntax at line 59**

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

- **rule at line 60**

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

- **rule at line 61**

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

- **rule at line 62**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

- **rule at line 64**

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

- **syntax at line 67**

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

- **rule at line 68**

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

- **rule at line 69**

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

- **rule at line 70**

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

- **rule at line 72**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

- **syntax at line 76**

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

- **rule at line 77**

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

- **rule at line 78**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

- **rule at line 80**

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

- **rule at line 81**

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

- **rule at line 82**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

- **syntax at line 86**

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

- **rule at line 87**

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

- **rule at line 88**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

- **rule at line 90**

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

- **rule at line 91**

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

- **rule at line 92**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

- **syntax at line 97** — tags: function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

- **rule at line 98**

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

- **rule at line 99**

```k
  rule maxVals(M:Int, .Vals)           => M
```

- **rule at line 100**

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

- **syntax at line 102** — tags: function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

- **rule at line 103**

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

- **rule at line 104**

```k
  rule minVals(M:Int, .Vals)           => M
```

- **rule at line 105**

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

- **rule at line 108**

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

- **rule at line 111**

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

- **syntax at line 114** — tags: function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

- **rule at line 115**

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

- **rule at line 116**

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

- **syntax at line 117** — tags: function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

- **rule at line 118**

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

- **rule at line 119**

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

- **rule at line 124**

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

- **syntax at line 126** — tags: function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

- **rule at line 127**

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

- **rule at line 128**

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

- **rule at line 132**

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

- **syntax at line 134** — tags: function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

- **rule at line 135**

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

- **rule at line 136**

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

- **rule at line 137**

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

- **rule at line 140**

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

- **rule at line 143**

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

- **rule at line 144**

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

- **rule at line 148**

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

- **rule at line 149**

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

- **rule at line 152**

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

- **rule at line 156**

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

- **syntax at line 158** — tags: function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

- **rule at line 159**

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

- **rule at line 160**

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

- **rule at line 163**

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

- **rule at line 164**

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

- **rule at line 167**

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

- **rule at line 169**

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

- **rule at line 170**

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

- **rule at line 171**

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

- **rule at line 173**

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

- **rule at line 174**

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

- **rule at line 177**

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

- **rule at line 178**

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

- **rule at line 179**

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

- **rule at line 187**

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

- **syntax at line 188** — tags: function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

- **rule at line 189**

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

- **syntax at line 192**

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

- **syntax at line 194** — tags: function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

- **rule at line 195**

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

- **syntax at line 196** — tags: function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

- **rule at line 197**

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

- **rule at line 198** — tags: owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

- **syntax at line 199** — tags: function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

- **rule at line 200**

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

- **rule at line 201** — tags: owise

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

- **syntax at line 203** — tags: function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

- **rule at line 204**

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

- **rule at line 205**

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

- **rule at line 206**

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

- **rule at line 207**

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

- **rule at line 208**

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

- **rule at line 209**

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

- **rule at line 210**

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

- **rule at line 211**

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

- **rule at line 212**

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

- **syntax at line 214** — tags: function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

- **rule at line 216**

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

- **rule at line 217**

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

- **rule at line 218**

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

- **rule at line 219**

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

- **rule at line 221**

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

- **rule at line 223** — tags: owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

- **syntax at line 225**

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

- **syntax at line 226** — tags: function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

- **rule at line 227**

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

- **rule at line 228** — tags: owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

- **syntax at line 230** — tags: function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

- **rule at line 231**

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

- **rule at line 232**

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

- **rule at line 233**

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

- **rule at line 234**

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

- **rule at line 235**

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

- **rule at line 236** — tags: owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

- **syntax at line 238** — tags: function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

- **rule at line 239**

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

- **rule at line 240**

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

- **rule at line 241**

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

- **rule at line 243** — tags: owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

- **syntax at line 244** — tags: function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

- **rule at line 245**

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

- **rule at line 246**

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

- **syntax at line 247** — tags: function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

- **rule at line 248**

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

- **syntax at line 250** — tags: function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

- **rule at line 251**

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

- **rule at line 252**

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

- **rule at line 253**

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

- **rule at line 254**

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

- **syntax at line 255** — tags: function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

- **rule at line 256**

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

- **rule at line 257**

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

- **rule at line 260**

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

- **rule at line 263** — tags: owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

- **syntax at line 265** — tags: function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

- **rule at line 266**

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

- **rule at line 267**

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

- **rule at line 268** — tags: owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

- **syntax at line 269** — tags: function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

- **rule at line 270**

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

- **rule at line 271**

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

- **syntax at line 272** — tags: function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

- **rule at line 273**

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

- **rule at line 274**

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

- **syntax at line 279**

```k
  syntax KItem ::= "#md5"
```

- **rule at line 280** — tags: priority

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

- **rule at line 282**

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

- **syntax at line 283**

```k
  syntax Val ::= md5Obj(IntSeq)
```

- **rule at line 284**

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

- **syntax at line 285** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

- **rule at line 291**

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

- **rule at line 292**

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

- **syntax at line 293** — tags: function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

- **rule at line 294**

```k
  rule isIntV(_:Int)         => true
```

- **rule at line 295** — tags: owise

```k
  rule isIntV(_:Val)         => false [owise]
```

- **rule at line 296**

```k
  rule isStrV(str(_:IntSeq)) => true
```

- **rule at line 297** — tags: owise

```k
  rule isStrV(_:Val)         => false [owise]
```

### `reference-semantics/semantics/call.k`

- **rule at line 16**

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

- **syntax at line 19**

```k
  syntax KItem ::= #callee(Exprs)
```

- **rule at line 20** — tags: owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

- **rule at line 21**

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

- **rule at line 24**

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

- **rule at line 26**

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

- **rule at line 27**

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

- **rule at line 28**

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

- **rule at line 29**

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

- **rule at line 30**

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

- **rule at line 31** — tags: owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

- **rule at line 32**

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

- **rule at line 38** — tags: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **rule at line 42** — tags: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

- **rule at line 47** — tags: priority

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **syntax at line 52** — tags: function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

- **rule at line 53**

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

- **rule at line 56** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

- **rule at line 63** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

- **rule at line 69**

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

- **rule at line 80**

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

- **syntax at line 87**

```k
  syntax KItem ::= #allocCells(ParamNames)
```

- **rule at line 88**

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

- **rule at line 89**

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### `reference-semantics/semantics/comprehension.k`

- **rule at line 11**

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

- **rule at line 12**

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

- **syntax at line 14** — tags: macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

- **rule at line 15**

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

- **syntax at line 18** — tags: macro

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

- **rule at line 19**

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

- **rule at line 21**

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

- **syntax at line 24** — tags: macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

- **rule at line 25**

```k
  rule compGuard(.Exprs)             => Bool(true)
```

- **rule at line 26**

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### `reference-semantics/semantics/concrete.k`

- **rule at line 13**

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

- **rule at line 16**

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

- **syntax at line 25**

```k
  syntax Val ::= kvP(Val, Val)
```

- **syntax at line 26**

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

- **rule at line 28** — tags: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

- **rule at line 31** — tags: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

- **rule at line 34**

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

- **rule at line 36**

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

- **rule at line 38**

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

- **syntax at line 42** — tags: function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

- **rule at line 43**

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

- **rule at line 44**

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

- **rule at line 47**

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

- **syntax at line 51** — tags: function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

- **rule at line 52**

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

- **rule at line 53**

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

- **rule at line 54**

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

- **syntax at line 56** — tags: function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

- **rule at line 57**

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

- **rule at line 58**

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

- **rule at line 59** — tags: owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### `reference-semantics/semantics/controls.k`

- **rule at line 9**

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

- **rule at line 12** — tags: priority

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

- **rule at line 20**

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

- **rule at line 27** — tags: priority

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

- **rule at line 35**

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

- **rule at line 36** — tags: owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

- **syntax at line 37**

```k
  syntax KItem ::= #bindImports(ParamNames)
```

- **rule at line 38**

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

- **rule at line 39**

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

- **rule at line 43**

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

- **rule at line 48**

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

- **syntax at line 51**

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

- **rule at line 52**

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

- **rule at line 53**

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

- **rule at line 54**

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

- **rule at line 57**

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

- **rule at line 59**

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

- **syntax at line 65**

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

- **rule at line 69**

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

- **rule at line 71**

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

- **rule at line 72**

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

- **rule at line 73**

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

- **rule at line 77**

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

- **rule at line 78**

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

- **rule at line 79**

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

- **rule at line 81**

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

- **rule at line 85**

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

- **rule at line 86**

```k
  rule <k> Continue => #cont ... </k>
```

- **rule at line 87**

```k
  rule <k> Break => #brk ... </k>
```

- **rule at line 88**

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

- **rule at line 89** — tags: owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

- **rule at line 90**

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

- **rule at line 91** — tags: owise

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

- **rule at line 95** — tags: priority

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **rule at line 98** — tags: priority

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **rule at line 101** — tags: priority

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **rule at line 106** — tags: priority

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/core.k`

- **syntax at line 13**

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

- **syntax at line 14**

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

- **syntax at line 15**

```k
  syntax Str    ::= str(IntSeq)
```

- **syntax at line 18**

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

- **syntax at line 25** — tags: function

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

- **syntax at line 36**

```k
  syntax Parent   ::= "root" | parent(Int)
```

- **syntax at line 37**

```k
  syntax Scope    ::= scope(Map, Parent)
```

- **syntax at line 38**

```k
  syntax KResult  ::= Val
```

- **syntax at line 39**

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

- **syntax at line 40**

```k
  syntax Vals     ::= List{Val, ","}
```

- **syntax at line 41**

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

- **syntax at line 42**

```k
  syntax RetState ::= "noRet" | retV(Val)
```

- **configuration at line 49**

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
```

- **syntax at line 68** — tags: function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

- **rule at line 69**

```k
  rule isRefV(ref(_:Int)) => true
```

- **rule at line 70** — tags: owise

```k
  rule isRefV(_:Val)      => false [owise]
```

- **syntax at line 75**

```k
  syntax HeapVal ::= cellV(Val)
```

- **syntax at line 76** — tags: function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

- **rule at line 77**

```k
  rule isCellRef(cellRef(_:Int)) => true
```

- **rule at line 78** — tags: owise

```k
  rule isCellRef(_:Val)          => false [owise]
```

- **rule at line 85** — tags: priority

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

- **syntax at line 95**

```k
  syntax Val ::= kwV(String, Val)
```

- **syntax at line 96**

```k
  syntax KItem ::= #kwTag(String)
```

- **rule at line 97**

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

- **rule at line 98**

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

- **syntax at line 100** — tags: function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

- **rule at line 101**

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

- **rule at line 102** — tags: owise

```k
  rule isKwV(_:Val)                => false [owise]
```

- **syntax at line 106**

```k
  syntax Val ::= cellsMark(ParamNames)
```

- **syntax at line 107** — tags: function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

- **rule at line 108**

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

- **syntax at line 109** — tags: function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

- **rule at line 110**

```k
  rule pnMember(_:String, .ParamNames) => false
```

- **rule at line 111**

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

- **syntax at line 113**

```k
  syntax KItem ::= #cellW(Val, Val)
```

- **rule at line 114**

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

- **syntax at line 117**

```k
  syntax KItem ::= #alloc(Val)
```

- **rule at line 118**

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

- **syntax at line 124**

```k
  syntax KItem ::= #loadAll(Module)
```

- **rule at line 125**

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

- **rule at line 126**

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

- **rule at line 127**

```k
  rule <k> .Stmts => .K ... </k>
```

- **syntax at line 130**

```k
  syntax KItem ::= #look(String, Int)
```

- **rule at line 131**

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

- **rule at line 132**

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

- **rule at line 145** — tags: priority

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

- **rule at line 152**

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

- **syntax at line 157** — tags: function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

- **rule at line 158**

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
```

- **syntax at line 185**

```k
  syntax ApplyK ::= toCall(Val)
```

- **syntax at line 186**

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

- **rule at line 189**

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

- **rule at line 190**

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

- **rule at line 191**

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

- **rule at line 194**

```k
  rule <k> Int(I:Int)   => I ... </k>
```

- **rule at line 195**

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

- **rule at line 196**

```k
  rule <k> NoneVal      => noneV ... </k>
```

- **syntax at line 199** — tags: function

```k
  syntax Bool ::= truthy(Val) [function]
```

- **rule at line 200**

```k
  rule truthy(B:Bool)          => B
```

- **rule at line 201**

```k
  rule truthy(noneV)           => false
```

- **rule at line 202**

```k
  rule truthy(I:Int)           => I =/=Int 0
```

- **rule at line 203**

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

- **rule at line 204**

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

- **rule at line 205**

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

- **syntax at line 208** — tags: function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

- **syntax at line 209** — tags: function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

- **syntax at line 210** — tags: function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

- **syntax at line 213** — tags: function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

- **rule at line 214**

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

- **rule at line 215**

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

- **syntax at line 217** — tags: function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

- **rule at line 218**

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

- **rule at line 219**

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

- **syntax at line 223** — tags: function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

- **rule at line 224**

```k
  rule vsLen(.ValSeq)                => 0
```

- **rule at line 225**

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

- **syntax at line 227** — tags: function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

- **rule at line 228**

```k
  rule isLen(.IntSeq)                => 0
```

- **rule at line 229**

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

- **syntax at line 233** — tags: function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

- **rule at line 234**

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

- **rule at line 235**

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

- **rule at line 236**

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

- **rule at line 238**

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### `reference-semantics/semantics/dict.k`

- **syntax at line 20**

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

- **syntax at line 23**

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

- **rule at line 26**

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

- **rule at line 27**

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

- **rule at line 28**

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

- **rule at line 30**

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

- **rule at line 32**

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

- **syntax at line 37** — tags: function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

- **rule at line 38**

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

- **rule at line 39**

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

- **rule at line 40**

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

- **syntax at line 43** — tags: function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

- **rule at line 44**

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

- **rule at line 45**

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

- **syntax at line 49** — tags: function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

- **rule at line 50**

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

- **rule at line 52**

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

- **rule at line 54** — tags: owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

- **rule at line 58** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

- **rule at line 63**

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

- **syntax at line 64** — tags: function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

- **rule at line 65** — tags: priority

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

- **syntax at line 70** — tags: function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

- **rule at line 71**

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

- **syntax at line 76**

```k
  syntax KItem ::= #dsetK(String, Val)
```

- **rule at line 77**

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

- **rule at line 78**

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

- **rule at line 82**

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

- **syntax at line 86**

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

- **rule at line 87**

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

- **syntax at line 90** — tags: function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

- **rule at line 91**

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

- **rule at line 92**

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

- **rule at line 95**

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

- **syntax at line 97** — tags: function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

- **rule at line 98**

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

- **rule at line 99**

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

- **syntax at line 101** — tags: function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

- **rule at line 102**

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

- **rule at line 103**

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### `reference-semantics/semantics/float.k`

- **syntax at line 20**

```k
  syntax Val ::= Float
```

- **rule at line 21**

```k
  rule <k> Float(F:Float) => F ... </k>
```

- **syntax at line 24** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

- **rule at line 25** — tags: concrete

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

- **rule at line 27**

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

- **syntax at line 30** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

- **rule at line 31** — tags: concrete

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

- **rule at line 32**

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

- **syntax at line 37** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

- **rule at line 38** — tags: concrete

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

- **rule at line 39**

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

- **rule at line 43**

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

- **rule at line 44**

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

- **syntax at line 50** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

- **rule at line 51** — tags: concrete

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

- **rule at line 52**

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

- **syntax at line 54** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

- **rule at line 55** — tags: concrete

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

- **rule at line 56**

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

- **rule at line 61**

```k
  rule <k> Import(_:String) => .K ... </k>
```

- **syntax at line 65**

```k
  syntax KItem ::= "#mathCeil"
```

- **rule at line 66** — tags: priority

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

- **rule at line 67**

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

- **syntax at line 70**

```k
  syntax KItem ::= "#mathFloor"
```

- **rule at line 71** — tags: priority

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

- **rule at line 72**

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

- **syntax at line 73** — tags: function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

- **rule at line 74** — tags: concrete

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

- **rule at line 75** — tags: concrete

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

- **rule at line 78**

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

- **rule at line 79**

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

- **syntax at line 82**

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

- **rule at line 83** — tags: priority

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

- **rule at line 84**

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

- **rule at line 85**

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

- **syntax at line 86** — tags: function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

- **rule at line 87** — tags: concrete

```k
  rule toF(F:Float) => F        [concrete]
```

- **rule at line 88** — tags: concrete

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

- **syntax at line 93** — tags: function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

- **rule at line 94** — tags: concrete

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

- **rule at line 95** — tags: concrete

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

- **rule at line 99**

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

- **syntax at line 103** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

- **rule at line 104** — tags: concrete

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

- **rule at line 105**

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

- **syntax at line 107** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

- **rule at line 108** — tags: concrete

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

- **rule at line 109**

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

- **syntax at line 111** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

- **rule at line 112** — tags: concrete

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

- **rule at line 113**

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

- **syntax at line 115** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

- **rule at line 116** — tags: concrete

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

- **rule at line 117**

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

- **syntax at line 119** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

- **rule at line 120** — tags: concrete

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

- **rule at line 121**

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

- **syntax at line 125** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

- **rule at line 126** — tags: concrete

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

- **rule at line 127**

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

- **rule at line 128**

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

- **rule at line 129**

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

- **rule at line 132**

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

- **rule at line 133**

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

- **rule at line 134**

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

- **rule at line 135**

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

- **rule at line 136**

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

- **rule at line 137**

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

- **rule at line 138**

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

- **rule at line 139**

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

- **syntax at line 142** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

- **rule at line 143** — tags: concrete

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

- **rule at line 144**

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

- **rule at line 145**

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

- **rule at line 146**

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

- **rule at line 147**

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

- **rule at line 148**

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

- **rule at line 149**

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

- **rule at line 150**

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

- **rule at line 151**

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

- **rule at line 154**

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

- **rule at line 155**

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

- **syntax at line 160** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

- **rule at line 161** — tags: concrete

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

- **rule at line 162** — tags: concrete

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

- **syntax at line 165** — tags: function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

- **rule at line 166**

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

- **syntax at line 167** — tags: function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

- **rule at line 168**

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

- **rule at line 169**

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

- **rule at line 170**

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

- **rule at line 171**

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

- **syntax at line 173** — tags: function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

- **rule at line 174**

```k
  rule fracPart(.IntSeq) => 0
```

- **rule at line 175**

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

- **rule at line 176**

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

- **rule at line 177**

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

- **rule at line 178**

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

- **syntax at line 179** — tags: function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

- **rule at line 180**

```k
  rule fracScale(.IntSeq) => 1
```

- **rule at line 181**

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

- **rule at line 182**

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

- **rule at line 183**

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

- **rule at line 184**

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

- **rule at line 185**

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

- **rule at line 186**

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

- **rule at line 187**

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

- **syntax at line 190** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

- **rule at line 191** — tags: concrete

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

- **rule at line 192**

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

- **syntax at line 195** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

- **rule at line 196** — tags: concrete

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

- **rule at line 197**

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

- **rule at line 198**

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

- **rule at line 199**

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

- **rule at line 200**

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

- **rule at line 201**

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

- **rule at line 202**

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

- **rule at line 203**

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

- **rule at line 204**

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

- **rule at line 205**

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

- **rule at line 206**

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

- **syntax at line 209** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

- **rule at line 210** — tags: concrete

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

- **rule at line 211**

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

- **rule at line 213**

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

- **rule at line 214**

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

- **syntax at line 217** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

- **rule at line 218** — tags: concrete

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

- **syntax at line 223** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

- **rule at line 224** — tags: concrete

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

- **rule at line 227**

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

- **rule at line 228**

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

- **syntax at line 230** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

- **rule at line 231** — tags: concrete

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

- **syntax at line 232**

```k
  syntax KItem ::= "#mathSqrt"
```

- **rule at line 233** — tags: priority

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

- **rule at line 234**

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

- **rule at line 235**

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

- **syntax at line 243**

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

- **rule at line 244**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

- **rule at line 245**

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

- **rule at line 246**

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

- **rule at line 247**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

- **syntax at line 250**

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

- **rule at line 251**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

- **rule at line 252**

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

- **rule at line 253**

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

- **rule at line 254**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

- **syntax at line 261**

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

- **rule at line 262**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

- **rule at line 265**

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

- **rule at line 266**

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

- **rule at line 267**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

- **rule at line 270**

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### `reference-semantics/semantics/functions.k`

- **syntax at line 8**

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

- **rule at line 14**

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

- **syntax at line 18**

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

- **rule at line 19**

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

- **syntax at line 27**

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

- **syntax at line 31**

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

- **rule at line 33**

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

- **rule at line 36**

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

- **rule at line 42**

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

- **rule at line 47**

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

- **rule at line 50**

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

- **rule at line 53**

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

- **rule at line 59**

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

- **rule at line 63**

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

- **rule at line 64**

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

- **rule at line 68** — tags: priority

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
        andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
       [priority(40)]
```

- **rule at line 78**

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

- **rule at line 80**

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

- **rule at line 85**

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### `reference-semantics/semantics/int.k`

- **rule at line 7**

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

- **rule at line 9**

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

- **rule at line 11**

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

- **rule at line 12**

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

- **rule at line 13**

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

- **rule at line 14**

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

- **rule at line 15**

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

- **rule at line 16**

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

- **rule at line 17**

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

- **syntax at line 19** — tags: function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

- **rule at line 20**

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

- **rule at line 22**

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

- **rule at line 23**

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

- **rule at line 24**

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

- **rule at line 25**

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

- **rule at line 26**

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

- **rule at line 27**

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### `reference-semantics/semantics/iter.k`

- **syntax at line 8**

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### `reference-semantics/semantics/list.k`

- **rule at line 9**

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

- **rule at line 10**

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

- **syntax at line 13**

```k
  syntax ApplyK ::= "toList"
```

- **rule at line 14**

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

- **rule at line 15**

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

- **syntax at line 18** — tags: function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

- **rule at line 19**

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

- **rule at line 20**

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

- **rule at line 24** — tags: priority

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

- **rule at line 27**

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

- **rule at line 28**

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

- **syntax at line 33** — tags: function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

- **rule at line 34**

```k
  rule hasRefVS(.ValSeq)                => false
```

- **rule at line 35**

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

- **syntax at line 37** — tags: function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

- **rule at line 39**

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

- **rule at line 40**

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

- **rule at line 41**

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

- **rule at line 42**

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

- **rule at line 45**

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

- **rule at line 47**

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

- **rule at line 49**

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

- **rule at line 50** — tags: owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

- **rule at line 53** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

- **syntax at line 58**

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

- **rule at line 59**

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

- **rule at line 60**

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

- **rule at line 61**

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

- **rule at line 62**

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

- **rule at line 63**

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

- **rule at line 65**

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

- **rule at line 67**

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### `reference-semantics/semantics/methods.k`

- **syntax at line 10** — tags: function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

- **rule at line 13**

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

- **rule at line 14**

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

- **rule at line 15**

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

- **rule at line 16**

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

- **rule at line 19**

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

- **rule at line 20**

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

- **rule at line 21**

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

- **rule at line 26**

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

- **syntax at line 27** — tags: function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

- **rule at line 28**

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

- **rule at line 29**

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

- **rule at line 30**

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

- **rule at line 34**

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

- **syntax at line 35** — tags: function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

- **rule at line 36**

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

- **rule at line 37**

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

- **rule at line 39**

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

- **syntax at line 41** — tags: function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

- **rule at line 42**

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

- **rule at line 43** — tags: owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

- **rule at line 44**

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

- **rule at line 47**

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

- **syntax at line 48** — tags: function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

- **rule at line 49**

```k
  rule trimWS(.IntSeq) => .IntSeq
```

- **rule at line 50**

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

- **rule at line 51**

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

- **syntax at line 52** — tags: function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

- **rule at line 53**

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

- **rule at line 54**

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

- **rule at line 55**

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

- **rule at line 58**

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

- **rule at line 61**

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

- **rule at line 64**

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

- **syntax at line 65** — tags: function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

- **rule at line 66**

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

- **rule at line 67**

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

- **rule at line 68**

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

- **rule at line 72** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

- **syntax at line 75** — tags: function

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

- **rule at line 76**

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

- **rule at line 77**

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

- **rule at line 79**

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

- **syntax at line 82** — tags: function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

- **rule at line 83**

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

- **rule at line 84**

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

- **syntax at line 85** — tags: function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

- **rule at line 86**

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

- **rule at line 89** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

- **rule at line 94** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

- **syntax at line 97** — tags: function

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

- **rule at line 98**

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

- **rule at line 99**

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

- **rule at line 101**

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

- **rule at line 104**

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

- **syntax at line 106** — tags: function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

- **rule at line 107**

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

- **rule at line 108**

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

- **rule at line 109**

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

- **syntax at line 112** — tags: function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

- **rule at line 113**

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

- **syntax at line 115** — tags: function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

- **rule at line 116**

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

- **syntax at line 118** — tags: function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

- **rule at line 119**

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

- **syntax at line 121** — tags: function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

- **rule at line 122**

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

- **syntax at line 124** — tags: function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

- **rule at line 125**

```k
  rule hasUpper(.IntSeq) => false
```

- **rule at line 126**

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

- **syntax at line 128** — tags: function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

- **rule at line 129**

```k
  rule hasLower(.IntSeq) => false
```

- **rule at line 130**

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

- **syntax at line 132** — tags: function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

- **rule at line 133**

```k
  rule allAlpha(.IntSeq) => true
```

- **rule at line 134**

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

- **syntax at line 136** — tags: function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

- **rule at line 137**

```k
  rule allDigit(.IntSeq) => true
```

- **rule at line 138**

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

- **syntax at line 140** — tags: function, total

```k
  syntax Int ::= lowerC(Int) [function, total]
```

- **rule at line 142**

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

- **rule at line 143** — tags: owise

```k
  rule lowerC(C:Int) => C         [owise]
```

- **syntax at line 145** — tags: function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

- **rule at line 146**

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

- **rule at line 147** — tags: owise

```k
  rule upperC(C:Int) => C         [owise]
```

- **syntax at line 149** — tags: function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

- **rule at line 150**

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

- **rule at line 151**

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

- **rule at line 152** — tags: owise

```k
  rule swapC(C:Int) => C         [owise]
```

- **syntax at line 154** — tags: function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

- **rule at line 155**

```k
  rule mapLower(.IntSeq) => .IntSeq
```

- **rule at line 156**

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

- **syntax at line 158** — tags: function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

- **rule at line 159**

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

- **rule at line 160**

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

- **syntax at line 162** — tags: function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

- **rule at line 163**

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

- **rule at line 164**

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

- **syntax at line 166** — tags: function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

- **rule at line 167**

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

- **rule at line 168**

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

- **rule at line 169**

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### `reference-semantics/semantics/operators.k`

- **rule at line 10**

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

- **rule at line 12**

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

- **context at line 15**

```k
  context Compare(HOLE, _)
```

- **context at line 16**

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

- **rule at line 17** — tags: owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

- **rule at line 19**

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

- **rule at line 20**

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

- **rule at line 25** — tags: priority

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **rule at line 28** — tags: priority

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

- **rule at line 34** — tags: priority

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

- **rule at line 38** — tags: priority

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

- **rule at line 44** — tags: priority

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/range.k`

- **syntax at line 9** — tags: function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

- **rule at line 10**

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

- **syntax at line 12** — tags: function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

- **rule at line 13**

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

- **rule at line 15**

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

- **rule at line 17**

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

- **rule at line 20**

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

- **rule at line 23**

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### `reference-semantics/semantics/set.k`

- **syntax at line 8**

```k
  syntax Val ::= setV(IntSeq)
```

- **syntax at line 11** — tags: function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

- **rule at line 12**

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

- **rule at line 13**

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

- **syntax at line 16** — tags: function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

- **rule at line 18**

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

- **rule at line 19**

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

- **rule at line 20**

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

- **rule at line 22**

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

- **syntax at line 25** — tags: function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

- **rule at line 26**

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

- **rule at line 27**

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

- **syntax at line 31** — tags: function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

- **rule at line 32**

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

- **rule at line 33**

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

- **syntax at line 35** — tags: function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

- **rule at line 36**

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

- **rule at line 39**

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### `reference-semantics/semantics/sort.k`

- **syntax at line 18** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

- **syntax at line 19** — tags: function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

- **rule at line 20** — tags: concrete

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

- **rule at line 21** — tags: concrete

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

- **rule at line 22** — tags: concrete

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

- **rule at line 23** — tags: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

- **rule at line 24** — tags: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

- **syntax at line 26** — tags: function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

- **rule at line 27** — tags: concrete

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

- **rule at line 28** — tags: concrete

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

- **rule at line 29** — tags: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

- **rule at line 31** — tags: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

- **rule at line 36**

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

- **rule at line 40** — tags: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

- **syntax at line 49** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

- **syntax at line 51** — tags: function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

- **rule at line 53**

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

- **rule at line 54**

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

- **rule at line 55**

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

- **syntax at line 57** — tags: function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

- **rule at line 58**

```k
  rule condRev(S:ValSeq, false) => S
```

- **rule at line 59**

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

- **rule at line 61**

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

- **rule at line 63**

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

- **rule at line 65**

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

### `reference-semantics/semantics/str.k`

- **rule at line 8**

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

- **rule at line 9**

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

- **syntax at line 13** — tags: function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

- **rule at line 14**

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

- **rule at line 15**

```k
  rule strToCodes("") => .IntSeq
```

- **rule at line 16**

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

- **syntax at line 20** — tags: function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

- **rule at line 21**

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

- **rule at line 22**

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

- **rule at line 24**

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

- **rule at line 25**

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

- **rule at line 26**

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

- **rule at line 29**

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

- **rule at line 30**

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

- **syntax at line 32** — tags: function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

- **rule at line 33**

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

- **rule at line 34**

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

- **rule at line 35**

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

- **syntax at line 37** — tags: function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

- **rule at line 38**

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

- **rule at line 39**

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

- **rule at line 40**

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

- **syntax at line 48** — tags: function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

- **rule at line 49**

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

- **rule at line 50**

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

- **rule at line 51**

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

- **rule at line 52**

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

- **rule at line 53**

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

- **rule at line 54**

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

- **rule at line 56**

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

- **rule at line 57**

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

- **rule at line 58**

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

- **rule at line 59**

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### `reference-semantics/semantics/subscript.k`

- **syntax at line 11** — tags: function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

- **rule at line 12**

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

- **rule at line 13**

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

- **syntax at line 16** — tags: function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

- **rule at line 17**

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

- **rule at line 18**

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

- **syntax at line 21** — tags: function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

- **rule at line 22**

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

- **rule at line 23**

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

- **context at line 27**

```k
  context Subscript(HOLE, _)
```

- **context at line 28**

```k
  context Subscript(_:Val, HOLE:Expr)
```

- **rule at line 31** — tags: priority

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **rule at line 35**

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

- **syntax at line 37** — tags: function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

- **rule at line 38**

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

- **rule at line 39**

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

- **rule at line 40**

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

- **syntax at line 44**

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

- **syntax at line 49**

```k
  syntax OptInt ::= "noB" | someB(Int)
```

- **rule at line 50**

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

- **rule at line 51**

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

- **rule at line 52**

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

- **rule at line 54**

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

- **rule at line 55**

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

- **rule at line 56**

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

- **rule at line 58** — tags: priority

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

- **rule at line 61**

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

- **syntax at line 63** — tags: function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

- **rule at line 64**

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

- **rule at line 66**

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

- **rule at line 68**

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

- **syntax at line 72** — tags: function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

- **rule at line 73**

```k
  rule slStep(noB)          => 1
```

- **rule at line 74**

```k
  rule slStep(someB(S:Int)) => S
```

- **syntax at line 76** — tags: function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

- **rule at line 77**

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

- **rule at line 79**

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

- **rule at line 81**

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

- **syntax at line 83** — tags: function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

- **rule at line 84**

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

- **rule at line 86**

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

- **rule at line 88**

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

- **syntax at line 90** — tags: function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

- **rule at line 91**

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

- **rule at line 93**

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

- **syntax at line 96** — tags: function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

- **rule at line 97**

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

- **rule at line 99**

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

- **syntax at line 102** — tags: function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

- **rule at line 103**

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

- **rule at line 105**

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

- **syntax at line 109** — tags: function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

- **rule at line 110**

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

- **rule at line 113**

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

- **syntax at line 116** — tags: function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

- **rule at line 117**

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

- **rule at line 120**

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### `reference-semantics/semantics/syntax.k`

- **syntax at line 9** — tags: macro, strict

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

- **syntax at line 32**

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

- **syntax at line 33**

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

- **syntax at line 34**

```k
  syntax Entries  ::= List{Entry, ","}
```

- **syntax at line 35**

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

- **syntax at line 36**

```k
  syntax CompFors ::= List{CompFor, ""}
```

- **syntax at line 37**

```k
  syntax Exprs    ::= List{Expr, ","}
```

- **syntax at line 38**

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

- **syntax at line 39**

```k
  syntax Bound    ::= Expr | "NoBound"
```

- **syntax at line 41** — tags: strict

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

- **syntax at line 56**

```k
  syntax Stmts      ::= List{Stmt, ""}
```

- **syntax at line 57**

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

- **syntax at line 58**

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

- **syntax at line 59**

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

- **syntax at line 60**

```k
  syntax ParamNames ::= List{String, ","}
```

- **syntax at line 61**

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### `reference-semantics/semantics/tuple.k`

- **rule at line 10**

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

- **rule at line 11**

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

- **syntax at line 14**

```k
  syntax ApplyK ::= "toTuple"
```

- **rule at line 15**

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

- **rule at line 16**

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

- **rule at line 18**

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

- **rule at line 20**

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

- **rule at line 21**

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

- **rule at line 23**

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

- **syntax at line 24** — tags: function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

- **rule at line 25**

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

- **rule at line 26**

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

- **rule at line 28**

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

- **syntax at line 31**

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

- **rule at line 32**

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

- **rule at line 35** — tags: priority

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

- **rule at line 42**

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

- **rule at line 43**

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

- **rule at line 44** — tags: priority

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **syntax at line 49**

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

- **rule at line 50**

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

- **rule at line 51**

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

- **rule at line 52** — tags: priority

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

- **rule at line 55**

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

- **rule at line 57**

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### `verification.k`

- **rule at line 9** — tags: simplification

```k
  rule vsLen(sortVS(VS:ValSeq)) => vsLen(VS) [simplification]
```

- **syntax at line 13** — tags: function, total

```k
  syntax Bool ::= allInts(ValSeq) [function, total]
```

- **rule at line 14**

```k
  rule allInts(.ValSeq) => true
```

- **rule at line 15**

```k
  rule allInts(vCons(_:Int, VS:ValSeq)) => allInts(VS)
```

- **rule at line 16** — tags: owise

```k
  rule allInts(vCons(_:Val, _:ValSeq)) => false [owise]
```

- **syntax at line 21** — tags: function, total, symbol, no-evaluators, opaque-declaration

```k
  syntax Int ::= sortedIntAt(ValSeq, Int)
    [function, total, symbol(sortedIntAt), no-evaluators]
```

- **rule at line 23** — tags: simplification

```k
  rule valSeqAt(sortVS(VS:ValSeq), I:Int) => sortedIntAt(VS, I)
    requires allInts(VS)
     andBool I >=Int 0
     andBool I <Int vsLen(VS)
    [simplification]
```

### `spec.k`

- **claim at line 6**

```k
  claim [median-odd]:
    <k>
      #loadAll(Module(
        FuncDef("median", Params("l"),
          Assign(Name("values"), Call(Name("sorted"), Name("l")))
          Assign(
            Name("middle"),
            BinOp("//", Call(Name("len"), Name("values")), Int(2)))
          If(Compare(
            BinOp("%", Call(Name("len"), Name("values")), Int(2)),
            CmpOp("==", Int(1))),
            Return(Subscript(Name("values"), Name("middle"))),
            .Stmts)
          Return(
            BinOp(
              "/",
              BinOp(
                "+",
                Subscript(Name("values"), Name("middle")),
                Subscript(
                  Name("values"),
                  BinOp("+", Name("middle"), Int(1)))),
              Float(2.0)))
        )))
      ~> Call(Name("median"), list(VS:ValSeq))
      =>
      sortedIntAt(VS, (vsLen(VS) -Int 1) /Int 2)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?_:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
     andBool vsLen(VS) >Int 0
     andBool pyMod(vsLen(VS), 2) ==Int 1
```

- **claim at line 52**

```k
  claim [median-even]:
    <k>
      #loadAll(Module(
        FuncDef("median", Params("l"),
          Assign(Name("values"), Call(Name("sorted"), Name("l")))
          Assign(
            Name("middle"),
            BinOp("//", Call(Name("len"), Name("values")), Int(2)))
          If(Compare(
            BinOp("%", Call(Name("len"), Name("values")), Int(2)),
            CmpOp("==", Int(1))),
            Return(Subscript(Name("values"), Name("middle"))),
            .Stmts)
          Return(
            BinOp(
              "/",
              BinOp(
                "+",
                Subscript(Name("values"), Name("middle")),
                Subscript(
                  Name("values"),
                  BinOp("+", Name("middle"), Int(1)))),
              Float(2.0)))
        )))
      ~> Call(Name("median"), list(VS:ValSeq))
      =>
      intFloatDiv(
        sortedIntAt(VS, vsLen(VS) /Int 2)
        +Int sortedIntAt(VS, vsLen(VS) /Int 2 +Int 1),
        2.0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?_:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
     andBool vsLen(VS) >=Int 4
     andBool pyMod(vsLen(VS), 2) ==Int 0
```


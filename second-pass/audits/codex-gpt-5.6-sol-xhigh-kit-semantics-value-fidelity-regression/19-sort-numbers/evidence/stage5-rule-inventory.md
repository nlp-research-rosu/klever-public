# Exhaustive K source inventory

This mechanically enumerates every `configuration`, `syntax`, `rule`, `claim`, `context`, and `alias` source unit in the clean scratch inputs. Dispositions are audit classifications, not K attributes. An outside-slice disposition means only that the real submitted program cannot reach the unit on the intended domain; it is not a global soundness endorsement.

## Counts

- claim: 2
- configuration: 1
- context: 5
- equational-rule: 471
- function-declaration: 131
- opaque-symbol-declaration: 22
- ordinary-semantic-rule: 200
- priority-semantic-rule: 45
- symbol-declaration: 3
- syntax-declaration: 81

## Disposition counts

- CLAIM_MANUAL_REVIEW_PASS: 2
- CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS: 18
- OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS: 779
- PROOF_LOCAL_MANUAL_REVIEW_PASS: 31
- REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS: 109
- REACHABLE_TRUSTED_OPAQUE_PRIMITIVE: 1
- UNUSED_TRUSTED_OPAQUE_PRIMITIVE: 21

## Units

### `reference-semantics/semantics/assert.k:6`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### `reference-semantics/semantics/assert.k:8`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### `reference-semantics/semantics/assert.k:13`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

### `reference-semantics/semantics/bool.k:8`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### `reference-semantics/semantics/bool.k:10`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### `reference-semantics/semantics/bool.k:11`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### `reference-semantics/semantics/bool.k:16`

- Kind: `context` / `context`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### `reference-semantics/semantics/bool.k:17`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### `reference-semantics/semantics/bool.k:18`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### `reference-semantics/semantics/bool.k:20`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### `reference-semantics/semantics/bool.k:22`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### `reference-semantics/semantics/bool.k:24`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

### `reference-semantics/semantics/bool.k:29`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### `reference-semantics/semantics/bool.k:31`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### `reference-semantics/semantics/bool.k:35`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### `reference-semantics/semantics/bool.k:39`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### `reference-semantics/semantics/bool.k:43`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
endmodule
```

### `reference-semantics/semantics/builtins.k:17`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### `reference-semantics/semantics/builtins.k:20`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= seqLen(Val) [function]
```

### `reference-semantics/semantics/builtins.k:21`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### `reference-semantics/semantics/builtins.k:22`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### `reference-semantics/semantics/builtins.k:23`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### `reference-semantics/semantics/builtins.k:24`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### `reference-semantics/semantics/builtins.k:25`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### `reference-semantics/semantics/builtins.k:26`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### `reference-semantics/semantics/builtins.k:32`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### `reference-semantics/semantics/builtins.k:33`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### `reference-semantics/semantics/builtins.k:34`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### `reference-semantics/semantics/builtins.k:35`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### `reference-semantics/semantics/builtins.k:36`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:37`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### `reference-semantics/semantics/builtins.k:38`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### `reference-semantics/semantics/builtins.k:41`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### `reference-semantics/semantics/builtins.k:44`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### `reference-semantics/semantics/builtins.k:47`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### `reference-semantics/semantics/builtins.k:48`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### `reference-semantics/semantics/builtins.k:49`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### `reference-semantics/semantics/builtins.k:50`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### `reference-semantics/semantics/builtins.k:54`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= intOf(Val) [function]
```

### `reference-semantics/semantics/builtins.k:55`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intOf(I:Int)  => I
```

### `reference-semantics/semantics/builtins.k:56`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### `reference-semantics/semantics/builtins.k:59`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### `reference-semantics/semantics/builtins.k:60`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### `reference-semantics/semantics/builtins.k:61`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### `reference-semantics/semantics/builtins.k:62`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### `reference-semantics/semantics/builtins.k:64`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### `reference-semantics/semantics/builtins.k:67`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### `reference-semantics/semantics/builtins.k:68`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### `reference-semantics/semantics/builtins.k:69`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### `reference-semantics/semantics/builtins.k:70`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### `reference-semantics/semantics/builtins.k:72`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

### `reference-semantics/semantics/builtins.k:76`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### `reference-semantics/semantics/builtins.k:77`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### `reference-semantics/semantics/builtins.k:78`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### `reference-semantics/semantics/builtins.k:80`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### `reference-semantics/semantics/builtins.k:81`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### `reference-semantics/semantics/builtins.k:82`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### `reference-semantics/semantics/builtins.k:86`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### `reference-semantics/semantics/builtins.k:87`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### `reference-semantics/semantics/builtins.k:88`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### `reference-semantics/semantics/builtins.k:90`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### `reference-semantics/semantics/builtins.k:91`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### `reference-semantics/semantics/builtins.k:92`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### `reference-semantics/semantics/builtins.k:97`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### `reference-semantics/semantics/builtins.k:98`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### `reference-semantics/semantics/builtins.k:99`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule maxVals(M:Int, .Vals)           => M
```

### `reference-semantics/semantics/builtins.k:100`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### `reference-semantics/semantics/builtins.k:102`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### `reference-semantics/semantics/builtins.k:103`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### `reference-semantics/semantics/builtins.k:104`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule minVals(M:Int, .Vals)           => M
```

### `reference-semantics/semantics/builtins.k:105`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### `reference-semantics/semantics/builtins.k:108`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

### `reference-semantics/semantics/builtins.k:111`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### `reference-semantics/semantics/builtins.k:114`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### `reference-semantics/semantics/builtins.k:115`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### `reference-semantics/semantics/builtins.k:116`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### `reference-semantics/semantics/builtins.k:117`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:118`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### `reference-semantics/semantics/builtins.k:119`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

### `reference-semantics/semantics/builtins.k:124`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### `reference-semantics/semantics/builtins.k:126`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### `reference-semantics/semantics/builtins.k:127`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### `reference-semantics/semantics/builtins.k:128`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### `reference-semantics/semantics/builtins.k:132`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### `reference-semantics/semantics/builtins.k:134`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:135`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### `reference-semantics/semantics/builtins.k:136`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### `reference-semantics/semantics/builtins.k:137`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### `reference-semantics/semantics/builtins.k:140`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### `reference-semantics/semantics/builtins.k:143`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### `reference-semantics/semantics/builtins.k:144`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

### `reference-semantics/semantics/builtins.k:148`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### `reference-semantics/semantics/builtins.k:149`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### `reference-semantics/semantics/builtins.k:152`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

### `reference-semantics/semantics/builtins.k:156`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### `reference-semantics/semantics/builtins.k:158`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### `reference-semantics/semantics/builtins.k:159`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### `reference-semantics/semantics/builtins.k:160`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### `reference-semantics/semantics/builtins.k:163`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### `reference-semantics/semantics/builtins.k:164`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### `reference-semantics/semantics/builtins.k:167`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### `reference-semantics/semantics/builtins.k:169`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### `reference-semantics/semantics/builtins.k:170`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### `reference-semantics/semantics/builtins.k:171`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### `reference-semantics/semantics/builtins.k:173`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### `reference-semantics/semantics/builtins.k:174`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### `reference-semantics/semantics/builtins.k:177`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### `reference-semantics/semantics/builtins.k:178`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### `reference-semantics/semantics/builtins.k:179`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

### `reference-semantics/semantics/builtins.k:187`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### `reference-semantics/semantics/builtins.k:188`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### `reference-semantics/semantics/builtins.k:189`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### `reference-semantics/semantics/builtins.k:192`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### `reference-semantics/semantics/builtins.k:194`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### `reference-semantics/semantics/builtins.k:195`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### `reference-semantics/semantics/builtins.k:196`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:197`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### `reference-semantics/semantics/builtins.k:198`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### `reference-semantics/semantics/builtins.k:199`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:200`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### `reference-semantics/semantics/builtins.k:201`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### `reference-semantics/semantics/builtins.k:203`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:204`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### `reference-semantics/semantics/builtins.k:205`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### `reference-semantics/semantics/builtins.k:206`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### `reference-semantics/semantics/builtins.k:207`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### `reference-semantics/semantics/builtins.k:208`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### `reference-semantics/semantics/builtins.k:209`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### `reference-semantics/semantics/builtins.k:210`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### `reference-semantics/semantics/builtins.k:211`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### `reference-semantics/semantics/builtins.k:212`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### `reference-semantics/semantics/builtins.k:214`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:216`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### `reference-semantics/semantics/builtins.k:217`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### `reference-semantics/semantics/builtins.k:218`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### `reference-semantics/semantics/builtins.k:219`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### `reference-semantics/semantics/builtins.k:221`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### `reference-semantics/semantics/builtins.k:223`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### `reference-semantics/semantics/builtins.k:225`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### `reference-semantics/semantics/builtins.k:226`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### `reference-semantics/semantics/builtins.k:227`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### `reference-semantics/semantics/builtins.k:228`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### `reference-semantics/semantics/builtins.k:230`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### `reference-semantics/semantics/builtins.k:231`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### `reference-semantics/semantics/builtins.k:232`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### `reference-semantics/semantics/builtins.k:233`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### `reference-semantics/semantics/builtins.k:234`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### `reference-semantics/semantics/builtins.k:235`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### `reference-semantics/semantics/builtins.k:236`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### `reference-semantics/semantics/builtins.k:238`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:239`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### `reference-semantics/semantics/builtins.k:240`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### `reference-semantics/semantics/builtins.k:241`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### `reference-semantics/semantics/builtins.k:243`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### `reference-semantics/semantics/builtins.k:244`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### `reference-semantics/semantics/builtins.k:245`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### `reference-semantics/semantics/builtins.k:246`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### `reference-semantics/semantics/builtins.k:247`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### `reference-semantics/semantics/builtins.k:248`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### `reference-semantics/semantics/builtins.k:250`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### `reference-semantics/semantics/builtins.k:251`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### `reference-semantics/semantics/builtins.k:252`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### `reference-semantics/semantics/builtins.k:253`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### `reference-semantics/semantics/builtins.k:254`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### `reference-semantics/semantics/builtins.k:255`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/builtins.k:256`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### `reference-semantics/semantics/builtins.k:257`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### `reference-semantics/semantics/builtins.k:260`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### `reference-semantics/semantics/builtins.k:263`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### `reference-semantics/semantics/builtins.k:265`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### `reference-semantics/semantics/builtins.k:266`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### `reference-semantics/semantics/builtins.k:267`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### `reference-semantics/semantics/builtins.k:268`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### `reference-semantics/semantics/builtins.k:269`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### `reference-semantics/semantics/builtins.k:270`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### `reference-semantics/semantics/builtins.k:271`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### `reference-semantics/semantics/builtins.k:272`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### `reference-semantics/semantics/builtins.k:273`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### `reference-semantics/semantics/builtins.k:274`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### `reference-semantics/semantics/builtins.k:279`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= "#md5"
```

### `reference-semantics/semantics/builtins.k:280`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### `reference-semantics/semantics/builtins.k:282`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### `reference-semantics/semantics/builtins.k:283`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= md5Obj(IntSeq)
```

### `reference-semantics/semantics/builtins.k:284`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### `reference-semantics/semantics/builtins.k:285`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### `reference-semantics/semantics/builtins.k:291`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### `reference-semantics/semantics/builtins.k:292`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### `reference-semantics/semantics/builtins.k:293`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### `reference-semantics/semantics/builtins.k:294`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isIntV(_:Int)         => true
```

### `reference-semantics/semantics/builtins.k:295`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isIntV(_:Val)         => false [owise]
```

### `reference-semantics/semantics/builtins.k:296`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isStrV(str(_:IntSeq)) => true
```

### `reference-semantics/semantics/builtins.k:297`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isStrV(_:Val)         => false [owise]
endmodule
```

### `reference-semantics/semantics/call.k:16`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### `reference-semantics/semantics/call.k:19`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= #callee(Exprs)
```

### `reference-semantics/semantics/call.k:20`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: `owise`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### `reference-semantics/semantics/call.k:21`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### `reference-semantics/semantics/call.k:24`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### `reference-semantics/semantics/call.k:26`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### `reference-semantics/semantics/call.k:27`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### `reference-semantics/semantics/call.k:28`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### `reference-semantics/semantics/call.k:29`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### `reference-semantics/semantics/call.k:30`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### `reference-semantics/semantics/call.k:31`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: `owise`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### `reference-semantics/semantics/call.k:32`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### `reference-semantics/semantics/call.k:38`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/call.k:42`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### `reference-semantics/semantics/call.k:47`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/call.k:52`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### `reference-semantics/semantics/call.k:53`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### `reference-semantics/semantics/call.k:56`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

### `reference-semantics/semantics/call.k:63`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### `reference-semantics/semantics/call.k:69`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### `reference-semantics/semantics/call.k:80`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### `reference-semantics/semantics/call.k:87`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### `reference-semantics/semantics/call.k:88`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### `reference-semantics/semantics/call.k:89`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
endmodule
```

### `reference-semantics/semantics/comprehension.k:11`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### `reference-semantics/semantics/comprehension.k:12`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### `reference-semantics/semantics/comprehension.k:14`

- Kind: `syntax` / `syntax-declaration`
- Attributes: `macro`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### `reference-semantics/semantics/comprehension.k:15`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### `reference-semantics/semantics/comprehension.k:18`

- Kind: `syntax` / `syntax-declaration`
- Attributes: `macro`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### `reference-semantics/semantics/comprehension.k:19`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### `reference-semantics/semantics/comprehension.k:21`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### `reference-semantics/semantics/comprehension.k:24`

- Kind: `syntax` / `syntax-declaration`
- Attributes: `macro`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### `reference-semantics/semantics/comprehension.k:25`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### `reference-semantics/semantics/comprehension.k:26`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
endmodule
```

### `reference-semantics/semantics/concrete.k:13`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### `reference-semantics/semantics/concrete.k:16`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### `reference-semantics/semantics/concrete.k:25`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= kvP(Val, Val)
```

### `reference-semantics/semantics/concrete.k:26`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### `reference-semantics/semantics/concrete.k:28`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### `reference-semantics/semantics/concrete.k:31`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### `reference-semantics/semantics/concrete.k:34`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### `reference-semantics/semantics/concrete.k:36`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### `reference-semantics/semantics/concrete.k:38`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### `reference-semantics/semantics/concrete.k:42`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### `reference-semantics/semantics/concrete.k:43`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### `reference-semantics/semantics/concrete.k:44`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### `reference-semantics/semantics/concrete.k:47`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### `reference-semantics/semantics/concrete.k:51`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### `reference-semantics/semantics/concrete.k:52`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### `reference-semantics/semantics/concrete.k:53`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### `reference-semantics/semantics/concrete.k:54`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### `reference-semantics/semantics/concrete.k:56`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### `reference-semantics/semantics/concrete.k:57`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### `reference-semantics/semantics/concrete.k:58`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### `reference-semantics/semantics/concrete.k:59`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS`

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
endmodule
```

### `reference-semantics/semantics/controls.k:9`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### `reference-semantics/semantics/controls.k:12`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### `reference-semantics/semantics/controls.k:20`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

### `reference-semantics/semantics/controls.k:27`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

### `reference-semantics/semantics/controls.k:35`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### `reference-semantics/semantics/controls.k:36`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### `reference-semantics/semantics/controls.k:37`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### `reference-semantics/semantics/controls.k:38`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### `reference-semantics/semantics/controls.k:39`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### `reference-semantics/semantics/controls.k:43`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### `reference-semantics/semantics/controls.k:48`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### `reference-semantics/semantics/controls.k:51`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### `reference-semantics/semantics/controls.k:52`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### `reference-semantics/semantics/controls.k:53`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### `reference-semantics/semantics/controls.k:54`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### `reference-semantics/semantics/controls.k:57`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### `reference-semantics/semantics/controls.k:59`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

### `reference-semantics/semantics/controls.k:65`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### `reference-semantics/semantics/controls.k:69`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### `reference-semantics/semantics/controls.k:71`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### `reference-semantics/semantics/controls.k:72`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### `reference-semantics/semantics/controls.k:73`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### `reference-semantics/semantics/controls.k:77`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### `reference-semantics/semantics/controls.k:78`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### `reference-semantics/semantics/controls.k:79`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### `reference-semantics/semantics/controls.k:81`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

### `reference-semantics/semantics/controls.k:85`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### `reference-semantics/semantics/controls.k:86`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Continue => #cont ... </k>
```

### `reference-semantics/semantics/controls.k:87`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Break => #brk ... </k>
```

### `reference-semantics/semantics/controls.k:88`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### `reference-semantics/semantics/controls.k:89`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### `reference-semantics/semantics/controls.k:90`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### `reference-semantics/semantics/controls.k:91`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### `reference-semantics/semantics/controls.k:95`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/controls.k:98`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/controls.k:101`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/controls.k:106`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

### `reference-semantics/semantics/core.k:13`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### `reference-semantics/semantics/core.k:14`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### `reference-semantics/semantics/core.k:15`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Str    ::= str(IntSeq)
```

### `reference-semantics/semantics/core.k:18`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### `reference-semantics/semantics/core.k:25`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

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

### `reference-semantics/semantics/core.k:36`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Parent   ::= "root" | parent(Int)
```

### `reference-semantics/semantics/core.k:37`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Scope    ::= scope(Map, Parent)
```

### `reference-semantics/semantics/core.k:38`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KResult  ::= Val
```

### `reference-semantics/semantics/core.k:39`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### `reference-semantics/semantics/core.k:40`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Vals     ::= List{Val, ","}
```

### `reference-semantics/semantics/core.k:41`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### `reference-semantics/semantics/core.k:42`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### `reference-semantics/semantics/core.k:49`

- Kind: `configuration` / `configuration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

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

### `reference-semantics/semantics/core.k:68`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### `reference-semantics/semantics/core.k:69`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isRefV(ref(_:Int)) => true
```

### `reference-semantics/semantics/core.k:70`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isRefV(_:Val)      => false [owise]
```

### `reference-semantics/semantics/core.k:75`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax HeapVal ::= cellV(Val)
```

### `reference-semantics/semantics/core.k:76`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### `reference-semantics/semantics/core.k:77`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### `reference-semantics/semantics/core.k:78`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isCellRef(_:Val)          => false [owise]
```

### `reference-semantics/semantics/core.k:85`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

### `reference-semantics/semantics/core.k:95`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= kwV(String, Val)
```

### `reference-semantics/semantics/core.k:96`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= #kwTag(String)
```

### `reference-semantics/semantics/core.k:97`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### `reference-semantics/semantics/core.k:98`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### `reference-semantics/semantics/core.k:100`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### `reference-semantics/semantics/core.k:101`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### `reference-semantics/semantics/core.k:102`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isKwV(_:Val)                => false [owise]
```

### `reference-semantics/semantics/core.k:106`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= cellsMark(ParamNames)
```

### `reference-semantics/semantics/core.k:107`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### `reference-semantics/semantics/core.k:108`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### `reference-semantics/semantics/core.k:109`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### `reference-semantics/semantics/core.k:110`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule pnMember(_:String, .ParamNames) => false
```

### `reference-semantics/semantics/core.k:111`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### `reference-semantics/semantics/core.k:113`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #cellW(Val, Val)
```

### `reference-semantics/semantics/core.k:114`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### `reference-semantics/semantics/core.k:117`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= #alloc(Val)
```

### `reference-semantics/semantics/core.k:118`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### `reference-semantics/semantics/core.k:124`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= #loadAll(Module)
```

### `reference-semantics/semantics/core.k:125`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### `reference-semantics/semantics/core.k:126`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### `reference-semantics/semantics/core.k:127`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> .Stmts => .K ... </k>
```

### `reference-semantics/semantics/core.k:130`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= #look(String, Int)
```

### `reference-semantics/semantics/core.k:131`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### `reference-semantics/semantics/core.k:132`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

### `reference-semantics/semantics/core.k:145`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### `reference-semantics/semantics/core.k:152`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

### `reference-semantics/semantics/core.k:157`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### `reference-semantics/semantics/core.k:158`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

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

### `reference-semantics/semantics/core.k:185`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ApplyK ::= toCall(Val)
```

### `reference-semantics/semantics/core.k:186`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### `reference-semantics/semantics/core.k:189`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### `reference-semantics/semantics/core.k:190`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### `reference-semantics/semantics/core.k:191`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### `reference-semantics/semantics/core.k:194`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### `reference-semantics/semantics/core.k:195`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### `reference-semantics/semantics/core.k:196`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> NoneVal      => noneV ... </k>
```

### `reference-semantics/semantics/core.k:199`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax Bool ::= truthy(Val) [function]
```

### `reference-semantics/semantics/core.k:200`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule truthy(B:Bool)          => B
```

### `reference-semantics/semantics/core.k:201`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule truthy(noneV)           => false
```

### `reference-semantics/semantics/core.k:202`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### `reference-semantics/semantics/core.k:203`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### `reference-semantics/semantics/core.k:204`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### `reference-semantics/semantics/core.k:205`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### `reference-semantics/semantics/core.k:208`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### `reference-semantics/semantics/core.k:209`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### `reference-semantics/semantics/core.k:210`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### `reference-semantics/semantics/core.k:213`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### `reference-semantics/semantics/core.k:214`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### `reference-semantics/semantics/core.k:215`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### `reference-semantics/semantics/core.k:217`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### `reference-semantics/semantics/core.k:218`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### `reference-semantics/semantics/core.k:219`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### `reference-semantics/semantics/core.k:223`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### `reference-semantics/semantics/core.k:224`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule vsLen(.ValSeq)                => 0
```

### `reference-semantics/semantics/core.k:225`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### `reference-semantics/semantics/core.k:227`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### `reference-semantics/semantics/core.k:228`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isLen(.IntSeq)                => 0
```

### `reference-semantics/semantics/core.k:229`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### `reference-semantics/semantics/core.k:233`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### `reference-semantics/semantics/core.k:234`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### `reference-semantics/semantics/core.k:235`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### `reference-semantics/semantics/core.k:236`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### `reference-semantics/semantics/core.k:238`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
endmodule
```

### `reference-semantics/semantics/dict.k:20`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### `reference-semantics/semantics/dict.k:23`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### `reference-semantics/semantics/dict.k:26`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### `reference-semantics/semantics/dict.k:27`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### `reference-semantics/semantics/dict.k:28`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### `reference-semantics/semantics/dict.k:30`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### `reference-semantics/semantics/dict.k:32`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### `reference-semantics/semantics/dict.k:37`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### `reference-semantics/semantics/dict.k:38`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### `reference-semantics/semantics/dict.k:39`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### `reference-semantics/semantics/dict.k:40`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### `reference-semantics/semantics/dict.k:43`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### `reference-semantics/semantics/dict.k:44`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### `reference-semantics/semantics/dict.k:45`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### `reference-semantics/semantics/dict.k:49`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### `reference-semantics/semantics/dict.k:50`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### `reference-semantics/semantics/dict.k:52`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### `reference-semantics/semantics/dict.k:54`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### `reference-semantics/semantics/dict.k:58`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### `reference-semantics/semantics/dict.k:63`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### `reference-semantics/semantics/dict.k:64`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### `reference-semantics/semantics/dict.k:65`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### `reference-semantics/semantics/dict.k:70`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### `reference-semantics/semantics/dict.k:71`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### `reference-semantics/semantics/dict.k:76`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #dsetK(String, Val)
```

### `reference-semantics/semantics/dict.k:77`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### `reference-semantics/semantics/dict.k:78`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### `reference-semantics/semantics/dict.k:82`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### `reference-semantics/semantics/dict.k:86`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### `reference-semantics/semantics/dict.k:87`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### `reference-semantics/semantics/dict.k:90`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### `reference-semantics/semantics/dict.k:91`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### `reference-semantics/semantics/dict.k:92`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### `reference-semantics/semantics/dict.k:95`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### `reference-semantics/semantics/dict.k:97`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### `reference-semantics/semantics/dict.k:98`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### `reference-semantics/semantics/dict.k:99`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### `reference-semantics/semantics/dict.k:101`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### `reference-semantics/semantics/dict.k:102`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### `reference-semantics/semantics/dict.k:103`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
endmodule
```

### `reference-semantics/semantics/float.k:20`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= Float
```

### `reference-semantics/semantics/float.k:21`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Float(F:Float) => F ... </k>
```

### `reference-semantics/semantics/float.k:24`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### `reference-semantics/semantics/float.k:25`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### `reference-semantics/semantics/float.k:27`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### `reference-semantics/semantics/float.k:30`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### `reference-semantics/semantics/float.k:31`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### `reference-semantics/semantics/float.k:32`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### `reference-semantics/semantics/float.k:37`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### `reference-semantics/semantics/float.k:38`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### `reference-semantics/semantics/float.k:39`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### `reference-semantics/semantics/float.k:43`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### `reference-semantics/semantics/float.k:44`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### `reference-semantics/semantics/float.k:50`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### `reference-semantics/semantics/float.k:51`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:52`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### `reference-semantics/semantics/float.k:54`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### `reference-semantics/semantics/float.k:55`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### `reference-semantics/semantics/float.k:56`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### `reference-semantics/semantics/float.k:61`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Import(_:String) => .K ... </k>
```

### `reference-semantics/semantics/float.k:65`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= "#mathCeil"
```

### `reference-semantics/semantics/float.k:66`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### `reference-semantics/semantics/float.k:67`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### `reference-semantics/semantics/float.k:70`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= "#mathFloor"
```

### `reference-semantics/semantics/float.k:71`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### `reference-semantics/semantics/float.k:72`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### `reference-semantics/semantics/float.k:73`

- Kind: `syntax` / `symbol-declaration`
- Attributes: `function`, `total`, `symbol`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### `reference-semantics/semantics/float.k:74`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### `reference-semantics/semantics/float.k:75`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### `reference-semantics/semantics/float.k:78`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### `reference-semantics/semantics/float.k:79`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### `reference-semantics/semantics/float.k:82`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### `reference-semantics/semantics/float.k:83`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### `reference-semantics/semantics/float.k:84`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### `reference-semantics/semantics/float.k:85`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### `reference-semantics/semantics/float.k:86`

- Kind: `syntax` / `symbol-declaration`
- Attributes: `function`, `total`, `symbol`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### `reference-semantics/semantics/float.k:87`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule toF(F:Float) => F        [concrete]
```

### `reference-semantics/semantics/float.k:88`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### `reference-semantics/semantics/float.k:93`

- Kind: `syntax` / `symbol-declaration`
- Attributes: `function`, `total`, `symbol`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### `reference-semantics/semantics/float.k:94`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### `reference-semantics/semantics/float.k:95`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### `reference-semantics/semantics/float.k:99`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### `reference-semantics/semantics/float.k:103`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### `reference-semantics/semantics/float.k:104`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:105`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### `reference-semantics/semantics/float.k:107`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### `reference-semantics/semantics/float.k:108`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:109`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### `reference-semantics/semantics/float.k:111`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### `reference-semantics/semantics/float.k:112`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:113`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### `reference-semantics/semantics/float.k:115`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### `reference-semantics/semantics/float.k:116`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:117`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### `reference-semantics/semantics/float.k:119`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### `reference-semantics/semantics/float.k:120`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:121`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### `reference-semantics/semantics/float.k:125`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### `reference-semantics/semantics/float.k:126`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:127`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### `reference-semantics/semantics/float.k:128`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### `reference-semantics/semantics/float.k:129`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### `reference-semantics/semantics/float.k:132`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:133`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:134`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:135`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:136`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:137`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:138`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:139`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:142`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### `reference-semantics/semantics/float.k:143`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### `reference-semantics/semantics/float.k:144`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:145`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:146`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:147`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:148`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### `reference-semantics/semantics/float.k:149`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### `reference-semantics/semantics/float.k:150`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:151`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:154`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### `reference-semantics/semantics/float.k:155`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### `reference-semantics/semantics/float.k:160`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### `reference-semantics/semantics/float.k:161`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### `reference-semantics/semantics/float.k:162`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### `reference-semantics/semantics/float.k:165`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### `reference-semantics/semantics/float.k:166`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### `reference-semantics/semantics/float.k:167`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### `reference-semantics/semantics/float.k:168`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### `reference-semantics/semantics/float.k:169`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### `reference-semantics/semantics/float.k:170`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### `reference-semantics/semantics/float.k:171`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### `reference-semantics/semantics/float.k:173`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### `reference-semantics/semantics/float.k:174`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracPart(.IntSeq) => 0
```

### `reference-semantics/semantics/float.k:175`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### `reference-semantics/semantics/float.k:176`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### `reference-semantics/semantics/float.k:177`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### `reference-semantics/semantics/float.k:178`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### `reference-semantics/semantics/float.k:179`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### `reference-semantics/semantics/float.k:180`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracScale(.IntSeq) => 1
```

### `reference-semantics/semantics/float.k:181`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### `reference-semantics/semantics/float.k:182`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### `reference-semantics/semantics/float.k:183`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### `reference-semantics/semantics/float.k:184`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### `reference-semantics/semantics/float.k:185`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### `reference-semantics/semantics/float.k:186`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### `reference-semantics/semantics/float.k:187`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### `reference-semantics/semantics/float.k:190`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### `reference-semantics/semantics/float.k:191`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### `reference-semantics/semantics/float.k:192`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### `reference-semantics/semantics/float.k:195`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### `reference-semantics/semantics/float.k:196`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### `reference-semantics/semantics/float.k:197`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:198`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:199`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:200`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:201`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:202`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:203`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### `reference-semantics/semantics/float.k:204`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### `reference-semantics/semantics/float.k:205`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### `reference-semantics/semantics/float.k:206`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### `reference-semantics/semantics/float.k:209`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### `reference-semantics/semantics/float.k:210`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### `reference-semantics/semantics/float.k:211`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### `reference-semantics/semantics/float.k:213`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### `reference-semantics/semantics/float.k:214`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### `reference-semantics/semantics/float.k:217`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### `reference-semantics/semantics/float.k:218`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### `reference-semantics/semantics/float.k:223`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### `reference-semantics/semantics/float.k:224`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### `reference-semantics/semantics/float.k:227`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### `reference-semantics/semantics/float.k:228`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### `reference-semantics/semantics/float.k:230`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### `reference-semantics/semantics/float.k:231`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### `reference-semantics/semantics/float.k:232`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= "#mathSqrt"
```

### `reference-semantics/semantics/float.k:233`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### `reference-semantics/semantics/float.k:234`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### `reference-semantics/semantics/float.k:235`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### `reference-semantics/semantics/float.k:243`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### `reference-semantics/semantics/float.k:244`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### `reference-semantics/semantics/float.k:245`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### `reference-semantics/semantics/float.k:246`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### `reference-semantics/semantics/float.k:247`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### `reference-semantics/semantics/float.k:250`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### `reference-semantics/semantics/float.k:251`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### `reference-semantics/semantics/float.k:252`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### `reference-semantics/semantics/float.k:253`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### `reference-semantics/semantics/float.k:254`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### `reference-semantics/semantics/float.k:261`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### `reference-semantics/semantics/float.k:262`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### `reference-semantics/semantics/float.k:265`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### `reference-semantics/semantics/float.k:266`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### `reference-semantics/semantics/float.k:267`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### `reference-semantics/semantics/float.k:270`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
endmodule
```

### `reference-semantics/semantics/functions.k:8`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### `reference-semantics/semantics/functions.k:14`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### `reference-semantics/semantics/functions.k:18`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### `reference-semantics/semantics/functions.k:19`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### `reference-semantics/semantics/functions.k:27`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### `reference-semantics/semantics/functions.k:31`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### `reference-semantics/semantics/functions.k:33`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### `reference-semantics/semantics/functions.k:36`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### `reference-semantics/semantics/functions.k:42`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### `reference-semantics/semantics/functions.k:47`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### `reference-semantics/semantics/functions.k:50`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### `reference-semantics/semantics/functions.k:53`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### `reference-semantics/semantics/functions.k:59`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### `reference-semantics/semantics/functions.k:63`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### `reference-semantics/semantics/functions.k:64`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### `reference-semantics/semantics/functions.k:68`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

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

### `reference-semantics/semantics/functions.k:78`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### `reference-semantics/semantics/functions.k:80`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### `reference-semantics/semantics/functions.k:85`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
endmodule
```

### `reference-semantics/semantics/int.k:7`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### `reference-semantics/semantics/int.k:9`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### `reference-semantics/semantics/int.k:11`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### `reference-semantics/semantics/int.k:12`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### `reference-semantics/semantics/int.k:13`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### `reference-semantics/semantics/int.k:14`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### `reference-semantics/semantics/int.k:15`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### `reference-semantics/semantics/int.k:16`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### `reference-semantics/semantics/int.k:17`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### `reference-semantics/semantics/int.k:19`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### `reference-semantics/semantics/int.k:20`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### `reference-semantics/semantics/int.k:22`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### `reference-semantics/semantics/int.k:23`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### `reference-semantics/semantics/int.k:24`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### `reference-semantics/semantics/int.k:25`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### `reference-semantics/semantics/int.k:26`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### `reference-semantics/semantics/int.k:27`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
endmodule
```

### `reference-semantics/semantics/iter.k:8`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
endmodule
```

### `reference-semantics/semantics/list.k:9`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### `reference-semantics/semantics/list.k:10`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### `reference-semantics/semantics/list.k:13`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ApplyK ::= "toList"
```

### `reference-semantics/semantics/list.k:14`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### `reference-semantics/semantics/list.k:15`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### `reference-semantics/semantics/list.k:18`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### `reference-semantics/semantics/list.k:19`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### `reference-semantics/semantics/list.k:20`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### `reference-semantics/semantics/list.k:24`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### `reference-semantics/semantics/list.k:27`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### `reference-semantics/semantics/list.k:28`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### `reference-semantics/semantics/list.k:33`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### `reference-semantics/semantics/list.k:34`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule hasRefVS(.ValSeq)                => false
```

### `reference-semantics/semantics/list.k:35`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### `reference-semantics/semantics/list.k:37`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### `reference-semantics/semantics/list.k:39`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### `reference-semantics/semantics/list.k:40`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### `reference-semantics/semantics/list.k:41`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### `reference-semantics/semantics/list.k:42`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### `reference-semantics/semantics/list.k:45`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### `reference-semantics/semantics/list.k:47`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### `reference-semantics/semantics/list.k:49`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### `reference-semantics/semantics/list.k:50`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### `reference-semantics/semantics/list.k:53`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/list.k:58`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### `reference-semantics/semantics/list.k:59`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### `reference-semantics/semantics/list.k:60`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### `reference-semantics/semantics/list.k:61`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### `reference-semantics/semantics/list.k:62`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### `reference-semantics/semantics/list.k:63`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### `reference-semantics/semantics/list.k:65`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### `reference-semantics/semantics/list.k:67`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
endmodule
```

### `reference-semantics/semantics/methods.k:10`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### `reference-semantics/semantics/methods.k:13`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### `reference-semantics/semantics/methods.k:14`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### `reference-semantics/semantics/methods.k:15`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### `reference-semantics/semantics/methods.k:16`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### `reference-semantics/semantics/methods.k:19`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### `reference-semantics/semantics/methods.k:20`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### `reference-semantics/semantics/methods.k:21`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### `reference-semantics/semantics/methods.k:26`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### `reference-semantics/semantics/methods.k:27`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:28`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### `reference-semantics/semantics/methods.k:29`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### `reference-semantics/semantics/methods.k:30`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### `reference-semantics/semantics/methods.k:34`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### `reference-semantics/semantics/methods.k:35`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### `reference-semantics/semantics/methods.k:36`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### `reference-semantics/semantics/methods.k:37`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### `reference-semantics/semantics/methods.k:39`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### `reference-semantics/semantics/methods.k:41`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### `reference-semantics/semantics/methods.k:42`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### `reference-semantics/semantics/methods.k:43`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### `reference-semantics/semantics/methods.k:44`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### `reference-semantics/semantics/methods.k:47`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### `reference-semantics/semantics/methods.k:48`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:49`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### `reference-semantics/semantics/methods.k:50`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### `reference-semantics/semantics/methods.k:51`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### `reference-semantics/semantics/methods.k:52`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:53`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### `reference-semantics/semantics/methods.k:54`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### `reference-semantics/semantics/methods.k:55`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### `reference-semantics/semantics/methods.k:58`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### `reference-semantics/semantics/methods.k:61`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### `reference-semantics/semantics/methods.k:64`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### `reference-semantics/semantics/methods.k:65`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### `reference-semantics/semantics/methods.k:66`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### `reference-semantics/semantics/methods.k:67`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### `reference-semantics/semantics/methods.k:68`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### `reference-semantics/semantics/methods.k:72`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### `reference-semantics/semantics/methods.k:75`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### `reference-semantics/semantics/methods.k:76`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### `reference-semantics/semantics/methods.k:77`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### `reference-semantics/semantics/methods.k:79`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

### `reference-semantics/semantics/methods.k:82`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### `reference-semantics/semantics/methods.k:83`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### `reference-semantics/semantics/methods.k:84`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### `reference-semantics/semantics/methods.k:85`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:86`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### `reference-semantics/semantics/methods.k:89`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### `reference-semantics/semantics/methods.k:94`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### `reference-semantics/semantics/methods.k:97`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### `reference-semantics/semantics/methods.k:98`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### `reference-semantics/semantics/methods.k:99`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### `reference-semantics/semantics/methods.k:101`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### `reference-semantics/semantics/methods.k:104`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### `reference-semantics/semantics/methods.k:106`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### `reference-semantics/semantics/methods.k:107`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### `reference-semantics/semantics/methods.k:108`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### `reference-semantics/semantics/methods.k:109`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### `reference-semantics/semantics/methods.k:112`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:113`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### `reference-semantics/semantics/methods.k:115`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:116`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### `reference-semantics/semantics/methods.k:118`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:119`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### `reference-semantics/semantics/methods.k:121`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:122`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### `reference-semantics/semantics/methods.k:124`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:125`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule hasUpper(.IntSeq) => false
```

### `reference-semantics/semantics/methods.k:126`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### `reference-semantics/semantics/methods.k:128`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:129`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule hasLower(.IntSeq) => false
```

### `reference-semantics/semantics/methods.k:130`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### `reference-semantics/semantics/methods.k:132`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:133`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule allAlpha(.IntSeq) => true
```

### `reference-semantics/semantics/methods.k:134`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### `reference-semantics/semantics/methods.k:136`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:137`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule allDigit(.IntSeq) => true
```

### `reference-semantics/semantics/methods.k:138`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### `reference-semantics/semantics/methods.k:140`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:142`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### `reference-semantics/semantics/methods.k:143`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule lowerC(C:Int) => C         [owise]
```

### `reference-semantics/semantics/methods.k:145`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= upperC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:146`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### `reference-semantics/semantics/methods.k:147`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule upperC(C:Int) => C         [owise]
```

### `reference-semantics/semantics/methods.k:149`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= swapC(Int) [function, total]
```

### `reference-semantics/semantics/methods.k:150`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### `reference-semantics/semantics/methods.k:151`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### `reference-semantics/semantics/methods.k:152`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule swapC(C:Int) => C         [owise]
```

### `reference-semantics/semantics/methods.k:154`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:155`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### `reference-semantics/semantics/methods.k:156`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### `reference-semantics/semantics/methods.k:158`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:159`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### `reference-semantics/semantics/methods.k:160`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### `reference-semantics/semantics/methods.k:162`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:163`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### `reference-semantics/semantics/methods.k:164`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### `reference-semantics/semantics/methods.k:166`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/methods.k:167`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### `reference-semantics/semantics/methods.k:168`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### `reference-semantics/semantics/methods.k:169`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
endmodule
```

### `reference-semantics/semantics/operators.k:10`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### `reference-semantics/semantics/operators.k:12`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### `reference-semantics/semantics/operators.k:15`

- Kind: `context` / `context`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  context Compare(HOLE, _)
```

### `reference-semantics/semantics/operators.k:16`

- Kind: `context` / `context`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### `reference-semantics/semantics/operators.k:17`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: `owise`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### `reference-semantics/semantics/operators.k:19`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### `reference-semantics/semantics/operators.k:20`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### `reference-semantics/semantics/operators.k:25`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/operators.k:28`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

### `reference-semantics/semantics/operators.k:34`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### `reference-semantics/semantics/operators.k:38`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### `reference-semantics/semantics/operators.k:44`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

### `reference-semantics/semantics/range.k:9`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### `reference-semantics/semantics/range.k:10`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### `reference-semantics/semantics/range.k:12`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### `reference-semantics/semantics/range.k:13`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### `reference-semantics/semantics/range.k:15`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### `reference-semantics/semantics/range.k:17`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### `reference-semantics/semantics/range.k:20`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### `reference-semantics/semantics/range.k:23`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
endmodule
```

### `reference-semantics/semantics/set.k:8`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= setV(IntSeq)
```

### `reference-semantics/semantics/set.k:11`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### `reference-semantics/semantics/set.k:12`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### `reference-semantics/semantics/set.k:13`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### `reference-semantics/semantics/set.k:16`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### `reference-semantics/semantics/set.k:18`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### `reference-semantics/semantics/set.k:19`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### `reference-semantics/semantics/set.k:20`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### `reference-semantics/semantics/set.k:22`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### `reference-semantics/semantics/set.k:25`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### `reference-semantics/semantics/set.k:26`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### `reference-semantics/semantics/set.k:27`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### `reference-semantics/semantics/set.k:31`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/set.k:32`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### `reference-semantics/semantics/set.k:33`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### `reference-semantics/semantics/set.k:35`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/set.k:36`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### `reference-semantics/semantics/set.k:39`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
endmodule
```

### `reference-semantics/semantics/sort.k:18`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `UNUSED_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### `reference-semantics/semantics/sort.k:19`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### `reference-semantics/semantics/sort.k:20`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### `reference-semantics/semantics/sort.k:21`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### `reference-semantics/semantics/sort.k:22`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### `reference-semantics/semantics/sort.k:23`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### `reference-semantics/semantics/sort.k:24`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### `reference-semantics/semantics/sort.k:26`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### `reference-semantics/semantics/sort.k:27`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### `reference-semantics/semantics/sort.k:28`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### `reference-semantics/semantics/sort.k:29`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### `reference-semantics/semantics/sort.k:31`

- Kind: `rule` / `equational-rule`
- Attributes: `concrete`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### `reference-semantics/semantics/sort.k:36`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### `reference-semantics/semantics/sort.k:40`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/sort.k:49`

- Kind: `syntax` / `opaque-symbol-declaration`
- Attributes: `function`, `total`, `no-evaluators`, `symbol`
- Disposition: `REACHABLE_TRUSTED_OPAQUE_PRIMITIVE`

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### `reference-semantics/semantics/sort.k:51`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### `reference-semantics/semantics/sort.k:53`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### `reference-semantics/semantics/sort.k:54`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### `reference-semantics/semantics/sort.k:55`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### `reference-semantics/semantics/sort.k:57`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### `reference-semantics/semantics/sort.k:58`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule condRev(S:ValSeq, false) => S
```

### `reference-semantics/semantics/sort.k:59`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### `reference-semantics/semantics/sort.k:61`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### `reference-semantics/semantics/sort.k:63`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### `reference-semantics/semantics/sort.k:65`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: `total`, `concrete`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
endmodule
```

### `reference-semantics/semantics/str.k:8`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### `reference-semantics/semantics/str.k:9`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### `reference-semantics/semantics/str.k:13`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### `reference-semantics/semantics/str.k:14`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### `reference-semantics/semantics/str.k:15`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule strToCodes("") => .IntSeq
```

### `reference-semantics/semantics/str.k:16`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### `reference-semantics/semantics/str.k:20`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/str.k:21`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### `reference-semantics/semantics/str.k:22`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### `reference-semantics/semantics/str.k:24`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### `reference-semantics/semantics/str.k:25`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### `reference-semantics/semantics/str.k:26`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### `reference-semantics/semantics/str.k:29`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### `reference-semantics/semantics/str.k:30`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### `reference-semantics/semantics/str.k:32`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/str.k:33`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### `reference-semantics/semantics/str.k:34`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### `reference-semantics/semantics/str.k:35`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### `reference-semantics/semantics/str.k:37`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/str.k:38`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### `reference-semantics/semantics/str.k:39`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### `reference-semantics/semantics/str.k:40`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

### `reference-semantics/semantics/str.k:48`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### `reference-semantics/semantics/str.k:49`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### `reference-semantics/semantics/str.k:50`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### `reference-semantics/semantics/str.k:51`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### `reference-semantics/semantics/str.k:52`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### `reference-semantics/semantics/str.k:53`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### `reference-semantics/semantics/str.k:54`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### `reference-semantics/semantics/str.k:56`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### `reference-semantics/semantics/str.k:57`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### `reference-semantics/semantics/str.k:58`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### `reference-semantics/semantics/str.k:59`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
endmodule
```

### `reference-semantics/semantics/subscript.k:11`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### `reference-semantics/semantics/subscript.k:12`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### `reference-semantics/semantics/subscript.k:13`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### `reference-semantics/semantics/subscript.k:16`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### `reference-semantics/semantics/subscript.k:17`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### `reference-semantics/semantics/subscript.k:18`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### `reference-semantics/semantics/subscript.k:21`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### `reference-semantics/semantics/subscript.k:22`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### `reference-semantics/semantics/subscript.k:23`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### `reference-semantics/semantics/subscript.k:27`

- Kind: `context` / `context`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  context Subscript(HOLE, _)
```

### `reference-semantics/semantics/subscript.k:28`

- Kind: `context` / `context`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  context Subscript(_:Val, HOLE:Expr)
```

### `reference-semantics/semantics/subscript.k:31`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/subscript.k:35`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### `reference-semantics/semantics/subscript.k:37`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### `reference-semantics/semantics/subscript.k:38`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### `reference-semantics/semantics/subscript.k:39`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### `reference-semantics/semantics/subscript.k:40`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### `reference-semantics/semantics/subscript.k:44`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### `reference-semantics/semantics/subscript.k:49`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### `reference-semantics/semantics/subscript.k:50`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### `reference-semantics/semantics/subscript.k:51`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### `reference-semantics/semantics/subscript.k:52`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### `reference-semantics/semantics/subscript.k:54`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### `reference-semantics/semantics/subscript.k:55`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### `reference-semantics/semantics/subscript.k:56`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### `reference-semantics/semantics/subscript.k:58`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### `reference-semantics/semantics/subscript.k:61`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### `reference-semantics/semantics/subscript.k:63`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### `reference-semantics/semantics/subscript.k:64`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### `reference-semantics/semantics/subscript.k:66`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### `reference-semantics/semantics/subscript.k:68`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### `reference-semantics/semantics/subscript.k:72`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### `reference-semantics/semantics/subscript.k:73`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStep(noB)          => 1
```

### `reference-semantics/semantics/subscript.k:74`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStep(someB(S:Int)) => S
```

### `reference-semantics/semantics/subscript.k:76`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### `reference-semantics/semantics/subscript.k:77`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### `reference-semantics/semantics/subscript.k:79`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### `reference-semantics/semantics/subscript.k:81`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### `reference-semantics/semantics/subscript.k:83`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### `reference-semantics/semantics/subscript.k:84`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### `reference-semantics/semantics/subscript.k:86`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### `reference-semantics/semantics/subscript.k:88`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### `reference-semantics/semantics/subscript.k:90`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### `reference-semantics/semantics/subscript.k:91`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### `reference-semantics/semantics/subscript.k:93`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### `reference-semantics/semantics/subscript.k:96`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### `reference-semantics/semantics/subscript.k:97`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### `reference-semantics/semantics/subscript.k:99`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### `reference-semantics/semantics/subscript.k:102`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### `reference-semantics/semantics/subscript.k:103`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### `reference-semantics/semantics/subscript.k:105`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

### `reference-semantics/semantics/subscript.k:109`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### `reference-semantics/semantics/subscript.k:110`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### `reference-semantics/semantics/subscript.k:113`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### `reference-semantics/semantics/subscript.k:116`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### `reference-semantics/semantics/subscript.k:117`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### `reference-semantics/semantics/subscript.k:120`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
endmodule
```

### `reference-semantics/semantics/syntax.k:9`

- Kind: `syntax` / `syntax-declaration`
- Attributes: `macro`
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

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

### `reference-semantics/semantics/syntax.k:32`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### `reference-semantics/semantics/syntax.k:33`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### `reference-semantics/semantics/syntax.k:34`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Entries  ::= List{Entry, ","}
```

### `reference-semantics/semantics/syntax.k:35`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### `reference-semantics/semantics/syntax.k:36`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax CompFors ::= List{CompFor, ""}
```

### `reference-semantics/semantics/syntax.k:37`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Exprs    ::= List{Expr, ","}
```

### `reference-semantics/semantics/syntax.k:38`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### `reference-semantics/semantics/syntax.k:39`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Bound    ::= Expr | "NoBound"
```

### `reference-semantics/semantics/syntax.k:41`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

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

### `reference-semantics/semantics/syntax.k:56`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### `reference-semantics/semantics/syntax.k:57`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### `reference-semantics/semantics/syntax.k:58`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### `reference-semantics/semantics/syntax.k:59`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### `reference-semantics/semantics/syntax.k:60`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS`

```k
  syntax ParamNames ::= List{String, ","}
```

### `reference-semantics/semantics/syntax.k:61`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Module     ::= "Module" "(" Stmts ")"
endmodule
```

### `reference-semantics/semantics/tuple.k:10`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### `reference-semantics/semantics/tuple.k:11`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### `reference-semantics/semantics/tuple.k:14`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax ApplyK ::= "toTuple"
```

### `reference-semantics/semantics/tuple.k:15`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### `reference-semantics/semantics/tuple.k:16`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### `reference-semantics/semantics/tuple.k:18`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### `reference-semantics/semantics/tuple.k:20`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### `reference-semantics/semantics/tuple.k:21`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### `reference-semantics/semantics/tuple.k:23`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### `reference-semantics/semantics/tuple.k:24`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### `reference-semantics/semantics/tuple.k:25`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### `reference-semantics/semantics/tuple.k:26`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### `reference-semantics/semantics/tuple.k:28`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### `reference-semantics/semantics/tuple.k:31`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### `reference-semantics/semantics/tuple.k:32`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### `reference-semantics/semantics/tuple.k:35`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### `reference-semantics/semantics/tuple.k:42`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### `reference-semantics/semantics/tuple.k:43`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### `reference-semantics/semantics/tuple.k:44`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/tuple.k:49`

- Kind: `syntax` / `syntax-declaration`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### `reference-semantics/semantics/tuple.k:50`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### `reference-semantics/semantics/tuple.k:51`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### `reference-semantics/semantics/tuple.k:52`

- Kind: `rule` / `priority-semantic-rule`
- Attributes: `priority`
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### `reference-semantics/semantics/tuple.k:55`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### `reference-semantics/semantics/tuple.k:57`

- Kind: `rule` / `ordinary-semantic-rule`
- Attributes: none
- Disposition: `OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS`

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
endmodule
```

### `verification.k:8`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Stmts ::= "numberRankBody" [function, total]
```

### `verification.k:9`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRankBody
    => If(Compare(Name("number"), CmpOp("==", Str("zero"))),
          Return(Int(0)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("one"))),
          Return(Int(1)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("two"))),
          Return(Int(2)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("three"))),
          Return(Int(3)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("four"))),
          Return(Int(4)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("five"))),
          Return(Int(5)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("six"))),
          Return(Int(6)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("seven"))),
          Return(Int(7)) .Stmts, .Stmts)
       If(Compare(Name("number"), CmpOp("==", Str("eight"))),
          Return(Int(8)) .Stmts, .Stmts)
       Return(Int(9)) .Stmts
```

### `verification.k:30`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Stmts ::= "sortNumbersBody" [function, total]
```

### `verification.k:31`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule sortNumbersBody
    => Return(
         Call(
           Attribute(Str(" "), "join"),
           (Call(
              Name("sorted"),
              (Call(Attribute(Name("numbers"), "split"), .Exprs),
               KwArg("key", Name("_number_rank")),
               .Exprs)),
            .Exprs)))
       .Stmts
```

### `verification.k:43`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Val ::= "numberRankClosure" [function, total]
```

### `verification.k:44`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRankClosure
    => closureVal(("number", .ParamNames), numberRankBody, 0)
```

### `verification.k:47`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Val ::= "sortNumbersClosure" [function, total]
```

### `verification.k:48`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule sortNumbersClosure
    => closureVal(("numbers", .ParamNames), sortNumbersBody, 0)
```

### `verification.k:51`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Module ::= "solutionProgram" [function, total]
```

### `verification.k:52`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule solutionProgram
    => Module(
         FuncDef("_number_rank", Params("number", .ParamNames), numberRankBody)
         FuncDef("sort_numbers", Params("numbers", .ParamNames), sortNumbersBody)
         .Stmts)
```

### `verification.k:60`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Int ::= numberRank(IntSeq) [function, total]
```

### `verification.k:61`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 0
    requires CS ==K strToCodes("zero")
```

### `verification.k:63`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 1
    requires CS ==K strToCodes("one")
```

### `verification.k:65`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 2
    requires CS ==K strToCodes("two")
```

### `verification.k:67`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 3
    requires CS ==K strToCodes("three")
```

### `verification.k:69`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 4
    requires CS ==K strToCodes("four")
```

### `verification.k:71`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 5
    requires CS ==K strToCodes("five")
```

### `verification.k:73`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 6
    requires CS ==K strToCodes("six")
```

### `verification.k:75`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 7
    requires CS ==K strToCodes("seven")
```

### `verification.k:77`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(CS:IntSeq) => 8
    requires CS ==K strToCodes("eight")
```

### `verification.k:79`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule numberRank(_:IntSeq) => 9 [owise]
```

### `verification.k:83`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Bool ::= validNumberWord(IntSeq) [function, total]
```

### `verification.k:84`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule validNumberWord(CS:IntSeq)
    => (CS ==K strToCodes("zero"))
       orBool (CS ==K strToCodes("one"))
       orBool (CS ==K strToCodes("two"))
       orBool (CS ==K strToCodes("three"))
       orBool (CS ==K strToCodes("four"))
       orBool (CS ==K strToCodes("five"))
       orBool (CS ==K strToCodes("six"))
       orBool (CS ==K strToCodes("seven"))
       orBool (CS ==K strToCodes("eight"))
       orBool (CS ==K strToCodes("nine"))
```

### `verification.k:96`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Bool ::= validNumberWords(ValSeq) [function, total]
```

### `verification.k:97`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule validNumberWords(.ValSeq) => true
```

### `verification.k:98`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule validNumberWords(vCons(str(CS:IntSeq), REST:ValSeq))
    => validNumberWord(CS) andBool validNumberWords(REST)
```

### `verification.k:100`

- Kind: `rule` / `equational-rule`
- Attributes: `owise`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule validNumberWords(vCons(_:Val, _:ValSeq)) => false [owise]
```

### `verification.k:102`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax Bool ::= validNumberInput(IntSeq) [function, total]
```

### `verification.k:103`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule validNumberInput(CS:IntSeq)
    => validNumberWords(splitWS(CS, .IntSeq, .ValSeq))
```

### `verification.k:108`

- Kind: `syntax` / `function-declaration`
- Attributes: `function`, `total`
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  syntax IntSeq ::= sortNumbersResult(IntSeq) [function, total]
```

### `verification.k:109`

- Kind: `rule` / `equational-rule`
- Attributes: none
- Disposition: `PROOF_LOCAL_MANUAL_REVIEW_PASS`

```k
  rule sortNumbersResult(CS:IntSeq)
    => joinCodes(
         iCons(32, .IntSeq),
         sortKeyVS(
           splitWS(CS, .IntSeq, .ValSeq),
           numberRankClosure))
endmodule
```

### `spec.k:6`

- Kind: `claim` / `claim`
- Attributes: none
- Disposition: `CLAIM_MANUAL_REVIEW_PASS`

```k
  claim [number-rank-connection]:
    <k> Call(Name("_number_rank"), (str(CS:IntSeq), .Exprs))
      => numberRank(CS) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map [ "_number_rank" <- numberRankClosure ], parent(-1))
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

### `spec.k:22`

- Kind: `claim` / `claim`
- Attributes: none
- Disposition: `CLAIM_MANUAL_REVIEW_PASS`

```k
  claim [sort-numbers]:
    <k> #loadAll(solutionProgram)
         ~> Call(Name("sort_numbers"), (str(CS:IntSeq), .Exprs))
      => str(sortNumbersResult(CS)) </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
        => scope(
             .Map
               [ "_number_rank" <- numberRankClosure ]
               [ "sort_numbers" <- sortNumbersClosure ],
             parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(splitWS(CS, .IntSeq, .ValSeq))
         1 |-> list(sortKeyVS(
                       splitWS(CS, .IntSeq, .ValSeq),
                       numberRankClosure))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validNumberInput(CS)
endmodule
```


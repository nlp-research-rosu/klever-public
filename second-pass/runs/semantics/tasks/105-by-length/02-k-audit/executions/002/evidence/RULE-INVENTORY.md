# Exhaustive K declaration and rule inventory

Generated from the clean scratch copies of every supplied semantics file plus `verification.k` and `spec.k`. Each top-level `configuration`, `syntax`, `context`, `rule`, and `claim` entry is listed exactly once. “Accepted fixed baseline” means the declaration belongs to the launcher-supplied semantics tree, whose candidate copy is byte-identical; it does not turn opaque primitives into proved Python facts.

- Total entries: 949
- Kinds: {'claim': 1, 'configuration': 1, 'context': 5, 'rule': 708, 'syntax': 234}
- Sources: {'proof-local': 20, 'supplied-fixed': 928, 'target-spec': 1}
- Attribute flags: {'anywhere': 0, 'concrete': 55, 'function': 154, 'functional': 0, 'macro': 4, 'no-evaluators': 25, 'owise': 30, 'priority': 54, 'seqstrict': 1, 'simplification': 0, 'strict': 3, 'symbol': 25, 'total': 116}

## K-0001

- Location: `reference-semantics/semantics/assert.k:6`–`7`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

## K-0002

- Location: `reference-semantics/semantics/assert.k:8`–`11`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

## K-0003

- Location: `reference-semantics/semantics/assert.k:13`–`16`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

## K-0004

- Location: `reference-semantics/semantics/bool.k:8`–`8`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

## K-0005

- Location: `reference-semantics/semantics/bool.k:10`–`10`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

## K-0006

- Location: `reference-semantics/semantics/bool.k:11`–`15`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

## K-0007

- Location: `reference-semantics/semantics/bool.k:16`–`16`
- Source class: supplied-fixed
- Entry kind: context
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

## K-0008

- Location: `reference-semantics/semantics/bool.k:17`–`17`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

## K-0009

- Location: `reference-semantics/semantics/bool.k:18`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

## K-0010

- Location: `reference-semantics/semantics/bool.k:20`–`21`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

## K-0011

- Location: `reference-semantics/semantics/bool.k:22`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

## K-0012

- Location: `reference-semantics/semantics/bool.k:24`–`28`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

## K-0013

- Location: `reference-semantics/semantics/bool.k:29`–`30`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

## K-0014

- Location: `reference-semantics/semantics/bool.k:31`–`34`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## K-0015

- Location: `reference-semantics/semantics/bool.k:35`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## K-0016

- Location: `reference-semantics/semantics/bool.k:39`–`42`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## K-0017

- Location: `reference-semantics/semantics/bool.k:43`–`47`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
endmodule
```

## K-0018

- Location: `reference-semantics/semantics/builtins.k:17`–`19`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

## K-0019

- Location: `reference-semantics/semantics/builtins.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= seqLen(Val) [function]
```

## K-0020

- Location: `reference-semantics/semantics/builtins.k:21`–`21`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

## K-0021

- Location: `reference-semantics/semantics/builtins.k:22`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

## K-0022

- Location: `reference-semantics/semantics/builtins.k:23`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

## K-0023

- Location: `reference-semantics/semantics/builtins.k:24`–`24`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

## K-0024

- Location: `reference-semantics/semantics/builtins.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

## K-0025

- Location: `reference-semantics/semantics/builtins.k:26`–`31`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

## K-0026

- Location: `reference-semantics/semantics/builtins.k:32`–`32`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

## K-0027

- Location: `reference-semantics/semantics/builtins.k:33`–`33`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

## K-0028

- Location: `reference-semantics/semantics/builtins.k:34`–`34`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

## K-0029

- Location: `reference-semantics/semantics/builtins.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

## K-0030

- Location: `reference-semantics/semantics/builtins.k:36`–`36`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

## K-0031

- Location: `reference-semantics/semantics/builtins.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

## K-0032

- Location: `reference-semantics/semantics/builtins.k:38`–`40`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

## K-0033

- Location: `reference-semantics/semantics/builtins.k:41`–`43`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

## K-0034

- Location: `reference-semantics/semantics/builtins.k:44`–`46`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

## K-0035

- Location: `reference-semantics/semantics/builtins.k:47`–`47`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

## K-0036

- Location: `reference-semantics/semantics/builtins.k:48`–`48`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

## K-0037

- Location: `reference-semantics/semantics/builtins.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

## K-0038

- Location: `reference-semantics/semantics/builtins.k:50`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

## K-0039

- Location: `reference-semantics/semantics/builtins.k:54`–`54`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= intOf(Val) [function]
```

## K-0040

- Location: `reference-semantics/semantics/builtins.k:55`–`55`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intOf(I:Int)  => I
```

## K-0041

- Location: `reference-semantics/semantics/builtins.k:56`–`58`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

## K-0042

- Location: `reference-semantics/semantics/builtins.k:59`–`59`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

## K-0043

- Location: `reference-semantics/semantics/builtins.k:60`–`60`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

## K-0044

- Location: `reference-semantics/semantics/builtins.k:61`–`61`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

## K-0045

- Location: `reference-semantics/semantics/builtins.k:62`–`63`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

## K-0046

- Location: `reference-semantics/semantics/builtins.k:64`–`65`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

## K-0047

- Location: `reference-semantics/semantics/builtins.k:67`–`67`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

## K-0048

- Location: `reference-semantics/semantics/builtins.k:68`–`68`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

## K-0049

- Location: `reference-semantics/semantics/builtins.k:69`–`69`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

## K-0050

- Location: `reference-semantics/semantics/builtins.k:70`–`71`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

## K-0051

- Location: `reference-semantics/semantics/builtins.k:72`–`75`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

## K-0052

- Location: `reference-semantics/semantics/builtins.k:76`–`76`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

## K-0053

- Location: `reference-semantics/semantics/builtins.k:77`–`77`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

## K-0054

- Location: `reference-semantics/semantics/builtins.k:78`–`79`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## K-0055

- Location: `reference-semantics/semantics/builtins.k:80`–`80`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

## K-0056

- Location: `reference-semantics/semantics/builtins.k:81`–`81`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

## K-0057

- Location: `reference-semantics/semantics/builtins.k:82`–`84`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

## K-0058

- Location: `reference-semantics/semantics/builtins.k:86`–`86`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

## K-0059

- Location: `reference-semantics/semantics/builtins.k:87`–`87`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

## K-0060

- Location: `reference-semantics/semantics/builtins.k:88`–`89`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## K-0061

- Location: `reference-semantics/semantics/builtins.k:90`–`90`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

## K-0062

- Location: `reference-semantics/semantics/builtins.k:91`–`91`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

## K-0063

- Location: `reference-semantics/semantics/builtins.k:92`–`96`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

## K-0064

- Location: `reference-semantics/semantics/builtins.k:97`–`97`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

## K-0065

- Location: `reference-semantics/semantics/builtins.k:98`–`98`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

## K-0066

- Location: `reference-semantics/semantics/builtins.k:99`–`99`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule maxVals(M:Int, .Vals)           => M
```

## K-0067

- Location: `reference-semantics/semantics/builtins.k:100`–`100`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

## K-0068

- Location: `reference-semantics/semantics/builtins.k:102`–`102`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

## K-0069

- Location: `reference-semantics/semantics/builtins.k:103`–`103`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

## K-0070

- Location: `reference-semantics/semantics/builtins.k:104`–`104`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule minVals(M:Int, .Vals)           => M
```

## K-0071

- Location: `reference-semantics/semantics/builtins.k:105`–`107`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

## K-0072

- Location: `reference-semantics/semantics/builtins.k:108`–`110`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

## K-0073

- Location: `reference-semantics/semantics/builtins.k:111`–`113`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

## K-0074

- Location: `reference-semantics/semantics/builtins.k:114`–`114`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

## K-0075

- Location: `reference-semantics/semantics/builtins.k:115`–`115`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

## K-0076

- Location: `reference-semantics/semantics/builtins.k:116`–`116`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

## K-0077

- Location: `reference-semantics/semantics/builtins.k:117`–`117`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

## K-0078

- Location: `reference-semantics/semantics/builtins.k:118`–`118`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

## K-0079

- Location: `reference-semantics/semantics/builtins.k:119`–`123`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

## K-0080

- Location: `reference-semantics/semantics/builtins.k:124`–`125`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

## K-0081

- Location: `reference-semantics/semantics/builtins.k:126`–`126`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

## K-0082

- Location: `reference-semantics/semantics/builtins.k:127`–`127`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

## K-0083

- Location: `reference-semantics/semantics/builtins.k:128`–`131`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

## K-0084

- Location: `reference-semantics/semantics/builtins.k:132`–`133`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

## K-0085

- Location: `reference-semantics/semantics/builtins.k:134`–`134`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

## K-0086

- Location: `reference-semantics/semantics/builtins.k:135`–`135`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

## K-0087

- Location: `reference-semantics/semantics/builtins.k:136`–`136`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

## K-0088

- Location: `reference-semantics/semantics/builtins.k:137`–`139`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

## K-0089

- Location: `reference-semantics/semantics/builtins.k:140`–`142`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

## K-0090

- Location: `reference-semantics/semantics/builtins.k:143`–`143`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

## K-0091

- Location: `reference-semantics/semantics/builtins.k:144`–`147`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

## K-0092

- Location: `reference-semantics/semantics/builtins.k:148`–`148`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

## K-0093

- Location: `reference-semantics/semantics/builtins.k:149`–`151`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

## K-0094

- Location: `reference-semantics/semantics/builtins.k:152`–`155`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

## K-0095

- Location: `reference-semantics/semantics/builtins.k:156`–`157`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

## K-0096

- Location: `reference-semantics/semantics/builtins.k:158`–`158`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

## K-0097

- Location: `reference-semantics/semantics/builtins.k:159`–`159`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

## K-0098

- Location: `reference-semantics/semantics/builtins.k:160`–`162`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

## K-0099

- Location: `reference-semantics/semantics/builtins.k:163`–`163`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

## K-0100

- Location: `reference-semantics/semantics/builtins.k:164`–`166`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

## K-0101

- Location: `reference-semantics/semantics/builtins.k:167`–`168`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

## K-0102

- Location: `reference-semantics/semantics/builtins.k:169`–`169`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

## K-0103

- Location: `reference-semantics/semantics/builtins.k:170`–`170`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

## K-0104

- Location: `reference-semantics/semantics/builtins.k:171`–`172`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

## K-0105

- Location: `reference-semantics/semantics/builtins.k:173`–`173`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

## K-0106

- Location: `reference-semantics/semantics/builtins.k:174`–`176`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

## K-0107

- Location: `reference-semantics/semantics/builtins.k:177`–`177`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

## K-0108

- Location: `reference-semantics/semantics/builtins.k:178`–`178`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

## K-0109

- Location: `reference-semantics/semantics/builtins.k:179`–`186`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

## K-0110

- Location: `reference-semantics/semantics/builtins.k:187`–`187`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

## K-0111

- Location: `reference-semantics/semantics/builtins.k:188`–`188`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

## K-0112

- Location: `reference-semantics/semantics/builtins.k:189`–`190`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

## K-0113

- Location: `reference-semantics/semantics/builtins.k:192`–`192`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

## K-0114

- Location: `reference-semantics/semantics/builtins.k:194`–`194`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

## K-0115

- Location: `reference-semantics/semantics/builtins.k:195`–`195`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

## K-0116

- Location: `reference-semantics/semantics/builtins.k:196`–`196`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

## K-0117

- Location: `reference-semantics/semantics/builtins.k:197`–`197`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

## K-0118

- Location: `reference-semantics/semantics/builtins.k:198`–`198`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

## K-0119

- Location: `reference-semantics/semantics/builtins.k:199`–`199`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

## K-0120

- Location: `reference-semantics/semantics/builtins.k:200`–`200`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

## K-0121

- Location: `reference-semantics/semantics/builtins.k:201`–`201`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

## K-0122

- Location: `reference-semantics/semantics/builtins.k:203`–`203`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

## K-0123

- Location: `reference-semantics/semantics/builtins.k:204`–`204`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

## K-0124

- Location: `reference-semantics/semantics/builtins.k:205`–`205`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

## K-0125

- Location: `reference-semantics/semantics/builtins.k:206`–`206`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

## K-0126

- Location: `reference-semantics/semantics/builtins.k:207`–`207`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

## K-0127

- Location: `reference-semantics/semantics/builtins.k:208`–`208`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

## K-0128

- Location: `reference-semantics/semantics/builtins.k:209`–`209`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

## K-0129

- Location: `reference-semantics/semantics/builtins.k:210`–`210`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

## K-0130

- Location: `reference-semantics/semantics/builtins.k:211`–`211`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

## K-0131

- Location: `reference-semantics/semantics/builtins.k:212`–`212`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

## K-0132

- Location: `reference-semantics/semantics/builtins.k:214`–`215`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

## K-0133

- Location: `reference-semantics/semantics/builtins.k:216`–`216`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

## K-0134

- Location: `reference-semantics/semantics/builtins.k:217`–`217`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

## K-0135

- Location: `reference-semantics/semantics/builtins.k:218`–`218`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

## K-0136

- Location: `reference-semantics/semantics/builtins.k:219`–`220`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

## K-0137

- Location: `reference-semantics/semantics/builtins.k:221`–`222`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

## K-0138

- Location: `reference-semantics/semantics/builtins.k:223`–`223`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

## K-0139

- Location: `reference-semantics/semantics/builtins.k:225`–`225`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

## K-0140

- Location: `reference-semantics/semantics/builtins.k:226`–`226`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

## K-0141

- Location: `reference-semantics/semantics/builtins.k:227`–`227`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

## K-0142

- Location: `reference-semantics/semantics/builtins.k:228`–`228`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

## K-0143

- Location: `reference-semantics/semantics/builtins.k:230`–`230`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

## K-0144

- Location: `reference-semantics/semantics/builtins.k:231`–`231`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

## K-0145

- Location: `reference-semantics/semantics/builtins.k:232`–`232`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

## K-0146

- Location: `reference-semantics/semantics/builtins.k:233`–`233`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

## K-0147

- Location: `reference-semantics/semantics/builtins.k:234`–`234`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

## K-0148

- Location: `reference-semantics/semantics/builtins.k:235`–`235`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

## K-0149

- Location: `reference-semantics/semantics/builtins.k:236`–`236`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

## K-0150

- Location: `reference-semantics/semantics/builtins.k:238`–`238`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

## K-0151

- Location: `reference-semantics/semantics/builtins.k:239`–`239`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

## K-0152

- Location: `reference-semantics/semantics/builtins.k:240`–`240`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

## K-0153

- Location: `reference-semantics/semantics/builtins.k:241`–`242`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

## K-0154

- Location: `reference-semantics/semantics/builtins.k:243`–`243`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

## K-0155

- Location: `reference-semantics/semantics/builtins.k:244`–`244`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

## K-0156

- Location: `reference-semantics/semantics/builtins.k:245`–`245`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

## K-0157

- Location: `reference-semantics/semantics/builtins.k:246`–`246`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

## K-0158

- Location: `reference-semantics/semantics/builtins.k:247`–`247`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

## K-0159

- Location: `reference-semantics/semantics/builtins.k:248`–`248`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

## K-0160

- Location: `reference-semantics/semantics/builtins.k:250`–`250`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

## K-0161

- Location: `reference-semantics/semantics/builtins.k:251`–`251`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## K-0162

- Location: `reference-semantics/semantics/builtins.k:252`–`252`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## K-0163

- Location: `reference-semantics/semantics/builtins.k:253`–`253`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## K-0164

- Location: `reference-semantics/semantics/builtins.k:254`–`254`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## K-0165

- Location: `reference-semantics/semantics/builtins.k:255`–`255`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

## K-0166

- Location: `reference-semantics/semantics/builtins.k:256`–`256`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

## K-0167

- Location: `reference-semantics/semantics/builtins.k:257`–`259`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

## K-0168

- Location: `reference-semantics/semantics/builtins.k:260`–`262`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

## K-0169

- Location: `reference-semantics/semantics/builtins.k:263`–`264`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

## K-0170

- Location: `reference-semantics/semantics/builtins.k:265`–`265`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

## K-0171

- Location: `reference-semantics/semantics/builtins.k:266`–`266`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

## K-0172

- Location: `reference-semantics/semantics/builtins.k:267`–`267`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

## K-0173

- Location: `reference-semantics/semantics/builtins.k:268`–`268`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

## K-0174

- Location: `reference-semantics/semantics/builtins.k:269`–`269`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

## K-0175

- Location: `reference-semantics/semantics/builtins.k:270`–`270`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

## K-0176

- Location: `reference-semantics/semantics/builtins.k:271`–`271`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

## K-0177

- Location: `reference-semantics/semantics/builtins.k:272`–`272`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

## K-0178

- Location: `reference-semantics/semantics/builtins.k:273`–`273`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

## K-0179

- Location: `reference-semantics/semantics/builtins.k:274`–`278`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

## K-0180

- Location: `reference-semantics/semantics/builtins.k:279`–`279`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= "#md5"
```

## K-0181

- Location: `reference-semantics/semantics/builtins.k:280`–`281`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

## K-0182

- Location: `reference-semantics/semantics/builtins.k:282`–`282`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

## K-0183

- Location: `reference-semantics/semantics/builtins.k:283`–`283`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= md5Obj(IntSeq)
```

## K-0184

- Location: `reference-semantics/semantics/builtins.k:284`–`284`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

## K-0185

- Location: `reference-semantics/semantics/builtins.k:285`–`290`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol, concrete, owise
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

## K-0186

- Location: `reference-semantics/semantics/builtins.k:291`–`291`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

## K-0187

- Location: `reference-semantics/semantics/builtins.k:292`–`292`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

## K-0188

- Location: `reference-semantics/semantics/builtins.k:293`–`293`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

## K-0189

- Location: `reference-semantics/semantics/builtins.k:294`–`294`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isIntV(_:Int)         => true
```

## K-0190

- Location: `reference-semantics/semantics/builtins.k:295`–`295`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isIntV(_:Val)         => false [owise]
```

## K-0191

- Location: `reference-semantics/semantics/builtins.k:296`–`296`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isStrV(str(_:IntSeq)) => true
```

## K-0192

- Location: `reference-semantics/semantics/builtins.k:297`–`298`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isStrV(_:Val)         => false [owise]
endmodule
```

## K-0193

- Location: `reference-semantics/semantics/call.k:16`–`18`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

## K-0194

- Location: `reference-semantics/semantics/call.k:19`–`19`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #callee(Exprs)
```

## K-0195

- Location: `reference-semantics/semantics/call.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

## K-0196

- Location: `reference-semantics/semantics/call.k:21`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

## K-0197

- Location: `reference-semantics/semantics/call.k:24`–`24`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

## K-0198

- Location: `reference-semantics/semantics/call.k:26`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

## K-0199

- Location: `reference-semantics/semantics/call.k:27`–`27`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

## K-0200

- Location: `reference-semantics/semantics/call.k:28`–`28`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

## K-0201

- Location: `reference-semantics/semantics/call.k:29`–`29`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

## K-0202

- Location: `reference-semantics/semantics/call.k:30`–`30`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

## K-0203

- Location: `reference-semantics/semantics/call.k:31`–`31`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

## K-0204

- Location: `reference-semantics/semantics/call.k:32`–`37`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

## K-0205

- Location: `reference-semantics/semantics/call.k:38`–`41`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## K-0206

- Location: `reference-semantics/semantics/call.k:42`–`46`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

## K-0207

- Location: `reference-semantics/semantics/call.k:47`–`50`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## K-0208

- Location: `reference-semantics/semantics/call.k:52`–`52`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

## K-0209

- Location: `reference-semantics/semantics/call.k:53`–`55`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

## K-0210

- Location: `reference-semantics/semantics/call.k:56`–`62`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

## K-0211

- Location: `reference-semantics/semantics/call.k:63`–`67`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

## K-0212

- Location: `reference-semantics/semantics/call.k:69`–`79`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0213

- Location: `reference-semantics/semantics/call.k:80`–`85`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

## K-0214

- Location: `reference-semantics/semantics/call.k:87`–`87`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #allocCells(ParamNames)
```

## K-0215

- Location: `reference-semantics/semantics/call.k:88`–`88`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

## K-0216

- Location: `reference-semantics/semantics/call.k:89`–`95`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
endmodule
```

## K-0217

- Location: `reference-semantics/semantics/comprehension.k:11`–`11`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## K-0218

- Location: `reference-semantics/semantics/comprehension.k:12`–`12`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## K-0219

- Location: `reference-semantics/semantics/comprehension.k:14`–`14`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: macro
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

## K-0220

- Location: `reference-semantics/semantics/comprehension.k:15`–`16`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

## K-0221

- Location: `reference-semantics/semantics/comprehension.k:18`–`18`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: macro
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

## K-0222

- Location: `reference-semantics/semantics/comprehension.k:19`–`20`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

## K-0223

- Location: `reference-semantics/semantics/comprehension.k:21`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

## K-0224

- Location: `reference-semantics/semantics/comprehension.k:24`–`24`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: macro
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

## K-0225

- Location: `reference-semantics/semantics/comprehension.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule compGuard(.Exprs)             => Bool(true)
```

## K-0226

- Location: `reference-semantics/semantics/comprehension.k:26`–`27`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
endmodule
```

## K-0227

- Location: `reference-semantics/semantics/concrete.k:13`–`15`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

## K-0228

- Location: `reference-semantics/semantics/concrete.k:16`–`24`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority, concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0229

- Location: `reference-semantics/semantics/concrete.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= kvP(Val, Val)
```

## K-0230

- Location: `reference-semantics/semantics/concrete.k:26`–`27`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

## K-0231

- Location: `reference-semantics/semantics/concrete.k:28`–`30`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

## K-0232

- Location: `reference-semantics/semantics/concrete.k:31`–`33`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

## K-0233

- Location: `reference-semantics/semantics/concrete.k:34`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

## K-0234

- Location: `reference-semantics/semantics/concrete.k:36`–`37`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

## K-0235

- Location: `reference-semantics/semantics/concrete.k:38`–`40`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

## K-0236

- Location: `reference-semantics/semantics/concrete.k:42`–`42`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

## K-0237

- Location: `reference-semantics/semantics/concrete.k:43`–`43`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

## K-0238

- Location: `reference-semantics/semantics/concrete.k:44`–`46`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

## K-0239

- Location: `reference-semantics/semantics/concrete.k:47`–`49`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

## K-0240

- Location: `reference-semantics/semantics/concrete.k:51`–`51`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

## K-0241

- Location: `reference-semantics/semantics/concrete.k:52`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

## K-0242

- Location: `reference-semantics/semantics/concrete.k:53`–`53`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

## K-0243

- Location: `reference-semantics/semantics/concrete.k:54`–`54`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## K-0244

- Location: `reference-semantics/semantics/concrete.k:56`–`56`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

## K-0245

- Location: `reference-semantics/semantics/concrete.k:57`–`57`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

## K-0246

- Location: `reference-semantics/semantics/concrete.k:58`–`58`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

## K-0247

- Location: `reference-semantics/semantics/concrete.k:59`–`60`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
endmodule
```

## K-0248

- Location: `reference-semantics/semantics/controls.k:9`–`11`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## K-0249

- Location: `reference-semantics/semantics/controls.k:12`–`18`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## K-0250

- Location: `reference-semantics/semantics/controls.k:20`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

## K-0251

- Location: `reference-semantics/semantics/controls.k:27`–`34`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

## K-0252

- Location: `reference-semantics/semantics/controls.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

## K-0253

- Location: `reference-semantics/semantics/controls.k:36`–`36`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

## K-0254

- Location: `reference-semantics/semantics/controls.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #bindImports(ParamNames)
```

## K-0255

- Location: `reference-semantics/semantics/controls.k:38`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

## K-0256

- Location: `reference-semantics/semantics/controls.k:39`–`42`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

## K-0257

- Location: `reference-semantics/semantics/controls.k:43`–`47`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

## K-0258

- Location: `reference-semantics/semantics/controls.k:48`–`50`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

## K-0259

- Location: `reference-semantics/semantics/controls.k:51`–`51`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

## K-0260

- Location: `reference-semantics/semantics/controls.k:52`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

## K-0261

- Location: `reference-semantics/semantics/controls.k:53`–`53`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

## K-0262

- Location: `reference-semantics/semantics/controls.k:54`–`56`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

## K-0263

- Location: `reference-semantics/semantics/controls.k:57`–`58`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

## K-0264

- Location: `reference-semantics/semantics/controls.k:59`–`64`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

## K-0265

- Location: `reference-semantics/semantics/controls.k:65`–`67`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

## K-0266

- Location: `reference-semantics/semantics/controls.k:69`–`69`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

## K-0267

- Location: `reference-semantics/semantics/controls.k:71`–`71`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

## K-0268

- Location: `reference-semantics/semantics/controls.k:72`–`72`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

## K-0269

- Location: `reference-semantics/semantics/controls.k:73`–`76`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

## K-0270

- Location: `reference-semantics/semantics/controls.k:77`–`77`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

## K-0271

- Location: `reference-semantics/semantics/controls.k:78`–`78`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

## K-0272

- Location: `reference-semantics/semantics/controls.k:79`–`80`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

## K-0273

- Location: `reference-semantics/semantics/controls.k:81`–`84`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

## K-0274

- Location: `reference-semantics/semantics/controls.k:85`–`85`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

## K-0275

- Location: `reference-semantics/semantics/controls.k:86`–`86`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Continue => #cont ... </k>
```

## K-0276

- Location: `reference-semantics/semantics/controls.k:87`–`87`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Break => #brk ... </k>
```

## K-0277

- Location: `reference-semantics/semantics/controls.k:88`–`88`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

## K-0278

- Location: `reference-semantics/semantics/controls.k:89`–`89`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

## K-0279

- Location: `reference-semantics/semantics/controls.k:90`–`90`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

## K-0280

- Location: `reference-semantics/semantics/controls.k:91`–`94`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority, owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

## K-0281

- Location: `reference-semantics/semantics/controls.k:95`–`97`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## K-0282

- Location: `reference-semantics/semantics/controls.k:98`–`100`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## K-0283

- Location: `reference-semantics/semantics/controls.k:101`–`105`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

## K-0284

- Location: `reference-semantics/semantics/controls.k:106`–`109`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

## K-0285

- Location: `reference-semantics/semantics/core.k:13`–`13`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

## K-0286

- Location: `reference-semantics/semantics/core.k:14`–`14`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

## K-0287

- Location: `reference-semantics/semantics/core.k:15`–`17`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

## K-0288

- Location: `reference-semantics/semantics/core.k:18`–`23`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

## K-0289

- Location: `reference-semantics/semantics/core.k:25`–`34`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0290

- Location: `reference-semantics/semantics/core.k:36`–`36`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Parent   ::= "root" | parent(Int)
```

## K-0291

- Location: `reference-semantics/semantics/core.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Scope    ::= scope(Map, Parent)
```

## K-0292

- Location: `reference-semantics/semantics/core.k:38`–`38`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KResult  ::= Val
```

## K-0293

- Location: `reference-semantics/semantics/core.k:39`–`39`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

## K-0294

- Location: `reference-semantics/semantics/core.k:40`–`40`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Vals     ::= List{Val, ","}
```

## K-0295

- Location: `reference-semantics/semantics/core.k:41`–`41`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

## K-0296

- Location: `reference-semantics/semantics/core.k:42`–`48`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

## K-0297

- Location: `reference-semantics/semantics/core.k:49`–`67`
- Source class: supplied-fixed
- Entry kind: configuration
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0298

- Location: `reference-semantics/semantics/core.k:68`–`68`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

## K-0299

- Location: `reference-semantics/semantics/core.k:69`–`69`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isRefV(ref(_:Int)) => true
```

## K-0300

- Location: `reference-semantics/semantics/core.k:70`–`74`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

## K-0301

- Location: `reference-semantics/semantics/core.k:75`–`75`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax HeapVal ::= cellV(Val)
```

## K-0302

- Location: `reference-semantics/semantics/core.k:76`–`76`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

## K-0303

- Location: `reference-semantics/semantics/core.k:77`–`77`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isCellRef(cellRef(_:Int)) => true
```

## K-0304

- Location: `reference-semantics/semantics/core.k:78`–`84`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: function, owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

## K-0305

- Location: `reference-semantics/semantics/core.k:85`–`94`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0306

- Location: `reference-semantics/semantics/core.k:95`–`95`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= kwV(String, Val)
```

## K-0307

- Location: `reference-semantics/semantics/core.k:96`–`96`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #kwTag(String)
```

## K-0308

- Location: `reference-semantics/semantics/core.k:97`–`97`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

## K-0309

- Location: `reference-semantics/semantics/core.k:98`–`99`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

## K-0310

- Location: `reference-semantics/semantics/core.k:100`–`100`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

## K-0311

- Location: `reference-semantics/semantics/core.k:101`–`101`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

## K-0312

- Location: `reference-semantics/semantics/core.k:102`–`105`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

## K-0313

- Location: `reference-semantics/semantics/core.k:106`–`106`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= cellsMark(ParamNames)
```

## K-0314

- Location: `reference-semantics/semantics/core.k:107`–`107`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

## K-0315

- Location: `reference-semantics/semantics/core.k:108`–`108`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

## K-0316

- Location: `reference-semantics/semantics/core.k:109`–`109`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

## K-0317

- Location: `reference-semantics/semantics/core.k:110`–`110`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule pnMember(_:String, .ParamNames) => false
```

## K-0318

- Location: `reference-semantics/semantics/core.k:111`–`111`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

## K-0319

- Location: `reference-semantics/semantics/core.k:113`–`113`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #cellW(Val, Val)
```

## K-0320

- Location: `reference-semantics/semantics/core.k:114`–`115`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

## K-0321

- Location: `reference-semantics/semantics/core.k:117`–`117`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #alloc(Val)
```

## K-0322

- Location: `reference-semantics/semantics/core.k:118`–`123`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

## K-0323

- Location: `reference-semantics/semantics/core.k:124`–`124`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #loadAll(Module)
```

## K-0324

- Location: `reference-semantics/semantics/core.k:125`–`125`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

## K-0325

- Location: `reference-semantics/semantics/core.k:126`–`126`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

## K-0326

- Location: `reference-semantics/semantics/core.k:127`–`129`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

## K-0327

- Location: `reference-semantics/semantics/core.k:130`–`130`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #look(String, Int)
```

## K-0328

- Location: `reference-semantics/semantics/core.k:131`–`131`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

## K-0329

- Location: `reference-semantics/semantics/core.k:132`–`144`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: function, priority, concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0330

- Location: `reference-semantics/semantics/core.k:145`–`151`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

## K-0331

- Location: `reference-semantics/semantics/core.k:152`–`156`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

## K-0332

- Location: `reference-semantics/semantics/core.k:157`–`157`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

## K-0333

- Location: `reference-semantics/semantics/core.k:158`–`184`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0334

- Location: `reference-semantics/semantics/core.k:185`–`185`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ApplyK ::= toCall(Val)
```

## K-0335

- Location: `reference-semantics/semantics/core.k:186`–`188`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

## K-0336

- Location: `reference-semantics/semantics/core.k:189`–`189`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

## K-0337

- Location: `reference-semantics/semantics/core.k:190`–`190`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

## K-0338

- Location: `reference-semantics/semantics/core.k:191`–`193`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

## K-0339

- Location: `reference-semantics/semantics/core.k:194`–`194`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Int(I:Int)   => I ... </k>
```

## K-0340

- Location: `reference-semantics/semantics/core.k:195`–`195`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

## K-0341

- Location: `reference-semantics/semantics/core.k:196`–`198`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

## K-0342

- Location: `reference-semantics/semantics/core.k:199`–`199`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= truthy(Val) [function]
```

## K-0343

- Location: `reference-semantics/semantics/core.k:200`–`200`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule truthy(B:Bool)          => B
```

## K-0344

- Location: `reference-semantics/semantics/core.k:201`–`201`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule truthy(noneV)           => false
```

## K-0345

- Location: `reference-semantics/semantics/core.k:202`–`202`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule truthy(I:Int)           => I =/=Int 0
```

## K-0346

- Location: `reference-semantics/semantics/core.k:203`–`203`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

## K-0347

- Location: `reference-semantics/semantics/core.k:204`–`204`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

## K-0348

- Location: `reference-semantics/semantics/core.k:205`–`207`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

## K-0349

- Location: `reference-semantics/semantics/core.k:208`–`208`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

## K-0350

- Location: `reference-semantics/semantics/core.k:209`–`209`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

## K-0351

- Location: `reference-semantics/semantics/core.k:210`–`212`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

## K-0352

- Location: `reference-semantics/semantics/core.k:213`–`213`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

## K-0353

- Location: `reference-semantics/semantics/core.k:214`–`214`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

## K-0354

- Location: `reference-semantics/semantics/core.k:215`–`215`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

## K-0355

- Location: `reference-semantics/semantics/core.k:217`–`217`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

## K-0356

- Location: `reference-semantics/semantics/core.k:218`–`218`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

## K-0357

- Location: `reference-semantics/semantics/core.k:219`–`222`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

## K-0358

- Location: `reference-semantics/semantics/core.k:223`–`223`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

## K-0359

- Location: `reference-semantics/semantics/core.k:224`–`224`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule vsLen(.ValSeq)                => 0
```

## K-0360

- Location: `reference-semantics/semantics/core.k:225`–`225`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

## K-0361

- Location: `reference-semantics/semantics/core.k:227`–`227`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

## K-0362

- Location: `reference-semantics/semantics/core.k:228`–`228`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isLen(.IntSeq)                => 0
```

## K-0363

- Location: `reference-semantics/semantics/core.k:229`–`232`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

## K-0364

- Location: `reference-semantics/semantics/core.k:233`–`233`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

## K-0365

- Location: `reference-semantics/semantics/core.k:234`–`234`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

## K-0366

- Location: `reference-semantics/semantics/core.k:235`–`235`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

## K-0367

- Location: `reference-semantics/semantics/core.k:236`–`237`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

## K-0368

- Location: `reference-semantics/semantics/core.k:238`–`240`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
endmodule
```

## K-0369

- Location: `reference-semantics/semantics/dict.k:20`–`22`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

## K-0370

- Location: `reference-semantics/semantics/dict.k:23`–`25`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

## K-0371

- Location: `reference-semantics/semantics/dict.k:26`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

## K-0372

- Location: `reference-semantics/semantics/dict.k:27`–`27`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

## K-0373

- Location: `reference-semantics/semantics/dict.k:28`–`29`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

## K-0374

- Location: `reference-semantics/semantics/dict.k:30`–`31`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

## K-0375

- Location: `reference-semantics/semantics/dict.k:32`–`36`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: total, concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

## K-0376

- Location: `reference-semantics/semantics/dict.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

## K-0377

- Location: `reference-semantics/semantics/dict.k:38`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

## K-0378

- Location: `reference-semantics/semantics/dict.k:39`–`39`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

## K-0379

- Location: `reference-semantics/semantics/dict.k:40`–`42`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

## K-0380

- Location: `reference-semantics/semantics/dict.k:43`–`43`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

## K-0381

- Location: `reference-semantics/semantics/dict.k:44`–`44`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

## K-0382

- Location: `reference-semantics/semantics/dict.k:45`–`48`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

## K-0383

- Location: `reference-semantics/semantics/dict.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

## K-0384

- Location: `reference-semantics/semantics/dict.k:50`–`51`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

## K-0385

- Location: `reference-semantics/semantics/dict.k:52`–`53`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

## K-0386

- Location: `reference-semantics/semantics/dict.k:54`–`57`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

## K-0387

- Location: `reference-semantics/semantics/dict.k:58`–`62`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

## K-0388

- Location: `reference-semantics/semantics/dict.k:63`–`63`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

## K-0389

- Location: `reference-semantics/semantics/dict.k:64`–`64`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

## K-0390

- Location: `reference-semantics/semantics/dict.k:65`–`69`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

## K-0391

- Location: `reference-semantics/semantics/dict.k:70`–`70`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

## K-0392

- Location: `reference-semantics/semantics/dict.k:71`–`75`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

## K-0393

- Location: `reference-semantics/semantics/dict.k:76`–`76`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #dsetK(String, Val)
```

## K-0394

- Location: `reference-semantics/semantics/dict.k:77`–`77`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

## K-0395

- Location: `reference-semantics/semantics/dict.k:78`–`81`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

## K-0396

- Location: `reference-semantics/semantics/dict.k:82`–`85`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

## K-0397

- Location: `reference-semantics/semantics/dict.k:86`–`86`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

## K-0398

- Location: `reference-semantics/semantics/dict.k:87`–`89`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

## K-0399

- Location: `reference-semantics/semantics/dict.k:90`–`90`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

## K-0400

- Location: `reference-semantics/semantics/dict.k:91`–`91`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## K-0401

- Location: `reference-semantics/semantics/dict.k:92`–`94`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

## K-0402

- Location: `reference-semantics/semantics/dict.k:95`–`96`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

## K-0403

- Location: `reference-semantics/semantics/dict.k:97`–`97`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

## K-0404

- Location: `reference-semantics/semantics/dict.k:98`–`98`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

## K-0405

- Location: `reference-semantics/semantics/dict.k:99`–`100`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

## K-0406

- Location: `reference-semantics/semantics/dict.k:101`–`101`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

## K-0407

- Location: `reference-semantics/semantics/dict.k:102`–`102`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

## K-0408

- Location: `reference-semantics/semantics/dict.k:103`–`104`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
endmodule
```

## K-0409

- Location: `reference-semantics/semantics/float.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= Float
```

## K-0410

- Location: `reference-semantics/semantics/float.k:21`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: no-evaluators, concrete
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

## K-0411

- Location: `reference-semantics/semantics/float.k:24`–`24`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

## K-0412

- Location: `reference-semantics/semantics/float.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

## K-0413

- Location: `reference-semantics/semantics/float.k:27`–`29`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

## K-0414

- Location: `reference-semantics/semantics/float.k:30`–`30`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

## K-0415

- Location: `reference-semantics/semantics/float.k:31`–`31`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

## K-0416

- Location: `reference-semantics/semantics/float.k:32`–`36`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

## K-0417

- Location: `reference-semantics/semantics/float.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

## K-0418

- Location: `reference-semantics/semantics/float.k:38`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

## K-0419

- Location: `reference-semantics/semantics/float.k:39`–`42`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

## K-0420

- Location: `reference-semantics/semantics/float.k:43`–`43`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

## K-0421

- Location: `reference-semantics/semantics/float.k:44`–`49`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: no-evaluators, concrete
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

## K-0422

- Location: `reference-semantics/semantics/float.k:50`–`50`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

## K-0423

- Location: `reference-semantics/semantics/float.k:51`–`51`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

## K-0424

- Location: `reference-semantics/semantics/float.k:52`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

## K-0425

- Location: `reference-semantics/semantics/float.k:54`–`54`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

## K-0426

- Location: `reference-semantics/semantics/float.k:55`–`55`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

## K-0427

- Location: `reference-semantics/semantics/float.k:56`–`60`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

## K-0428

- Location: `reference-semantics/semantics/float.k:61`–`64`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

## K-0429

- Location: `reference-semantics/semantics/float.k:65`–`65`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= "#mathCeil"
```

## K-0430

- Location: `reference-semantics/semantics/float.k:66`–`66`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

## K-0431

- Location: `reference-semantics/semantics/float.k:67`–`69`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

## K-0432

- Location: `reference-semantics/semantics/float.k:70`–`70`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= "#mathFloor"
```

## K-0433

- Location: `reference-semantics/semantics/float.k:71`–`71`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

## K-0434

- Location: `reference-semantics/semantics/float.k:72`–`72`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

## K-0435

- Location: `reference-semantics/semantics/float.k:73`–`73`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, symbol
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

## K-0436

- Location: `reference-semantics/semantics/float.k:74`–`74`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

## K-0437

- Location: `reference-semantics/semantics/float.k:75`–`77`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

## K-0438

- Location: `reference-semantics/semantics/float.k:78`–`78`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

## K-0439

- Location: `reference-semantics/semantics/float.k:79`–`81`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

## K-0440

- Location: `reference-semantics/semantics/float.k:82`–`82`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

## K-0441

- Location: `reference-semantics/semantics/float.k:83`–`83`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

## K-0442

- Location: `reference-semantics/semantics/float.k:84`–`84`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

## K-0443

- Location: `reference-semantics/semantics/float.k:85`–`85`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

## K-0444

- Location: `reference-semantics/semantics/float.k:86`–`86`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, symbol
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

## K-0445

- Location: `reference-semantics/semantics/float.k:87`–`87`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule toF(F:Float) => F        [concrete]
```

## K-0446

- Location: `reference-semantics/semantics/float.k:88`–`92`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

## K-0447

- Location: `reference-semantics/semantics/float.k:93`–`93`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, symbol
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

## K-0448

- Location: `reference-semantics/semantics/float.k:94`–`94`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

## K-0449

- Location: `reference-semantics/semantics/float.k:95`–`98`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

## K-0450

- Location: `reference-semantics/semantics/float.k:99`–`102`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: no-evaluators, concrete
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

## K-0451

- Location: `reference-semantics/semantics/float.k:103`–`103`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

## K-0452

- Location: `reference-semantics/semantics/float.k:104`–`104`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

## K-0453

- Location: `reference-semantics/semantics/float.k:105`–`105`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

## K-0454

- Location: `reference-semantics/semantics/float.k:107`–`107`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

## K-0455

- Location: `reference-semantics/semantics/float.k:108`–`108`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

## K-0456

- Location: `reference-semantics/semantics/float.k:109`–`109`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

## K-0457

- Location: `reference-semantics/semantics/float.k:111`–`111`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

## K-0458

- Location: `reference-semantics/semantics/float.k:112`–`112`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

## K-0459

- Location: `reference-semantics/semantics/float.k:113`–`113`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

## K-0460

- Location: `reference-semantics/semantics/float.k:115`–`115`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

## K-0461

- Location: `reference-semantics/semantics/float.k:116`–`116`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

## K-0462

- Location: `reference-semantics/semantics/float.k:117`–`117`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

## K-0463

- Location: `reference-semantics/semantics/float.k:119`–`119`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

## K-0464

- Location: `reference-semantics/semantics/float.k:120`–`120`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

## K-0465

- Location: `reference-semantics/semantics/float.k:121`–`124`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

## K-0466

- Location: `reference-semantics/semantics/float.k:125`–`125`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

## K-0467

- Location: `reference-semantics/semantics/float.k:126`–`126`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

## K-0468

- Location: `reference-semantics/semantics/float.k:127`–`127`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

## K-0469

- Location: `reference-semantics/semantics/float.k:128`–`128`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

## K-0470

- Location: `reference-semantics/semantics/float.k:129`–`131`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

## K-0471

- Location: `reference-semantics/semantics/float.k:132`–`132`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

## K-0472

- Location: `reference-semantics/semantics/float.k:133`–`133`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

## K-0473

- Location: `reference-semantics/semantics/float.k:134`–`134`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

## K-0474

- Location: `reference-semantics/semantics/float.k:135`–`135`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

## K-0475

- Location: `reference-semantics/semantics/float.k:136`–`136`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

## K-0476

- Location: `reference-semantics/semantics/float.k:137`–`137`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

## K-0477

- Location: `reference-semantics/semantics/float.k:138`–`138`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

## K-0478

- Location: `reference-semantics/semantics/float.k:139`–`141`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

## K-0479

- Location: `reference-semantics/semantics/float.k:142`–`142`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

## K-0480

- Location: `reference-semantics/semantics/float.k:143`–`143`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

## K-0481

- Location: `reference-semantics/semantics/float.k:144`–`144`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

## K-0482

- Location: `reference-semantics/semantics/float.k:145`–`145`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

## K-0483

- Location: `reference-semantics/semantics/float.k:146`–`146`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

## K-0484

- Location: `reference-semantics/semantics/float.k:147`–`147`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

## K-0485

- Location: `reference-semantics/semantics/float.k:148`–`148`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

## K-0486

- Location: `reference-semantics/semantics/float.k:149`–`149`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

## K-0487

- Location: `reference-semantics/semantics/float.k:150`–`150`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

## K-0488

- Location: `reference-semantics/semantics/float.k:151`–`153`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

## K-0489

- Location: `reference-semantics/semantics/float.k:154`–`154`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

## K-0490

- Location: `reference-semantics/semantics/float.k:155`–`159`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

## K-0491

- Location: `reference-semantics/semantics/float.k:160`–`160`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

## K-0492

- Location: `reference-semantics/semantics/float.k:161`–`161`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

## K-0493

- Location: `reference-semantics/semantics/float.k:162`–`164`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

## K-0494

- Location: `reference-semantics/semantics/float.k:165`–`165`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= headIS(IntSeq) [function]
```

## K-0495

- Location: `reference-semantics/semantics/float.k:166`–`166`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

## K-0496

- Location: `reference-semantics/semantics/float.k:167`–`167`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

## K-0497

- Location: `reference-semantics/semantics/float.k:168`–`168`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

## K-0498

- Location: `reference-semantics/semantics/float.k:169`–`169`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

## K-0499

- Location: `reference-semantics/semantics/float.k:170`–`170`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

## K-0500

- Location: `reference-semantics/semantics/float.k:171`–`172`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

## K-0501

- Location: `reference-semantics/semantics/float.k:173`–`173`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

## K-0502

- Location: `reference-semantics/semantics/float.k:174`–`174`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracPart(.IntSeq) => 0
```

## K-0503

- Location: `reference-semantics/semantics/float.k:175`–`175`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

## K-0504

- Location: `reference-semantics/semantics/float.k:176`–`176`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

## K-0505

- Location: `reference-semantics/semantics/float.k:177`–`177`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

## K-0506

- Location: `reference-semantics/semantics/float.k:178`–`178`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

## K-0507

- Location: `reference-semantics/semantics/float.k:179`–`179`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

## K-0508

- Location: `reference-semantics/semantics/float.k:180`–`180`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracScale(.IntSeq) => 1
```

## K-0509

- Location: `reference-semantics/semantics/float.k:181`–`181`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

## K-0510

- Location: `reference-semantics/semantics/float.k:182`–`182`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

## K-0511

- Location: `reference-semantics/semantics/float.k:183`–`183`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

## K-0512

- Location: `reference-semantics/semantics/float.k:184`–`184`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

## K-0513

- Location: `reference-semantics/semantics/float.k:185`–`185`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

## K-0514

- Location: `reference-semantics/semantics/float.k:186`–`186`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

## K-0515

- Location: `reference-semantics/semantics/float.k:187`–`189`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

## K-0516

- Location: `reference-semantics/semantics/float.k:190`–`190`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

## K-0517

- Location: `reference-semantics/semantics/float.k:191`–`191`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

## K-0518

- Location: `reference-semantics/semantics/float.k:192`–`194`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

## K-0519

- Location: `reference-semantics/semantics/float.k:195`–`195`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

## K-0520

- Location: `reference-semantics/semantics/float.k:196`–`196`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

## K-0521

- Location: `reference-semantics/semantics/float.k:197`–`197`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

## K-0522

- Location: `reference-semantics/semantics/float.k:198`–`198`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

## K-0523

- Location: `reference-semantics/semantics/float.k:199`–`199`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

## K-0524

- Location: `reference-semantics/semantics/float.k:200`–`200`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

## K-0525

- Location: `reference-semantics/semantics/float.k:201`–`201`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

## K-0526

- Location: `reference-semantics/semantics/float.k:202`–`202`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

## K-0527

- Location: `reference-semantics/semantics/float.k:203`–`203`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

## K-0528

- Location: `reference-semantics/semantics/float.k:204`–`204`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

## K-0529

- Location: `reference-semantics/semantics/float.k:205`–`205`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

## K-0530

- Location: `reference-semantics/semantics/float.k:206`–`208`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

## K-0531

- Location: `reference-semantics/semantics/float.k:209`–`209`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

## K-0532

- Location: `reference-semantics/semantics/float.k:210`–`210`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

## K-0533

- Location: `reference-semantics/semantics/float.k:211`–`211`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

## K-0534

- Location: `reference-semantics/semantics/float.k:213`–`213`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

## K-0535

- Location: `reference-semantics/semantics/float.k:214`–`216`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

## K-0536

- Location: `reference-semantics/semantics/float.k:217`–`217`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

## K-0537

- Location: `reference-semantics/semantics/float.k:218`–`222`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

## K-0538

- Location: `reference-semantics/semantics/float.k:223`–`223`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

## K-0539

- Location: `reference-semantics/semantics/float.k:224`–`226`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

## K-0540

- Location: `reference-semantics/semantics/float.k:227`–`227`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

## K-0541

- Location: `reference-semantics/semantics/float.k:228`–`228`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

## K-0542

- Location: `reference-semantics/semantics/float.k:230`–`230`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

## K-0543

- Location: `reference-semantics/semantics/float.k:231`–`231`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

## K-0544

- Location: `reference-semantics/semantics/float.k:232`–`232`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= "#mathSqrt"
```

## K-0545

- Location: `reference-semantics/semantics/float.k:233`–`233`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

## K-0546

- Location: `reference-semantics/semantics/float.k:234`–`234`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

## K-0547

- Location: `reference-semantics/semantics/float.k:235`–`242`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority, concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

## K-0548

- Location: `reference-semantics/semantics/float.k:243`–`243`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

## K-0549

- Location: `reference-semantics/semantics/float.k:244`–`244`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## K-0550

- Location: `reference-semantics/semantics/float.k:245`–`245`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

## K-0551

- Location: `reference-semantics/semantics/float.k:246`–`246`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

## K-0552

- Location: `reference-semantics/semantics/float.k:247`–`248`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## K-0553

- Location: `reference-semantics/semantics/float.k:250`–`250`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

## K-0554

- Location: `reference-semantics/semantics/float.k:251`–`251`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## K-0555

- Location: `reference-semantics/semantics/float.k:252`–`252`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

## K-0556

- Location: `reference-semantics/semantics/float.k:253`–`253`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

## K-0557

- Location: `reference-semantics/semantics/float.k:254`–`260`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

## K-0558

- Location: `reference-semantics/semantics/float.k:261`–`261`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

## K-0559

- Location: `reference-semantics/semantics/float.k:262`–`264`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

## K-0560

- Location: `reference-semantics/semantics/float.k:265`–`265`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

## K-0561

- Location: `reference-semantics/semantics/float.k:266`–`266`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

## K-0562

- Location: `reference-semantics/semantics/float.k:267`–`269`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## K-0563

- Location: `reference-semantics/semantics/float.k:270`–`273`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
endmodule
```

## K-0564

- Location: `reference-semantics/semantics/functions.k:8`–`13`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

## K-0565

- Location: `reference-semantics/semantics/functions.k:14`–`16`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

## K-0566

- Location: `reference-semantics/semantics/functions.k:18`–`18`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

## K-0567

- Location: `reference-semantics/semantics/functions.k:19`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

## K-0568

- Location: `reference-semantics/semantics/functions.k:27`–`30`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

## K-0569

- Location: `reference-semantics/semantics/functions.k:31`–`32`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

## K-0570

- Location: `reference-semantics/semantics/functions.k:33`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

## K-0571

- Location: `reference-semantics/semantics/functions.k:36`–`41`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## K-0572

- Location: `reference-semantics/semantics/functions.k:42`–`45`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

## K-0573

- Location: `reference-semantics/semantics/functions.k:47`–`49`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

## K-0574

- Location: `reference-semantics/semantics/functions.k:50`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

## K-0575

- Location: `reference-semantics/semantics/functions.k:53`–`58`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## K-0576

- Location: `reference-semantics/semantics/functions.k:59`–`62`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

## K-0577

- Location: `reference-semantics/semantics/functions.k:63`–`63`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

## K-0578

- Location: `reference-semantics/semantics/functions.k:64`–`67`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

## K-0579

- Location: `reference-semantics/semantics/functions.k:68`–`77`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0580

- Location: `reference-semantics/semantics/functions.k:78`–`79`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

## K-0581

- Location: `reference-semantics/semantics/functions.k:80`–`84`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

## K-0582

- Location: `reference-semantics/semantics/functions.k:85`–`91`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
endmodule
```

## K-0583

- Location: `reference-semantics/semantics/int.k:7`–`7`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

## K-0584

- Location: `reference-semantics/semantics/int.k:9`–`10`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

## K-0585

- Location: `reference-semantics/semantics/int.k:11`–`11`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

## K-0586

- Location: `reference-semantics/semantics/int.k:12`–`12`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

## K-0587

- Location: `reference-semantics/semantics/int.k:13`–`13`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

## K-0588

- Location: `reference-semantics/semantics/int.k:14`–`14`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

## K-0589

- Location: `reference-semantics/semantics/int.k:15`–`15`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

## K-0590

- Location: `reference-semantics/semantics/int.k:16`–`16`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

## K-0591

- Location: `reference-semantics/semantics/int.k:17`–`17`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

## K-0592

- Location: `reference-semantics/semantics/int.k:19`–`19`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

## K-0593

- Location: `reference-semantics/semantics/int.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

## K-0594

- Location: `reference-semantics/semantics/int.k:22`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

## K-0595

- Location: `reference-semantics/semantics/int.k:23`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

## K-0596

- Location: `reference-semantics/semantics/int.k:24`–`24`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

## K-0597

- Location: `reference-semantics/semantics/int.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

## K-0598

- Location: `reference-semantics/semantics/int.k:26`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

## K-0599

- Location: `reference-semantics/semantics/int.k:27`–`28`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
endmodule
```

## K-0600

- Location: `reference-semantics/semantics/iter.k:8`–`9`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
endmodule
```

## K-0601

- Location: `reference-semantics/semantics/list.k:9`–`9`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

## K-0602

- Location: `reference-semantics/semantics/list.k:10`–`12`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

## K-0603

- Location: `reference-semantics/semantics/list.k:13`–`13`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ApplyK ::= "toList"
```

## K-0604

- Location: `reference-semantics/semantics/list.k:14`–`14`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

## K-0605

- Location: `reference-semantics/semantics/list.k:15`–`17`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

## K-0606

- Location: `reference-semantics/semantics/list.k:18`–`18`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

## K-0607

- Location: `reference-semantics/semantics/list.k:19`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

## K-0608

- Location: `reference-semantics/semantics/list.k:20`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

## K-0609

- Location: `reference-semantics/semantics/list.k:24`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

## K-0610

- Location: `reference-semantics/semantics/list.k:27`–`27`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

## K-0611

- Location: `reference-semantics/semantics/list.k:28`–`32`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

## K-0612

- Location: `reference-semantics/semantics/list.k:33`–`33`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

## K-0613

- Location: `reference-semantics/semantics/list.k:34`–`34`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule hasRefVS(.ValSeq)                => false
```

## K-0614

- Location: `reference-semantics/semantics/list.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

## K-0615

- Location: `reference-semantics/semantics/list.k:37`–`38`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

## K-0616

- Location: `reference-semantics/semantics/list.k:39`–`39`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

## K-0617

- Location: `reference-semantics/semantics/list.k:40`–`40`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

## K-0618

- Location: `reference-semantics/semantics/list.k:41`–`41`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

## K-0619

- Location: `reference-semantics/semantics/list.k:42`–`43`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

## K-0620

- Location: `reference-semantics/semantics/list.k:45`–`46`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

## K-0621

- Location: `reference-semantics/semantics/list.k:47`–`48`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

## K-0622

- Location: `reference-semantics/semantics/list.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

## K-0623

- Location: `reference-semantics/semantics/list.k:50`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

## K-0624

- Location: `reference-semantics/semantics/list.k:53`–`57`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

## K-0625

- Location: `reference-semantics/semantics/list.k:58`–`58`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

## K-0626

- Location: `reference-semantics/semantics/list.k:59`–`59`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

## K-0627

- Location: `reference-semantics/semantics/list.k:60`–`60`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

## K-0628

- Location: `reference-semantics/semantics/list.k:61`–`61`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

## K-0629

- Location: `reference-semantics/semantics/list.k:62`–`62`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

## K-0630

- Location: `reference-semantics/semantics/list.k:63`–`64`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

## K-0631

- Location: `reference-semantics/semantics/list.k:65`–`66`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

## K-0632

- Location: `reference-semantics/semantics/list.k:67`–`68`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
endmodule
```

## K-0633

- Location: `reference-semantics/semantics/methods.k:10`–`12`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

## K-0634

- Location: `reference-semantics/semantics/methods.k:13`–`13`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

## K-0635

- Location: `reference-semantics/semantics/methods.k:14`–`14`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

## K-0636

- Location: `reference-semantics/semantics/methods.k:15`–`15`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

## K-0637

- Location: `reference-semantics/semantics/methods.k:16`–`18`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

## K-0638

- Location: `reference-semantics/semantics/methods.k:19`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

## K-0639

- Location: `reference-semantics/semantics/methods.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

## K-0640

- Location: `reference-semantics/semantics/methods.k:21`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

## K-0641

- Location: `reference-semantics/semantics/methods.k:26`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

## K-0642

- Location: `reference-semantics/semantics/methods.k:27`–`27`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

## K-0643

- Location: `reference-semantics/semantics/methods.k:28`–`28`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

## K-0644

- Location: `reference-semantics/semantics/methods.k:29`–`29`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

## K-0645

- Location: `reference-semantics/semantics/methods.k:30`–`33`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

## K-0646

- Location: `reference-semantics/semantics/methods.k:34`–`34`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

## K-0647

- Location: `reference-semantics/semantics/methods.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

## K-0648

- Location: `reference-semantics/semantics/methods.k:36`–`36`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

## K-0649

- Location: `reference-semantics/semantics/methods.k:37`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

## K-0650

- Location: `reference-semantics/semantics/methods.k:39`–`40`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

## K-0651

- Location: `reference-semantics/semantics/methods.k:41`–`41`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

## K-0652

- Location: `reference-semantics/semantics/methods.k:42`–`42`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

## K-0653

- Location: `reference-semantics/semantics/methods.k:43`–`43`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

## K-0654

- Location: `reference-semantics/semantics/methods.k:44`–`46`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

## K-0655

- Location: `reference-semantics/semantics/methods.k:47`–`47`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

## K-0656

- Location: `reference-semantics/semantics/methods.k:48`–`48`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

## K-0657

- Location: `reference-semantics/semantics/methods.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule trimWS(.IntSeq) => .IntSeq
```

## K-0658

- Location: `reference-semantics/semantics/methods.k:50`–`50`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

## K-0659

- Location: `reference-semantics/semantics/methods.k:51`–`51`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

## K-0660

- Location: `reference-semantics/semantics/methods.k:52`–`52`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

## K-0661

- Location: `reference-semantics/semantics/methods.k:53`–`53`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

## K-0662

- Location: `reference-semantics/semantics/methods.k:54`–`54`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

## K-0663

- Location: `reference-semantics/semantics/methods.k:55`–`57`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

## K-0664

- Location: `reference-semantics/semantics/methods.k:58`–`60`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

## K-0665

- Location: `reference-semantics/semantics/methods.k:61`–`63`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

## K-0666

- Location: `reference-semantics/semantics/methods.k:64`–`64`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

## K-0667

- Location: `reference-semantics/semantics/methods.k:65`–`65`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

## K-0668

- Location: `reference-semantics/semantics/methods.k:66`–`66`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

## K-0669

- Location: `reference-semantics/semantics/methods.k:67`–`67`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

## K-0670

- Location: `reference-semantics/semantics/methods.k:68`–`71`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

## K-0671

- Location: `reference-semantics/semantics/methods.k:72`–`74`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

## K-0672

- Location: `reference-semantics/semantics/methods.k:75`–`75`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

## K-0673

- Location: `reference-semantics/semantics/methods.k:76`–`76`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

## K-0674

- Location: `reference-semantics/semantics/methods.k:77`–`78`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

## K-0675

- Location: `reference-semantics/semantics/methods.k:79`–`81`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

## K-0676

- Location: `reference-semantics/semantics/methods.k:82`–`82`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

## K-0677

- Location: `reference-semantics/semantics/methods.k:83`–`83`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

## K-0678

- Location: `reference-semantics/semantics/methods.k:84`–`84`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

## K-0679

- Location: `reference-semantics/semantics/methods.k:85`–`85`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

## K-0680

- Location: `reference-semantics/semantics/methods.k:86`–`88`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

## K-0681

- Location: `reference-semantics/semantics/methods.k:89`–`93`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

## K-0682

- Location: `reference-semantics/semantics/methods.k:94`–`96`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

## K-0683

- Location: `reference-semantics/semantics/methods.k:97`–`97`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

## K-0684

- Location: `reference-semantics/semantics/methods.k:98`–`98`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

## K-0685

- Location: `reference-semantics/semantics/methods.k:99`–`100`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

## K-0686

- Location: `reference-semantics/semantics/methods.k:101`–`102`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

## K-0687

- Location: `reference-semantics/semantics/methods.k:104`–`105`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

## K-0688

- Location: `reference-semantics/semantics/methods.k:106`–`106`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

## K-0689

- Location: `reference-semantics/semantics/methods.k:107`–`107`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

## K-0690

- Location: `reference-semantics/semantics/methods.k:108`–`108`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

## K-0691

- Location: `reference-semantics/semantics/methods.k:109`–`111`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

## K-0692

- Location: `reference-semantics/semantics/methods.k:112`–`112`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

## K-0693

- Location: `reference-semantics/semantics/methods.k:113`–`113`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

## K-0694

- Location: `reference-semantics/semantics/methods.k:115`–`115`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

## K-0695

- Location: `reference-semantics/semantics/methods.k:116`–`116`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

## K-0696

- Location: `reference-semantics/semantics/methods.k:118`–`118`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

## K-0697

- Location: `reference-semantics/semantics/methods.k:119`–`119`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

## K-0698

- Location: `reference-semantics/semantics/methods.k:121`–`121`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

## K-0699

- Location: `reference-semantics/semantics/methods.k:122`–`122`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

## K-0700

- Location: `reference-semantics/semantics/methods.k:124`–`124`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

## K-0701

- Location: `reference-semantics/semantics/methods.k:125`–`125`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule hasUpper(.IntSeq) => false
```

## K-0702

- Location: `reference-semantics/semantics/methods.k:126`–`126`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

## K-0703

- Location: `reference-semantics/semantics/methods.k:128`–`128`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

## K-0704

- Location: `reference-semantics/semantics/methods.k:129`–`129`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule hasLower(.IntSeq) => false
```

## K-0705

- Location: `reference-semantics/semantics/methods.k:130`–`130`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

## K-0706

- Location: `reference-semantics/semantics/methods.k:132`–`132`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

## K-0707

- Location: `reference-semantics/semantics/methods.k:133`–`133`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule allAlpha(.IntSeq) => true
```

## K-0708

- Location: `reference-semantics/semantics/methods.k:134`–`134`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

## K-0709

- Location: `reference-semantics/semantics/methods.k:136`–`136`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

## K-0710

- Location: `reference-semantics/semantics/methods.k:137`–`137`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule allDigit(.IntSeq) => true
```

## K-0711

- Location: `reference-semantics/semantics/methods.k:138`–`138`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

## K-0712

- Location: `reference-semantics/semantics/methods.k:140`–`140`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= lowerC(Int) [function, total]
```

## K-0713

- Location: `reference-semantics/semantics/methods.k:142`–`142`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

## K-0714

- Location: `reference-semantics/semantics/methods.k:143`–`143`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule lowerC(C:Int) => C         [owise]
```

## K-0715

- Location: `reference-semantics/semantics/methods.k:145`–`145`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= upperC(Int) [function, total]
```

## K-0716

- Location: `reference-semantics/semantics/methods.k:146`–`146`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

## K-0717

- Location: `reference-semantics/semantics/methods.k:147`–`147`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule upperC(C:Int) => C         [owise]
```

## K-0718

- Location: `reference-semantics/semantics/methods.k:149`–`149`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= swapC(Int) [function, total]
```

## K-0719

- Location: `reference-semantics/semantics/methods.k:150`–`150`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

## K-0720

- Location: `reference-semantics/semantics/methods.k:151`–`151`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

## K-0721

- Location: `reference-semantics/semantics/methods.k:152`–`152`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule swapC(C:Int) => C         [owise]
```

## K-0722

- Location: `reference-semantics/semantics/methods.k:154`–`154`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

## K-0723

- Location: `reference-semantics/semantics/methods.k:155`–`155`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapLower(.IntSeq) => .IntSeq
```

## K-0724

- Location: `reference-semantics/semantics/methods.k:156`–`156`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

## K-0725

- Location: `reference-semantics/semantics/methods.k:158`–`158`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

## K-0726

- Location: `reference-semantics/semantics/methods.k:159`–`159`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

## K-0727

- Location: `reference-semantics/semantics/methods.k:160`–`160`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

## K-0728

- Location: `reference-semantics/semantics/methods.k:162`–`162`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

## K-0729

- Location: `reference-semantics/semantics/methods.k:163`–`163`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

## K-0730

- Location: `reference-semantics/semantics/methods.k:164`–`164`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

## K-0731

- Location: `reference-semantics/semantics/methods.k:166`–`166`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

## K-0732

- Location: `reference-semantics/semantics/methods.k:167`–`167`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

## K-0733

- Location: `reference-semantics/semantics/methods.k:168`–`168`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## K-0734

- Location: `reference-semantics/semantics/methods.k:169`–`170`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
endmodule
```

## K-0735

- Location: `reference-semantics/semantics/operators.k:10`–`10`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

## K-0736

- Location: `reference-semantics/semantics/operators.k:12`–`14`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

## K-0737

- Location: `reference-semantics/semantics/operators.k:15`–`15`
- Source class: supplied-fixed
- Entry kind: context
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  context Compare(HOLE, _)
```

## K-0738

- Location: `reference-semantics/semantics/operators.k:16`–`16`
- Source class: supplied-fixed
- Entry kind: context
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

## K-0739

- Location: `reference-semantics/semantics/operators.k:17`–`17`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

## K-0740

- Location: `reference-semantics/semantics/operators.k:19`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

## K-0741

- Location: `reference-semantics/semantics/operators.k:20`–`24`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

## K-0742

- Location: `reference-semantics/semantics/operators.k:25`–`27`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## K-0743

- Location: `reference-semantics/semantics/operators.k:28`–`33`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

## K-0744

- Location: `reference-semantics/semantics/operators.k:34`–`37`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

## K-0745

- Location: `reference-semantics/semantics/operators.k:38`–`42`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

## K-0746

- Location: `reference-semantics/semantics/operators.k:44`–`47`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
endmodule
```

## K-0747

- Location: `reference-semantics/semantics/range.k:9`–`9`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

## K-0748

- Location: `reference-semantics/semantics/range.k:10`–`10`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

## K-0749

- Location: `reference-semantics/semantics/range.k:12`–`12`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

## K-0750

- Location: `reference-semantics/semantics/range.k:13`–`14`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

## K-0751

- Location: `reference-semantics/semantics/range.k:15`–`16`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

## K-0752

- Location: `reference-semantics/semantics/range.k:17`–`18`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

## K-0753

- Location: `reference-semantics/semantics/range.k:20`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

## K-0754

- Location: `reference-semantics/semantics/range.k:23`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
endmodule
```

## K-0755

- Location: `reference-semantics/semantics/set.k:8`–`10`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

## K-0756

- Location: `reference-semantics/semantics/set.k:11`–`11`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

## K-0757

- Location: `reference-semantics/semantics/set.k:12`–`12`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

## K-0758

- Location: `reference-semantics/semantics/set.k:13`–`15`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

## K-0759

- Location: `reference-semantics/semantics/set.k:16`–`17`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

## K-0760

- Location: `reference-semantics/semantics/set.k:18`–`18`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

## K-0761

- Location: `reference-semantics/semantics/set.k:19`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

## K-0762

- Location: `reference-semantics/semantics/set.k:20`–`21`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

## K-0763

- Location: `reference-semantics/semantics/set.k:22`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

## K-0764

- Location: `reference-semantics/semantics/set.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

## K-0765

- Location: `reference-semantics/semantics/set.k:26`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

## K-0766

- Location: `reference-semantics/semantics/set.k:27`–`30`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

## K-0767

- Location: `reference-semantics/semantics/set.k:31`–`31`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

## K-0768

- Location: `reference-semantics/semantics/set.k:32`–`32`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

## K-0769

- Location: `reference-semantics/semantics/set.k:33`–`33`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

## K-0770

- Location: `reference-semantics/semantics/set.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

## K-0771

- Location: `reference-semantics/semantics/set.k:36`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

## K-0772

- Location: `reference-semantics/semantics/set.k:39`–`40`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
endmodule
```

## K-0773

- Location: `reference-semantics/semantics/sort.k:18`–`18`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque ascending sort; material to this theorem and accounted explicitly

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

## K-0774

- Location: `reference-semantics/semantics/sort.k:19`–`19`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

## K-0775

- Location: `reference-semantics/semantics/sort.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

## K-0776

- Location: `reference-semantics/semantics/sort.k:21`–`21`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

## K-0777

- Location: `reference-semantics/semantics/sort.k:22`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

## K-0778

- Location: `reference-semantics/semantics/sort.k:23`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

## K-0779

- Location: `reference-semantics/semantics/sort.k:24`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

## K-0780

- Location: `reference-semantics/semantics/sort.k:26`–`26`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

## K-0781

- Location: `reference-semantics/semantics/sort.k:27`–`27`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

## K-0782

- Location: `reference-semantics/semantics/sort.k:28`–`28`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

## K-0783

- Location: `reference-semantics/semantics/sort.k:29`–`30`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

## K-0784

- Location: `reference-semantics/semantics/sort.k:31`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: concrete, owise
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

## K-0785

- Location: `reference-semantics/semantics/sort.k:36`–`39`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

## K-0786

- Location: `reference-semantics/semantics/sort.k:40`–`48`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority, concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0787

- Location: `reference-semantics/semantics/sort.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total, no-evaluators, symbol
- Audit disposition: ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; not reached by this integer-list program

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

## K-0788

- Location: `reference-semantics/semantics/sort.k:51`–`52`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

## K-0789

- Location: `reference-semantics/semantics/sort.k:53`–`53`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

## K-0790

- Location: `reference-semantics/semantics/sort.k:54`–`54`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

## K-0791

- Location: `reference-semantics/semantics/sort.k:55`–`55`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

## K-0792

- Location: `reference-semantics/semantics/sort.k:57`–`57`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

## K-0793

- Location: `reference-semantics/semantics/sort.k:58`–`58`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule condRev(S:ValSeq, false) => S
```

## K-0794

- Location: `reference-semantics/semantics/sort.k:59`–`59`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

## K-0795

- Location: `reference-semantics/semantics/sort.k:61`–`62`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

## K-0796

- Location: `reference-semantics/semantics/sort.k:63`–`64`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

## K-0797

- Location: `reference-semantics/semantics/sort.k:65`–`72`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: total, concrete
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
endmodule
```

## K-0798

- Location: `reference-semantics/semantics/str.k:8`–`8`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

## K-0799

- Location: `reference-semantics/semantics/str.k:9`–`12`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

## K-0800

- Location: `reference-semantics/semantics/str.k:13`–`13`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

## K-0801

- Location: `reference-semantics/semantics/str.k:14`–`14`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

## K-0802

- Location: `reference-semantics/semantics/str.k:15`–`15`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strToCodes("") => .IntSeq
```

## K-0803

- Location: `reference-semantics/semantics/str.k:16`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

## K-0804

- Location: `reference-semantics/semantics/str.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

## K-0805

- Location: `reference-semantics/semantics/str.k:21`–`21`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

## K-0806

- Location: `reference-semantics/semantics/str.k:22`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

## K-0807

- Location: `reference-semantics/semantics/str.k:24`–`24`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

## K-0808

- Location: `reference-semantics/semantics/str.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

## K-0809

- Location: `reference-semantics/semantics/str.k:26`–`28`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

## K-0810

- Location: `reference-semantics/semantics/str.k:29`–`29`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

## K-0811

- Location: `reference-semantics/semantics/str.k:30`–`30`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

## K-0812

- Location: `reference-semantics/semantics/str.k:32`–`32`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

## K-0813

- Location: `reference-semantics/semantics/str.k:33`–`33`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

## K-0814

- Location: `reference-semantics/semantics/str.k:34`–`34`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## K-0815

- Location: `reference-semantics/semantics/str.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

## K-0816

- Location: `reference-semantics/semantics/str.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

## K-0817

- Location: `reference-semantics/semantics/str.k:38`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

## K-0818

- Location: `reference-semantics/semantics/str.k:39`–`39`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

## K-0819

- Location: `reference-semantics/semantics/str.k:40`–`47`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

## K-0820

- Location: `reference-semantics/semantics/str.k:48`–`48`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

## K-0821

- Location: `reference-semantics/semantics/str.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

## K-0822

- Location: `reference-semantics/semantics/str.k:50`–`50`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

## K-0823

- Location: `reference-semantics/semantics/str.k:51`–`51`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## K-0824

- Location: `reference-semantics/semantics/str.k:52`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

## K-0825

- Location: `reference-semantics/semantics/str.k:53`–`53`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

## K-0826

- Location: `reference-semantics/semantics/str.k:54`–`54`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

## K-0827

- Location: `reference-semantics/semantics/str.k:56`–`56`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## K-0828

- Location: `reference-semantics/semantics/str.k:57`–`57`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

## K-0829

- Location: `reference-semantics/semantics/str.k:58`–`58`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

## K-0830

- Location: `reference-semantics/semantics/str.k:59`–`60`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
endmodule
```

## K-0831

- Location: `reference-semantics/semantics/subscript.k:11`–`11`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

## K-0832

- Location: `reference-semantics/semantics/subscript.k:12`–`12`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

## K-0833

- Location: `reference-semantics/semantics/subscript.k:13`–`14`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

## K-0834

- Location: `reference-semantics/semantics/subscript.k:16`–`16`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

## K-0835

- Location: `reference-semantics/semantics/subscript.k:17`–`17`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

## K-0836

- Location: `reference-semantics/semantics/subscript.k:18`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

## K-0837

- Location: `reference-semantics/semantics/subscript.k:21`–`21`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

## K-0838

- Location: `reference-semantics/semantics/subscript.k:22`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## K-0839

- Location: `reference-semantics/semantics/subscript.k:23`–`26`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: strict
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

## K-0840

- Location: `reference-semantics/semantics/subscript.k:27`–`27`
- Source class: supplied-fixed
- Entry kind: context
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  context Subscript(HOLE, _)
```

## K-0841

- Location: `reference-semantics/semantics/subscript.k:28`–`30`
- Source class: supplied-fixed
- Entry kind: context
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

## K-0842

- Location: `reference-semantics/semantics/subscript.k:31`–`33`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## K-0843

- Location: `reference-semantics/semantics/subscript.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

## K-0844

- Location: `reference-semantics/semantics/subscript.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

## K-0845

- Location: `reference-semantics/semantics/subscript.k:38`–`38`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## K-0846

- Location: `reference-semantics/semantics/subscript.k:39`–`39`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## K-0847

- Location: `reference-semantics/semantics/subscript.k:40`–`43`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

## K-0848

- Location: `reference-semantics/semantics/subscript.k:44`–`47`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

## K-0849

- Location: `reference-semantics/semantics/subscript.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax OptInt ::= "noB" | someB(Int)
```

## K-0850

- Location: `reference-semantics/semantics/subscript.k:50`–`50`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

## K-0851

- Location: `reference-semantics/semantics/subscript.k:51`–`51`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

## K-0852

- Location: `reference-semantics/semantics/subscript.k:52`–`52`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

## K-0853

- Location: `reference-semantics/semantics/subscript.k:54`–`54`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

## K-0854

- Location: `reference-semantics/semantics/subscript.k:55`–`55`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

## K-0855

- Location: `reference-semantics/semantics/subscript.k:56`–`57`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

## K-0856

- Location: `reference-semantics/semantics/subscript.k:58`–`60`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

## K-0857

- Location: `reference-semantics/semantics/subscript.k:61`–`61`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

## K-0858

- Location: `reference-semantics/semantics/subscript.k:63`–`63`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

## K-0859

- Location: `reference-semantics/semantics/subscript.k:64`–`65`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## K-0860

- Location: `reference-semantics/semantics/subscript.k:66`–`67`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## K-0861

- Location: `reference-semantics/semantics/subscript.k:68`–`71`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

## K-0862

- Location: `reference-semantics/semantics/subscript.k:72`–`72`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

## K-0863

- Location: `reference-semantics/semantics/subscript.k:73`–`73`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStep(noB)          => 1
```

## K-0864

- Location: `reference-semantics/semantics/subscript.k:74`–`74`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStep(someB(S:Int)) => S
```

## K-0865

- Location: `reference-semantics/semantics/subscript.k:76`–`76`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

## K-0866

- Location: `reference-semantics/semantics/subscript.k:77`–`78`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

## K-0867

- Location: `reference-semantics/semantics/subscript.k:79`–`80`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

## K-0868

- Location: `reference-semantics/semantics/subscript.k:81`–`81`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## K-0869

- Location: `reference-semantics/semantics/subscript.k:83`–`83`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

## K-0870

- Location: `reference-semantics/semantics/subscript.k:84`–`85`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

## K-0871

- Location: `reference-semantics/semantics/subscript.k:86`–`87`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

## K-0872

- Location: `reference-semantics/semantics/subscript.k:88`–`88`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## K-0873

- Location: `reference-semantics/semantics/subscript.k:90`–`90`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

## K-0874

- Location: `reference-semantics/semantics/subscript.k:91`–`92`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

## K-0875

- Location: `reference-semantics/semantics/subscript.k:93`–`94`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

## K-0876

- Location: `reference-semantics/semantics/subscript.k:96`–`96`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

## K-0877

- Location: `reference-semantics/semantics/subscript.k:97`–`98`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

## K-0878

- Location: `reference-semantics/semantics/subscript.k:99`–`100`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

## K-0879

- Location: `reference-semantics/semantics/subscript.k:102`–`102`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

## K-0880

- Location: `reference-semantics/semantics/subscript.k:103`–`104`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

## K-0881

- Location: `reference-semantics/semantics/subscript.k:105`–`108`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

## K-0882

- Location: `reference-semantics/semantics/subscript.k:109`–`109`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

## K-0883

- Location: `reference-semantics/semantics/subscript.k:110`–`112`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## K-0884

- Location: `reference-semantics/semantics/subscript.k:113`–`114`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## K-0885

- Location: `reference-semantics/semantics/subscript.k:116`–`116`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

## K-0886

- Location: `reference-semantics/semantics/subscript.k:117`–`119`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## K-0887

- Location: `reference-semantics/semantics/subscript.k:120`–`122`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
endmodule
```

## K-0888

- Location: `reference-semantics/semantics/syntax.k:9`–`30`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: macro, strict, seqstrict
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0889

- Location: `reference-semantics/semantics/syntax.k:32`–`32`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

## K-0890

- Location: `reference-semantics/semantics/syntax.k:33`–`33`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

## K-0891

- Location: `reference-semantics/semantics/syntax.k:34`–`34`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Entries  ::= List{Entry, ","}
```

## K-0892

- Location: `reference-semantics/semantics/syntax.k:35`–`35`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

## K-0893

- Location: `reference-semantics/semantics/syntax.k:36`–`36`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax CompFors ::= List{CompFor, ""}
```

## K-0894

- Location: `reference-semantics/semantics/syntax.k:37`–`37`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Exprs    ::= List{Expr, ","}
```

## K-0895

- Location: `reference-semantics/semantics/syntax.k:38`–`38`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

## K-0896

- Location: `reference-semantics/semantics/syntax.k:39`–`39`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Bound    ::= Expr | "NoBound"
```

## K-0897

- Location: `reference-semantics/semantics/syntax.k:41`–`54`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: strict
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

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

## K-0898

- Location: `reference-semantics/semantics/syntax.k:56`–`56`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Stmts      ::= List{Stmt, ""}
```

## K-0899

- Location: `reference-semantics/semantics/syntax.k:57`–`57`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

## K-0900

- Location: `reference-semantics/semantics/syntax.k:58`–`58`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

## K-0901

- Location: `reference-semantics/semantics/syntax.k:59`–`59`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

## K-0902

- Location: `reference-semantics/semantics/syntax.k:60`–`60`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ParamNames ::= List{String, ","}
```

## K-0903

- Location: `reference-semantics/semantics/syntax.k:61`–`62`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Module     ::= "Module" "(" Stmts ")"
endmodule
```

## K-0904

- Location: `reference-semantics/semantics/tuple.k:10`–`10`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

## K-0905

- Location: `reference-semantics/semantics/tuple.k:11`–`13`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

## K-0906

- Location: `reference-semantics/semantics/tuple.k:14`–`14`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax ApplyK ::= "toTuple"
```

## K-0907

- Location: `reference-semantics/semantics/tuple.k:15`–`15`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

## K-0908

- Location: `reference-semantics/semantics/tuple.k:16`–`16`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

## K-0909

- Location: `reference-semantics/semantics/tuple.k:18`–`19`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

## K-0910

- Location: `reference-semantics/semantics/tuple.k:20`–`20`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

## K-0911

- Location: `reference-semantics/semantics/tuple.k:21`–`22`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

## K-0912

- Location: `reference-semantics/semantics/tuple.k:23`–`23`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

## K-0913

- Location: `reference-semantics/semantics/tuple.k:24`–`24`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: function
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

## K-0914

- Location: `reference-semantics/semantics/tuple.k:25`–`25`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

## K-0915

- Location: `reference-semantics/semantics/tuple.k:26`–`27`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

## K-0916

- Location: `reference-semantics/semantics/tuple.k:28`–`30`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

## K-0917

- Location: `reference-semantics/semantics/tuple.k:31`–`31`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

## K-0918

- Location: `reference-semantics/semantics/tuple.k:32`–`34`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## K-0919

- Location: `reference-semantics/semantics/tuple.k:35`–`41`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## K-0920

- Location: `reference-semantics/semantics/tuple.k:42`–`42`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## K-0921

- Location: `reference-semantics/semantics/tuple.k:43`–`43`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## K-0922

- Location: `reference-semantics/semantics/tuple.k:44`–`48`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

## K-0923

- Location: `reference-semantics/semantics/tuple.k:49`–`49`
- Source class: supplied-fixed
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

## K-0924

- Location: `reference-semantics/semantics/tuple.k:50`–`50`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## K-0925

- Location: `reference-semantics/semantics/tuple.k:51`–`51`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## K-0926

- Location: `reference-semantics/semantics/tuple.k:52`–`54`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## K-0927

- Location: `reference-semantics/semantics/tuple.k:55`–`56`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

## K-0928

- Location: `reference-semantics/semantics/tuple.k:57`–`58`
- Source class: supplied-fixed
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no task-specific conclusion and no adverse interaction found

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
endmodule
```

## K-0929

- Location: `verification.k:9`–`9`
- Source class: proof-local
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  syntax Stmts ::= "byLengthBody" [function, total]
```

## K-0930

- Location: `verification.k:10`–`47`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule byLengthBody
    => Assign(
         Name("names"),
         ListExpr(
           Str("One"), Str("Two"), Str("Three"), Str("Four"),
           Str("Five"), Str("Six"), Str("Seven"), Str("Eight"),
           Str("Nine")))
       Assign(Name("values"), ListExpr(.Exprs))
       For(
         Name("value"),
         Name("arr"),
         If(
           BoolOp(
             "and",
             Compare(Name("value"), CmpOp(">=", Int(1))),
             Compare(Name("value"), CmpOp("<=", Int(9)))),
           Expr(
             Call(
               Attribute(Name("values"), "append"),
               Name("value"))),
           .Stmts))
       Assign(
         Name("values"),
         Call(
           Name("sorted"),
           Name("values"),
           KwArg("reverse", Bool(true))))
       Assign(Name("result"), ListExpr(.Exprs))
       For(
         Name("value"),
         Name("values"),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Subscript(
               Name("names"),
               BinOp("-", Name("value"), Int(1))))))
       Return(Name("result"))
```

## K-0931

- Location: `verification.k:49`–`49`
- Source class: proof-local
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  syntax Val ::= "byLengthClosure" [function, total]
```

## K-0932

- Location: `verification.k:50`–`53`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule byLengthClosure => closureVal("arr", byLengthBody, 0)

  // Embed an arbitrary sequence of mathematical integers as Python values.
  // Quantifying IS:IntSeq in spec.k therefore covers every finite integer list.
```

## K-0933

- Location: `verification.k:54`–`54`
- Source class: proof-local
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  syntax ValSeq ::= intVals(IntSeq) [function, total]
```

## K-0934

- Location: `verification.k:55`–`55`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule intVals(.IntSeq) => .ValSeq
```

## K-0935

- Location: `verification.k:56`–`59`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule intVals(iCons(I:Int, IS:IntSeq)) => vCons(I, intVals(IS))

  // Contract-level filtering: retain exactly the values in [1, 9], preserving
  // duplicates and their relative order before the trusted sort.
```

## K-0936

- Location: `verification.k:60`–`60`
- Source class: proof-local
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: LIMITATION—[total] domain is broader than the constructor equations; uses reached by the target are integer-only

```k
  syntax ValSeq ::= filterDigits(ValSeq) [function, total]
```

## K-0937

- Location: `verification.k:61`–`61`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule filterDigits(.ValSeq) => .ValSeq
```

## K-0938

- Location: `verification.k:62`–`64`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule filterDigits(vCons(I:Int, REST:ValSeq))
    => vCons(I, filterDigits(REST))
    requires I >=Int 1 andBool I <=Int 9
```

## K-0939

- Location: `verification.k:65`–`67`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule filterDigits(vCons(I:Int, REST:ValSeq))
    => filterDigits(REST)
    requires I <Int 1 orBool I >Int 9
```

## K-0940

- Location: `verification.k:69`–`69`
- Source class: proof-local
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  syntax ValSeq ::= "nameTable" [function, total]
```

## K-0941

- Location: `verification.k:70`–`81`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule nameTable
    => vCons(str(strToCodes("One")),
       vCons(str(strToCodes("Two")),
       vCons(str(strToCodes("Three")),
       vCons(str(strToCodes("Four")),
       vCons(str(strToCodes("Five")),
       vCons(str(strToCodes("Six")),
       vCons(str(strToCodes("Seven")),
       vCons(str(strToCodes("Eight")),
       vCons(str(strToCodes("Nine")), .ValSeq)))))))))

  // This is precisely names[value - 1] lifted pointwise to a value sequence.
```

## K-0942

- Location: `verification.k:82`–`82`
- Source class: proof-local
- Entry kind: syntax
- Attribute flags: function, total
- Audit disposition: LIMITATION—[total] domain is broader than the constructor equations; uses reached by the target are integer-only

```k
  syntax ValSeq ::= tableNames(ValSeq) [function, total]
```

## K-0943

- Location: `verification.k:83`–`83`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule tableNames(.ValSeq) => .ValSeq
```

## K-0944

- Location: `verification.k:84`–`88`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule tableNames(vCons(I:Int, REST:ValSeq))
    => vCons(valSeqAt(nameTable, I -Int 1), tableNames(REST))

  // Observe the structure of a returned heap list so that the postcondition
  // states the actual Python return value rather than an allocation address.
```

## K-0945

- Location: `verification.k:89`–`89`
- Source class: proof-local
- Entry kind: syntax
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  syntax KItem ::= "#observeList"
```

## K-0946

- Location: `verification.k:90`–`97`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: none
- Audit disposition: ACCEPTED LOCALLY—truthful constructor definition, guarded mathematical equation, or post-execution observation

```k
  rule <k> ref(H:Int) ~> #observeList => list(VS) ... </k>
       <heap> ... H |-> list(VS:ValSeq) ... </heap>

  // Symbolic summaries for the two source-level loops.  The supplied
  // semantics intentionally leaves sortVS opaque during proof, so a later
  // iteration over revVS(sortVS(...)) cannot constructor-unfold.  These exact
  // AST rules expose the loops' standard filter/map folds while leaving
  // sorted() itself governed by MPY-SORT.
```

## K-0947

- Location: `verification.k:98`–`124`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: REJECT—unsound operational bridge; arbitrary-continuation integer-list counterexample is machine-checked in 04-bridge-witnesses.log

```k
  rule <k>
         For(
           Name("value"),
           list(VS:ValSeq),
           If(
             BoolOp(
               "and",
               Compare(Name("value"), CmpOp(">=", Int(1))),
               Compare(Name("value"), CmpOp("<=", Int(9)))),
             Expr(
               Call(
                 Attribute(Name("values"), "append"),
                 Name("value"))),
             .Stmts))
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap>
         ...
         HV:Int |-> (list(.ValSeq) => list(filterDigits(VS)))
         ...
       </heap>
    requires "values" in_keys(M)
     andBool {M["values"]}:>Val ==K ref(HV)
    [priority(40)]
```

## K-0948

- Location: `verification.k:126`–`153`
- Source class: proof-local
- Entry kind: rule
- Attribute flags: priority
- Audit disposition: REJECT—unsound operational bridge; arbitrary-continuation integer-list counterexample is machine-checked in 04-bridge-witnesses.log

```k
  rule <k>
         For(
           Name("value"),
           list(VS:ValSeq),
           Expr(
             Call(
               Attribute(Name("result"), "append"),
               Subscript(
                 Name("names"),
                 BinOp("-", Name("value"), Int(1))))))
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap>
         ...
         HN:Int |-> list(NAMES:ValSeq)
         HR:Int |-> (list(.ValSeq) => list(tableNames(VS)))
         ...
       </heap>
    requires "names" in_keys(M)
     andBool "result" in_keys(M)
     andBool {M["names"]}:>Val ==K ref(HN)
     andBool {M["result"]}:>Val ==K ref(HR)
     andBool NAMES ==K nameTable
    [priority(40)]
endmodule
```

## K-0949

- Location: `spec.k:9`–`35`
- Source class: target-spec
- Entry kind: claim
- Attribute flags: none
- Audit disposition: TARGET OBLIGATION—adequacy and non-vacuity reviewed separately

```k
  claim
    <k>
      #applyK(
        toCall(byLengthClosure),
        (list(intVals(IS:IntSeq)), .Vals))
      ~> #observeList
    =>
      list(
        tableNames(
          revVS(
            sortVS(
              filterDigits(
                intVals(IS))))))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
```


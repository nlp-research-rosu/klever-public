# Exhaustive local K source inventory

Generated from the clean scratch source copy. Each row below is one local source statement beginning with `requires`, `module`, `endmodule`, `imports`, `syntax`, `configuration`, `context`, `rule`, `claim`, or `alias`. Continuation lines, guards, cells, and attributes are retained in the row.

## Counts

- Total records: 1140
- Kind counts: `{'claim': 11, 'configuration': 1, 'context': 5, 'endmodule': 37, 'imports': 98, 'module': 37, 'requires': 25, 'rule': 698, 'syntax': 228}`
- Attribute/class counts: `{'concrete': 36, 'function': 146, 'macro': 4, 'none': 290, 'opaque/no-evaluators': 22, 'ordinary-semantic-rule': 663, 'owise': 26, 'priority': 45, 'strictness': 2, 'symbol': 25, 'total': 107}`

### Records by file

- `reference-semantics/semantics.k`: 50
- `reference-semantics/semantics/assert.k`: 6
- `reference-semantics/semantics/bool.k`: 17
- `reference-semantics/semantics/builtins.k`: 184
- `reference-semantics/semantics/call.k`: 29
- `reference-semantics/semantics/comprehension.k`: 17
- `reference-semantics/semantics/concrete.k`: 24
- `reference-semantics/semantics/controls.k`: 42
- `reference-semantics/semantics/core.k`: 93
- `reference-semantics/semantics/dict.k`: 46
- `reference-semantics/semantics/float.k`: 160
- `reference-semantics/semantics/functions.k`: 22
- `reference-semantics/semantics/int.k`: 20
- `reference-semantics/semantics/iter.k`: 4
- `reference-semantics/semantics/list.k`: 37
- `reference-semantics/semantics/methods.k`: 108
- `reference-semantics/semantics/operators.k`: 16
- `reference-semantics/semantics/range.k`: 12
- `reference-semantics/semantics/set.k`: 21
- `reference-semantics/semantics/sort.k`: 29
- `reference-semantics/semantics/str.k`: 37
- `reference-semantics/semantics/subscript.k`: 60
- `reference-semantics/semantics/syntax.k`: 22
- `reference-semantics/semantics/tuple.k`: 31
- `spec.k`: 45
- `verification.k`: 8

## Row-by-row ledger

### K-0001 — `reference-semantics/semantics/assert.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-ASSERT
```

### K-0002 — `reference-semantics/semantics/assert.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0003 — `reference-semantics/semantics/assert.k:6`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### K-0004 — `reference-semantics/semantics/assert.k:8`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### K-0005 — `reference-semantics/semantics/assert.k:13`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0006 — `reference-semantics/semantics/assert.k:16`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0007 — `reference-semantics/semantics/bool.k:5`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-BOOL
```

### K-0008 — `reference-semantics/semantics/bool.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0009 — `reference-semantics/semantics/bool.k:8`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### K-0010 — `reference-semantics/semantics/bool.k:10`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### K-0011 — `reference-semantics/semantics/bool.k:11`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### K-0012 — `reference-semantics/semantics/bool.k:16`

- Kind: `context`
- Flags: `none`
- Decision: evaluation-order context checked

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### K-0013 — `reference-semantics/semantics/bool.k:17`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### K-0014 — `reference-semantics/semantics/bool.k:18`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### K-0015 — `reference-semantics/semantics/bool.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### K-0016 — `reference-semantics/semantics/bool.k:22`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### K-0017 — `reference-semantics/semantics/bool.k:24`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

### K-0018 — `reference-semantics/semantics/bool.k:29`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### K-0019 — `reference-semantics/semantics/bool.k:31`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K-0020 — `reference-semantics/semantics/bool.k:35`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K-0021 — `reference-semantics/semantics/bool.k:39`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K-0022 — `reference-semantics/semantics/bool.k:43`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K-0023 — `reference-semantics/semantics/bool.k:47`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0024 — `reference-semantics/semantics/builtins.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-BUILTINS
```

### K-0025 — `reference-semantics/semantics/builtins.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0026 — `reference-semantics/semantics/builtins.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-STR
```

### K-0027 — `reference-semantics/semantics/builtins.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-SET
```

### K-0028 — `reference-semantics/semantics/builtins.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-0029 — `reference-semantics/semantics/builtins.k:8`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-RANGE
```

### K-0030 — `reference-semantics/semantics/builtins.k:9`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-INT
```

### K-0031 — `reference-semantics/semantics/builtins.k:10`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-METHODS
```

### K-0032 — `reference-semantics/semantics/builtins.k:17`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### K-0033 — `reference-semantics/semantics/builtins.k:20`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= seqLen(Val) [function]
```

### K-0034 — `reference-semantics/semantics/builtins.k:21`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### K-0035 — `reference-semantics/semantics/builtins.k:22`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### K-0036 — `reference-semantics/semantics/builtins.k:23`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### K-0037 — `reference-semantics/semantics/builtins.k:24`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### K-0038 — `reference-semantics/semantics/builtins.k:25`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### K-0039 — `reference-semantics/semantics/builtins.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### K-0040 — `reference-semantics/semantics/builtins.k:32`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### K-0041 — `reference-semantics/semantics/builtins.k:33`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### K-0042 — `reference-semantics/semantics/builtins.k:34`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### K-0043 — `reference-semantics/semantics/builtins.k:35`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### K-0044 — `reference-semantics/semantics/builtins.k:36`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### K-0045 — `reference-semantics/semantics/builtins.k:37`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### K-0046 — `reference-semantics/semantics/builtins.k:38`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### K-0047 — `reference-semantics/semantics/builtins.k:41`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### K-0048 — `reference-semantics/semantics/builtins.k:44`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### K-0049 — `reference-semantics/semantics/builtins.k:47`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### K-0050 — `reference-semantics/semantics/builtins.k:48`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### K-0051 — `reference-semantics/semantics/builtins.k:49`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### K-0052 — `reference-semantics/semantics/builtins.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K-0053 — `reference-semantics/semantics/builtins.k:54`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= intOf(Val) [function]
```

### K-0054 — `reference-semantics/semantics/builtins.k:55`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intOf(I:Int)  => I
```

### K-0055 — `reference-semantics/semantics/builtins.k:56`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### K-0056 — `reference-semantics/semantics/builtins.k:59`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### K-0057 — `reference-semantics/semantics/builtins.k:60`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### K-0058 — `reference-semantics/semantics/builtins.k:61`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### K-0059 — `reference-semantics/semantics/builtins.k:62`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### K-0060 — `reference-semantics/semantics/builtins.k:64`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### K-0061 — `reference-semantics/semantics/builtins.k:67`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### K-0062 — `reference-semantics/semantics/builtins.k:68`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### K-0063 — `reference-semantics/semantics/builtins.k:69`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### K-0064 — `reference-semantics/semantics/builtins.k:70`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### K-0065 — `reference-semantics/semantics/builtins.k:72`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

### K-0066 — `reference-semantics/semantics/builtins.k:76`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### K-0067 — `reference-semantics/semantics/builtins.k:77`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### K-0068 — `reference-semantics/semantics/builtins.k:78`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K-0069 — `reference-semantics/semantics/builtins.k:80`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### K-0070 — `reference-semantics/semantics/builtins.k:81`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### K-0071 — `reference-semantics/semantics/builtins.k:82`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K-0072 — `reference-semantics/semantics/builtins.k:86`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### K-0073 — `reference-semantics/semantics/builtins.k:87`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### K-0074 — `reference-semantics/semantics/builtins.k:88`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K-0075 — `reference-semantics/semantics/builtins.k:90`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### K-0076 — `reference-semantics/semantics/builtins.k:91`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### K-0077 — `reference-semantics/semantics/builtins.k:92`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K-0078 — `reference-semantics/semantics/builtins.k:97`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### K-0079 — `reference-semantics/semantics/builtins.k:98`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### K-0080 — `reference-semantics/semantics/builtins.k:99`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule maxVals(M:Int, .Vals)           => M
```

### K-0081 — `reference-semantics/semantics/builtins.k:100`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### K-0082 — `reference-semantics/semantics/builtins.k:102`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### K-0083 — `reference-semantics/semantics/builtins.k:103`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### K-0084 — `reference-semantics/semantics/builtins.k:104`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule minVals(M:Int, .Vals)           => M
```

### K-0085 — `reference-semantics/semantics/builtins.k:105`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### K-0086 — `reference-semantics/semantics/builtins.k:108`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

### K-0087 — `reference-semantics/semantics/builtins.k:111`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### K-0088 — `reference-semantics/semantics/builtins.k:114`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### K-0089 — `reference-semantics/semantics/builtins.k:115`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### K-0090 — `reference-semantics/semantics/builtins.k:116`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### K-0091 — `reference-semantics/semantics/builtins.k:117`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### K-0092 — `reference-semantics/semantics/builtins.k:118`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### K-0093 — `reference-semantics/semantics/builtins.k:119`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

### K-0094 — `reference-semantics/semantics/builtins.k:124`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### K-0095 — `reference-semantics/semantics/builtins.k:126`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### K-0096 — `reference-semantics/semantics/builtins.k:127`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### K-0097 — `reference-semantics/semantics/builtins.k:128`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### K-0098 — `reference-semantics/semantics/builtins.k:132`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### K-0099 — `reference-semantics/semantics/builtins.k:134`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### K-0100 — `reference-semantics/semantics/builtins.k:135`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### K-0101 — `reference-semantics/semantics/builtins.k:136`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### K-0102 — `reference-semantics/semantics/builtins.k:137`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### K-0103 — `reference-semantics/semantics/builtins.k:140`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### K-0104 — `reference-semantics/semantics/builtins.k:143`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### K-0105 — `reference-semantics/semantics/builtins.k:144`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

### K-0106 — `reference-semantics/semantics/builtins.k:148`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### K-0107 — `reference-semantics/semantics/builtins.k:149`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### K-0108 — `reference-semantics/semantics/builtins.k:152`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

### K-0109 — `reference-semantics/semantics/builtins.k:156`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### K-0110 — `reference-semantics/semantics/builtins.k:158`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### K-0111 — `reference-semantics/semantics/builtins.k:159`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### K-0112 — `reference-semantics/semantics/builtins.k:160`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### K-0113 — `reference-semantics/semantics/builtins.k:163`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### K-0114 — `reference-semantics/semantics/builtins.k:164`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### K-0115 — `reference-semantics/semantics/builtins.k:167`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### K-0116 — `reference-semantics/semantics/builtins.k:169`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### K-0117 — `reference-semantics/semantics/builtins.k:170`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### K-0118 — `reference-semantics/semantics/builtins.k:171`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### K-0119 — `reference-semantics/semantics/builtins.k:173`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### K-0120 — `reference-semantics/semantics/builtins.k:174`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### K-0121 — `reference-semantics/semantics/builtins.k:177`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### K-0122 — `reference-semantics/semantics/builtins.k:178`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### K-0123 — `reference-semantics/semantics/builtins.k:179`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

### K-0124 — `reference-semantics/semantics/builtins.k:187`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### K-0125 — `reference-semantics/semantics/builtins.k:188`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### K-0126 — `reference-semantics/semantics/builtins.k:189`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### K-0127 — `reference-semantics/semantics/builtins.k:192`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### K-0128 — `reference-semantics/semantics/builtins.k:194`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### K-0129 — `reference-semantics/semantics/builtins.k:195`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K-0130 — `reference-semantics/semantics/builtins.k:196`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### K-0131 — `reference-semantics/semantics/builtins.k:197`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### K-0132 — `reference-semantics/semantics/builtins.k:198`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### K-0133 — `reference-semantics/semantics/builtins.k:199`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### K-0134 — `reference-semantics/semantics/builtins.k:200`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### K-0135 — `reference-semantics/semantics/builtins.k:201`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### K-0136 — `reference-semantics/semantics/builtins.k:203`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### K-0137 — `reference-semantics/semantics/builtins.k:204`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### K-0138 — `reference-semantics/semantics/builtins.k:205`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### K-0139 — `reference-semantics/semantics/builtins.k:206`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### K-0140 — `reference-semantics/semantics/builtins.k:207`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### K-0141 — `reference-semantics/semantics/builtins.k:208`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### K-0142 — `reference-semantics/semantics/builtins.k:209`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### K-0143 — `reference-semantics/semantics/builtins.k:210`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### K-0144 — `reference-semantics/semantics/builtins.k:211`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### K-0145 — `reference-semantics/semantics/builtins.k:212`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### K-0146 — `reference-semantics/semantics/builtins.k:214`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### K-0147 — `reference-semantics/semantics/builtins.k:216`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### K-0148 — `reference-semantics/semantics/builtins.k:217`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### K-0149 — `reference-semantics/semantics/builtins.k:218`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### K-0150 — `reference-semantics/semantics/builtins.k:219`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### K-0151 — `reference-semantics/semantics/builtins.k:221`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### K-0152 — `reference-semantics/semantics/builtins.k:223`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### K-0153 — `reference-semantics/semantics/builtins.k:225`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### K-0154 — `reference-semantics/semantics/builtins.k:226`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### K-0155 — `reference-semantics/semantics/builtins.k:227`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### K-0156 — `reference-semantics/semantics/builtins.k:228`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### K-0157 — `reference-semantics/semantics/builtins.k:230`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### K-0158 — `reference-semantics/semantics/builtins.k:231`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### K-0159 — `reference-semantics/semantics/builtins.k:232`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### K-0160 — `reference-semantics/semantics/builtins.k:233`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### K-0161 — `reference-semantics/semantics/builtins.k:234`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### K-0162 — `reference-semantics/semantics/builtins.k:235`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### K-0163 — `reference-semantics/semantics/builtins.k:236`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### K-0164 — `reference-semantics/semantics/builtins.k:238`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### K-0165 — `reference-semantics/semantics/builtins.k:239`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### K-0166 — `reference-semantics/semantics/builtins.k:240`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### K-0167 — `reference-semantics/semantics/builtins.k:241`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### K-0168 — `reference-semantics/semantics/builtins.k:243`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### K-0169 — `reference-semantics/semantics/builtins.k:244`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### K-0170 — `reference-semantics/semantics/builtins.k:245`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### K-0171 — `reference-semantics/semantics/builtins.k:246`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### K-0172 — `reference-semantics/semantics/builtins.k:247`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### K-0173 — `reference-semantics/semantics/builtins.k:248`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### K-0174 — `reference-semantics/semantics/builtins.k:250`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### K-0175 — `reference-semantics/semantics/builtins.k:251`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K-0176 — `reference-semantics/semantics/builtins.k:252`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K-0177 — `reference-semantics/semantics/builtins.k:253`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K-0178 — `reference-semantics/semantics/builtins.k:254`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K-0179 — `reference-semantics/semantics/builtins.k:255`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### K-0180 — `reference-semantics/semantics/builtins.k:256`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### K-0181 — `reference-semantics/semantics/builtins.k:257`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### K-0182 — `reference-semantics/semantics/builtins.k:260`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### K-0183 — `reference-semantics/semantics/builtins.k:263`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### K-0184 — `reference-semantics/semantics/builtins.k:265`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### K-0185 — `reference-semantics/semantics/builtins.k:266`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### K-0186 — `reference-semantics/semantics/builtins.k:267`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### K-0187 — `reference-semantics/semantics/builtins.k:268`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### K-0188 — `reference-semantics/semantics/builtins.k:269`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### K-0189 — `reference-semantics/semantics/builtins.k:270`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### K-0190 — `reference-semantics/semantics/builtins.k:271`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### K-0191 — `reference-semantics/semantics/builtins.k:272`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### K-0192 — `reference-semantics/semantics/builtins.k:273`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### K-0193 — `reference-semantics/semantics/builtins.k:274`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### K-0194 — `reference-semantics/semantics/builtins.k:279`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= "#md5"
```

### K-0195 — `reference-semantics/semantics/builtins.k:280`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### K-0196 — `reference-semantics/semantics/builtins.k:282`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### K-0197 — `reference-semantics/semantics/builtins.k:283`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= md5Obj(IntSeq)
```

### K-0198 — `reference-semantics/semantics/builtins.k:284`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### K-0199 — `reference-semantics/semantics/builtins.k:285`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### K-0200 — `reference-semantics/semantics/builtins.k:291`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### K-0201 — `reference-semantics/semantics/builtins.k:292`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### K-0202 — `reference-semantics/semantics/builtins.k:293`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### K-0203 — `reference-semantics/semantics/builtins.k:294`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isIntV(_:Int)         => true
```

### K-0204 — `reference-semantics/semantics/builtins.k:295`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isIntV(_:Val)         => false [owise]
```

### K-0205 — `reference-semantics/semantics/builtins.k:296`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isStrV(str(_:IntSeq)) => true
```

### K-0206 — `reference-semantics/semantics/builtins.k:297`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isStrV(_:Val)         => false [owise]
```

### K-0207 — `reference-semantics/semantics/builtins.k:298`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0208 — `reference-semantics/semantics/call.k:10`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-CALL
```

### K-0209 — `reference-semantics/semantics/call.k:11`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-METHODS
```

### K-0210 — `reference-semantics/semantics/call.k:12`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-BUILTINS
```

### K-0211 — `reference-semantics/semantics/call.k:13`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-FUNCTIONS
```

### K-0212 — `reference-semantics/semantics/call.k:16`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### K-0213 — `reference-semantics/semantics/call.k:19`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #callee(Exprs)
```

### K-0214 — `reference-semantics/semantics/call.k:20`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### K-0215 — `reference-semantics/semantics/call.k:21`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### K-0216 — `reference-semantics/semantics/call.k:24`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### K-0217 — `reference-semantics/semantics/call.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### K-0218 — `reference-semantics/semantics/call.k:27`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### K-0219 — `reference-semantics/semantics/call.k:28`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### K-0220 — `reference-semantics/semantics/call.k:29`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### K-0221 — `reference-semantics/semantics/call.k:30`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### K-0222 — `reference-semantics/semantics/call.k:31`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### K-0223 — `reference-semantics/semantics/call.k:32`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### K-0224 — `reference-semantics/semantics/call.k:38`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0225 — `reference-semantics/semantics/call.k:42`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### K-0226 — `reference-semantics/semantics/call.k:47`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0227 — `reference-semantics/semantics/call.k:52`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### K-0228 — `reference-semantics/semantics/call.k:53`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### K-0229 — `reference-semantics/semantics/call.k:56`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

### K-0230 — `reference-semantics/semantics/call.k:63`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### K-0231 — `reference-semantics/semantics/call.k:69`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K-0232 — `reference-semantics/semantics/call.k:80`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K-0233 — `reference-semantics/semantics/call.k:87`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### K-0234 — `reference-semantics/semantics/call.k:88`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### K-0235 — `reference-semantics/semantics/call.k:89`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K-0236 — `reference-semantics/semantics/call.k:95`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0237 — `reference-semantics/semantics/comprehension.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-COMPREHENSION
```

### K-0238 — `reference-semantics/semantics/comprehension.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0239 — `reference-semantics/semantics/comprehension.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-OPERATORS
```

### K-0240 — `reference-semantics/semantics/comprehension.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-LIST
```

### K-0241 — `reference-semantics/semantics/comprehension.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CONTROLS
```

### K-0242 — `reference-semantics/semantics/comprehension.k:8`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-FUNCTIONS
```

### K-0243 — `reference-semantics/semantics/comprehension.k:11`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K-0244 — `reference-semantics/semantics/comprehension.k:12`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K-0245 — `reference-semantics/semantics/comprehension.k:14`

- Kind: `syntax`
- Flags: `macro`
- Decision: declaration checked

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### K-0246 — `reference-semantics/semantics/comprehension.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### K-0247 — `reference-semantics/semantics/comprehension.k:18`

- Kind: `syntax`
- Flags: `macro`
- Decision: declaration checked

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### K-0248 — `reference-semantics/semantics/comprehension.k:19`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### K-0249 — `reference-semantics/semantics/comprehension.k:21`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### K-0250 — `reference-semantics/semantics/comprehension.k:24`

- Kind: `syntax`
- Flags: `macro`
- Decision: declaration checked

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### K-0251 — `reference-semantics/semantics/comprehension.k:25`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### K-0252 — `reference-semantics/semantics/comprehension.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### K-0253 — `reference-semantics/semantics/comprehension.k:27`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0254 — `reference-semantics/semantics/concrete.k:8`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-CONCRETE
```

### K-0255 — `reference-semantics/semantics/concrete.k:9`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY
```

### K-0256 — `reference-semantics/semantics/concrete.k:13`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K-0257 — `reference-semantics/semantics/concrete.k:16`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K-0258 — `reference-semantics/semantics/concrete.k:25`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= kvP(Val, Val)
```

### K-0259 — `reference-semantics/semantics/concrete.k:26`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### K-0260 — `reference-semantics/semantics/concrete.k:28`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### K-0261 — `reference-semantics/semantics/concrete.k:31`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### K-0262 — `reference-semantics/semantics/concrete.k:34`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### K-0263 — `reference-semantics/semantics/concrete.k:36`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### K-0264 — `reference-semantics/semantics/concrete.k:38`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### K-0265 — `reference-semantics/semantics/concrete.k:42`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### K-0266 — `reference-semantics/semantics/concrete.k:43`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### K-0267 — `reference-semantics/semantics/concrete.k:44`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### K-0268 — `reference-semantics/semantics/concrete.k:47`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### K-0269 — `reference-semantics/semantics/concrete.k:51`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### K-0270 — `reference-semantics/semantics/concrete.k:52`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### K-0271 — `reference-semantics/semantics/concrete.k:53`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### K-0272 — `reference-semantics/semantics/concrete.k:54`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K-0273 — `reference-semantics/semantics/concrete.k:56`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### K-0274 — `reference-semantics/semantics/concrete.k:57`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### K-0275 — `reference-semantics/semantics/concrete.k:58`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### K-0276 — `reference-semantics/semantics/concrete.k:59`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: excluded from Haskell proof definition

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### K-0277 — `reference-semantics/semantics/concrete.k:60`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0278 — `reference-semantics/semantics/controls.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-CONTROLS
```

### K-0279 — `reference-semantics/semantics/controls.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0280 — `reference-semantics/semantics/controls.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-TUPLE
```

### K-0281 — `reference-semantics/semantics/controls.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-0282 — `reference-semantics/semantics/controls.k:9`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K-0283 — `reference-semantics/semantics/controls.k:12`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K-0284 — `reference-semantics/semantics/controls.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

### K-0285 — `reference-semantics/semantics/controls.k:27`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

### K-0286 — `reference-semantics/semantics/controls.k:35`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### K-0287 — `reference-semantics/semantics/controls.k:36`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### K-0288 — `reference-semantics/semantics/controls.k:37`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### K-0289 — `reference-semantics/semantics/controls.k:38`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### K-0290 — `reference-semantics/semantics/controls.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### K-0291 — `reference-semantics/semantics/controls.k:43`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### K-0292 — `reference-semantics/semantics/controls.k:48`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### K-0293 — `reference-semantics/semantics/controls.k:51`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### K-0294 — `reference-semantics/semantics/controls.k:52`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### K-0295 — `reference-semantics/semantics/controls.k:53`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### K-0296 — `reference-semantics/semantics/controls.k:54`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### K-0297 — `reference-semantics/semantics/controls.k:57`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### K-0298 — `reference-semantics/semantics/controls.k:59`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

### K-0299 — `reference-semantics/semantics/controls.k:65`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### K-0300 — `reference-semantics/semantics/controls.k:69`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### K-0301 — `reference-semantics/semantics/controls.k:71`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### K-0302 — `reference-semantics/semantics/controls.k:72`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### K-0303 — `reference-semantics/semantics/controls.k:73`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### K-0304 — `reference-semantics/semantics/controls.k:77`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### K-0305 — `reference-semantics/semantics/controls.k:78`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### K-0306 — `reference-semantics/semantics/controls.k:79`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### K-0307 — `reference-semantics/semantics/controls.k:81`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

### K-0308 — `reference-semantics/semantics/controls.k:85`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K-0309 — `reference-semantics/semantics/controls.k:86`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Continue => #cont ... </k>
```

### K-0310 — `reference-semantics/semantics/controls.k:87`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Break => #brk ... </k>
```

### K-0311 — `reference-semantics/semantics/controls.k:88`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K-0312 — `reference-semantics/semantics/controls.k:89`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### K-0313 — `reference-semantics/semantics/controls.k:90`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### K-0314 — `reference-semantics/semantics/controls.k:91`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### K-0315 — `reference-semantics/semantics/controls.k:95`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0316 — `reference-semantics/semantics/controls.k:98`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0317 — `reference-semantics/semantics/controls.k:101`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0318 — `reference-semantics/semantics/controls.k:106`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0319 — `reference-semantics/semantics/controls.k:109`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0320 — `reference-semantics/semantics/core.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-CORE
```

### K-0321 — `reference-semantics/semantics/core.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-SYNTAX
```

### K-0322 — `reference-semantics/semantics/core.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports INT
```

### K-0323 — `reference-semantics/semantics/core.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports BOOL
```

### K-0324 — `reference-semantics/semantics/core.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports STRING
```

### K-0325 — `reference-semantics/semantics/core.k:8`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MAP
```

### K-0326 — `reference-semantics/semantics/core.k:9`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports LIST
```

### K-0327 — `reference-semantics/semantics/core.k:10`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports K-EQUAL
```

### K-0328 — `reference-semantics/semantics/core.k:13`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### K-0329 — `reference-semantics/semantics/core.k:14`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### K-0330 — `reference-semantics/semantics/core.k:15`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Str    ::= str(IntSeq)
```

### K-0331 — `reference-semantics/semantics/core.k:18`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### K-0332 — `reference-semantics/semantics/core.k:25`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

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

### K-0333 — `reference-semantics/semantics/core.k:36`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Parent   ::= "root" | parent(Int)
```

### K-0334 — `reference-semantics/semantics/core.k:37`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Scope    ::= scope(Map, Parent)
```

### K-0335 — `reference-semantics/semantics/core.k:38`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KResult  ::= Val
```

### K-0336 — `reference-semantics/semantics/core.k:39`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### K-0337 — `reference-semantics/semantics/core.k:40`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Vals     ::= List{Val, ","}
```

### K-0338 — `reference-semantics/semantics/core.k:41`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### K-0339 — `reference-semantics/semantics/core.k:42`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### K-0340 — `reference-semantics/semantics/core.k:49`

- Kind: `configuration`
- Flags: `none`
- Decision: initial cells checked and realizable

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

### K-0341 — `reference-semantics/semantics/core.k:68`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### K-0342 — `reference-semantics/semantics/core.k:69`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule isRefV(ref(_:Int)) => true
```

### K-0343 — `reference-semantics/semantics/core.k:70`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule isRefV(_:Val)      => false [owise]
```

### K-0344 — `reference-semantics/semantics/core.k:75`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax HeapVal ::= cellV(Val)
```

### K-0345 — `reference-semantics/semantics/core.k:76`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### K-0346 — `reference-semantics/semantics/core.k:77`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### K-0347 — `reference-semantics/semantics/core.k:78`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isCellRef(_:Val)          => false [owise]
```

### K-0348 — `reference-semantics/semantics/core.k:85`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

### K-0349 — `reference-semantics/semantics/core.k:95`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= kwV(String, Val)
```

### K-0350 — `reference-semantics/semantics/core.k:96`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #kwTag(String)
```

### K-0351 — `reference-semantics/semantics/core.k:97`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### K-0352 — `reference-semantics/semantics/core.k:98`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### K-0353 — `reference-semantics/semantics/core.k:100`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### K-0354 — `reference-semantics/semantics/core.k:101`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### K-0355 — `reference-semantics/semantics/core.k:102`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isKwV(_:Val)                => false [owise]
```

### K-0356 — `reference-semantics/semantics/core.k:106`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= cellsMark(ParamNames)
```

### K-0357 — `reference-semantics/semantics/core.k:107`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### K-0358 — `reference-semantics/semantics/core.k:108`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### K-0359 — `reference-semantics/semantics/core.k:109`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### K-0360 — `reference-semantics/semantics/core.k:110`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule pnMember(_:String, .ParamNames) => false
```

### K-0361 — `reference-semantics/semantics/core.k:111`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### K-0362 — `reference-semantics/semantics/core.k:113`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #cellW(Val, Val)
```

### K-0363 — `reference-semantics/semantics/core.k:114`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### K-0364 — `reference-semantics/semantics/core.k:117`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #alloc(Val)
```

### K-0365 — `reference-semantics/semantics/core.k:118`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K-0366 — `reference-semantics/semantics/core.k:124`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #loadAll(Module)
```

### K-0367 — `reference-semantics/semantics/core.k:125`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### K-0368 — `reference-semantics/semantics/core.k:126`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### K-0369 — `reference-semantics/semantics/core.k:127`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> .Stmts => .K ... </k>
```

### K-0370 — `reference-semantics/semantics/core.k:130`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #look(String, Int)
```

### K-0371 — `reference-semantics/semantics/core.k:131`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### K-0372 — `reference-semantics/semantics/core.k:132`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

### K-0373 — `reference-semantics/semantics/core.k:145`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### K-0374 — `reference-semantics/semantics/core.k:152`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

### K-0375 — `reference-semantics/semantics/core.k:157`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### K-0376 — `reference-semantics/semantics/core.k:158`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

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

### K-0377 — `reference-semantics/semantics/core.k:185`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax ApplyK ::= toCall(Val)
```

### K-0378 — `reference-semantics/semantics/core.k:186`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### K-0379 — `reference-semantics/semantics/core.k:189`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### K-0380 — `reference-semantics/semantics/core.k:190`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### K-0381 — `reference-semantics/semantics/core.k:191`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### K-0382 — `reference-semantics/semantics/core.k:194`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### K-0383 — `reference-semantics/semantics/core.k:195`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### K-0384 — `reference-semantics/semantics/core.k:196`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> NoneVal      => noneV ... </k>
```

### K-0385 — `reference-semantics/semantics/core.k:199`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Bool ::= truthy(Val) [function]
```

### K-0386 — `reference-semantics/semantics/core.k:200`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule truthy(B:Bool)          => B
```

### K-0387 — `reference-semantics/semantics/core.k:201`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule truthy(noneV)           => false
```

### K-0388 — `reference-semantics/semantics/core.k:202`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### K-0389 — `reference-semantics/semantics/core.k:203`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### K-0390 — `reference-semantics/semantics/core.k:204`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### K-0391 — `reference-semantics/semantics/core.k:205`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### K-0392 — `reference-semantics/semantics/core.k:208`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### K-0393 — `reference-semantics/semantics/core.k:209`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### K-0394 — `reference-semantics/semantics/core.k:210`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### K-0395 — `reference-semantics/semantics/core.k:213`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### K-0396 — `reference-semantics/semantics/core.k:214`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### K-0397 — `reference-semantics/semantics/core.k:215`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### K-0398 — `reference-semantics/semantics/core.k:217`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### K-0399 — `reference-semantics/semantics/core.k:218`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### K-0400 — `reference-semantics/semantics/core.k:219`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### K-0401 — `reference-semantics/semantics/core.k:223`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### K-0402 — `reference-semantics/semantics/core.k:224`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule vsLen(.ValSeq)                => 0
```

### K-0403 — `reference-semantics/semantics/core.k:225`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### K-0404 — `reference-semantics/semantics/core.k:227`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### K-0405 — `reference-semantics/semantics/core.k:228`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isLen(.IntSeq)                => 0
```

### K-0406 — `reference-semantics/semantics/core.k:229`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### K-0407 — `reference-semantics/semantics/core.k:233`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### K-0408 — `reference-semantics/semantics/core.k:234`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### K-0409 — `reference-semantics/semantics/core.k:235`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### K-0410 — `reference-semantics/semantics/core.k:236`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### K-0411 — `reference-semantics/semantics/core.k:238`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### K-0412 — `reference-semantics/semantics/core.k:240`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0413 — `reference-semantics/semantics/dict.k:13`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-DICT
```

### K-0414 — `reference-semantics/semantics/dict.k:14`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0415 — `reference-semantics/semantics/dict.k:15`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-0416 — `reference-semantics/semantics/dict.k:16`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-METHODS
```

### K-0417 — `reference-semantics/semantics/dict.k:17`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-LIST
```

### K-0418 — `reference-semantics/semantics/dict.k:20`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### K-0419 — `reference-semantics/semantics/dict.k:23`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### K-0420 — `reference-semantics/semantics/dict.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### K-0421 — `reference-semantics/semantics/dict.k:27`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### K-0422 — `reference-semantics/semantics/dict.k:28`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### K-0423 — `reference-semantics/semantics/dict.k:30`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### K-0424 — `reference-semantics/semantics/dict.k:32`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### K-0425 — `reference-semantics/semantics/dict.k:37`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### K-0426 — `reference-semantics/semantics/dict.k:38`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### K-0427 — `reference-semantics/semantics/dict.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### K-0428 — `reference-semantics/semantics/dict.k:40`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### K-0429 — `reference-semantics/semantics/dict.k:43`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### K-0430 — `reference-semantics/semantics/dict.k:44`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### K-0431 — `reference-semantics/semantics/dict.k:45`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### K-0432 — `reference-semantics/semantics/dict.k:49`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### K-0433 — `reference-semantics/semantics/dict.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### K-0434 — `reference-semantics/semantics/dict.k:52`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### K-0435 — `reference-semantics/semantics/dict.k:54`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### K-0436 — `reference-semantics/semantics/dict.k:58`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### K-0437 — `reference-semantics/semantics/dict.k:63`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### K-0438 — `reference-semantics/semantics/dict.k:64`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### K-0439 — `reference-semantics/semantics/dict.k:65`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### K-0440 — `reference-semantics/semantics/dict.k:70`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### K-0441 — `reference-semantics/semantics/dict.k:71`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### K-0442 — `reference-semantics/semantics/dict.k:76`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #dsetK(String, Val)
```

### K-0443 — `reference-semantics/semantics/dict.k:77`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### K-0444 — `reference-semantics/semantics/dict.k:78`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### K-0445 — `reference-semantics/semantics/dict.k:82`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### K-0446 — `reference-semantics/semantics/dict.k:86`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### K-0447 — `reference-semantics/semantics/dict.k:87`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### K-0448 — `reference-semantics/semantics/dict.k:90`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### K-0449 — `reference-semantics/semantics/dict.k:91`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K-0450 — `reference-semantics/semantics/dict.k:92`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### K-0451 — `reference-semantics/semantics/dict.k:95`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### K-0452 — `reference-semantics/semantics/dict.k:97`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### K-0453 — `reference-semantics/semantics/dict.k:98`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### K-0454 — `reference-semantics/semantics/dict.k:99`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### K-0455 — `reference-semantics/semantics/dict.k:101`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### K-0456 — `reference-semantics/semantics/dict.k:102`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### K-0457 — `reference-semantics/semantics/dict.k:103`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### K-0458 — `reference-semantics/semantics/dict.k:104`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0459 — `reference-semantics/semantics/float.k:14`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-FLOAT
```

### K-0460 — `reference-semantics/semantics/float.k:15`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-OPERATORS
```

### K-0461 — `reference-semantics/semantics/float.k:16`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-BUILTINS
```

### K-0462 — `reference-semantics/semantics/float.k:17`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports FLOAT
```

### K-0463 — `reference-semantics/semantics/float.k:20`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= Float
```

### K-0464 — `reference-semantics/semantics/float.k:21`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Float(F:Float) => F ... </k>
```

### K-0465 — `reference-semantics/semantics/float.k:24`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### K-0466 — `reference-semantics/semantics/float.k:25`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### K-0467 — `reference-semantics/semantics/float.k:27`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### K-0468 — `reference-semantics/semantics/float.k:30`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### K-0469 — `reference-semantics/semantics/float.k:31`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### K-0470 — `reference-semantics/semantics/float.k:32`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### K-0471 — `reference-semantics/semantics/float.k:37`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### K-0472 — `reference-semantics/semantics/float.k:38`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### K-0473 — `reference-semantics/semantics/float.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### K-0474 — `reference-semantics/semantics/float.k:43`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### K-0475 — `reference-semantics/semantics/float.k:44`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### K-0476 — `reference-semantics/semantics/float.k:50`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### K-0477 — `reference-semantics/semantics/float.k:51`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### K-0478 — `reference-semantics/semantics/float.k:52`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### K-0479 — `reference-semantics/semantics/float.k:54`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### K-0480 — `reference-semantics/semantics/float.k:55`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### K-0481 — `reference-semantics/semantics/float.k:56`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### K-0482 — `reference-semantics/semantics/float.k:61`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Import(_:String) => .K ... </k>
```

### K-0483 — `reference-semantics/semantics/float.k:65`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= "#mathCeil"
```

### K-0484 — `reference-semantics/semantics/float.k:66`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### K-0485 — `reference-semantics/semantics/float.k:67`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### K-0486 — `reference-semantics/semantics/float.k:70`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= "#mathFloor"
```

### K-0487 — `reference-semantics/semantics/float.k:71`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### K-0488 — `reference-semantics/semantics/float.k:72`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### K-0489 — `reference-semantics/semantics/float.k:73`

- Kind: `syntax`
- Flags: `function, total, symbol`
- Decision: declaration checked

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### K-0490 — `reference-semantics/semantics/float.k:74`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### K-0491 — `reference-semantics/semantics/float.k:75`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### K-0492 — `reference-semantics/semantics/float.k:78`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### K-0493 — `reference-semantics/semantics/float.k:79`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### K-0494 — `reference-semantics/semantics/float.k:82`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### K-0495 — `reference-semantics/semantics/float.k:83`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### K-0496 — `reference-semantics/semantics/float.k:84`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### K-0497 — `reference-semantics/semantics/float.k:85`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### K-0498 — `reference-semantics/semantics/float.k:86`

- Kind: `syntax`
- Flags: `function, total, symbol`
- Decision: declaration checked

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### K-0499 — `reference-semantics/semantics/float.k:87`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule toF(F:Float) => F        [concrete]
```

### K-0500 — `reference-semantics/semantics/float.k:88`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### K-0501 — `reference-semantics/semantics/float.k:93`

- Kind: `syntax`
- Flags: `function, total, symbol`
- Decision: declaration checked

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### K-0502 — `reference-semantics/semantics/float.k:94`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### K-0503 — `reference-semantics/semantics/float.k:95`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### K-0504 — `reference-semantics/semantics/float.k:99`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### K-0505 — `reference-semantics/semantics/float.k:103`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### K-0506 — `reference-semantics/semantics/float.k:104`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### K-0507 — `reference-semantics/semantics/float.k:105`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### K-0508 — `reference-semantics/semantics/float.k:107`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### K-0509 — `reference-semantics/semantics/float.k:108`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### K-0510 — `reference-semantics/semantics/float.k:109`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### K-0511 — `reference-semantics/semantics/float.k:111`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### K-0512 — `reference-semantics/semantics/float.k:112`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### K-0513 — `reference-semantics/semantics/float.k:113`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### K-0514 — `reference-semantics/semantics/float.k:115`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### K-0515 — `reference-semantics/semantics/float.k:116`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### K-0516 — `reference-semantics/semantics/float.k:117`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### K-0517 — `reference-semantics/semantics/float.k:119`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### K-0518 — `reference-semantics/semantics/float.k:120`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### K-0519 — `reference-semantics/semantics/float.k:121`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### K-0520 — `reference-semantics/semantics/float.k:125`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### K-0521 — `reference-semantics/semantics/float.k:126`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### K-0522 — `reference-semantics/semantics/float.k:127`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### K-0523 — `reference-semantics/semantics/float.k:128`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### K-0524 — `reference-semantics/semantics/float.k:129`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### K-0525 — `reference-semantics/semantics/float.k:132`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### K-0526 — `reference-semantics/semantics/float.k:133`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### K-0527 — `reference-semantics/semantics/float.k:134`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### K-0528 — `reference-semantics/semantics/float.k:135`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### K-0529 — `reference-semantics/semantics/float.k:136`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### K-0530 — `reference-semantics/semantics/float.k:137`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### K-0531 — `reference-semantics/semantics/float.k:138`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### K-0532 — `reference-semantics/semantics/float.k:139`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### K-0533 — `reference-semantics/semantics/float.k:142`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### K-0534 — `reference-semantics/semantics/float.k:143`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### K-0535 — `reference-semantics/semantics/float.k:144`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### K-0536 — `reference-semantics/semantics/float.k:145`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### K-0537 — `reference-semantics/semantics/float.k:146`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### K-0538 — `reference-semantics/semantics/float.k:147`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### K-0539 — `reference-semantics/semantics/float.k:148`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### K-0540 — `reference-semantics/semantics/float.k:149`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### K-0541 — `reference-semantics/semantics/float.k:150`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### K-0542 — `reference-semantics/semantics/float.k:151`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### K-0543 — `reference-semantics/semantics/float.k:154`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### K-0544 — `reference-semantics/semantics/float.k:155`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### K-0545 — `reference-semantics/semantics/float.k:160`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### K-0546 — `reference-semantics/semantics/float.k:161`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### K-0547 — `reference-semantics/semantics/float.k:162`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### K-0548 — `reference-semantics/semantics/float.k:165`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### K-0549 — `reference-semantics/semantics/float.k:166`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### K-0550 — `reference-semantics/semantics/float.k:167`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### K-0551 — `reference-semantics/semantics/float.k:168`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### K-0552 — `reference-semantics/semantics/float.k:169`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### K-0553 — `reference-semantics/semantics/float.k:170`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### K-0554 — `reference-semantics/semantics/float.k:171`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### K-0555 — `reference-semantics/semantics/float.k:173`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### K-0556 — `reference-semantics/semantics/float.k:174`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracPart(.IntSeq) => 0
```

### K-0557 — `reference-semantics/semantics/float.k:175`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### K-0558 — `reference-semantics/semantics/float.k:176`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### K-0559 — `reference-semantics/semantics/float.k:177`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### K-0560 — `reference-semantics/semantics/float.k:178`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### K-0561 — `reference-semantics/semantics/float.k:179`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### K-0562 — `reference-semantics/semantics/float.k:180`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracScale(.IntSeq) => 1
```

### K-0563 — `reference-semantics/semantics/float.k:181`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### K-0564 — `reference-semantics/semantics/float.k:182`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### K-0565 — `reference-semantics/semantics/float.k:183`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### K-0566 — `reference-semantics/semantics/float.k:184`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### K-0567 — `reference-semantics/semantics/float.k:185`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### K-0568 — `reference-semantics/semantics/float.k:186`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### K-0569 — `reference-semantics/semantics/float.k:187`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### K-0570 — `reference-semantics/semantics/float.k:190`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### K-0571 — `reference-semantics/semantics/float.k:191`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### K-0572 — `reference-semantics/semantics/float.k:192`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### K-0573 — `reference-semantics/semantics/float.k:195`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### K-0574 — `reference-semantics/semantics/float.k:196`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### K-0575 — `reference-semantics/semantics/float.k:197`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### K-0576 — `reference-semantics/semantics/float.k:198`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### K-0577 — `reference-semantics/semantics/float.k:199`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### K-0578 — `reference-semantics/semantics/float.k:200`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### K-0579 — `reference-semantics/semantics/float.k:201`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### K-0580 — `reference-semantics/semantics/float.k:202`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### K-0581 — `reference-semantics/semantics/float.k:203`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### K-0582 — `reference-semantics/semantics/float.k:204`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### K-0583 — `reference-semantics/semantics/float.k:205`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### K-0584 — `reference-semantics/semantics/float.k:206`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### K-0585 — `reference-semantics/semantics/float.k:209`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### K-0586 — `reference-semantics/semantics/float.k:210`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### K-0587 — `reference-semantics/semantics/float.k:211`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### K-0588 — `reference-semantics/semantics/float.k:213`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### K-0589 — `reference-semantics/semantics/float.k:214`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### K-0590 — `reference-semantics/semantics/float.k:217`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### K-0591 — `reference-semantics/semantics/float.k:218`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### K-0592 — `reference-semantics/semantics/float.k:223`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### K-0593 — `reference-semantics/semantics/float.k:224`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### K-0594 — `reference-semantics/semantics/float.k:227`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### K-0595 — `reference-semantics/semantics/float.k:228`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### K-0596 — `reference-semantics/semantics/float.k:230`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### K-0597 — `reference-semantics/semantics/float.k:231`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### K-0598 — `reference-semantics/semantics/float.k:232`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= "#mathSqrt"
```

### K-0599 — `reference-semantics/semantics/float.k:233`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### K-0600 — `reference-semantics/semantics/float.k:234`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### K-0601 — `reference-semantics/semantics/float.k:235`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### K-0602 — `reference-semantics/semantics/float.k:243`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### K-0603 — `reference-semantics/semantics/float.k:244`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K-0604 — `reference-semantics/semantics/float.k:245`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### K-0605 — `reference-semantics/semantics/float.k:246`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### K-0606 — `reference-semantics/semantics/float.k:247`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0607 — `reference-semantics/semantics/float.k:250`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### K-0608 — `reference-semantics/semantics/float.k:251`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K-0609 — `reference-semantics/semantics/float.k:252`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### K-0610 — `reference-semantics/semantics/float.k:253`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### K-0611 — `reference-semantics/semantics/float.k:254`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0612 — `reference-semantics/semantics/float.k:261`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### K-0613 — `reference-semantics/semantics/float.k:262`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### K-0614 — `reference-semantics/semantics/float.k:265`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### K-0615 — `reference-semantics/semantics/float.k:266`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### K-0616 — `reference-semantics/semantics/float.k:267`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0617 — `reference-semantics/semantics/float.k:270`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K-0618 — `reference-semantics/semantics/float.k:273`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0619 — `reference-semantics/semantics/functions.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-FUNCTIONS
```

### K-0620 — `reference-semantics/semantics/functions.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0621 — `reference-semantics/semantics/functions.k:8`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### K-0622 — `reference-semantics/semantics/functions.k:14`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### K-0623 — `reference-semantics/semantics/functions.k:18`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### K-0624 — `reference-semantics/semantics/functions.k:19`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### K-0625 — `reference-semantics/semantics/functions.k:27`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### K-0626 — `reference-semantics/semantics/functions.k:31`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### K-0627 — `reference-semantics/semantics/functions.k:33`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### K-0628 — `reference-semantics/semantics/functions.k:36`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K-0629 — `reference-semantics/semantics/functions.k:42`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### K-0630 — `reference-semantics/semantics/functions.k:47`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### K-0631 — `reference-semantics/semantics/functions.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### K-0632 — `reference-semantics/semantics/functions.k:53`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K-0633 — `reference-semantics/semantics/functions.k:59`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### K-0634 — `reference-semantics/semantics/functions.k:63`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### K-0635 — `reference-semantics/semantics/functions.k:64`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### K-0636 — `reference-semantics/semantics/functions.k:68`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

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

### K-0637 — `reference-semantics/semantics/functions.k:78`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### K-0638 — `reference-semantics/semantics/functions.k:80`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### K-0639 — `reference-semantics/semantics/functions.k:85`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### K-0640 — `reference-semantics/semantics/functions.k:91`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0641 — `reference-semantics/semantics/int.k:4`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-INT
```

### K-0642 — `reference-semantics/semantics/int.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0643 — `reference-semantics/semantics/int.k:7`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### K-0644 — `reference-semantics/semantics/int.k:9`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### K-0645 — `reference-semantics/semantics/int.k:11`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### K-0646 — `reference-semantics/semantics/int.k:12`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### K-0647 — `reference-semantics/semantics/int.k:13`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### K-0648 — `reference-semantics/semantics/int.k:14`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### K-0649 — `reference-semantics/semantics/int.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### K-0650 — `reference-semantics/semantics/int.k:16`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### K-0651 — `reference-semantics/semantics/int.k:17`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### K-0652 — `reference-semantics/semantics/int.k:19`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### K-0653 — `reference-semantics/semantics/int.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### K-0654 — `reference-semantics/semantics/int.k:22`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### K-0655 — `reference-semantics/semantics/int.k:23`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### K-0656 — `reference-semantics/semantics/int.k:24`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### K-0657 — `reference-semantics/semantics/int.k:25`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### K-0658 — `reference-semantics/semantics/int.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### K-0659 — `reference-semantics/semantics/int.k:27`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### K-0660 — `reference-semantics/semantics/int.k:28`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0661 — `reference-semantics/semantics/iter.k:6`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-ITER
```

### K-0662 — `reference-semantics/semantics/iter.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0663 — `reference-semantics/semantics/iter.k:8`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### K-0664 — `reference-semantics/semantics/iter.k:9`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0665 — `reference-semantics/semantics/list.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-LIST
```

### K-0666 — `reference-semantics/semantics/list.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0667 — `reference-semantics/semantics/list.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-0668 — `reference-semantics/semantics/list.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-OPERATORS
```

### K-0669 — `reference-semantics/semantics/list.k:9`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### K-0670 — `reference-semantics/semantics/list.k:10`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### K-0671 — `reference-semantics/semantics/list.k:13`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax ApplyK ::= "toList"
```

### K-0672 — `reference-semantics/semantics/list.k:14`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### K-0673 — `reference-semantics/semantics/list.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### K-0674 — `reference-semantics/semantics/list.k:18`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### K-0675 — `reference-semantics/semantics/list.k:19`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### K-0676 — `reference-semantics/semantics/list.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### K-0677 — `reference-semantics/semantics/list.k:24`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### K-0678 — `reference-semantics/semantics/list.k:27`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### K-0679 — `reference-semantics/semantics/list.k:28`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### K-0680 — `reference-semantics/semantics/list.k:33`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### K-0681 — `reference-semantics/semantics/list.k:34`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule hasRefVS(.ValSeq)                => false
```

### K-0682 — `reference-semantics/semantics/list.k:35`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### K-0683 — `reference-semantics/semantics/list.k:37`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### K-0684 — `reference-semantics/semantics/list.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### K-0685 — `reference-semantics/semantics/list.k:40`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### K-0686 — `reference-semantics/semantics/list.k:41`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### K-0687 — `reference-semantics/semantics/list.k:42`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### K-0688 — `reference-semantics/semantics/list.k:45`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### K-0689 — `reference-semantics/semantics/list.k:47`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### K-0690 — `reference-semantics/semantics/list.k:49`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### K-0691 — `reference-semantics/semantics/list.k:50`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### K-0692 — `reference-semantics/semantics/list.k:53`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### K-0693 — `reference-semantics/semantics/list.k:58`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### K-0694 — `reference-semantics/semantics/list.k:59`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### K-0695 — `reference-semantics/semantics/list.k:60`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### K-0696 — `reference-semantics/semantics/list.k:61`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### K-0697 — `reference-semantics/semantics/list.k:62`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### K-0698 — `reference-semantics/semantics/list.k:63`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### K-0699 — `reference-semantics/semantics/list.k:65`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### K-0700 — `reference-semantics/semantics/list.k:67`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### K-0701 — `reference-semantics/semantics/list.k:68`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0702 — `reference-semantics/semantics/methods.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-METHODS
```

### K-0703 — `reference-semantics/semantics/methods.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0704 — `reference-semantics/semantics/methods.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports K-EQUAL
```

### K-0705 — `reference-semantics/semantics/methods.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-STR
```

### K-0706 — `reference-semantics/semantics/methods.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-LIST
```

### K-0707 — `reference-semantics/semantics/methods.k:10`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### K-0708 — `reference-semantics/semantics/methods.k:13`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### K-0709 — `reference-semantics/semantics/methods.k:14`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### K-0710 — `reference-semantics/semantics/methods.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### K-0711 — `reference-semantics/semantics/methods.k:16`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### K-0712 — `reference-semantics/semantics/methods.k:19`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### K-0713 — `reference-semantics/semantics/methods.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### K-0714 — `reference-semantics/semantics/methods.k:21`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### K-0715 — `reference-semantics/semantics/methods.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### K-0716 — `reference-semantics/semantics/methods.k:27`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### K-0717 — `reference-semantics/semantics/methods.k:28`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### K-0718 — `reference-semantics/semantics/methods.k:29`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### K-0719 — `reference-semantics/semantics/methods.k:30`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### K-0720 — `reference-semantics/semantics/methods.k:34`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### K-0721 — `reference-semantics/semantics/methods.k:35`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### K-0722 — `reference-semantics/semantics/methods.k:36`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### K-0723 — `reference-semantics/semantics/methods.k:37`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### K-0724 — `reference-semantics/semantics/methods.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### K-0725 — `reference-semantics/semantics/methods.k:41`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### K-0726 — `reference-semantics/semantics/methods.k:42`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### K-0727 — `reference-semantics/semantics/methods.k:43`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### K-0728 — `reference-semantics/semantics/methods.k:44`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### K-0729 — `reference-semantics/semantics/methods.k:47`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### K-0730 — `reference-semantics/semantics/methods.k:48`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### K-0731 — `reference-semantics/semantics/methods.k:49`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### K-0732 — `reference-semantics/semantics/methods.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### K-0733 — `reference-semantics/semantics/methods.k:51`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### K-0734 — `reference-semantics/semantics/methods.k:52`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### K-0735 — `reference-semantics/semantics/methods.k:53`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### K-0736 — `reference-semantics/semantics/methods.k:54`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### K-0737 — `reference-semantics/semantics/methods.k:55`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### K-0738 — `reference-semantics/semantics/methods.k:58`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### K-0739 — `reference-semantics/semantics/methods.k:61`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### K-0740 — `reference-semantics/semantics/methods.k:64`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### K-0741 — `reference-semantics/semantics/methods.k:65`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### K-0742 — `reference-semantics/semantics/methods.k:66`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### K-0743 — `reference-semantics/semantics/methods.k:67`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### K-0744 — `reference-semantics/semantics/methods.k:68`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### K-0745 — `reference-semantics/semantics/methods.k:72`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### K-0746 — `reference-semantics/semantics/methods.k:75`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### K-0747 — `reference-semantics/semantics/methods.k:76`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### K-0748 — `reference-semantics/semantics/methods.k:77`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### K-0749 — `reference-semantics/semantics/methods.k:79`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

### K-0750 — `reference-semantics/semantics/methods.k:82`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### K-0751 — `reference-semantics/semantics/methods.k:83`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### K-0752 — `reference-semantics/semantics/methods.k:84`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### K-0753 — `reference-semantics/semantics/methods.k:85`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### K-0754 — `reference-semantics/semantics/methods.k:86`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### K-0755 — `reference-semantics/semantics/methods.k:89`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### K-0756 — `reference-semantics/semantics/methods.k:94`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### K-0757 — `reference-semantics/semantics/methods.k:97`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### K-0758 — `reference-semantics/semantics/methods.k:98`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### K-0759 — `reference-semantics/semantics/methods.k:99`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### K-0760 — `reference-semantics/semantics/methods.k:101`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### K-0761 — `reference-semantics/semantics/methods.k:104`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### K-0762 — `reference-semantics/semantics/methods.k:106`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### K-0763 — `reference-semantics/semantics/methods.k:107`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### K-0764 — `reference-semantics/semantics/methods.k:108`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### K-0765 — `reference-semantics/semantics/methods.k:109`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### K-0766 — `reference-semantics/semantics/methods.k:112`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### K-0767 — `reference-semantics/semantics/methods.k:113`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### K-0768 — `reference-semantics/semantics/methods.k:115`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### K-0769 — `reference-semantics/semantics/methods.k:116`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### K-0770 — `reference-semantics/semantics/methods.k:118`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### K-0771 — `reference-semantics/semantics/methods.k:119`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### K-0772 — `reference-semantics/semantics/methods.k:121`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### K-0773 — `reference-semantics/semantics/methods.k:122`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K-0774 — `reference-semantics/semantics/methods.k:124`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### K-0775 — `reference-semantics/semantics/methods.k:125`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule hasUpper(.IntSeq) => false
```

### K-0776 — `reference-semantics/semantics/methods.k:126`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### K-0777 — `reference-semantics/semantics/methods.k:128`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### K-0778 — `reference-semantics/semantics/methods.k:129`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule hasLower(.IntSeq) => false
```

### K-0779 — `reference-semantics/semantics/methods.k:130`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### K-0780 — `reference-semantics/semantics/methods.k:132`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### K-0781 — `reference-semantics/semantics/methods.k:133`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule allAlpha(.IntSeq) => true
```

### K-0782 — `reference-semantics/semantics/methods.k:134`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### K-0783 — `reference-semantics/semantics/methods.k:136`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### K-0784 — `reference-semantics/semantics/methods.k:137`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule allDigit(.IntSeq) => true
```

### K-0785 — `reference-semantics/semantics/methods.k:138`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### K-0786 — `reference-semantics/semantics/methods.k:140`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### K-0787 — `reference-semantics/semantics/methods.k:142`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K-0788 — `reference-semantics/semantics/methods.k:143`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule lowerC(C:Int) => C         [owise]
```

### K-0789 — `reference-semantics/semantics/methods.k:145`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= upperC(Int) [function, total]
```

### K-0790 — `reference-semantics/semantics/methods.k:146`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K-0791 — `reference-semantics/semantics/methods.k:147`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule upperC(C:Int) => C         [owise]
```

### K-0792 — `reference-semantics/semantics/methods.k:149`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= swapC(Int) [function, total]
```

### K-0793 — `reference-semantics/semantics/methods.k:150`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K-0794 — `reference-semantics/semantics/methods.k:151`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K-0795 — `reference-semantics/semantics/methods.k:152`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule swapC(C:Int) => C         [owise]
```

### K-0796 — `reference-semantics/semantics/methods.k:154`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### K-0797 — `reference-semantics/semantics/methods.k:155`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### K-0798 — `reference-semantics/semantics/methods.k:156`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### K-0799 — `reference-semantics/semantics/methods.k:158`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### K-0800 — `reference-semantics/semantics/methods.k:159`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### K-0801 — `reference-semantics/semantics/methods.k:160`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### K-0802 — `reference-semantics/semantics/methods.k:162`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### K-0803 — `reference-semantics/semantics/methods.k:163`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### K-0804 — `reference-semantics/semantics/methods.k:164`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### K-0805 — `reference-semantics/semantics/methods.k:166`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### K-0806 — `reference-semantics/semantics/methods.k:167`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### K-0807 — `reference-semantics/semantics/methods.k:168`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0808 — `reference-semantics/semantics/methods.k:169`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### K-0809 — `reference-semantics/semantics/methods.k:170`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0810 — `reference-semantics/semantics/operators.k:6`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-OPERATORS
```

### K-0811 — `reference-semantics/semantics/operators.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0812 — `reference-semantics/semantics/operators.k:8`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-0813 — `reference-semantics/semantics/operators.k:10`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### K-0814 — `reference-semantics/semantics/operators.k:12`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### K-0815 — `reference-semantics/semantics/operators.k:15`

- Kind: `context`
- Flags: `none`
- Decision: evaluation-order context checked

```k
  context Compare(HOLE, _)
```

### K-0816 — `reference-semantics/semantics/operators.k:16`

- Kind: `context`
- Flags: `none`
- Decision: evaluation-order context checked

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### K-0817 — `reference-semantics/semantics/operators.k:17`

- Kind: `rule`
- Flags: `owise, ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### K-0818 — `reference-semantics/semantics/operators.k:19`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### K-0819 — `reference-semantics/semantics/operators.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### K-0820 — `reference-semantics/semantics/operators.k:25`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0821 — `reference-semantics/semantics/operators.k:28`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

### K-0822 — `reference-semantics/semantics/operators.k:34`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### K-0823 — `reference-semantics/semantics/operators.k:38`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### K-0824 — `reference-semantics/semantics/operators.k:44`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0825 — `reference-semantics/semantics/operators.k:47`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0826 — `reference-semantics/semantics/range.k:5`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-RANGE
```

### K-0827 — `reference-semantics/semantics/range.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0828 — `reference-semantics/semantics/range.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-0829 — `reference-semantics/semantics/range.k:9`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### K-0830 — `reference-semantics/semantics/range.k:10`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### K-0831 — `reference-semantics/semantics/range.k:12`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### K-0832 — `reference-semantics/semantics/range.k:13`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### K-0833 — `reference-semantics/semantics/range.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### K-0834 — `reference-semantics/semantics/range.k:17`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### K-0835 — `reference-semantics/semantics/range.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### K-0836 — `reference-semantics/semantics/range.k:23`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### K-0837 — `reference-semantics/semantics/range.k:25`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0838 — `reference-semantics/semantics/set.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-SET
```

### K-0839 — `reference-semantics/semantics/set.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0840 — `reference-semantics/semantics/set.k:8`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Val ::= setV(IntSeq)
```

### K-0841 — `reference-semantics/semantics/set.k:11`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### K-0842 — `reference-semantics/semantics/set.k:12`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### K-0843 — `reference-semantics/semantics/set.k:13`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### K-0844 — `reference-semantics/semantics/set.k:16`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### K-0845 — `reference-semantics/semantics/set.k:18`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### K-0846 — `reference-semantics/semantics/set.k:19`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### K-0847 — `reference-semantics/semantics/set.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### K-0848 — `reference-semantics/semantics/set.k:22`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### K-0849 — `reference-semantics/semantics/set.k:25`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### K-0850 — `reference-semantics/semantics/set.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### K-0851 — `reference-semantics/semantics/set.k:27`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### K-0852 — `reference-semantics/semantics/set.k:31`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### K-0853 — `reference-semantics/semantics/set.k:32`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### K-0854 — `reference-semantics/semantics/set.k:33`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### K-0855 — `reference-semantics/semantics/set.k:35`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### K-0856 — `reference-semantics/semantics/set.k:36`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### K-0857 — `reference-semantics/semantics/set.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### K-0858 — `reference-semantics/semantics/set.k:40`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0859 — `reference-semantics/semantics/sort.k:10`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-SORT
```

### K-0860 — `reference-semantics/semantics/sort.k:11`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-BUILTINS
```

### K-0861 — `reference-semantics/semantics/sort.k:12`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-SUBSCRIPT
```

### K-0862 — `reference-semantics/semantics/sort.k:18`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### K-0863 — `reference-semantics/semantics/sort.k:19`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### K-0864 — `reference-semantics/semantics/sort.k:20`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### K-0865 — `reference-semantics/semantics/sort.k:21`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### K-0866 — `reference-semantics/semantics/sort.k:22`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### K-0867 — `reference-semantics/semantics/sort.k:23`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### K-0868 — `reference-semantics/semantics/sort.k:24`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### K-0869 — `reference-semantics/semantics/sort.k:26`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### K-0870 — `reference-semantics/semantics/sort.k:27`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### K-0871 — `reference-semantics/semantics/sort.k:28`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### K-0872 — `reference-semantics/semantics/sort.k:29`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### K-0873 — `reference-semantics/semantics/sort.k:31`

- Kind: `rule`
- Flags: `concrete`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### K-0874 — `reference-semantics/semantics/sort.k:36`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### K-0875 — `reference-semantics/semantics/sort.k:40`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### K-0876 — `reference-semantics/semantics/sort.k:49`

- Kind: `syntax`
- Flags: `function, total, symbol, opaque/no-evaluators`
- Decision: declaration checked

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### K-0877 — `reference-semantics/semantics/sort.k:51`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### K-0878 — `reference-semantics/semantics/sort.k:53`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### K-0879 — `reference-semantics/semantics/sort.k:54`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### K-0880 — `reference-semantics/semantics/sort.k:55`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### K-0881 — `reference-semantics/semantics/sort.k:57`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### K-0882 — `reference-semantics/semantics/sort.k:58`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule condRev(S:ValSeq, false) => S
```

### K-0883 — `reference-semantics/semantics/sort.k:59`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### K-0884 — `reference-semantics/semantics/sort.k:61`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### K-0885 — `reference-semantics/semantics/sort.k:63`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### K-0886 — `reference-semantics/semantics/sort.k:65`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

### K-0887 — `reference-semantics/semantics/sort.k:72`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0888 — `reference-semantics/semantics/str.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-STR
```

### K-0889 — `reference-semantics/semantics/str.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0890 — `reference-semantics/semantics/str.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-0891 — `reference-semantics/semantics/str.k:8`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### K-0892 — `reference-semantics/semantics/str.k:9`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### K-0893 — `reference-semantics/semantics/str.k:13`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### K-0894 — `reference-semantics/semantics/str.k:14`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### K-0895 — `reference-semantics/semantics/str.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule strToCodes("") => .IntSeq
```

### K-0896 — `reference-semantics/semantics/str.k:16`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: faithful on every reachable submitted-program state

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### K-0897 — `reference-semantics/semantics/str.k:20`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### K-0898 — `reference-semantics/semantics/str.k:21`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### K-0899 — `reference-semantics/semantics/str.k:22`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### K-0900 — `reference-semantics/semantics/str.k:24`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### K-0901 — `reference-semantics/semantics/str.k:25`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### K-0902 — `reference-semantics/semantics/str.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### K-0903 — `reference-semantics/semantics/str.k:29`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### K-0904 — `reference-semantics/semantics/str.k:30`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### K-0905 — `reference-semantics/semantics/str.k:32`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### K-0906 — `reference-semantics/semantics/str.k:33`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### K-0907 — `reference-semantics/semantics/str.k:34`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0908 — `reference-semantics/semantics/str.k:35`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### K-0909 — `reference-semantics/semantics/str.k:37`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### K-0910 — `reference-semantics/semantics/str.k:38`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### K-0911 — `reference-semantics/semantics/str.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### K-0912 — `reference-semantics/semantics/str.k:40`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

### K-0913 — `reference-semantics/semantics/str.k:48`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### K-0914 — `reference-semantics/semantics/str.k:49`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### K-0915 — `reference-semantics/semantics/str.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### K-0916 — `reference-semantics/semantics/str.k:51`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0917 — `reference-semantics/semantics/str.k:52`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### K-0918 — `reference-semantics/semantics/str.k:53`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### K-0919 — `reference-semantics/semantics/str.k:54`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### K-0920 — `reference-semantics/semantics/str.k:56`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K-0921 — `reference-semantics/semantics/str.k:57`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### K-0922 — `reference-semantics/semantics/str.k:58`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### K-0923 — `reference-semantics/semantics/str.k:59`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### K-0924 — `reference-semantics/semantics/str.k:60`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0925 — `reference-semantics/semantics/subscript.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-SUBSCRIPT
```

### K-0926 — `reference-semantics/semantics/subscript.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-0927 — `reference-semantics/semantics/subscript.k:11`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### K-0928 — `reference-semantics/semantics/subscript.k:12`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### K-0929 — `reference-semantics/semantics/subscript.k:13`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K-0930 — `reference-semantics/semantics/subscript.k:16`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### K-0931 — `reference-semantics/semantics/subscript.k:17`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### K-0932 — `reference-semantics/semantics/subscript.k:18`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K-0933 — `reference-semantics/semantics/subscript.k:21`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### K-0934 — `reference-semantics/semantics/subscript.k:22`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K-0935 — `reference-semantics/semantics/subscript.k:23`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### K-0936 — `reference-semantics/semantics/subscript.k:27`

- Kind: `context`
- Flags: `none`
- Decision: evaluation-order context checked

```k
  context Subscript(HOLE, _)
```

### K-0937 — `reference-semantics/semantics/subscript.k:28`

- Kind: `context`
- Flags: `none`
- Decision: evaluation-order context checked

```k
  context Subscript(_:Val, HOLE:Expr)
```

### K-0938 — `reference-semantics/semantics/subscript.k:31`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0939 — `reference-semantics/semantics/subscript.k:35`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### K-0940 — `reference-semantics/semantics/subscript.k:37`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### K-0941 — `reference-semantics/semantics/subscript.k:38`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K-0942 — `reference-semantics/semantics/subscript.k:39`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K-0943 — `reference-semantics/semantics/subscript.k:40`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### K-0944 — `reference-semantics/semantics/subscript.k:44`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### K-0945 — `reference-semantics/semantics/subscript.k:49`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### K-0946 — `reference-semantics/semantics/subscript.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### K-0947 — `reference-semantics/semantics/subscript.k:51`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### K-0948 — `reference-semantics/semantics/subscript.k:52`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### K-0949 — `reference-semantics/semantics/subscript.k:54`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### K-0950 — `reference-semantics/semantics/subscript.k:55`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### K-0951 — `reference-semantics/semantics/subscript.k:56`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### K-0952 — `reference-semantics/semantics/subscript.k:58`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### K-0953 — `reference-semantics/semantics/subscript.k:61`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### K-0954 — `reference-semantics/semantics/subscript.k:63`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### K-0955 — `reference-semantics/semantics/subscript.k:64`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K-0956 — `reference-semantics/semantics/subscript.k:66`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K-0957 — `reference-semantics/semantics/subscript.k:68`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### K-0958 — `reference-semantics/semantics/subscript.k:72`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### K-0959 — `reference-semantics/semantics/subscript.k:73`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStep(noB)          => 1
```

### K-0960 — `reference-semantics/semantics/subscript.k:74`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStep(someB(S:Int)) => S
```

### K-0961 — `reference-semantics/semantics/subscript.k:76`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### K-0962 — `reference-semantics/semantics/subscript.k:77`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### K-0963 — `reference-semantics/semantics/subscript.k:79`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### K-0964 — `reference-semantics/semantics/subscript.k:81`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K-0965 — `reference-semantics/semantics/subscript.k:83`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### K-0966 — `reference-semantics/semantics/subscript.k:84`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### K-0967 — `reference-semantics/semantics/subscript.k:86`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### K-0968 — `reference-semantics/semantics/subscript.k:88`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K-0969 — `reference-semantics/semantics/subscript.k:90`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### K-0970 — `reference-semantics/semantics/subscript.k:91`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### K-0971 — `reference-semantics/semantics/subscript.k:93`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### K-0972 — `reference-semantics/semantics/subscript.k:96`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### K-0973 — `reference-semantics/semantics/subscript.k:97`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### K-0974 — `reference-semantics/semantics/subscript.k:99`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### K-0975 — `reference-semantics/semantics/subscript.k:102`

- Kind: `syntax`
- Flags: `function, total`
- Decision: declaration checked

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### K-0976 — `reference-semantics/semantics/subscript.k:103`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### K-0977 — `reference-semantics/semantics/subscript.k:105`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

### K-0978 — `reference-semantics/semantics/subscript.k:109`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### K-0979 — `reference-semantics/semantics/subscript.k:110`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K-0980 — `reference-semantics/semantics/subscript.k:113`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K-0981 — `reference-semantics/semantics/subscript.k:116`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### K-0982 — `reference-semantics/semantics/subscript.k:117`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K-0983 — `reference-semantics/semantics/subscript.k:120`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K-0984 — `reference-semantics/semantics/subscript.k:122`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-0985 — `reference-semantics/semantics/syntax.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-SYNTAX
```

### K-0986 — `reference-semantics/semantics/syntax.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports INT-SYNTAX
```

### K-0987 — `reference-semantics/semantics/syntax.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports FLOAT-SYNTAX
```

### K-0988 — `reference-semantics/semantics/syntax.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports BOOL-SYNTAX
```

### K-0989 — `reference-semantics/semantics/syntax.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports STRING-SYNTAX
```

### K-0990 — `reference-semantics/semantics/syntax.k:9`

- Kind: `syntax`
- Flags: `macro, strictness`
- Decision: declaration checked

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

### K-0991 — `reference-semantics/semantics/syntax.k:32`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### K-0992 — `reference-semantics/semantics/syntax.k:33`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### K-0993 — `reference-semantics/semantics/syntax.k:34`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Entries  ::= List{Entry, ","}
```

### K-0994 — `reference-semantics/semantics/syntax.k:35`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### K-0995 — `reference-semantics/semantics/syntax.k:36`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax CompFors ::= List{CompFor, ""}
```

### K-0996 — `reference-semantics/semantics/syntax.k:37`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Exprs    ::= List{Expr, ","}
```

### K-0997 — `reference-semantics/semantics/syntax.k:38`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### K-0998 — `reference-semantics/semantics/syntax.k:39`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Bound    ::= Expr | "NoBound"
```

### K-0999 — `reference-semantics/semantics/syntax.k:41`

- Kind: `syntax`
- Flags: `strictness`
- Decision: declaration checked

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

### K-1000 — `reference-semantics/semantics/syntax.k:56`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### K-1001 — `reference-semantics/semantics/syntax.k:57`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### K-1002 — `reference-semantics/semantics/syntax.k:58`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### K-1003 — `reference-semantics/semantics/syntax.k:59`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### K-1004 — `reference-semantics/semantics/syntax.k:60`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax ParamNames ::= List{String, ","}
```

### K-1005 — `reference-semantics/semantics/syntax.k:61`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### K-1006 — `reference-semantics/semantics/syntax.k:62`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1007 — `reference-semantics/semantics/tuple.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-TUPLE
```

### K-1008 — `reference-semantics/semantics/tuple.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-1009 — `reference-semantics/semantics/tuple.k:5`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-1010 — `reference-semantics/semantics/tuple.k:6`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-LIST
```

### K-1011 — `reference-semantics/semantics/tuple.k:7`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-METHODS
```

### K-1012 — `reference-semantics/semantics/tuple.k:10`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### K-1013 — `reference-semantics/semantics/tuple.k:11`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### K-1014 — `reference-semantics/semantics/tuple.k:14`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax ApplyK ::= "toTuple"
```

### K-1015 — `reference-semantics/semantics/tuple.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### K-1016 — `reference-semantics/semantics/tuple.k:16`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### K-1017 — `reference-semantics/semantics/tuple.k:18`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### K-1018 — `reference-semantics/semantics/tuple.k:20`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### K-1019 — `reference-semantics/semantics/tuple.k:21`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### K-1020 — `reference-semantics/semantics/tuple.k:23`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### K-1021 — `reference-semantics/semantics/tuple.k:24`

- Kind: `syntax`
- Flags: `function`
- Decision: declaration checked

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### K-1022 — `reference-semantics/semantics/tuple.k:25`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### K-1023 — `reference-semantics/semantics/tuple.k:26`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### K-1024 — `reference-semantics/semantics/tuple.k:28`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### K-1025 — `reference-semantics/semantics/tuple.k:31`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### K-1026 — `reference-semantics/semantics/tuple.k:32`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K-1027 — `reference-semantics/semantics/tuple.k:35`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K-1028 — `reference-semantics/semantics/tuple.k:42`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K-1029 — `reference-semantics/semantics/tuple.k:43`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K-1030 — `reference-semantics/semantics/tuple.k:44`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-1031 — `reference-semantics/semantics/tuple.k:49`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### K-1032 — `reference-semantics/semantics/tuple.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K-1033 — `reference-semantics/semantics/tuple.k:51`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K-1034 — `reference-semantics/semantics/tuple.k:52`

- Kind: `rule`
- Flags: `priority, ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-1035 — `reference-semantics/semantics/tuple.k:55`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### K-1036 — `reference-semantics/semantics/tuple.k:57`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: unreached by submitted program; no path to this theorem's result (supplied-semantics limitation if non-CPython outside its subset)

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### K-1037 — `reference-semantics/semantics/tuple.k:58`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1038 — `reference-semantics/semantics.k:34`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/syntax.k"
```

### K-1039 — `reference-semantics/semantics.k:35`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/core.k"
```

### K-1040 — `reference-semantics/semantics.k:36`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/iter.k"
```

### K-1041 — `reference-semantics/semantics.k:37`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/range.k"
```

### K-1042 — `reference-semantics/semantics.k:38`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/operators.k"
```

### K-1043 — `reference-semantics/semantics.k:39`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/int.k"
```

### K-1044 — `reference-semantics/semantics.k:40`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/bool.k"
```

### K-1045 — `reference-semantics/semantics.k:41`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/float.k"
```

### K-1046 — `reference-semantics/semantics.k:42`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/str.k"
```

### K-1047 — `reference-semantics/semantics.k:43`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/set.k"
```

### K-1048 — `reference-semantics/semantics.k:44`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/list.k"
```

### K-1049 — `reference-semantics/semantics.k:45`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/tuple.k"
```

### K-1050 — `reference-semantics/semantics.k:46`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/subscript.k"
```

### K-1051 — `reference-semantics/semantics.k:47`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/comprehension.k"
```

### K-1052 — `reference-semantics/semantics.k:48`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/methods.k"
```

### K-1053 — `reference-semantics/semantics.k:49`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/controls.k"
```

### K-1054 — `reference-semantics/semantics.k:50`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/functions.k"
```

### K-1055 — `reference-semantics/semantics.k:51`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/builtins.k"
```

### K-1056 — `reference-semantics/semantics.k:52`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/call.k"
```

### K-1057 — `reference-semantics/semantics.k:53`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/sort.k"
```

### K-1058 — `reference-semantics/semantics.k:54`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/assert.k"
```

### K-1059 — `reference-semantics/semantics.k:55`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "semantics/dict.k"
```

### K-1060 — `reference-semantics/semantics.k:56`

- Kind: `requires`
- Flags: `concrete`
- Decision: assembly checked

```k
requires "semantics/concrete.k"
```

### K-1061 — `reference-semantics/semantics.k:58`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY
```

### K-1062 — `reference-semantics/semantics.k:59`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CORE
```

### K-1063 — `reference-semantics/semantics.k:60`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ITER
```

### K-1064 — `reference-semantics/semantics.k:61`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-RANGE
```

### K-1065 — `reference-semantics/semantics.k:62`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-OPERATORS
```

### K-1066 — `reference-semantics/semantics.k:63`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-INT
```

### K-1067 — `reference-semantics/semantics.k:64`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-BOOL
```

### K-1068 — `reference-semantics/semantics.k:65`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-FLOAT
```

### K-1069 — `reference-semantics/semantics.k:66`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-STR
```

### K-1070 — `reference-semantics/semantics.k:67`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-SET
```

### K-1071 — `reference-semantics/semantics.k:68`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-LIST
```

### K-1072 — `reference-semantics/semantics.k:69`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-TUPLE
```

### K-1073 — `reference-semantics/semantics.k:70`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-SUBSCRIPT
```

### K-1074 — `reference-semantics/semantics.k:71`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-COMPREHENSION
```

### K-1075 — `reference-semantics/semantics.k:72`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-METHODS
```

### K-1076 — `reference-semantics/semantics.k:73`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CONTROLS
```

### K-1077 — `reference-semantics/semantics.k:74`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-FUNCTIONS
```

### K-1078 — `reference-semantics/semantics.k:75`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-BUILTINS
```

### K-1079 — `reference-semantics/semantics.k:76`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CALL
```

### K-1080 — `reference-semantics/semantics.k:77`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-SORT
```

### K-1081 — `reference-semantics/semantics.k:78`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-ASSERT
```

### K-1082 — `reference-semantics/semantics.k:79`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-DICT
```

### K-1083 — `reference-semantics/semantics.k:80`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1084 — `reference-semantics/semantics.k:87`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module MPY-KRUN
```

### K-1085 — `reference-semantics/semantics.k:88`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY
```

### K-1086 — `reference-semantics/semantics.k:89`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY-CONCRETE
```

### K-1087 — `reference-semantics/semantics.k:90`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1088 — `verification.k:1`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "reference-semantics/semantics.k"
```

### K-1089 — `verification.k:3`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module VERIFICATION
```

### K-1090 — `verification.k:4`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports MPY
```

### K-1091 — `verification.k:9`

- Kind: `syntax`
- Flags: `none`
- Decision: declaration checked

```k
  syntax KItem ::= #runIsMultiplyPrime(Int)
                 | "#forgetEntryPoint"
                 | #expect(Bool)
```

### K-1092 — `verification.k:15`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: sound harness/checkpoint rule; no program execution skipped

```k
  rule <k> B:Bool ~> #expect(B) => .K ... </k>
```

### K-1093 — `verification.k:17`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: sound harness/checkpoint rule; no program execution skipped

```k
  rule <k> #runIsMultiplyPrime(A:Int)
        => #loadAll(
             Module(
               FuncDef(
                 "is_multiply_prime",
                 Params("a"),
                 Expr(
                   Str(
                     "Return whether a has exactly three prime factors, with multiplicity."))
                 Assign(Name("factor_count"), Int(0))
                 Assign(Name("factor"), Int(2))
                 While(
                   Compare(
                     BinOp("*", Name("factor"), Name("factor")),
                     CmpOp("<=", Name("a"))),
                   If(
                     Compare(
                       BinOp("%", Name("a"), Name("factor")),
                       CmpOp("==", Int(0))),
                     AugAssign(Name("factor_count"), "+", Int(1))
                     AugAssign(Name("a"), "//", Name("factor")),
                     AugAssign(Name("factor"), "+", Int(1))))
                 If(
                   Compare(Name("a"), CmpOp(">", Int(1))),
                   AugAssign(Name("factor_count"), "+", Int(1)),
                   .Stmts)
                 Return(
                   Compare(
                     Name("factor_count"),
                     CmpOp("==", Int(3)))))))
           ~> Call(Name("is_multiply_prime"), Int(A))
           ~> #forgetEntryPoint ... </k>
```

### K-1094 — `verification.k:50`

- Kind: `rule`
- Flags: `ordinary-semantic-rule`
- Decision: sound harness/checkpoint rule; no program execution skipped

```k
  rule <k> B:Bool ~> #forgetEntryPoint => B ... </k>
       <scopes>
         ... 0 |-> scope(
           M:Map => M [ "is_multiply_prime" <- undef ],
           parent(-1))
         ...
       </scopes>
    requires "is_multiply_prime" in_keys(M)
```

### K-1095 — `verification.k:58`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1096 — `spec.k:1`

- Kind: `requires`
- Flags: `none`
- Decision: assembly checked

```k
requires "verification.k"
```

### K-1097 — `spec.k:8`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-NEGATIVE
```

### K-1098 — `spec.k:9`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1099 — `spec.k:11`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k> #runIsMultiplyPrime(A:Int) => false </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A <Int 2
```

### K-1100 — `spec.k:25`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1101 — `spec.k:27`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-02-11
```

### K-1102 — `spec.k:28`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1103 — `spec.k:30`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(2) ~> #expect(false) ~>
    #runIsMultiplyPrime(3) ~> #expect(false) ~>
    #runIsMultiplyPrime(4) ~> #expect(false) ~>
    #runIsMultiplyPrime(5) ~> #expect(false) ~>
    #runIsMultiplyPrime(6) ~> #expect(false) ~>
    #runIsMultiplyPrime(7) ~> #expect(false) ~>
    #runIsMultiplyPrime(8) ~> #expect(true) ~>
    #runIsMultiplyPrime(9) ~> #expect(false) ~>
    #runIsMultiplyPrime(10) ~> #expect(false) ~>
    #runIsMultiplyPrime(11) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1104 — `spec.k:55`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1105 — `spec.k:57`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-12-21
```

### K-1106 — `spec.k:58`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1107 — `spec.k:60`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(12) ~> #expect(true) ~>
    #runIsMultiplyPrime(13) ~> #expect(false) ~>
    #runIsMultiplyPrime(14) ~> #expect(false) ~>
    #runIsMultiplyPrime(15) ~> #expect(false) ~>
    #runIsMultiplyPrime(16) ~> #expect(false) ~>
    #runIsMultiplyPrime(17) ~> #expect(false) ~>
    #runIsMultiplyPrime(18) ~> #expect(true) ~>
    #runIsMultiplyPrime(19) ~> #expect(false) ~>
    #runIsMultiplyPrime(20) ~> #expect(true) ~>
    #runIsMultiplyPrime(21) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1108 — `spec.k:85`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1109 — `spec.k:87`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-22-31
```

### K-1110 — `spec.k:88`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1111 — `spec.k:90`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(22) ~> #expect(false) ~>
    #runIsMultiplyPrime(23) ~> #expect(false) ~>
    #runIsMultiplyPrime(24) ~> #expect(false) ~>
    #runIsMultiplyPrime(25) ~> #expect(false) ~>
    #runIsMultiplyPrime(26) ~> #expect(false) ~>
    #runIsMultiplyPrime(27) ~> #expect(true) ~>
    #runIsMultiplyPrime(28) ~> #expect(true) ~>
    #runIsMultiplyPrime(29) ~> #expect(false) ~>
    #runIsMultiplyPrime(30) ~> #expect(true) ~>
    #runIsMultiplyPrime(31) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1112 — `spec.k:115`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1113 — `spec.k:117`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-32-41
```

### K-1114 — `spec.k:118`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1115 — `spec.k:120`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(32) ~> #expect(false) ~>
    #runIsMultiplyPrime(33) ~> #expect(false) ~>
    #runIsMultiplyPrime(34) ~> #expect(false) ~>
    #runIsMultiplyPrime(35) ~> #expect(false) ~>
    #runIsMultiplyPrime(36) ~> #expect(false) ~>
    #runIsMultiplyPrime(37) ~> #expect(false) ~>
    #runIsMultiplyPrime(38) ~> #expect(false) ~>
    #runIsMultiplyPrime(39) ~> #expect(false) ~>
    #runIsMultiplyPrime(40) ~> #expect(false) ~>
    #runIsMultiplyPrime(41) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1116 — `spec.k:145`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1117 — `spec.k:147`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-42-51
```

### K-1118 — `spec.k:148`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1119 — `spec.k:150`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(42) ~> #expect(true) ~>
    #runIsMultiplyPrime(43) ~> #expect(false) ~>
    #runIsMultiplyPrime(44) ~> #expect(true) ~>
    #runIsMultiplyPrime(45) ~> #expect(true) ~>
    #runIsMultiplyPrime(46) ~> #expect(false) ~>
    #runIsMultiplyPrime(47) ~> #expect(false) ~>
    #runIsMultiplyPrime(48) ~> #expect(false) ~>
    #runIsMultiplyPrime(49) ~> #expect(false) ~>
    #runIsMultiplyPrime(50) ~> #expect(true) ~>
    #runIsMultiplyPrime(51) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1120 — `spec.k:175`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1121 — `spec.k:177`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-52-61
```

### K-1122 — `spec.k:178`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1123 — `spec.k:180`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(52) ~> #expect(true) ~>
    #runIsMultiplyPrime(53) ~> #expect(false) ~>
    #runIsMultiplyPrime(54) ~> #expect(false) ~>
    #runIsMultiplyPrime(55) ~> #expect(false) ~>
    #runIsMultiplyPrime(56) ~> #expect(false) ~>
    #runIsMultiplyPrime(57) ~> #expect(false) ~>
    #runIsMultiplyPrime(58) ~> #expect(false) ~>
    #runIsMultiplyPrime(59) ~> #expect(false) ~>
    #runIsMultiplyPrime(60) ~> #expect(false) ~>
    #runIsMultiplyPrime(61) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1124 — `spec.k:205`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1125 — `spec.k:207`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-62-71
```

### K-1126 — `spec.k:208`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1127 — `spec.k:210`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(62) ~> #expect(false) ~>
    #runIsMultiplyPrime(63) ~> #expect(true) ~>
    #runIsMultiplyPrime(64) ~> #expect(false) ~>
    #runIsMultiplyPrime(65) ~> #expect(false) ~>
    #runIsMultiplyPrime(66) ~> #expect(true) ~>
    #runIsMultiplyPrime(67) ~> #expect(false) ~>
    #runIsMultiplyPrime(68) ~> #expect(true) ~>
    #runIsMultiplyPrime(69) ~> #expect(false) ~>
    #runIsMultiplyPrime(70) ~> #expect(true) ~>
    #runIsMultiplyPrime(71) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1128 — `spec.k:235`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1129 — `spec.k:237`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-72-81
```

### K-1130 — `spec.k:238`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1131 — `spec.k:240`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(72) ~> #expect(false) ~>
    #runIsMultiplyPrime(73) ~> #expect(false) ~>
    #runIsMultiplyPrime(74) ~> #expect(false) ~>
    #runIsMultiplyPrime(75) ~> #expect(true) ~>
    #runIsMultiplyPrime(76) ~> #expect(true) ~>
    #runIsMultiplyPrime(77) ~> #expect(false) ~>
    #runIsMultiplyPrime(78) ~> #expect(true) ~>
    #runIsMultiplyPrime(79) ~> #expect(false) ~>
    #runIsMultiplyPrime(80) ~> #expect(false) ~>
    #runIsMultiplyPrime(81) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1132 — `spec.k:265`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1133 — `spec.k:267`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-82-91
```

### K-1134 — `spec.k:268`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1135 — `spec.k:270`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(82) ~> #expect(false) ~>
    #runIsMultiplyPrime(83) ~> #expect(false) ~>
    #runIsMultiplyPrime(84) ~> #expect(false) ~>
    #runIsMultiplyPrime(85) ~> #expect(false) ~>
    #runIsMultiplyPrime(86) ~> #expect(false) ~>
    #runIsMultiplyPrime(87) ~> #expect(false) ~>
    #runIsMultiplyPrime(88) ~> #expect(false) ~>
    #runIsMultiplyPrime(89) ~> #expect(false) ~>
    #runIsMultiplyPrime(90) ~> #expect(false) ~>
    #runIsMultiplyPrime(91) ~> #expect(false)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1136 — `spec.k:295`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

### K-1137 — `spec.k:297`

- Kind: `module`
- Flags: `none`
- Decision: assembly checked

```k
module SPEC-92-99
```

### K-1138 — `spec.k:298`

- Kind: `imports`
- Flags: `none`
- Decision: assembly checked

```k
  imports VERIFICATION
```

### K-1139 — `spec.k:300`

- Kind: `claim`
- Flags: `none`
- Decision: result obligation; adequacy checked separately

```k
  claim <k>
    #runIsMultiplyPrime(92) ~> #expect(true) ~>
    #runIsMultiplyPrime(93) ~> #expect(false) ~>
    #runIsMultiplyPrime(94) ~> #expect(false) ~>
    #runIsMultiplyPrime(95) ~> #expect(false) ~>
    #runIsMultiplyPrime(96) ~> #expect(false) ~>
    #runIsMultiplyPrime(97) ~> #expect(false) ~>
    #runIsMultiplyPrime(98) ~> #expect(true) ~>
    #runIsMultiplyPrime(99) ~> #expect(true)
    => .K
  </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
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

### K-1140 — `spec.k:323`

- Kind: `endmodule`
- Flags: `none`
- Decision: assembly checked

```k
endmodule
```

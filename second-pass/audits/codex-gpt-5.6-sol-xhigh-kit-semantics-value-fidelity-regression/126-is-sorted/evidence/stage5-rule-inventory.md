# Exhaustive K declaration and rule inventory

Generated from the fresh scratch source. The supplied-semantics entries are fixed by the trusted byte-identical baseline; proof-local entries require independent substantive review.

SOURCE_SET_SHA256: `505369f40d15ccda9964f6a2a6aa43d1211ad5820b8979e8fd8ede31bd50c3db`

TOTAL_ITEMS: 946

## Counts by file and kind

| File | Kind | Count |
|---|---:|---:|
| `reference-semantics/semantics.k` | no local syntax/config/rule/claim | 0 |
| `reference-semantics/semantics/assert.k` | rule | 3 |
| `reference-semantics/semantics/bool.k` | context | 1 |
| `reference-semantics/semantics/bool.k` | rule | 13 |
| `reference-semantics/semantics/builtins.k` | rule | 137 |
| `reference-semantics/semantics/builtins.k` | syntax | 38 |
| `reference-semantics/semantics/call.k` | rule | 21 |
| `reference-semantics/semantics/call.k` | syntax | 3 |
| `reference-semantics/semantics/comprehension.k` | rule | 7 |
| `reference-semantics/semantics/comprehension.k` | syntax | 3 |
| `reference-semantics/semantics/concrete.k` | rule | 16 |
| `reference-semantics/semantics/concrete.k` | syntax | 5 |
| `reference-semantics/semantics/controls.k` | rule | 34 |
| `reference-semantics/semantics/controls.k` | syntax | 3 |
| `reference-semantics/semantics/core.k` | configuration | 1 |
| `reference-semantics/semantics/core.k` | rule | 46 |
| `reference-semantics/semantics/core.k` | syntax | 37 |
| `reference-semantics/semantics/dict.k` | rule | 28 |
| `reference-semantics/semantics/dict.k` | syntax | 12 |
| `reference-semantics/semantics/float.k` | rule | 121 |
| `reference-semantics/semantics/float.k` | syntax | 34 |
| `reference-semantics/semantics/functions.k` | rule | 15 |
| `reference-semantics/semantics/functions.k` | syntax | 4 |
| `reference-semantics/semantics/int.k` | rule | 16 |
| `reference-semantics/semantics/int.k` | syntax | 1 |
| `reference-semantics/semantics/iter.k` | syntax | 1 |
| `reference-semantics/semantics/list.k` | rule | 27 |
| `reference-semantics/semantics/list.k` | syntax | 5 |
| `reference-semantics/semantics/methods.k` | rule | 75 |
| `reference-semantics/semantics/methods.k` | syntax | 27 |
| `reference-semantics/semantics/operators.k` | context | 2 |
| `reference-semantics/semantics/operators.k` | rule | 10 |
| `reference-semantics/semantics/range.k` | rule | 6 |
| `reference-semantics/semantics/range.k` | syntax | 2 |
| `reference-semantics/semantics/set.k` | rule | 12 |
| `reference-semantics/semantics/set.k` | syntax | 6 |
| `reference-semantics/semantics/sort.k` | rule | 19 |
| `reference-semantics/semantics/sort.k` | syntax | 6 |
| `reference-semantics/semantics/str.k` | rule | 28 |
| `reference-semantics/semantics/str.k` | syntax | 5 |
| `reference-semantics/semantics/subscript.k` | context | 2 |
| `reference-semantics/semantics/subscript.k` | rule | 40 |
| `reference-semantics/semantics/subscript.k` | syntax | 15 |
| `reference-semantics/semantics/syntax.k` | syntax | 16 |
| `reference-semantics/semantics/tuple.k` | rule | 21 |
| `reference-semantics/semantics/tuple.k` | syntax | 4 |
| `spec.k` | claim | 2 |
| `verification.k` | rule | 12 |
| `verification.k` | syntax | 4 |

## Attribute/tag counts

| Tag | Count |
|---|---:|
| concrete | 35 |
| function | 148 |
| macro | 6 |
| no-evaluators | 22 |
| owise | 27 |
| priority | 45 |
| symbol | 25 |
| total | 109 |

## Every declaration/rule/claim

### K-0001: `reference-semantics/semantics/assert.k:6`

- Kind: rule
- Lines: 6-7
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### K-0002: `reference-semantics/semantics/assert.k:8`

- Kind: rule
- Lines: 8-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### K-0003: `reference-semantics/semantics/assert.k:13`

- Kind: rule
- Lines: 13-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0004: `reference-semantics/semantics/bool.k:8`

- Kind: rule
- Lines: 8-8
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### K-0005: `reference-semantics/semantics/bool.k:10`

- Kind: rule
- Lines: 10-10
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### K-0006: `reference-semantics/semantics/bool.k:11`

- Kind: rule
- Lines: 11-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### K-0007: `reference-semantics/semantics/bool.k:16`

- Kind: context
- Lines: 16-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### K-0008: `reference-semantics/semantics/bool.k:17`

- Kind: rule
- Lines: 17-17
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### K-0009: `reference-semantics/semantics/bool.k:18`

- Kind: rule
- Lines: 18-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### K-0010: `reference-semantics/semantics/bool.k:20`

- Kind: rule
- Lines: 20-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### K-0011: `reference-semantics/semantics/bool.k:22`

- Kind: rule
- Lines: 22-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### K-0012: `reference-semantics/semantics/bool.k:24`

- Kind: rule
- Lines: 24-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

### K-0013: `reference-semantics/semantics/bool.k:29`

- Kind: rule
- Lines: 29-30
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### K-0014: `reference-semantics/semantics/bool.k:31`

- Kind: rule
- Lines: 31-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K-0015: `reference-semantics/semantics/bool.k:35`

- Kind: rule
- Lines: 35-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K-0016: `reference-semantics/semantics/bool.k:39`

- Kind: rule
- Lines: 39-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K-0017: `reference-semantics/semantics/bool.k:43`

- Kind: rule
- Lines: 43-46
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K-0018: `reference-semantics/semantics/builtins.k:17`

- Kind: syntax
- Lines: 17-17
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### K-0019: `reference-semantics/semantics/builtins.k:20`

- Kind: syntax
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= seqLen(Val) [function]
```

### K-0020: `reference-semantics/semantics/builtins.k:21`

- Kind: rule
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### K-0021: `reference-semantics/semantics/builtins.k:22`

- Kind: rule
- Lines: 22-22
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### K-0022: `reference-semantics/semantics/builtins.k:23`

- Kind: rule
- Lines: 23-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### K-0023: `reference-semantics/semantics/builtins.k:24`

- Kind: rule
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### K-0024: `reference-semantics/semantics/builtins.k:25`

- Kind: rule
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### K-0025: `reference-semantics/semantics/builtins.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### K-0026: `reference-semantics/semantics/builtins.k:32`

- Kind: rule
- Lines: 32-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### K-0027: `reference-semantics/semantics/builtins.k:33`

- Kind: rule
- Lines: 33-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### K-0028: `reference-semantics/semantics/builtins.k:34`

- Kind: rule
- Lines: 34-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### K-0029: `reference-semantics/semantics/builtins.k:35`

- Kind: rule
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### K-0030: `reference-semantics/semantics/builtins.k:36`

- Kind: syntax
- Lines: 36-36
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### K-0031: `reference-semantics/semantics/builtins.k:37`

- Kind: rule
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### K-0032: `reference-semantics/semantics/builtins.k:38`

- Kind: rule
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### K-0033: `reference-semantics/semantics/builtins.k:41`

- Kind: rule
- Lines: 41-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### K-0034: `reference-semantics/semantics/builtins.k:44`

- Kind: rule
- Lines: 44-44
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### K-0035: `reference-semantics/semantics/builtins.k:47`

- Kind: syntax
- Lines: 47-47
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### K-0036: `reference-semantics/semantics/builtins.k:48`

- Kind: rule
- Lines: 48-48
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### K-0037: `reference-semantics/semantics/builtins.k:49`

- Kind: rule
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### K-0038: `reference-semantics/semantics/builtins.k:50`

- Kind: rule
- Lines: 50-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K-0039: `reference-semantics/semantics/builtins.k:54`

- Kind: syntax
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= intOf(Val) [function]
```

### K-0040: `reference-semantics/semantics/builtins.k:55`

- Kind: rule
- Lines: 55-55
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intOf(I:Int)  => I
```

### K-0041: `reference-semantics/semantics/builtins.k:56`

- Kind: rule
- Lines: 56-56
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### K-0042: `reference-semantics/semantics/builtins.k:59`

- Kind: syntax
- Lines: 59-59
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### K-0043: `reference-semantics/semantics/builtins.k:60`

- Kind: rule
- Lines: 60-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### K-0044: `reference-semantics/semantics/builtins.k:61`

- Kind: rule
- Lines: 61-61
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### K-0045: `reference-semantics/semantics/builtins.k:62`

- Kind: rule
- Lines: 62-63
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### K-0046: `reference-semantics/semantics/builtins.k:64`

- Kind: rule
- Lines: 64-65
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### K-0047: `reference-semantics/semantics/builtins.k:67`

- Kind: syntax
- Lines: 67-67
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### K-0048: `reference-semantics/semantics/builtins.k:68`

- Kind: rule
- Lines: 68-68
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### K-0049: `reference-semantics/semantics/builtins.k:69`

- Kind: rule
- Lines: 69-69
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### K-0050: `reference-semantics/semantics/builtins.k:70`

- Kind: rule
- Lines: 70-71
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### K-0051: `reference-semantics/semantics/builtins.k:72`

- Kind: rule
- Lines: 72-73
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

### K-0052: `reference-semantics/semantics/builtins.k:76`

- Kind: syntax
- Lines: 76-76
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### K-0053: `reference-semantics/semantics/builtins.k:77`

- Kind: rule
- Lines: 77-77
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### K-0054: `reference-semantics/semantics/builtins.k:78`

- Kind: rule
- Lines: 78-79
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K-0055: `reference-semantics/semantics/builtins.k:80`

- Kind: rule
- Lines: 80-80
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### K-0056: `reference-semantics/semantics/builtins.k:81`

- Kind: rule
- Lines: 81-81
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### K-0057: `reference-semantics/semantics/builtins.k:82`

- Kind: rule
- Lines: 82-84
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K-0058: `reference-semantics/semantics/builtins.k:86`

- Kind: syntax
- Lines: 86-86
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### K-0059: `reference-semantics/semantics/builtins.k:87`

- Kind: rule
- Lines: 87-87
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### K-0060: `reference-semantics/semantics/builtins.k:88`

- Kind: rule
- Lines: 88-89
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K-0061: `reference-semantics/semantics/builtins.k:90`

- Kind: rule
- Lines: 90-90
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### K-0062: `reference-semantics/semantics/builtins.k:91`

- Kind: rule
- Lines: 91-91
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### K-0063: `reference-semantics/semantics/builtins.k:92`

- Kind: rule
- Lines: 92-94
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K-0064: `reference-semantics/semantics/builtins.k:97`

- Kind: syntax
- Lines: 97-97
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### K-0065: `reference-semantics/semantics/builtins.k:98`

- Kind: rule
- Lines: 98-98
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### K-0066: `reference-semantics/semantics/builtins.k:99`

- Kind: rule
- Lines: 99-99
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule maxVals(M:Int, .Vals)           => M
```

### K-0067: `reference-semantics/semantics/builtins.k:100`

- Kind: rule
- Lines: 100-100
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### K-0068: `reference-semantics/semantics/builtins.k:102`

- Kind: syntax
- Lines: 102-102
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### K-0069: `reference-semantics/semantics/builtins.k:103`

- Kind: rule
- Lines: 103-103
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### K-0070: `reference-semantics/semantics/builtins.k:104`

- Kind: rule
- Lines: 104-104
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule minVals(M:Int, .Vals)           => M
```

### K-0071: `reference-semantics/semantics/builtins.k:105`

- Kind: rule
- Lines: 105-105
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### K-0072: `reference-semantics/semantics/builtins.k:108`

- Kind: rule
- Lines: 108-109
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

### K-0073: `reference-semantics/semantics/builtins.k:111`

- Kind: rule
- Lines: 111-113
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### K-0074: `reference-semantics/semantics/builtins.k:114`

- Kind: syntax
- Lines: 114-114
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### K-0075: `reference-semantics/semantics/builtins.k:115`

- Kind: rule
- Lines: 115-115
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### K-0076: `reference-semantics/semantics/builtins.k:116`

- Kind: rule
- Lines: 116-116
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### K-0077: `reference-semantics/semantics/builtins.k:117`

- Kind: syntax
- Lines: 117-117
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### K-0078: `reference-semantics/semantics/builtins.k:118`

- Kind: rule
- Lines: 118-118
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### K-0079: `reference-semantics/semantics/builtins.k:119`

- Kind: rule
- Lines: 119-121
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

### K-0080: `reference-semantics/semantics/builtins.k:124`

- Kind: rule
- Lines: 124-125
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### K-0081: `reference-semantics/semantics/builtins.k:126`

- Kind: syntax
- Lines: 126-126
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### K-0082: `reference-semantics/semantics/builtins.k:127`

- Kind: rule
- Lines: 127-127
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### K-0083: `reference-semantics/semantics/builtins.k:128`

- Kind: rule
- Lines: 128-129
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### K-0084: `reference-semantics/semantics/builtins.k:132`

- Kind: rule
- Lines: 132-133
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### K-0085: `reference-semantics/semantics/builtins.k:134`

- Kind: syntax
- Lines: 134-134
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### K-0086: `reference-semantics/semantics/builtins.k:135`

- Kind: rule
- Lines: 135-135
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### K-0087: `reference-semantics/semantics/builtins.k:136`

- Kind: rule
- Lines: 136-136
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### K-0088: `reference-semantics/semantics/builtins.k:137`

- Kind: rule
- Lines: 137-137
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### K-0089: `reference-semantics/semantics/builtins.k:140`

- Kind: rule
- Lines: 140-140
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### K-0090: `reference-semantics/semantics/builtins.k:143`

- Kind: rule
- Lines: 143-143
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### K-0091: `reference-semantics/semantics/builtins.k:144`

- Kind: rule
- Lines: 144-145
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

### K-0092: `reference-semantics/semantics/builtins.k:148`

- Kind: rule
- Lines: 148-148
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### K-0093: `reference-semantics/semantics/builtins.k:149`

- Kind: rule
- Lines: 149-149
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### K-0094: `reference-semantics/semantics/builtins.k:152`

- Kind: rule
- Lines: 152-153
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

### K-0095: `reference-semantics/semantics/builtins.k:156`

- Kind: rule
- Lines: 156-157
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### K-0096: `reference-semantics/semantics/builtins.k:158`

- Kind: syntax
- Lines: 158-158
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### K-0097: `reference-semantics/semantics/builtins.k:159`

- Kind: rule
- Lines: 159-159
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### K-0098: `reference-semantics/semantics/builtins.k:160`

- Kind: rule
- Lines: 160-160
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### K-0099: `reference-semantics/semantics/builtins.k:163`

- Kind: rule
- Lines: 163-163
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### K-0100: `reference-semantics/semantics/builtins.k:164`

- Kind: rule
- Lines: 164-164
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### K-0101: `reference-semantics/semantics/builtins.k:167`

- Kind: rule
- Lines: 167-168
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### K-0102: `reference-semantics/semantics/builtins.k:169`

- Kind: rule
- Lines: 169-169
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### K-0103: `reference-semantics/semantics/builtins.k:170`

- Kind: rule
- Lines: 170-170
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### K-0104: `reference-semantics/semantics/builtins.k:171`

- Kind: rule
- Lines: 171-172
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### K-0105: `reference-semantics/semantics/builtins.k:173`

- Kind: rule
- Lines: 173-173
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### K-0106: `reference-semantics/semantics/builtins.k:174`

- Kind: rule
- Lines: 174-174
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### K-0107: `reference-semantics/semantics/builtins.k:177`

- Kind: rule
- Lines: 177-177
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### K-0108: `reference-semantics/semantics/builtins.k:178`

- Kind: rule
- Lines: 178-178
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### K-0109: `reference-semantics/semantics/builtins.k:179`

- Kind: rule
- Lines: 179-180
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

### K-0110: `reference-semantics/semantics/builtins.k:187`

- Kind: rule
- Lines: 187-187
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### K-0111: `reference-semantics/semantics/builtins.k:188`

- Kind: syntax
- Lines: 188-188
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### K-0112: `reference-semantics/semantics/builtins.k:189`

- Kind: rule
- Lines: 189-190
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### K-0113: `reference-semantics/semantics/builtins.k:192`

- Kind: syntax
- Lines: 192-192
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### K-0114: `reference-semantics/semantics/builtins.k:194`

- Kind: syntax
- Lines: 194-194
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### K-0115: `reference-semantics/semantics/builtins.k:195`

- Kind: rule
- Lines: 195-195
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K-0116: `reference-semantics/semantics/builtins.k:196`

- Kind: syntax
- Lines: 196-196
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### K-0117: `reference-semantics/semantics/builtins.k:197`

- Kind: rule
- Lines: 197-197
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### K-0118: `reference-semantics/semantics/builtins.k:198`

- Kind: rule
- Lines: 198-198
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### K-0119: `reference-semantics/semantics/builtins.k:199`

- Kind: syntax
- Lines: 199-199
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### K-0120: `reference-semantics/semantics/builtins.k:200`

- Kind: rule
- Lines: 200-200
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### K-0121: `reference-semantics/semantics/builtins.k:201`

- Kind: rule
- Lines: 201-201
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### K-0122: `reference-semantics/semantics/builtins.k:203`

- Kind: syntax
- Lines: 203-203
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### K-0123: `reference-semantics/semantics/builtins.k:204`

- Kind: rule
- Lines: 204-204
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### K-0124: `reference-semantics/semantics/builtins.k:205`

- Kind: rule
- Lines: 205-205
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### K-0125: `reference-semantics/semantics/builtins.k:206`

- Kind: rule
- Lines: 206-206
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### K-0126: `reference-semantics/semantics/builtins.k:207`

- Kind: rule
- Lines: 207-207
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### K-0127: `reference-semantics/semantics/builtins.k:208`

- Kind: rule
- Lines: 208-208
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### K-0128: `reference-semantics/semantics/builtins.k:209`

- Kind: rule
- Lines: 209-209
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### K-0129: `reference-semantics/semantics/builtins.k:210`

- Kind: rule
- Lines: 210-210
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### K-0130: `reference-semantics/semantics/builtins.k:211`

- Kind: rule
- Lines: 211-211
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### K-0131: `reference-semantics/semantics/builtins.k:212`

- Kind: rule
- Lines: 212-212
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### K-0132: `reference-semantics/semantics/builtins.k:214`

- Kind: syntax
- Lines: 214-215
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### K-0133: `reference-semantics/semantics/builtins.k:216`

- Kind: rule
- Lines: 216-216
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### K-0134: `reference-semantics/semantics/builtins.k:217`

- Kind: rule
- Lines: 217-217
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### K-0135: `reference-semantics/semantics/builtins.k:218`

- Kind: rule
- Lines: 218-218
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### K-0136: `reference-semantics/semantics/builtins.k:219`

- Kind: rule
- Lines: 219-220
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### K-0137: `reference-semantics/semantics/builtins.k:221`

- Kind: rule
- Lines: 221-222
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### K-0138: `reference-semantics/semantics/builtins.k:223`

- Kind: rule
- Lines: 223-223
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### K-0139: `reference-semantics/semantics/builtins.k:225`

- Kind: syntax
- Lines: 225-225
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### K-0140: `reference-semantics/semantics/builtins.k:226`

- Kind: syntax
- Lines: 226-226
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### K-0141: `reference-semantics/semantics/builtins.k:227`

- Kind: rule
- Lines: 227-227
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### K-0142: `reference-semantics/semantics/builtins.k:228`

- Kind: rule
- Lines: 228-228
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### K-0143: `reference-semantics/semantics/builtins.k:230`

- Kind: syntax
- Lines: 230-230
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### K-0144: `reference-semantics/semantics/builtins.k:231`

- Kind: rule
- Lines: 231-231
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### K-0145: `reference-semantics/semantics/builtins.k:232`

- Kind: rule
- Lines: 232-232
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### K-0146: `reference-semantics/semantics/builtins.k:233`

- Kind: rule
- Lines: 233-233
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### K-0147: `reference-semantics/semantics/builtins.k:234`

- Kind: rule
- Lines: 234-234
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### K-0148: `reference-semantics/semantics/builtins.k:235`

- Kind: rule
- Lines: 235-235
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### K-0149: `reference-semantics/semantics/builtins.k:236`

- Kind: rule
- Lines: 236-236
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### K-0150: `reference-semantics/semantics/builtins.k:238`

- Kind: syntax
- Lines: 238-238
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### K-0151: `reference-semantics/semantics/builtins.k:239`

- Kind: rule
- Lines: 239-239
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### K-0152: `reference-semantics/semantics/builtins.k:240`

- Kind: rule
- Lines: 240-240
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### K-0153: `reference-semantics/semantics/builtins.k:241`

- Kind: rule
- Lines: 241-242
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### K-0154: `reference-semantics/semantics/builtins.k:243`

- Kind: rule
- Lines: 243-243
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### K-0155: `reference-semantics/semantics/builtins.k:244`

- Kind: syntax
- Lines: 244-244
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### K-0156: `reference-semantics/semantics/builtins.k:245`

- Kind: rule
- Lines: 245-245
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### K-0157: `reference-semantics/semantics/builtins.k:246`

- Kind: rule
- Lines: 246-246
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### K-0158: `reference-semantics/semantics/builtins.k:247`

- Kind: syntax
- Lines: 247-247
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### K-0159: `reference-semantics/semantics/builtins.k:248`

- Kind: rule
- Lines: 248-248
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### K-0160: `reference-semantics/semantics/builtins.k:250`

- Kind: syntax
- Lines: 250-250
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### K-0161: `reference-semantics/semantics/builtins.k:251`

- Kind: rule
- Lines: 251-251
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K-0162: `reference-semantics/semantics/builtins.k:252`

- Kind: rule
- Lines: 252-252
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K-0163: `reference-semantics/semantics/builtins.k:253`

- Kind: rule
- Lines: 253-253
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K-0164: `reference-semantics/semantics/builtins.k:254`

- Kind: rule
- Lines: 254-254
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K-0165: `reference-semantics/semantics/builtins.k:255`

- Kind: syntax
- Lines: 255-255
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### K-0166: `reference-semantics/semantics/builtins.k:256`

- Kind: rule
- Lines: 256-256
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### K-0167: `reference-semantics/semantics/builtins.k:257`

- Kind: rule
- Lines: 257-259
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### K-0168: `reference-semantics/semantics/builtins.k:260`

- Kind: rule
- Lines: 260-262
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### K-0169: `reference-semantics/semantics/builtins.k:263`

- Kind: rule
- Lines: 263-264
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### K-0170: `reference-semantics/semantics/builtins.k:265`

- Kind: syntax
- Lines: 265-265
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### K-0171: `reference-semantics/semantics/builtins.k:266`

- Kind: rule
- Lines: 266-266
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### K-0172: `reference-semantics/semantics/builtins.k:267`

- Kind: rule
- Lines: 267-267
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### K-0173: `reference-semantics/semantics/builtins.k:268`

- Kind: rule
- Lines: 268-268
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### K-0174: `reference-semantics/semantics/builtins.k:269`

- Kind: syntax
- Lines: 269-269
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### K-0175: `reference-semantics/semantics/builtins.k:270`

- Kind: rule
- Lines: 270-270
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### K-0176: `reference-semantics/semantics/builtins.k:271`

- Kind: rule
- Lines: 271-271
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### K-0177: `reference-semantics/semantics/builtins.k:272`

- Kind: syntax
- Lines: 272-272
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### K-0178: `reference-semantics/semantics/builtins.k:273`

- Kind: rule
- Lines: 273-273
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### K-0179: `reference-semantics/semantics/builtins.k:274`

- Kind: rule
- Lines: 274-274
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### K-0180: `reference-semantics/semantics/builtins.k:279`

- Kind: syntax
- Lines: 279-279
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= "#md5"
```

### K-0181: `reference-semantics/semantics/builtins.k:280`

- Kind: rule
- Lines: 280-281
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### K-0182: `reference-semantics/semantics/builtins.k:282`

- Kind: rule
- Lines: 282-282
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### K-0183: `reference-semantics/semantics/builtins.k:283`

- Kind: syntax
- Lines: 283-283
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= md5Obj(IntSeq)
```

### K-0184: `reference-semantics/semantics/builtins.k:284`

- Kind: rule
- Lines: 284-284
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### K-0185: `reference-semantics/semantics/builtins.k:285`

- Kind: syntax
- Lines: 285-285
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### K-0186: `reference-semantics/semantics/builtins.k:291`

- Kind: rule
- Lines: 291-291
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### K-0187: `reference-semantics/semantics/builtins.k:292`

- Kind: rule
- Lines: 292-292
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### K-0188: `reference-semantics/semantics/builtins.k:293`

- Kind: syntax
- Lines: 293-293
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### K-0189: `reference-semantics/semantics/builtins.k:294`

- Kind: rule
- Lines: 294-294
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isIntV(_:Int)         => true
```

### K-0190: `reference-semantics/semantics/builtins.k:295`

- Kind: rule
- Lines: 295-295
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isIntV(_:Val)         => false [owise]
```

### K-0191: `reference-semantics/semantics/builtins.k:296`

- Kind: rule
- Lines: 296-296
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isStrV(str(_:IntSeq)) => true
```

### K-0192: `reference-semantics/semantics/builtins.k:297`

- Kind: rule
- Lines: 297-297
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isStrV(_:Val)         => false [owise]
```

### K-0193: `reference-semantics/semantics/call.k:16`

- Kind: rule
- Lines: 16-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### K-0194: `reference-semantics/semantics/call.k:19`

- Kind: syntax
- Lines: 19-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #callee(Exprs)
```

### K-0195: `reference-semantics/semantics/call.k:20`

- Kind: rule
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### K-0196: `reference-semantics/semantics/call.k:21`

- Kind: rule
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### K-0197: `reference-semantics/semantics/call.k:24`

- Kind: rule
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### K-0198: `reference-semantics/semantics/call.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### K-0199: `reference-semantics/semantics/call.k:27`

- Kind: rule
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### K-0200: `reference-semantics/semantics/call.k:28`

- Kind: rule
- Lines: 28-28
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### K-0201: `reference-semantics/semantics/call.k:29`

- Kind: rule
- Lines: 29-29
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### K-0202: `reference-semantics/semantics/call.k:30`

- Kind: rule
- Lines: 30-30
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### K-0203: `reference-semantics/semantics/call.k:31`

- Kind: rule
- Lines: 31-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### K-0204: `reference-semantics/semantics/call.k:32`

- Kind: rule
- Lines: 32-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### K-0205: `reference-semantics/semantics/call.k:38`

- Kind: rule
- Lines: 38-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0206: `reference-semantics/semantics/call.k:42`

- Kind: rule
- Lines: 42-46
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### K-0207: `reference-semantics/semantics/call.k:47`

- Kind: rule
- Lines: 47-50
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0208: `reference-semantics/semantics/call.k:52`

- Kind: syntax
- Lines: 52-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### K-0209: `reference-semantics/semantics/call.k:53`

- Kind: rule
- Lines: 53-55
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### K-0210: `reference-semantics/semantics/call.k:56`

- Kind: rule
- Lines: 56-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

### K-0211: `reference-semantics/semantics/call.k:63`

- Kind: rule
- Lines: 63-67
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### K-0212: `reference-semantics/semantics/call.k:69`

- Kind: rule
- Lines: 69-74
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K-0213: `reference-semantics/semantics/call.k:80`

- Kind: rule
- Lines: 80-85
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K-0214: `reference-semantics/semantics/call.k:87`

- Kind: syntax
- Lines: 87-87
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### K-0215: `reference-semantics/semantics/call.k:88`

- Kind: rule
- Lines: 88-88
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### K-0216: `reference-semantics/semantics/call.k:89`

- Kind: rule
- Lines: 89-94
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K-0217: `reference-semantics/semantics/comprehension.k:11`

- Kind: rule
- Lines: 11-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K-0218: `reference-semantics/semantics/comprehension.k:12`

- Kind: rule
- Lines: 12-12
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K-0219: `reference-semantics/semantics/comprehension.k:14`

- Kind: syntax
- Lines: 14-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: macro
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### K-0220: `reference-semantics/semantics/comprehension.k:15`

- Kind: rule
- Lines: 15-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### K-0221: `reference-semantics/semantics/comprehension.k:18`

- Kind: syntax
- Lines: 18-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: macro
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### K-0222: `reference-semantics/semantics/comprehension.k:19`

- Kind: rule
- Lines: 19-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### K-0223: `reference-semantics/semantics/comprehension.k:21`

- Kind: rule
- Lines: 21-22
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### K-0224: `reference-semantics/semantics/comprehension.k:24`

- Kind: syntax
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: macro
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### K-0225: `reference-semantics/semantics/comprehension.k:25`

- Kind: rule
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### K-0226: `reference-semantics/semantics/comprehension.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### K-0227: `reference-semantics/semantics/concrete.k:13`

- Kind: rule
- Lines: 13-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K-0228: `reference-semantics/semantics/concrete.k:16`

- Kind: rule
- Lines: 16-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K-0229: `reference-semantics/semantics/concrete.k:25`

- Kind: syntax
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= kvP(Val, Val)
```

### K-0230: `reference-semantics/semantics/concrete.k:26`

- Kind: syntax
- Lines: 26-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### K-0231: `reference-semantics/semantics/concrete.k:28`

- Kind: rule
- Lines: 28-30
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### K-0232: `reference-semantics/semantics/concrete.k:31`

- Kind: rule
- Lines: 31-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### K-0233: `reference-semantics/semantics/concrete.k:34`

- Kind: rule
- Lines: 34-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### K-0234: `reference-semantics/semantics/concrete.k:36`

- Kind: rule
- Lines: 36-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### K-0235: `reference-semantics/semantics/concrete.k:38`

- Kind: rule
- Lines: 38-40
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### K-0236: `reference-semantics/semantics/concrete.k:42`

- Kind: syntax
- Lines: 42-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### K-0237: `reference-semantics/semantics/concrete.k:43`

- Kind: rule
- Lines: 43-43
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### K-0238: `reference-semantics/semantics/concrete.k:44`

- Kind: rule
- Lines: 44-46
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### K-0239: `reference-semantics/semantics/concrete.k:47`

- Kind: rule
- Lines: 47-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### K-0240: `reference-semantics/semantics/concrete.k:51`

- Kind: syntax
- Lines: 51-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### K-0241: `reference-semantics/semantics/concrete.k:52`

- Kind: rule
- Lines: 52-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### K-0242: `reference-semantics/semantics/concrete.k:53`

- Kind: rule
- Lines: 53-53
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### K-0243: `reference-semantics/semantics/concrete.k:54`

- Kind: rule
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K-0244: `reference-semantics/semantics/concrete.k:56`

- Kind: syntax
- Lines: 56-56
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### K-0245: `reference-semantics/semantics/concrete.k:57`

- Kind: rule
- Lines: 57-57
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### K-0246: `reference-semantics/semantics/concrete.k:58`

- Kind: rule
- Lines: 58-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### K-0247: `reference-semantics/semantics/concrete.k:59`

- Kind: rule
- Lines: 59-59
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### K-0248: `reference-semantics/semantics/controls.k:9`

- Kind: rule
- Lines: 9-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K-0249: `reference-semantics/semantics/controls.k:12`

- Kind: rule
- Lines: 12-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K-0250: `reference-semantics/semantics/controls.k:20`

- Kind: rule
- Lines: 20-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

### K-0251: `reference-semantics/semantics/controls.k:27`

- Kind: rule
- Lines: 27-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

### K-0252: `reference-semantics/semantics/controls.k:35`

- Kind: rule
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### K-0253: `reference-semantics/semantics/controls.k:36`

- Kind: rule
- Lines: 36-36
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### K-0254: `reference-semantics/semantics/controls.k:37`

- Kind: syntax
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### K-0255: `reference-semantics/semantics/controls.k:38`

- Kind: rule
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### K-0256: `reference-semantics/semantics/controls.k:39`

- Kind: rule
- Lines: 39-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### K-0257: `reference-semantics/semantics/controls.k:43`

- Kind: rule
- Lines: 43-44
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### K-0258: `reference-semantics/semantics/controls.k:48`

- Kind: rule
- Lines: 48-48
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### K-0259: `reference-semantics/semantics/controls.k:51`

- Kind: syntax
- Lines: 51-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### K-0260: `reference-semantics/semantics/controls.k:52`

- Kind: rule
- Lines: 52-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### K-0261: `reference-semantics/semantics/controls.k:53`

- Kind: rule
- Lines: 53-53
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### K-0262: `reference-semantics/semantics/controls.k:54`

- Kind: rule
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### K-0263: `reference-semantics/semantics/controls.k:57`

- Kind: rule
- Lines: 57-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### K-0264: `reference-semantics/semantics/controls.k:59`

- Kind: rule
- Lines: 59-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

### K-0265: `reference-semantics/semantics/controls.k:65`

- Kind: syntax
- Lines: 65-67
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### K-0266: `reference-semantics/semantics/controls.k:69`

- Kind: rule
- Lines: 69-69
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### K-0267: `reference-semantics/semantics/controls.k:71`

- Kind: rule
- Lines: 71-71
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### K-0268: `reference-semantics/semantics/controls.k:72`

- Kind: rule
- Lines: 72-72
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### K-0269: `reference-semantics/semantics/controls.k:73`

- Kind: rule
- Lines: 73-74
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### K-0270: `reference-semantics/semantics/controls.k:77`

- Kind: rule
- Lines: 77-77
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### K-0271: `reference-semantics/semantics/controls.k:78`

- Kind: rule
- Lines: 78-78
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### K-0272: `reference-semantics/semantics/controls.k:79`

- Kind: rule
- Lines: 79-80
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### K-0273: `reference-semantics/semantics/controls.k:81`

- Kind: rule
- Lines: 81-82
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

### K-0274: `reference-semantics/semantics/controls.k:85`

- Kind: rule
- Lines: 85-85
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K-0275: `reference-semantics/semantics/controls.k:86`

- Kind: rule
- Lines: 86-86
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Continue => #cont ... </k>
```

### K-0276: `reference-semantics/semantics/controls.k:87`

- Kind: rule
- Lines: 87-87
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Break => #brk ... </k>
```

### K-0277: `reference-semantics/semantics/controls.k:88`

- Kind: rule
- Lines: 88-88
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K-0278: `reference-semantics/semantics/controls.k:89`

- Kind: rule
- Lines: 89-89
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### K-0279: `reference-semantics/semantics/controls.k:90`

- Kind: rule
- Lines: 90-90
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### K-0280: `reference-semantics/semantics/controls.k:91`

- Kind: rule
- Lines: 91-91
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### K-0281: `reference-semantics/semantics/controls.k:95`

- Kind: rule
- Lines: 95-97
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0282: `reference-semantics/semantics/controls.k:98`

- Kind: rule
- Lines: 98-100
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0283: `reference-semantics/semantics/controls.k:101`

- Kind: rule
- Lines: 101-103
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0284: `reference-semantics/semantics/controls.k:106`

- Kind: rule
- Lines: 106-108
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0285: `reference-semantics/semantics/core.k:13`

- Kind: syntax
- Lines: 13-13
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### K-0286: `reference-semantics/semantics/core.k:14`

- Kind: syntax
- Lines: 14-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### K-0287: `reference-semantics/semantics/core.k:15`

- Kind: syntax
- Lines: 15-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Str    ::= str(IntSeq)
```

### K-0288: `reference-semantics/semantics/core.k:18`

- Kind: syntax
- Lines: 18-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### K-0289: `reference-semantics/semantics/core.k:25`

- Kind: syntax
- Lines: 25-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

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

### K-0290: `reference-semantics/semantics/core.k:36`

- Kind: syntax
- Lines: 36-36
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Parent   ::= "root" | parent(Int)
```

### K-0291: `reference-semantics/semantics/core.k:37`

- Kind: syntax
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Scope    ::= scope(Map, Parent)
```

### K-0292: `reference-semantics/semantics/core.k:38`

- Kind: syntax
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KResult  ::= Val
```

### K-0293: `reference-semantics/semantics/core.k:39`

- Kind: syntax
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### K-0294: `reference-semantics/semantics/core.k:40`

- Kind: syntax
- Lines: 40-40
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Vals     ::= List{Val, ","}
```

### K-0295: `reference-semantics/semantics/core.k:41`

- Kind: syntax
- Lines: 41-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### K-0296: `reference-semantics/semantics/core.k:42`

- Kind: syntax
- Lines: 42-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### K-0297: `reference-semantics/semantics/core.k:49`

- Kind: configuration
- Lines: 49-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

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

### K-0298: `reference-semantics/semantics/core.k:68`

- Kind: syntax
- Lines: 68-68
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### K-0299: `reference-semantics/semantics/core.k:69`

- Kind: rule
- Lines: 69-69
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isRefV(ref(_:Int)) => true
```

### K-0300: `reference-semantics/semantics/core.k:70`

- Kind: rule
- Lines: 70-70
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isRefV(_:Val)      => false [owise]
```

### K-0301: `reference-semantics/semantics/core.k:75`

- Kind: syntax
- Lines: 75-75
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax HeapVal ::= cellV(Val)
```

### K-0302: `reference-semantics/semantics/core.k:76`

- Kind: syntax
- Lines: 76-76
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### K-0303: `reference-semantics/semantics/core.k:77`

- Kind: rule
- Lines: 77-77
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### K-0304: `reference-semantics/semantics/core.k:78`

- Kind: rule
- Lines: 78-78
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isCellRef(_:Val)          => false [owise]
```

### K-0305: `reference-semantics/semantics/core.k:85`

- Kind: rule
- Lines: 85-90
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

### K-0306: `reference-semantics/semantics/core.k:95`

- Kind: syntax
- Lines: 95-95
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= kwV(String, Val)
```

### K-0307: `reference-semantics/semantics/core.k:96`

- Kind: syntax
- Lines: 96-96
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #kwTag(String)
```

### K-0308: `reference-semantics/semantics/core.k:97`

- Kind: rule
- Lines: 97-97
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### K-0309: `reference-semantics/semantics/core.k:98`

- Kind: rule
- Lines: 98-99
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### K-0310: `reference-semantics/semantics/core.k:100`

- Kind: syntax
- Lines: 100-100
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### K-0311: `reference-semantics/semantics/core.k:101`

- Kind: rule
- Lines: 101-101
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### K-0312: `reference-semantics/semantics/core.k:102`

- Kind: rule
- Lines: 102-102
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isKwV(_:Val)                => false [owise]
```

### K-0313: `reference-semantics/semantics/core.k:106`

- Kind: syntax
- Lines: 106-106
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= cellsMark(ParamNames)
```

### K-0314: `reference-semantics/semantics/core.k:107`

- Kind: syntax
- Lines: 107-107
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### K-0315: `reference-semantics/semantics/core.k:108`

- Kind: rule
- Lines: 108-108
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### K-0316: `reference-semantics/semantics/core.k:109`

- Kind: syntax
- Lines: 109-109
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### K-0317: `reference-semantics/semantics/core.k:110`

- Kind: rule
- Lines: 110-110
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule pnMember(_:String, .ParamNames) => false
```

### K-0318: `reference-semantics/semantics/core.k:111`

- Kind: rule
- Lines: 111-111
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### K-0319: `reference-semantics/semantics/core.k:113`

- Kind: syntax
- Lines: 113-113
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #cellW(Val, Val)
```

### K-0320: `reference-semantics/semantics/core.k:114`

- Kind: rule
- Lines: 114-115
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### K-0321: `reference-semantics/semantics/core.k:117`

- Kind: syntax
- Lines: 117-117
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #alloc(Val)
```

### K-0322: `reference-semantics/semantics/core.k:118`

- Kind: rule
- Lines: 118-121
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K-0323: `reference-semantics/semantics/core.k:124`

- Kind: syntax
- Lines: 124-124
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #loadAll(Module)
```

### K-0324: `reference-semantics/semantics/core.k:125`

- Kind: rule
- Lines: 125-125
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### K-0325: `reference-semantics/semantics/core.k:126`

- Kind: rule
- Lines: 126-126
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### K-0326: `reference-semantics/semantics/core.k:127`

- Kind: rule
- Lines: 127-127
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> .Stmts => .K ... </k>
```

### K-0327: `reference-semantics/semantics/core.k:130`

- Kind: syntax
- Lines: 130-130
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #look(String, Int)
```

### K-0328: `reference-semantics/semantics/core.k:131`

- Kind: rule
- Lines: 131-131
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### K-0329: `reference-semantics/semantics/core.k:132`

- Kind: rule
- Lines: 132-134
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

### K-0330: `reference-semantics/semantics/core.k:145`

- Kind: rule
- Lines: 145-151
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### K-0331: `reference-semantics/semantics/core.k:152`

- Kind: rule
- Lines: 152-154
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

### K-0332: `reference-semantics/semantics/core.k:157`

- Kind: syntax
- Lines: 157-157
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### K-0333: `reference-semantics/semantics/core.k:158`

- Kind: rule
- Lines: 158-181
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

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

### K-0334: `reference-semantics/semantics/core.k:185`

- Kind: syntax
- Lines: 185-185
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ApplyK ::= toCall(Val)
```

### K-0335: `reference-semantics/semantics/core.k:186`

- Kind: syntax
- Lines: 186-188
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### K-0336: `reference-semantics/semantics/core.k:189`

- Kind: rule
- Lines: 189-189
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### K-0337: `reference-semantics/semantics/core.k:190`

- Kind: rule
- Lines: 190-190
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### K-0338: `reference-semantics/semantics/core.k:191`

- Kind: rule
- Lines: 191-191
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### K-0339: `reference-semantics/semantics/core.k:194`

- Kind: rule
- Lines: 194-194
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### K-0340: `reference-semantics/semantics/core.k:195`

- Kind: rule
- Lines: 195-195
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### K-0341: `reference-semantics/semantics/core.k:196`

- Kind: rule
- Lines: 196-196
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> NoneVal      => noneV ... </k>
```

### K-0342: `reference-semantics/semantics/core.k:199`

- Kind: syntax
- Lines: 199-199
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= truthy(Val) [function]
```

### K-0343: `reference-semantics/semantics/core.k:200`

- Kind: rule
- Lines: 200-200
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule truthy(B:Bool)          => B
```

### K-0344: `reference-semantics/semantics/core.k:201`

- Kind: rule
- Lines: 201-201
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule truthy(noneV)           => false
```

### K-0345: `reference-semantics/semantics/core.k:202`

- Kind: rule
- Lines: 202-202
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### K-0346: `reference-semantics/semantics/core.k:203`

- Kind: rule
- Lines: 203-203
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### K-0347: `reference-semantics/semantics/core.k:204`

- Kind: rule
- Lines: 204-204
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### K-0348: `reference-semantics/semantics/core.k:205`

- Kind: rule
- Lines: 205-205
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### K-0349: `reference-semantics/semantics/core.k:208`

- Kind: syntax
- Lines: 208-208
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### K-0350: `reference-semantics/semantics/core.k:209`

- Kind: syntax
- Lines: 209-209
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### K-0351: `reference-semantics/semantics/core.k:210`

- Kind: syntax
- Lines: 210-210
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### K-0352: `reference-semantics/semantics/core.k:213`

- Kind: syntax
- Lines: 213-213
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### K-0353: `reference-semantics/semantics/core.k:214`

- Kind: rule
- Lines: 214-214
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### K-0354: `reference-semantics/semantics/core.k:215`

- Kind: rule
- Lines: 215-215
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### K-0355: `reference-semantics/semantics/core.k:217`

- Kind: syntax
- Lines: 217-217
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### K-0356: `reference-semantics/semantics/core.k:218`

- Kind: rule
- Lines: 218-218
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### K-0357: `reference-semantics/semantics/core.k:219`

- Kind: rule
- Lines: 219-219
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### K-0358: `reference-semantics/semantics/core.k:223`

- Kind: syntax
- Lines: 223-223
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### K-0359: `reference-semantics/semantics/core.k:224`

- Kind: rule
- Lines: 224-224
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule vsLen(.ValSeq)                => 0
```

### K-0360: `reference-semantics/semantics/core.k:225`

- Kind: rule
- Lines: 225-225
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### K-0361: `reference-semantics/semantics/core.k:227`

- Kind: syntax
- Lines: 227-227
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### K-0362: `reference-semantics/semantics/core.k:228`

- Kind: rule
- Lines: 228-228
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isLen(.IntSeq)                => 0
```

### K-0363: `reference-semantics/semantics/core.k:229`

- Kind: rule
- Lines: 229-229
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### K-0364: `reference-semantics/semantics/core.k:233`

- Kind: syntax
- Lines: 233-233
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### K-0365: `reference-semantics/semantics/core.k:234`

- Kind: rule
- Lines: 234-234
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### K-0366: `reference-semantics/semantics/core.k:235`

- Kind: rule
- Lines: 235-235
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### K-0367: `reference-semantics/semantics/core.k:236`

- Kind: rule
- Lines: 236-237
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### K-0368: `reference-semantics/semantics/core.k:238`

- Kind: rule
- Lines: 238-239
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### K-0369: `reference-semantics/semantics/dict.k:20`

- Kind: syntax
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### K-0370: `reference-semantics/semantics/dict.k:23`

- Kind: syntax
- Lines: 23-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### K-0371: `reference-semantics/semantics/dict.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### K-0372: `reference-semantics/semantics/dict.k:27`

- Kind: rule
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### K-0373: `reference-semantics/semantics/dict.k:28`

- Kind: rule
- Lines: 28-29
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### K-0374: `reference-semantics/semantics/dict.k:30`

- Kind: rule
- Lines: 30-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### K-0375: `reference-semantics/semantics/dict.k:32`

- Kind: rule
- Lines: 32-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### K-0376: `reference-semantics/semantics/dict.k:37`

- Kind: syntax
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### K-0377: `reference-semantics/semantics/dict.k:38`

- Kind: rule
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### K-0378: `reference-semantics/semantics/dict.k:39`

- Kind: rule
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### K-0379: `reference-semantics/semantics/dict.k:40`

- Kind: rule
- Lines: 40-40
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### K-0380: `reference-semantics/semantics/dict.k:43`

- Kind: syntax
- Lines: 43-43
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### K-0381: `reference-semantics/semantics/dict.k:44`

- Kind: rule
- Lines: 44-44
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### K-0382: `reference-semantics/semantics/dict.k:45`

- Kind: rule
- Lines: 45-45
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### K-0383: `reference-semantics/semantics/dict.k:49`

- Kind: syntax
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### K-0384: `reference-semantics/semantics/dict.k:50`

- Kind: rule
- Lines: 50-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### K-0385: `reference-semantics/semantics/dict.k:52`

- Kind: rule
- Lines: 52-53
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### K-0386: `reference-semantics/semantics/dict.k:54`

- Kind: rule
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### K-0387: `reference-semantics/semantics/dict.k:58`

- Kind: rule
- Lines: 58-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### K-0388: `reference-semantics/semantics/dict.k:63`

- Kind: rule
- Lines: 63-63
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### K-0389: `reference-semantics/semantics/dict.k:64`

- Kind: syntax
- Lines: 64-64
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### K-0390: `reference-semantics/semantics/dict.k:65`

- Kind: rule
- Lines: 65-66
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### K-0391: `reference-semantics/semantics/dict.k:70`

- Kind: syntax
- Lines: 70-70
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### K-0392: `reference-semantics/semantics/dict.k:71`

- Kind: rule
- Lines: 71-71
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### K-0393: `reference-semantics/semantics/dict.k:76`

- Kind: syntax
- Lines: 76-76
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #dsetK(String, Val)
```

### K-0394: `reference-semantics/semantics/dict.k:77`

- Kind: rule
- Lines: 77-77
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### K-0395: `reference-semantics/semantics/dict.k:78`

- Kind: rule
- Lines: 78-81
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### K-0396: `reference-semantics/semantics/dict.k:82`

- Kind: rule
- Lines: 82-85
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### K-0397: `reference-semantics/semantics/dict.k:86`

- Kind: syntax
- Lines: 86-86
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### K-0398: `reference-semantics/semantics/dict.k:87`

- Kind: rule
- Lines: 87-88
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### K-0399: `reference-semantics/semantics/dict.k:90`

- Kind: syntax
- Lines: 90-90
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### K-0400: `reference-semantics/semantics/dict.k:91`

- Kind: rule
- Lines: 91-91
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K-0401: `reference-semantics/semantics/dict.k:92`

- Kind: rule
- Lines: 92-92
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### K-0402: `reference-semantics/semantics/dict.k:95`

- Kind: rule
- Lines: 95-96
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### K-0403: `reference-semantics/semantics/dict.k:97`

- Kind: syntax
- Lines: 97-97
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### K-0404: `reference-semantics/semantics/dict.k:98`

- Kind: rule
- Lines: 98-98
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### K-0405: `reference-semantics/semantics/dict.k:99`

- Kind: rule
- Lines: 99-100
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### K-0406: `reference-semantics/semantics/dict.k:101`

- Kind: syntax
- Lines: 101-101
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### K-0407: `reference-semantics/semantics/dict.k:102`

- Kind: rule
- Lines: 102-102
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### K-0408: `reference-semantics/semantics/dict.k:103`

- Kind: rule
- Lines: 103-103
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### K-0409: `reference-semantics/semantics/float.k:20`

- Kind: syntax
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= Float
```

### K-0410: `reference-semantics/semantics/float.k:21`

- Kind: rule
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Float(F:Float) => F ... </k>
```

### K-0411: `reference-semantics/semantics/float.k:24`

- Kind: syntax
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### K-0412: `reference-semantics/semantics/float.k:25`

- Kind: rule
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### K-0413: `reference-semantics/semantics/float.k:27`

- Kind: rule
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### K-0414: `reference-semantics/semantics/float.k:30`

- Kind: syntax
- Lines: 30-30
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### K-0415: `reference-semantics/semantics/float.k:31`

- Kind: rule
- Lines: 31-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### K-0416: `reference-semantics/semantics/float.k:32`

- Kind: rule
- Lines: 32-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### K-0417: `reference-semantics/semantics/float.k:37`

- Kind: syntax
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### K-0418: `reference-semantics/semantics/float.k:38`

- Kind: rule
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### K-0419: `reference-semantics/semantics/float.k:39`

- Kind: rule
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### K-0420: `reference-semantics/semantics/float.k:43`

- Kind: rule
- Lines: 43-43
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### K-0421: `reference-semantics/semantics/float.k:44`

- Kind: rule
- Lines: 44-44
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### K-0422: `reference-semantics/semantics/float.k:50`

- Kind: syntax
- Lines: 50-50
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### K-0423: `reference-semantics/semantics/float.k:51`

- Kind: rule
- Lines: 51-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### K-0424: `reference-semantics/semantics/float.k:52`

- Kind: rule
- Lines: 52-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### K-0425: `reference-semantics/semantics/float.k:54`

- Kind: syntax
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### K-0426: `reference-semantics/semantics/float.k:55`

- Kind: rule
- Lines: 55-55
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### K-0427: `reference-semantics/semantics/float.k:56`

- Kind: rule
- Lines: 56-56
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### K-0428: `reference-semantics/semantics/float.k:61`

- Kind: rule
- Lines: 61-61
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Import(_:String) => .K ... </k>
```

### K-0429: `reference-semantics/semantics/float.k:65`

- Kind: syntax
- Lines: 65-65
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= "#mathCeil"
```

### K-0430: `reference-semantics/semantics/float.k:66`

- Kind: rule
- Lines: 66-66
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### K-0431: `reference-semantics/semantics/float.k:67`

- Kind: rule
- Lines: 67-67
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### K-0432: `reference-semantics/semantics/float.k:70`

- Kind: syntax
- Lines: 70-70
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= "#mathFloor"
```

### K-0433: `reference-semantics/semantics/float.k:71`

- Kind: rule
- Lines: 71-71
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### K-0434: `reference-semantics/semantics/float.k:72`

- Kind: rule
- Lines: 72-72
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### K-0435: `reference-semantics/semantics/float.k:73`

- Kind: syntax
- Lines: 73-73
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### K-0436: `reference-semantics/semantics/float.k:74`

- Kind: rule
- Lines: 74-74
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### K-0437: `reference-semantics/semantics/float.k:75`

- Kind: rule
- Lines: 75-75
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### K-0438: `reference-semantics/semantics/float.k:78`

- Kind: rule
- Lines: 78-78
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### K-0439: `reference-semantics/semantics/float.k:79`

- Kind: rule
- Lines: 79-79
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### K-0440: `reference-semantics/semantics/float.k:82`

- Kind: syntax
- Lines: 82-82
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### K-0441: `reference-semantics/semantics/float.k:83`

- Kind: rule
- Lines: 83-83
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### K-0442: `reference-semantics/semantics/float.k:84`

- Kind: rule
- Lines: 84-84
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### K-0443: `reference-semantics/semantics/float.k:85`

- Kind: rule
- Lines: 85-85
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### K-0444: `reference-semantics/semantics/float.k:86`

- Kind: syntax
- Lines: 86-86
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### K-0445: `reference-semantics/semantics/float.k:87`

- Kind: rule
- Lines: 87-87
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule toF(F:Float) => F        [concrete]
```

### K-0446: `reference-semantics/semantics/float.k:88`

- Kind: rule
- Lines: 88-88
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### K-0447: `reference-semantics/semantics/float.k:93`

- Kind: syntax
- Lines: 93-93
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### K-0448: `reference-semantics/semantics/float.k:94`

- Kind: rule
- Lines: 94-94
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### K-0449: `reference-semantics/semantics/float.k:95`

- Kind: rule
- Lines: 95-95
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### K-0450: `reference-semantics/semantics/float.k:99`

- Kind: rule
- Lines: 99-99
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### K-0451: `reference-semantics/semantics/float.k:103`

- Kind: syntax
- Lines: 103-103
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### K-0452: `reference-semantics/semantics/float.k:104`

- Kind: rule
- Lines: 104-104
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### K-0453: `reference-semantics/semantics/float.k:105`

- Kind: rule
- Lines: 105-105
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### K-0454: `reference-semantics/semantics/float.k:107`

- Kind: syntax
- Lines: 107-107
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### K-0455: `reference-semantics/semantics/float.k:108`

- Kind: rule
- Lines: 108-108
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### K-0456: `reference-semantics/semantics/float.k:109`

- Kind: rule
- Lines: 109-109
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### K-0457: `reference-semantics/semantics/float.k:111`

- Kind: syntax
- Lines: 111-111
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### K-0458: `reference-semantics/semantics/float.k:112`

- Kind: rule
- Lines: 112-112
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### K-0459: `reference-semantics/semantics/float.k:113`

- Kind: rule
- Lines: 113-113
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### K-0460: `reference-semantics/semantics/float.k:115`

- Kind: syntax
- Lines: 115-115
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### K-0461: `reference-semantics/semantics/float.k:116`

- Kind: rule
- Lines: 116-116
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### K-0462: `reference-semantics/semantics/float.k:117`

- Kind: rule
- Lines: 117-117
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### K-0463: `reference-semantics/semantics/float.k:119`

- Kind: syntax
- Lines: 119-119
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### K-0464: `reference-semantics/semantics/float.k:120`

- Kind: rule
- Lines: 120-120
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### K-0465: `reference-semantics/semantics/float.k:121`

- Kind: rule
- Lines: 121-121
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### K-0466: `reference-semantics/semantics/float.k:125`

- Kind: syntax
- Lines: 125-125
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### K-0467: `reference-semantics/semantics/float.k:126`

- Kind: rule
- Lines: 126-126
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### K-0468: `reference-semantics/semantics/float.k:127`

- Kind: rule
- Lines: 127-127
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### K-0469: `reference-semantics/semantics/float.k:128`

- Kind: rule
- Lines: 128-128
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### K-0470: `reference-semantics/semantics/float.k:129`

- Kind: rule
- Lines: 129-129
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### K-0471: `reference-semantics/semantics/float.k:132`

- Kind: rule
- Lines: 132-132
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### K-0472: `reference-semantics/semantics/float.k:133`

- Kind: rule
- Lines: 133-133
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### K-0473: `reference-semantics/semantics/float.k:134`

- Kind: rule
- Lines: 134-134
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### K-0474: `reference-semantics/semantics/float.k:135`

- Kind: rule
- Lines: 135-135
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### K-0475: `reference-semantics/semantics/float.k:136`

- Kind: rule
- Lines: 136-136
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### K-0476: `reference-semantics/semantics/float.k:137`

- Kind: rule
- Lines: 137-137
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### K-0477: `reference-semantics/semantics/float.k:138`

- Kind: rule
- Lines: 138-138
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### K-0478: `reference-semantics/semantics/float.k:139`

- Kind: rule
- Lines: 139-139
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### K-0479: `reference-semantics/semantics/float.k:142`

- Kind: syntax
- Lines: 142-142
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### K-0480: `reference-semantics/semantics/float.k:143`

- Kind: rule
- Lines: 143-143
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### K-0481: `reference-semantics/semantics/float.k:144`

- Kind: rule
- Lines: 144-144
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### K-0482: `reference-semantics/semantics/float.k:145`

- Kind: rule
- Lines: 145-145
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### K-0483: `reference-semantics/semantics/float.k:146`

- Kind: rule
- Lines: 146-146
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### K-0484: `reference-semantics/semantics/float.k:147`

- Kind: rule
- Lines: 147-147
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### K-0485: `reference-semantics/semantics/float.k:148`

- Kind: rule
- Lines: 148-148
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### K-0486: `reference-semantics/semantics/float.k:149`

- Kind: rule
- Lines: 149-149
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### K-0487: `reference-semantics/semantics/float.k:150`

- Kind: rule
- Lines: 150-150
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### K-0488: `reference-semantics/semantics/float.k:151`

- Kind: rule
- Lines: 151-151
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### K-0489: `reference-semantics/semantics/float.k:154`

- Kind: rule
- Lines: 154-154
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### K-0490: `reference-semantics/semantics/float.k:155`

- Kind: rule
- Lines: 155-155
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### K-0491: `reference-semantics/semantics/float.k:160`

- Kind: syntax
- Lines: 160-160
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### K-0492: `reference-semantics/semantics/float.k:161`

- Kind: rule
- Lines: 161-161
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### K-0493: `reference-semantics/semantics/float.k:162`

- Kind: rule
- Lines: 162-164
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### K-0494: `reference-semantics/semantics/float.k:165`

- Kind: syntax
- Lines: 165-165
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### K-0495: `reference-semantics/semantics/float.k:166`

- Kind: rule
- Lines: 166-166
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### K-0496: `reference-semantics/semantics/float.k:167`

- Kind: syntax
- Lines: 167-167
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### K-0497: `reference-semantics/semantics/float.k:168`

- Kind: rule
- Lines: 168-168
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### K-0498: `reference-semantics/semantics/float.k:169`

- Kind: rule
- Lines: 169-169
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### K-0499: `reference-semantics/semantics/float.k:170`

- Kind: rule
- Lines: 170-170
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### K-0500: `reference-semantics/semantics/float.k:171`

- Kind: rule
- Lines: 171-172
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### K-0501: `reference-semantics/semantics/float.k:173`

- Kind: syntax
- Lines: 173-173
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### K-0502: `reference-semantics/semantics/float.k:174`

- Kind: rule
- Lines: 174-174
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracPart(.IntSeq) => 0
```

### K-0503: `reference-semantics/semantics/float.k:175`

- Kind: rule
- Lines: 175-175
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### K-0504: `reference-semantics/semantics/float.k:176`

- Kind: rule
- Lines: 176-176
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### K-0505: `reference-semantics/semantics/float.k:177`

- Kind: rule
- Lines: 177-177
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### K-0506: `reference-semantics/semantics/float.k:178`

- Kind: rule
- Lines: 178-178
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### K-0507: `reference-semantics/semantics/float.k:179`

- Kind: syntax
- Lines: 179-179
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### K-0508: `reference-semantics/semantics/float.k:180`

- Kind: rule
- Lines: 180-180
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracScale(.IntSeq) => 1
```

### K-0509: `reference-semantics/semantics/float.k:181`

- Kind: rule
- Lines: 181-181
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### K-0510: `reference-semantics/semantics/float.k:182`

- Kind: rule
- Lines: 182-182
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### K-0511: `reference-semantics/semantics/float.k:183`

- Kind: rule
- Lines: 183-183
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### K-0512: `reference-semantics/semantics/float.k:184`

- Kind: rule
- Lines: 184-184
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### K-0513: `reference-semantics/semantics/float.k:185`

- Kind: rule
- Lines: 185-185
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### K-0514: `reference-semantics/semantics/float.k:186`

- Kind: rule
- Lines: 186-186
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### K-0515: `reference-semantics/semantics/float.k:187`

- Kind: rule
- Lines: 187-187
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### K-0516: `reference-semantics/semantics/float.k:190`

- Kind: syntax
- Lines: 190-190
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### K-0517: `reference-semantics/semantics/float.k:191`

- Kind: rule
- Lines: 191-191
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### K-0518: `reference-semantics/semantics/float.k:192`

- Kind: rule
- Lines: 192-192
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### K-0519: `reference-semantics/semantics/float.k:195`

- Kind: syntax
- Lines: 195-195
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### K-0520: `reference-semantics/semantics/float.k:196`

- Kind: rule
- Lines: 196-196
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### K-0521: `reference-semantics/semantics/float.k:197`

- Kind: rule
- Lines: 197-197
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### K-0522: `reference-semantics/semantics/float.k:198`

- Kind: rule
- Lines: 198-198
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### K-0523: `reference-semantics/semantics/float.k:199`

- Kind: rule
- Lines: 199-199
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### K-0524: `reference-semantics/semantics/float.k:200`

- Kind: rule
- Lines: 200-200
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### K-0525: `reference-semantics/semantics/float.k:201`

- Kind: rule
- Lines: 201-201
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### K-0526: `reference-semantics/semantics/float.k:202`

- Kind: rule
- Lines: 202-202
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### K-0527: `reference-semantics/semantics/float.k:203`

- Kind: rule
- Lines: 203-203
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### K-0528: `reference-semantics/semantics/float.k:204`

- Kind: rule
- Lines: 204-204
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### K-0529: `reference-semantics/semantics/float.k:205`

- Kind: rule
- Lines: 205-205
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### K-0530: `reference-semantics/semantics/float.k:206`

- Kind: rule
- Lines: 206-206
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### K-0531: `reference-semantics/semantics/float.k:209`

- Kind: syntax
- Lines: 209-209
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### K-0532: `reference-semantics/semantics/float.k:210`

- Kind: rule
- Lines: 210-210
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### K-0533: `reference-semantics/semantics/float.k:211`

- Kind: rule
- Lines: 211-211
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### K-0534: `reference-semantics/semantics/float.k:213`

- Kind: rule
- Lines: 213-213
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### K-0535: `reference-semantics/semantics/float.k:214`

- Kind: rule
- Lines: 214-214
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### K-0536: `reference-semantics/semantics/float.k:217`

- Kind: syntax
- Lines: 217-217
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### K-0537: `reference-semantics/semantics/float.k:218`

- Kind: rule
- Lines: 218-222
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### K-0538: `reference-semantics/semantics/float.k:223`

- Kind: syntax
- Lines: 223-223
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### K-0539: `reference-semantics/semantics/float.k:224`

- Kind: rule
- Lines: 224-226
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### K-0540: `reference-semantics/semantics/float.k:227`

- Kind: rule
- Lines: 227-227
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### K-0541: `reference-semantics/semantics/float.k:228`

- Kind: rule
- Lines: 228-228
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### K-0542: `reference-semantics/semantics/float.k:230`

- Kind: syntax
- Lines: 230-230
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### K-0543: `reference-semantics/semantics/float.k:231`

- Kind: rule
- Lines: 231-231
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### K-0544: `reference-semantics/semantics/float.k:232`

- Kind: syntax
- Lines: 232-232
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= "#mathSqrt"
```

### K-0545: `reference-semantics/semantics/float.k:233`

- Kind: rule
- Lines: 233-233
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### K-0546: `reference-semantics/semantics/float.k:234`

- Kind: rule
- Lines: 234-234
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### K-0547: `reference-semantics/semantics/float.k:235`

- Kind: rule
- Lines: 235-235
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### K-0548: `reference-semantics/semantics/float.k:243`

- Kind: syntax
- Lines: 243-243
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### K-0549: `reference-semantics/semantics/float.k:244`

- Kind: rule
- Lines: 244-244
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K-0550: `reference-semantics/semantics/float.k:245`

- Kind: rule
- Lines: 245-245
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### K-0551: `reference-semantics/semantics/float.k:246`

- Kind: rule
- Lines: 246-246
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### K-0552: `reference-semantics/semantics/float.k:247`

- Kind: rule
- Lines: 247-248
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0553: `reference-semantics/semantics/float.k:250`

- Kind: syntax
- Lines: 250-250
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### K-0554: `reference-semantics/semantics/float.k:251`

- Kind: rule
- Lines: 251-251
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K-0555: `reference-semantics/semantics/float.k:252`

- Kind: rule
- Lines: 252-252
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### K-0556: `reference-semantics/semantics/float.k:253`

- Kind: rule
- Lines: 253-253
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### K-0557: `reference-semantics/semantics/float.k:254`

- Kind: rule
- Lines: 254-255
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0558: `reference-semantics/semantics/float.k:261`

- Kind: syntax
- Lines: 261-261
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### K-0559: `reference-semantics/semantics/float.k:262`

- Kind: rule
- Lines: 262-264
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### K-0560: `reference-semantics/semantics/float.k:265`

- Kind: rule
- Lines: 265-265
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### K-0561: `reference-semantics/semantics/float.k:266`

- Kind: rule
- Lines: 266-266
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### K-0562: `reference-semantics/semantics/float.k:267`

- Kind: rule
- Lines: 267-269
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0563: `reference-semantics/semantics/float.k:270`

- Kind: rule
- Lines: 270-272
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K-0564: `reference-semantics/semantics/functions.k:8`

- Kind: syntax
- Lines: 8-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### K-0565: `reference-semantics/semantics/functions.k:14`

- Kind: rule
- Lines: 14-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### K-0566: `reference-semantics/semantics/functions.k:18`

- Kind: syntax
- Lines: 18-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### K-0567: `reference-semantics/semantics/functions.k:19`

- Kind: rule
- Lines: 19-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### K-0568: `reference-semantics/semantics/functions.k:27`

- Kind: syntax
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### K-0569: `reference-semantics/semantics/functions.k:31`

- Kind: syntax
- Lines: 31-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### K-0570: `reference-semantics/semantics/functions.k:33`

- Kind: rule
- Lines: 33-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### K-0571: `reference-semantics/semantics/functions.k:36`

- Kind: rule
- Lines: 36-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K-0572: `reference-semantics/semantics/functions.k:42`

- Kind: rule
- Lines: 42-45
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### K-0573: `reference-semantics/semantics/functions.k:47`

- Kind: rule
- Lines: 47-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### K-0574: `reference-semantics/semantics/functions.k:50`

- Kind: rule
- Lines: 50-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### K-0575: `reference-semantics/semantics/functions.k:53`

- Kind: rule
- Lines: 53-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K-0576: `reference-semantics/semantics/functions.k:59`

- Kind: rule
- Lines: 59-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### K-0577: `reference-semantics/semantics/functions.k:63`

- Kind: rule
- Lines: 63-63
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### K-0578: `reference-semantics/semantics/functions.k:64`

- Kind: rule
- Lines: 64-66
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### K-0579: `reference-semantics/semantics/functions.k:68`

- Kind: rule
- Lines: 68-75
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

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

### K-0580: `reference-semantics/semantics/functions.k:78`

- Kind: rule
- Lines: 78-79
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### K-0581: `reference-semantics/semantics/functions.k:80`

- Kind: rule
- Lines: 80-81
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### K-0582: `reference-semantics/semantics/functions.k:85`

- Kind: rule
- Lines: 85-90
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### K-0583: `reference-semantics/semantics/int.k:7`

- Kind: rule
- Lines: 7-7
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### K-0584: `reference-semantics/semantics/int.k:9`

- Kind: rule
- Lines: 9-9
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### K-0585: `reference-semantics/semantics/int.k:11`

- Kind: rule
- Lines: 11-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### K-0586: `reference-semantics/semantics/int.k:12`

- Kind: rule
- Lines: 12-12
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### K-0587: `reference-semantics/semantics/int.k:13`

- Kind: rule
- Lines: 13-13
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### K-0588: `reference-semantics/semantics/int.k:14`

- Kind: rule
- Lines: 14-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### K-0589: `reference-semantics/semantics/int.k:15`

- Kind: rule
- Lines: 15-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### K-0590: `reference-semantics/semantics/int.k:16`

- Kind: rule
- Lines: 16-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### K-0591: `reference-semantics/semantics/int.k:17`

- Kind: rule
- Lines: 17-17
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### K-0592: `reference-semantics/semantics/int.k:19`

- Kind: syntax
- Lines: 19-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### K-0593: `reference-semantics/semantics/int.k:20`

- Kind: rule
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### K-0594: `reference-semantics/semantics/int.k:22`

- Kind: rule
- Lines: 22-22
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### K-0595: `reference-semantics/semantics/int.k:23`

- Kind: rule
- Lines: 23-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### K-0596: `reference-semantics/semantics/int.k:24`

- Kind: rule
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### K-0597: `reference-semantics/semantics/int.k:25`

- Kind: rule
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### K-0598: `reference-semantics/semantics/int.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### K-0599: `reference-semantics/semantics/int.k:27`

- Kind: rule
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### K-0600: `reference-semantics/semantics/iter.k:8`

- Kind: syntax
- Lines: 8-8
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### K-0601: `reference-semantics/semantics/list.k:9`

- Kind: rule
- Lines: 9-9
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### K-0602: `reference-semantics/semantics/list.k:10`

- Kind: rule
- Lines: 10-10
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### K-0603: `reference-semantics/semantics/list.k:13`

- Kind: syntax
- Lines: 13-13
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ApplyK ::= "toList"
```

### K-0604: `reference-semantics/semantics/list.k:14`

- Kind: rule
- Lines: 14-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### K-0605: `reference-semantics/semantics/list.k:15`

- Kind: rule
- Lines: 15-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### K-0606: `reference-semantics/semantics/list.k:18`

- Kind: syntax
- Lines: 18-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### K-0607: `reference-semantics/semantics/list.k:19`

- Kind: rule
- Lines: 19-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### K-0608: `reference-semantics/semantics/list.k:20`

- Kind: rule
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### K-0609: `reference-semantics/semantics/list.k:24`

- Kind: rule
- Lines: 24-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### K-0610: `reference-semantics/semantics/list.k:27`

- Kind: rule
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### K-0611: `reference-semantics/semantics/list.k:28`

- Kind: rule
- Lines: 28-28
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### K-0612: `reference-semantics/semantics/list.k:33`

- Kind: syntax
- Lines: 33-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### K-0613: `reference-semantics/semantics/list.k:34`

- Kind: rule
- Lines: 34-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule hasRefVS(.ValSeq)                => false
```

### K-0614: `reference-semantics/semantics/list.k:35`

- Kind: rule
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### K-0615: `reference-semantics/semantics/list.k:37`

- Kind: syntax
- Lines: 37-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### K-0616: `reference-semantics/semantics/list.k:39`

- Kind: rule
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### K-0617: `reference-semantics/semantics/list.k:40`

- Kind: rule
- Lines: 40-40
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### K-0618: `reference-semantics/semantics/list.k:41`

- Kind: rule
- Lines: 41-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### K-0619: `reference-semantics/semantics/list.k:42`

- Kind: rule
- Lines: 42-43
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### K-0620: `reference-semantics/semantics/list.k:45`

- Kind: rule
- Lines: 45-46
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### K-0621: `reference-semantics/semantics/list.k:47`

- Kind: rule
- Lines: 47-48
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### K-0622: `reference-semantics/semantics/list.k:49`

- Kind: rule
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### K-0623: `reference-semantics/semantics/list.k:50`

- Kind: rule
- Lines: 50-50
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### K-0624: `reference-semantics/semantics/list.k:53`

- Kind: rule
- Lines: 53-55
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### K-0625: `reference-semantics/semantics/list.k:58`

- Kind: syntax
- Lines: 58-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### K-0626: `reference-semantics/semantics/list.k:59`

- Kind: rule
- Lines: 59-59
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### K-0627: `reference-semantics/semantics/list.k:60`

- Kind: rule
- Lines: 60-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### K-0628: `reference-semantics/semantics/list.k:61`

- Kind: rule
- Lines: 61-61
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### K-0629: `reference-semantics/semantics/list.k:62`

- Kind: rule
- Lines: 62-62
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### K-0630: `reference-semantics/semantics/list.k:63`

- Kind: rule
- Lines: 63-64
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### K-0631: `reference-semantics/semantics/list.k:65`

- Kind: rule
- Lines: 65-66
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### K-0632: `reference-semantics/semantics/list.k:67`

- Kind: rule
- Lines: 67-67
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### K-0633: `reference-semantics/semantics/methods.k:10`

- Kind: syntax
- Lines: 10-10
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### K-0634: `reference-semantics/semantics/methods.k:13`

- Kind: rule
- Lines: 13-13
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### K-0635: `reference-semantics/semantics/methods.k:14`

- Kind: rule
- Lines: 14-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### K-0636: `reference-semantics/semantics/methods.k:15`

- Kind: rule
- Lines: 15-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### K-0637: `reference-semantics/semantics/methods.k:16`

- Kind: rule
- Lines: 16-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### K-0638: `reference-semantics/semantics/methods.k:19`

- Kind: rule
- Lines: 19-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### K-0639: `reference-semantics/semantics/methods.k:20`

- Kind: rule
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### K-0640: `reference-semantics/semantics/methods.k:21`

- Kind: rule
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### K-0641: `reference-semantics/semantics/methods.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### K-0642: `reference-semantics/semantics/methods.k:27`

- Kind: syntax
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### K-0643: `reference-semantics/semantics/methods.k:28`

- Kind: rule
- Lines: 28-28
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### K-0644: `reference-semantics/semantics/methods.k:29`

- Kind: rule
- Lines: 29-29
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### K-0645: `reference-semantics/semantics/methods.k:30`

- Kind: rule
- Lines: 30-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### K-0646: `reference-semantics/semantics/methods.k:34`

- Kind: rule
- Lines: 34-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### K-0647: `reference-semantics/semantics/methods.k:35`

- Kind: syntax
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### K-0648: `reference-semantics/semantics/methods.k:36`

- Kind: rule
- Lines: 36-36
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### K-0649: `reference-semantics/semantics/methods.k:37`

- Kind: rule
- Lines: 37-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### K-0650: `reference-semantics/semantics/methods.k:39`

- Kind: rule
- Lines: 39-40
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### K-0651: `reference-semantics/semantics/methods.k:41`

- Kind: syntax
- Lines: 41-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### K-0652: `reference-semantics/semantics/methods.k:42`

- Kind: rule
- Lines: 42-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### K-0653: `reference-semantics/semantics/methods.k:43`

- Kind: rule
- Lines: 43-43
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### K-0654: `reference-semantics/semantics/methods.k:44`

- Kind: rule
- Lines: 44-44
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### K-0655: `reference-semantics/semantics/methods.k:47`

- Kind: rule
- Lines: 47-47
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### K-0656: `reference-semantics/semantics/methods.k:48`

- Kind: syntax
- Lines: 48-48
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### K-0657: `reference-semantics/semantics/methods.k:49`

- Kind: rule
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### K-0658: `reference-semantics/semantics/methods.k:50`

- Kind: rule
- Lines: 50-50
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### K-0659: `reference-semantics/semantics/methods.k:51`

- Kind: rule
- Lines: 51-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### K-0660: `reference-semantics/semantics/methods.k:52`

- Kind: syntax
- Lines: 52-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### K-0661: `reference-semantics/semantics/methods.k:53`

- Kind: rule
- Lines: 53-53
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### K-0662: `reference-semantics/semantics/methods.k:54`

- Kind: rule
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### K-0663: `reference-semantics/semantics/methods.k:55`

- Kind: rule
- Lines: 55-55
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### K-0664: `reference-semantics/semantics/methods.k:58`

- Kind: rule
- Lines: 58-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### K-0665: `reference-semantics/semantics/methods.k:61`

- Kind: rule
- Lines: 61-61
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### K-0666: `reference-semantics/semantics/methods.k:64`

- Kind: rule
- Lines: 64-64
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### K-0667: `reference-semantics/semantics/methods.k:65`

- Kind: syntax
- Lines: 65-65
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### K-0668: `reference-semantics/semantics/methods.k:66`

- Kind: rule
- Lines: 66-66
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### K-0669: `reference-semantics/semantics/methods.k:67`

- Kind: rule
- Lines: 67-67
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### K-0670: `reference-semantics/semantics/methods.k:68`

- Kind: rule
- Lines: 68-68
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### K-0671: `reference-semantics/semantics/methods.k:72`

- Kind: rule
- Lines: 72-74
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### K-0672: `reference-semantics/semantics/methods.k:75`

- Kind: syntax
- Lines: 75-75
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### K-0673: `reference-semantics/semantics/methods.k:76`

- Kind: rule
- Lines: 76-76
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### K-0674: `reference-semantics/semantics/methods.k:77`

- Kind: rule
- Lines: 77-78
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### K-0675: `reference-semantics/semantics/methods.k:79`

- Kind: rule
- Lines: 79-80
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

### K-0676: `reference-semantics/semantics/methods.k:82`

- Kind: syntax
- Lines: 82-82
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### K-0677: `reference-semantics/semantics/methods.k:83`

- Kind: rule
- Lines: 83-83
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### K-0678: `reference-semantics/semantics/methods.k:84`

- Kind: rule
- Lines: 84-84
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### K-0679: `reference-semantics/semantics/methods.k:85`

- Kind: syntax
- Lines: 85-85
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### K-0680: `reference-semantics/semantics/methods.k:86`

- Kind: rule
- Lines: 86-86
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### K-0681: `reference-semantics/semantics/methods.k:89`

- Kind: rule
- Lines: 89-91
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### K-0682: `reference-semantics/semantics/methods.k:94`

- Kind: rule
- Lines: 94-96
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### K-0683: `reference-semantics/semantics/methods.k:97`

- Kind: syntax
- Lines: 97-97
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### K-0684: `reference-semantics/semantics/methods.k:98`

- Kind: rule
- Lines: 98-98
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### K-0685: `reference-semantics/semantics/methods.k:99`

- Kind: rule
- Lines: 99-100
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### K-0686: `reference-semantics/semantics/methods.k:101`

- Kind: rule
- Lines: 101-102
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### K-0687: `reference-semantics/semantics/methods.k:104`

- Kind: rule
- Lines: 104-105
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### K-0688: `reference-semantics/semantics/methods.k:106`

- Kind: syntax
- Lines: 106-106
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### K-0689: `reference-semantics/semantics/methods.k:107`

- Kind: rule
- Lines: 107-107
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### K-0690: `reference-semantics/semantics/methods.k:108`

- Kind: rule
- Lines: 108-108
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### K-0691: `reference-semantics/semantics/methods.k:109`

- Kind: rule
- Lines: 109-109
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### K-0692: `reference-semantics/semantics/methods.k:112`

- Kind: syntax
- Lines: 112-112
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### K-0693: `reference-semantics/semantics/methods.k:113`

- Kind: rule
- Lines: 113-113
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### K-0694: `reference-semantics/semantics/methods.k:115`

- Kind: syntax
- Lines: 115-115
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### K-0695: `reference-semantics/semantics/methods.k:116`

- Kind: rule
- Lines: 116-116
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### K-0696: `reference-semantics/semantics/methods.k:118`

- Kind: syntax
- Lines: 118-118
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### K-0697: `reference-semantics/semantics/methods.k:119`

- Kind: rule
- Lines: 119-119
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### K-0698: `reference-semantics/semantics/methods.k:121`

- Kind: syntax
- Lines: 121-121
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### K-0699: `reference-semantics/semantics/methods.k:122`

- Kind: rule
- Lines: 122-122
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K-0700: `reference-semantics/semantics/methods.k:124`

- Kind: syntax
- Lines: 124-124
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### K-0701: `reference-semantics/semantics/methods.k:125`

- Kind: rule
- Lines: 125-125
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule hasUpper(.IntSeq) => false
```

### K-0702: `reference-semantics/semantics/methods.k:126`

- Kind: rule
- Lines: 126-126
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### K-0703: `reference-semantics/semantics/methods.k:128`

- Kind: syntax
- Lines: 128-128
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### K-0704: `reference-semantics/semantics/methods.k:129`

- Kind: rule
- Lines: 129-129
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule hasLower(.IntSeq) => false
```

### K-0705: `reference-semantics/semantics/methods.k:130`

- Kind: rule
- Lines: 130-130
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### K-0706: `reference-semantics/semantics/methods.k:132`

- Kind: syntax
- Lines: 132-132
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### K-0707: `reference-semantics/semantics/methods.k:133`

- Kind: rule
- Lines: 133-133
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule allAlpha(.IntSeq) => true
```

### K-0708: `reference-semantics/semantics/methods.k:134`

- Kind: rule
- Lines: 134-134
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### K-0709: `reference-semantics/semantics/methods.k:136`

- Kind: syntax
- Lines: 136-136
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### K-0710: `reference-semantics/semantics/methods.k:137`

- Kind: rule
- Lines: 137-137
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule allDigit(.IntSeq) => true
```

### K-0711: `reference-semantics/semantics/methods.k:138`

- Kind: rule
- Lines: 138-138
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### K-0712: `reference-semantics/semantics/methods.k:140`

- Kind: syntax
- Lines: 140-140
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### K-0713: `reference-semantics/semantics/methods.k:142`

- Kind: rule
- Lines: 142-142
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K-0714: `reference-semantics/semantics/methods.k:143`

- Kind: rule
- Lines: 143-143
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule lowerC(C:Int) => C         [owise]
```

### K-0715: `reference-semantics/semantics/methods.k:145`

- Kind: syntax
- Lines: 145-145
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= upperC(Int) [function, total]
```

### K-0716: `reference-semantics/semantics/methods.k:146`

- Kind: rule
- Lines: 146-146
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K-0717: `reference-semantics/semantics/methods.k:147`

- Kind: rule
- Lines: 147-147
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule upperC(C:Int) => C         [owise]
```

### K-0718: `reference-semantics/semantics/methods.k:149`

- Kind: syntax
- Lines: 149-149
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= swapC(Int) [function, total]
```

### K-0719: `reference-semantics/semantics/methods.k:150`

- Kind: rule
- Lines: 150-150
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K-0720: `reference-semantics/semantics/methods.k:151`

- Kind: rule
- Lines: 151-151
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K-0721: `reference-semantics/semantics/methods.k:152`

- Kind: rule
- Lines: 152-152
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule swapC(C:Int) => C         [owise]
```

### K-0722: `reference-semantics/semantics/methods.k:154`

- Kind: syntax
- Lines: 154-154
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### K-0723: `reference-semantics/semantics/methods.k:155`

- Kind: rule
- Lines: 155-155
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### K-0724: `reference-semantics/semantics/methods.k:156`

- Kind: rule
- Lines: 156-156
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### K-0725: `reference-semantics/semantics/methods.k:158`

- Kind: syntax
- Lines: 158-158
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### K-0726: `reference-semantics/semantics/methods.k:159`

- Kind: rule
- Lines: 159-159
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### K-0727: `reference-semantics/semantics/methods.k:160`

- Kind: rule
- Lines: 160-160
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### K-0728: `reference-semantics/semantics/methods.k:162`

- Kind: syntax
- Lines: 162-162
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### K-0729: `reference-semantics/semantics/methods.k:163`

- Kind: rule
- Lines: 163-163
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### K-0730: `reference-semantics/semantics/methods.k:164`

- Kind: rule
- Lines: 164-164
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### K-0731: `reference-semantics/semantics/methods.k:166`

- Kind: syntax
- Lines: 166-166
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### K-0732: `reference-semantics/semantics/methods.k:167`

- Kind: rule
- Lines: 167-167
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### K-0733: `reference-semantics/semantics/methods.k:168`

- Kind: rule
- Lines: 168-168
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0734: `reference-semantics/semantics/methods.k:169`

- Kind: rule
- Lines: 169-169
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### K-0735: `reference-semantics/semantics/operators.k:10`

- Kind: rule
- Lines: 10-10
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### K-0736: `reference-semantics/semantics/operators.k:12`

- Kind: rule
- Lines: 12-12
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### K-0737: `reference-semantics/semantics/operators.k:15`

- Kind: context
- Lines: 15-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  context Compare(HOLE, _)
```

### K-0738: `reference-semantics/semantics/operators.k:16`

- Kind: context
- Lines: 16-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### K-0739: `reference-semantics/semantics/operators.k:17`

- Kind: rule
- Lines: 17-17
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: owise
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### K-0740: `reference-semantics/semantics/operators.k:19`

- Kind: rule
- Lines: 19-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### K-0741: `reference-semantics/semantics/operators.k:20`

- Kind: rule
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### K-0742: `reference-semantics/semantics/operators.k:25`

- Kind: rule
- Lines: 25-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0743: `reference-semantics/semantics/operators.k:28`

- Kind: rule
- Lines: 28-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

### K-0744: `reference-semantics/semantics/operators.k:34`

- Kind: rule
- Lines: 34-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### K-0745: `reference-semantics/semantics/operators.k:38`

- Kind: rule
- Lines: 38-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### K-0746: `reference-semantics/semantics/operators.k:44`

- Kind: rule
- Lines: 44-46
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0747: `reference-semantics/semantics/range.k:9`

- Kind: syntax
- Lines: 9-9
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### K-0748: `reference-semantics/semantics/range.k:10`

- Kind: rule
- Lines: 10-10
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### K-0749: `reference-semantics/semantics/range.k:12`

- Kind: syntax
- Lines: 12-12
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### K-0750: `reference-semantics/semantics/range.k:13`

- Kind: rule
- Lines: 13-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### K-0751: `reference-semantics/semantics/range.k:15`

- Kind: rule
- Lines: 15-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### K-0752: `reference-semantics/semantics/range.k:17`

- Kind: rule
- Lines: 17-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### K-0753: `reference-semantics/semantics/range.k:20`

- Kind: rule
- Lines: 20-22
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### K-0754: `reference-semantics/semantics/range.k:23`

- Kind: rule
- Lines: 23-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### K-0755: `reference-semantics/semantics/set.k:8`

- Kind: syntax
- Lines: 8-8
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= setV(IntSeq)
```

### K-0756: `reference-semantics/semantics/set.k:11`

- Kind: syntax
- Lines: 11-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### K-0757: `reference-semantics/semantics/set.k:12`

- Kind: rule
- Lines: 12-12
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### K-0758: `reference-semantics/semantics/set.k:13`

- Kind: rule
- Lines: 13-13
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### K-0759: `reference-semantics/semantics/set.k:16`

- Kind: syntax
- Lines: 16-17
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### K-0760: `reference-semantics/semantics/set.k:18`

- Kind: rule
- Lines: 18-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### K-0761: `reference-semantics/semantics/set.k:19`

- Kind: rule
- Lines: 19-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### K-0762: `reference-semantics/semantics/set.k:20`

- Kind: rule
- Lines: 20-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### K-0763: `reference-semantics/semantics/set.k:22`

- Kind: rule
- Lines: 22-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### K-0764: `reference-semantics/semantics/set.k:25`

- Kind: syntax
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### K-0765: `reference-semantics/semantics/set.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### K-0766: `reference-semantics/semantics/set.k:27`

- Kind: rule
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### K-0767: `reference-semantics/semantics/set.k:31`

- Kind: syntax
- Lines: 31-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### K-0768: `reference-semantics/semantics/set.k:32`

- Kind: rule
- Lines: 32-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### K-0769: `reference-semantics/semantics/set.k:33`

- Kind: rule
- Lines: 33-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### K-0770: `reference-semantics/semantics/set.k:35`

- Kind: syntax
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### K-0771: `reference-semantics/semantics/set.k:36`

- Kind: rule
- Lines: 36-36
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### K-0772: `reference-semantics/semantics/set.k:39`

- Kind: rule
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### K-0773: `reference-semantics/semantics/sort.k:18`

- Kind: syntax
- Lines: 18-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### K-0774: `reference-semantics/semantics/sort.k:19`

- Kind: syntax
- Lines: 19-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### K-0775: `reference-semantics/semantics/sort.k:20`

- Kind: rule
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### K-0776: `reference-semantics/semantics/sort.k:21`

- Kind: rule
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### K-0777: `reference-semantics/semantics/sort.k:22`

- Kind: rule
- Lines: 22-22
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### K-0778: `reference-semantics/semantics/sort.k:23`

- Kind: rule
- Lines: 23-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### K-0779: `reference-semantics/semantics/sort.k:24`

- Kind: rule
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### K-0780: `reference-semantics/semantics/sort.k:26`

- Kind: syntax
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### K-0781: `reference-semantics/semantics/sort.k:27`

- Kind: rule
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### K-0782: `reference-semantics/semantics/sort.k:28`

- Kind: rule
- Lines: 28-28
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### K-0783: `reference-semantics/semantics/sort.k:29`

- Kind: rule
- Lines: 29-30
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### K-0784: `reference-semantics/semantics/sort.k:31`

- Kind: rule
- Lines: 31-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: concrete
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### K-0785: `reference-semantics/semantics/sort.k:36`

- Kind: rule
- Lines: 36-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### K-0786: `reference-semantics/semantics/sort.k:40`

- Kind: rule
- Lines: 40-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### K-0787: `reference-semantics/semantics/sort.k:49`

- Kind: syntax
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total, symbol, no-evaluators
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### K-0788: `reference-semantics/semantics/sort.k:51`

- Kind: syntax
- Lines: 51-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### K-0789: `reference-semantics/semantics/sort.k:53`

- Kind: rule
- Lines: 53-53
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### K-0790: `reference-semantics/semantics/sort.k:54`

- Kind: rule
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### K-0791: `reference-semantics/semantics/sort.k:55`

- Kind: rule
- Lines: 55-55
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### K-0792: `reference-semantics/semantics/sort.k:57`

- Kind: syntax
- Lines: 57-57
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### K-0793: `reference-semantics/semantics/sort.k:58`

- Kind: rule
- Lines: 58-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule condRev(S:ValSeq, false) => S
```

### K-0794: `reference-semantics/semantics/sort.k:59`

- Kind: rule
- Lines: 59-59
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### K-0795: `reference-semantics/semantics/sort.k:61`

- Kind: rule
- Lines: 61-62
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### K-0796: `reference-semantics/semantics/sort.k:63`

- Kind: rule
- Lines: 63-64
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### K-0797: `reference-semantics/semantics/sort.k:65`

- Kind: rule
- Lines: 65-66
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

### K-0798: `reference-semantics/semantics/str.k:8`

- Kind: rule
- Lines: 8-8
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### K-0799: `reference-semantics/semantics/str.k:9`

- Kind: rule
- Lines: 9-10
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### K-0800: `reference-semantics/semantics/str.k:13`

- Kind: syntax
- Lines: 13-13
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### K-0801: `reference-semantics/semantics/str.k:14`

- Kind: rule
- Lines: 14-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### K-0802: `reference-semantics/semantics/str.k:15`

- Kind: rule
- Lines: 15-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strToCodes("") => .IntSeq
```

### K-0803: `reference-semantics/semantics/str.k:16`

- Kind: rule
- Lines: 16-17
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### K-0804: `reference-semantics/semantics/str.k:20`

- Kind: syntax
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### K-0805: `reference-semantics/semantics/str.k:21`

- Kind: rule
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### K-0806: `reference-semantics/semantics/str.k:22`

- Kind: rule
- Lines: 22-22
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### K-0807: `reference-semantics/semantics/str.k:24`

- Kind: rule
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### K-0808: `reference-semantics/semantics/str.k:25`

- Kind: rule
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### K-0809: `reference-semantics/semantics/str.k:26`

- Kind: rule
- Lines: 26-26
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### K-0810: `reference-semantics/semantics/str.k:29`

- Kind: rule
- Lines: 29-29
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### K-0811: `reference-semantics/semantics/str.k:30`

- Kind: rule
- Lines: 30-30
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### K-0812: `reference-semantics/semantics/str.k:32`

- Kind: syntax
- Lines: 32-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### K-0813: `reference-semantics/semantics/str.k:33`

- Kind: rule
- Lines: 33-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### K-0814: `reference-semantics/semantics/str.k:34`

- Kind: rule
- Lines: 34-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0815: `reference-semantics/semantics/str.k:35`

- Kind: rule
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### K-0816: `reference-semantics/semantics/str.k:37`

- Kind: syntax
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### K-0817: `reference-semantics/semantics/str.k:38`

- Kind: rule
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### K-0818: `reference-semantics/semantics/str.k:39`

- Kind: rule
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### K-0819: `reference-semantics/semantics/str.k:40`

- Kind: rule
- Lines: 40-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

### K-0820: `reference-semantics/semantics/str.k:48`

- Kind: syntax
- Lines: 48-48
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### K-0821: `reference-semantics/semantics/str.k:49`

- Kind: rule
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### K-0822: `reference-semantics/semantics/str.k:50`

- Kind: rule
- Lines: 50-50
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### K-0823: `reference-semantics/semantics/str.k:51`

- Kind: rule
- Lines: 51-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0824: `reference-semantics/semantics/str.k:52`

- Kind: rule
- Lines: 52-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### K-0825: `reference-semantics/semantics/str.k:53`

- Kind: rule
- Lines: 53-53
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### K-0826: `reference-semantics/semantics/str.k:54`

- Kind: rule
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### K-0827: `reference-semantics/semantics/str.k:56`

- Kind: rule
- Lines: 56-56
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K-0828: `reference-semantics/semantics/str.k:57`

- Kind: rule
- Lines: 57-57
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### K-0829: `reference-semantics/semantics/str.k:58`

- Kind: rule
- Lines: 58-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### K-0830: `reference-semantics/semantics/str.k:59`

- Kind: rule
- Lines: 59-59
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### K-0831: `reference-semantics/semantics/subscript.k:11`

- Kind: syntax
- Lines: 11-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### K-0832: `reference-semantics/semantics/subscript.k:12`

- Kind: rule
- Lines: 12-12
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### K-0833: `reference-semantics/semantics/subscript.k:13`

- Kind: rule
- Lines: 13-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K-0834: `reference-semantics/semantics/subscript.k:16`

- Kind: syntax
- Lines: 16-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### K-0835: `reference-semantics/semantics/subscript.k:17`

- Kind: rule
- Lines: 17-17
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### K-0836: `reference-semantics/semantics/subscript.k:18`

- Kind: rule
- Lines: 18-19
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K-0837: `reference-semantics/semantics/subscript.k:21`

- Kind: syntax
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### K-0838: `reference-semantics/semantics/subscript.k:22`

- Kind: rule
- Lines: 22-22
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K-0839: `reference-semantics/semantics/subscript.k:23`

- Kind: rule
- Lines: 23-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### K-0840: `reference-semantics/semantics/subscript.k:27`

- Kind: context
- Lines: 27-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  context Subscript(HOLE, _)
```

### K-0841: `reference-semantics/semantics/subscript.k:28`

- Kind: context
- Lines: 28-28
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  context Subscript(_:Val, HOLE:Expr)
```

### K-0842: `reference-semantics/semantics/subscript.k:31`

- Kind: rule
- Lines: 31-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0843: `reference-semantics/semantics/subscript.k:35`

- Kind: rule
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### K-0844: `reference-semantics/semantics/subscript.k:37`

- Kind: syntax
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### K-0845: `reference-semantics/semantics/subscript.k:38`

- Kind: rule
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K-0846: `reference-semantics/semantics/subscript.k:39`

- Kind: rule
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K-0847: `reference-semantics/semantics/subscript.k:40`

- Kind: rule
- Lines: 40-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### K-0848: `reference-semantics/semantics/subscript.k:44`

- Kind: syntax
- Lines: 44-47
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### K-0849: `reference-semantics/semantics/subscript.k:49`

- Kind: syntax
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### K-0850: `reference-semantics/semantics/subscript.k:50`

- Kind: rule
- Lines: 50-50
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### K-0851: `reference-semantics/semantics/subscript.k:51`

- Kind: rule
- Lines: 51-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### K-0852: `reference-semantics/semantics/subscript.k:52`

- Kind: rule
- Lines: 52-52
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### K-0853: `reference-semantics/semantics/subscript.k:54`

- Kind: rule
- Lines: 54-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### K-0854: `reference-semantics/semantics/subscript.k:55`

- Kind: rule
- Lines: 55-55
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### K-0855: `reference-semantics/semantics/subscript.k:56`

- Kind: rule
- Lines: 56-56
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### K-0856: `reference-semantics/semantics/subscript.k:58`

- Kind: rule
- Lines: 58-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### K-0857: `reference-semantics/semantics/subscript.k:61`

- Kind: rule
- Lines: 61-61
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### K-0858: `reference-semantics/semantics/subscript.k:63`

- Kind: syntax
- Lines: 63-63
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### K-0859: `reference-semantics/semantics/subscript.k:64`

- Kind: rule
- Lines: 64-65
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K-0860: `reference-semantics/semantics/subscript.k:66`

- Kind: rule
- Lines: 66-67
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K-0861: `reference-semantics/semantics/subscript.k:68`

- Kind: rule
- Lines: 68-69
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### K-0862: `reference-semantics/semantics/subscript.k:72`

- Kind: syntax
- Lines: 72-72
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### K-0863: `reference-semantics/semantics/subscript.k:73`

- Kind: rule
- Lines: 73-73
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStep(noB)          => 1
```

### K-0864: `reference-semantics/semantics/subscript.k:74`

- Kind: rule
- Lines: 74-74
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStep(someB(S:Int)) => S
```

### K-0865: `reference-semantics/semantics/subscript.k:76`

- Kind: syntax
- Lines: 76-76
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### K-0866: `reference-semantics/semantics/subscript.k:77`

- Kind: rule
- Lines: 77-78
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### K-0867: `reference-semantics/semantics/subscript.k:79`

- Kind: rule
- Lines: 79-80
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### K-0868: `reference-semantics/semantics/subscript.k:81`

- Kind: rule
- Lines: 81-81
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K-0869: `reference-semantics/semantics/subscript.k:83`

- Kind: syntax
- Lines: 83-83
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### K-0870: `reference-semantics/semantics/subscript.k:84`

- Kind: rule
- Lines: 84-85
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### K-0871: `reference-semantics/semantics/subscript.k:86`

- Kind: rule
- Lines: 86-87
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### K-0872: `reference-semantics/semantics/subscript.k:88`

- Kind: rule
- Lines: 88-88
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K-0873: `reference-semantics/semantics/subscript.k:90`

- Kind: syntax
- Lines: 90-90
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### K-0874: `reference-semantics/semantics/subscript.k:91`

- Kind: rule
- Lines: 91-92
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### K-0875: `reference-semantics/semantics/subscript.k:93`

- Kind: rule
- Lines: 93-94
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### K-0876: `reference-semantics/semantics/subscript.k:96`

- Kind: syntax
- Lines: 96-96
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### K-0877: `reference-semantics/semantics/subscript.k:97`

- Kind: rule
- Lines: 97-98
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### K-0878: `reference-semantics/semantics/subscript.k:99`

- Kind: rule
- Lines: 99-100
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### K-0879: `reference-semantics/semantics/subscript.k:102`

- Kind: syntax
- Lines: 102-102
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function, total
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### K-0880: `reference-semantics/semantics/subscript.k:103`

- Kind: rule
- Lines: 103-104
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### K-0881: `reference-semantics/semantics/subscript.k:105`

- Kind: rule
- Lines: 105-106
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

### K-0882: `reference-semantics/semantics/subscript.k:109`

- Kind: syntax
- Lines: 109-109
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### K-0883: `reference-semantics/semantics/subscript.k:110`

- Kind: rule
- Lines: 110-112
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K-0884: `reference-semantics/semantics/subscript.k:113`

- Kind: rule
- Lines: 113-114
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K-0885: `reference-semantics/semantics/subscript.k:116`

- Kind: syntax
- Lines: 116-116
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### K-0886: `reference-semantics/semantics/subscript.k:117`

- Kind: rule
- Lines: 117-119
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K-0887: `reference-semantics/semantics/subscript.k:120`

- Kind: rule
- Lines: 120-121
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K-0888: `reference-semantics/semantics/syntax.k:9`

- Kind: syntax
- Lines: 9-30
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: macro
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

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

### K-0889: `reference-semantics/semantics/syntax.k:32`

- Kind: syntax
- Lines: 32-32
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### K-0890: `reference-semantics/semantics/syntax.k:33`

- Kind: syntax
- Lines: 33-33
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### K-0891: `reference-semantics/semantics/syntax.k:34`

- Kind: syntax
- Lines: 34-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Entries  ::= List{Entry, ","}
```

### K-0892: `reference-semantics/semantics/syntax.k:35`

- Kind: syntax
- Lines: 35-35
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### K-0893: `reference-semantics/semantics/syntax.k:36`

- Kind: syntax
- Lines: 36-36
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax CompFors ::= List{CompFor, ""}
```

### K-0894: `reference-semantics/semantics/syntax.k:37`

- Kind: syntax
- Lines: 37-37
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Exprs    ::= List{Expr, ","}
```

### K-0895: `reference-semantics/semantics/syntax.k:38`

- Kind: syntax
- Lines: 38-38
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### K-0896: `reference-semantics/semantics/syntax.k:39`

- Kind: syntax
- Lines: 39-39
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Bound    ::= Expr | "NoBound"
```

### K-0897: `reference-semantics/semantics/syntax.k:41`

- Kind: syntax
- Lines: 41-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

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

### K-0898: `reference-semantics/semantics/syntax.k:56`

- Kind: syntax
- Lines: 56-56
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### K-0899: `reference-semantics/semantics/syntax.k:57`

- Kind: syntax
- Lines: 57-57
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### K-0900: `reference-semantics/semantics/syntax.k:58`

- Kind: syntax
- Lines: 58-58
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### K-0901: `reference-semantics/semantics/syntax.k:59`

- Kind: syntax
- Lines: 59-59
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### K-0902: `reference-semantics/semantics/syntax.k:60`

- Kind: syntax
- Lines: 60-60
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ParamNames ::= List{String, ","}
```

### K-0903: `reference-semantics/semantics/syntax.k:61`

- Kind: syntax
- Lines: 61-61
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### K-0904: `reference-semantics/semantics/tuple.k:10`

- Kind: rule
- Lines: 10-10
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### K-0905: `reference-semantics/semantics/tuple.k:11`

- Kind: rule
- Lines: 11-11
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### K-0906: `reference-semantics/semantics/tuple.k:14`

- Kind: syntax
- Lines: 14-14
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax ApplyK ::= "toTuple"
```

### K-0907: `reference-semantics/semantics/tuple.k:15`

- Kind: rule
- Lines: 15-15
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### K-0908: `reference-semantics/semantics/tuple.k:16`

- Kind: rule
- Lines: 16-16
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### K-0909: `reference-semantics/semantics/tuple.k:18`

- Kind: rule
- Lines: 18-18
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### K-0910: `reference-semantics/semantics/tuple.k:20`

- Kind: rule
- Lines: 20-20
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### K-0911: `reference-semantics/semantics/tuple.k:21`

- Kind: rule
- Lines: 21-21
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### K-0912: `reference-semantics/semantics/tuple.k:23`

- Kind: rule
- Lines: 23-23
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### K-0913: `reference-semantics/semantics/tuple.k:24`

- Kind: syntax
- Lines: 24-24
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: function
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### K-0914: `reference-semantics/semantics/tuple.k:25`

- Kind: rule
- Lines: 25-25
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### K-0915: `reference-semantics/semantics/tuple.k:26`

- Kind: rule
- Lines: 26-27
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### K-0916: `reference-semantics/semantics/tuple.k:28`

- Kind: rule
- Lines: 28-28
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### K-0917: `reference-semantics/semantics/tuple.k:31`

- Kind: syntax
- Lines: 31-31
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### K-0918: `reference-semantics/semantics/tuple.k:32`

- Kind: rule
- Lines: 32-34
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K-0919: `reference-semantics/semantics/tuple.k:35`

- Kind: rule
- Lines: 35-41
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K-0920: `reference-semantics/semantics/tuple.k:42`

- Kind: rule
- Lines: 42-42
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K-0921: `reference-semantics/semantics/tuple.k:43`

- Kind: rule
- Lines: 43-43
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K-0922: `reference-semantics/semantics/tuple.k:44`

- Kind: rule
- Lines: 44-46
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0923: `reference-semantics/semantics/tuple.k:49`

- Kind: syntax
- Lines: 49-49
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### K-0924: `reference-semantics/semantics/tuple.k:50`

- Kind: rule
- Lines: 50-50
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K-0925: `reference-semantics/semantics/tuple.k:51`

- Kind: rule
- Lines: 51-51
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K-0926: `reference-semantics/semantics/tuple.k:52`

- Kind: rule
- Lines: 52-54
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: priority
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0927: `reference-semantics/semantics/tuple.k:55`

- Kind: rule
- Lines: 55-56
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### K-0928: `reference-semantics/semantics/tuple.k:57`

- Kind: rule
- Lines: 57-57
- Origin: selected supplied semantics; byte-identical trusted baseline
- Tags: none
- Disposition: FIXED_BASELINE: accepted as the selected operational language definition in SUPPLIED_SEMANTICS mode; any opaque or partial boundary is accounted for separately if reachable.

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### K-0929: `verification.k:7`

- Kind: syntax
- Lines: 7-7
- Origin: candidate proof-local
- Tags: macro
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  syntax Stmts ::= "isSortedLoopBody" [macro]
```

### K-0930: `verification.k:8`

- Kind: syntax
- Lines: 8-8
- Origin: candidate proof-local
- Tags: macro
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  syntax Stmts ::= "isSortedFunctionBody" [macro]
```

### K-0931: `verification.k:10`

- Kind: syntax
- Lines: 10-13
- Origin: candidate proof-local
- Tags: function, total
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  syntax Bool ::= nonNegativeInts(ValSeq) [function, total]
                | scanCounts(ValSeq, Bool, ValSeq) [function, total]
                | nextCountResult(Bool, Int) [function, total]
                | intendedSorted(ValSeq) [function, total]
```

### K-0932: `verification.k:14`

- Kind: syntax
- Lines: 14-19
- Origin: candidate proof-local
- Tags: function, total
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  syntax Val ::= countArgument(Val, ValSeq) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX
```

### K-0933: `verification.k:21`

- Kind: rule
- Lines: 21-27
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule isSortedLoopBody
    => If(Compare(
            Call(Attribute(Name("lst"), "count"), Name("current")),
            CmpOp(">", Int(2))),
          Assign(Name("result"), Bool(false)) .Stmts,
          .Stmts)
       .Stmts
```

### K-0934: `verification.k:29`

- Kind: rule
- Lines: 29-36
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule isSortedFunctionBody
    => Assign(Name("result"),
              Compare(Name("lst"),
                      CmpOp("==", Call(Name("sorted"), Name("lst")))))
       Assign(Name("current"), Int(0))
       For(Name("current"), Name("lst"), isSortedLoopBody)
       Return(Name("result"))
       .Stmts
```

### K-0935: `verification.k:38`

- Kind: rule
- Lines: 38-38
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule nonNegativeInts(.ValSeq) => true
```

### K-0936: `verification.k:39`

- Kind: rule
- Lines: 39-40
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule nonNegativeInts(vCons(I:Int, REST:ValSeq))
    => I >=Int 0 andBool nonNegativeInts(REST)
```

### K-0937: `verification.k:41`

- Kind: rule
- Lines: 41-42
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule nonNegativeInts(vCons(V:Val, _REST:ValSeq)) => false
    requires notBool isInt(V)
```

### K-0938: `verification.k:44`

- Kind: rule
- Lines: 44-46
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule nextCountResult(_RESULT:Bool, COUNT:Int)
    => false
    requires COUNT >Int 2
```

### K-0939: `verification.k:47`

- Kind: rule
- Lines: 47-49
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule nextCountResult(RESULT:Bool, COUNT:Int)
    => RESULT
    requires COUNT <=Int 2
```

### K-0940: `verification.k:51`

- Kind: rule
- Lines: 51-51
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule countArgument(ref(0), INPUT:ValSeq) => list(sortVS(INPUT))
```

### K-0941: `verification.k:52`

- Kind: rule
- Lines: 52-52
- Origin: candidate proof-local
- Tags: owise
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule countArgument(VALUE:Val, _INPUT:ValSeq) => VALUE [owise]
```

### K-0942: `verification.k:54`

- Kind: rule
- Lines: 54-55
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule scanCounts(_INPUT:ValSeq, RESULT:Bool, .ValSeq)
    => RESULT
```

### K-0943: `verification.k:56`

- Kind: rule
- Lines: 56-62
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule scanCounts(INPUT:ValSeq, RESULT:Bool,
                  vCons(CURRENT:Val, REST:ValSeq))
    => scanCounts(
         INPUT,
         nextCountResult(
           RESULT, cntOccVS(INPUT, countArgument(CURRENT, INPUT))),
         REST)
```

### K-0944: `verification.k:64`

- Kind: rule
- Lines: 64-65
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  rule intendedSorted(VALUES:ValSeq)
    => scanCounts(VALUES, VALUES ==K sortVS(VALUES), VALUES)
```

### K-0945: `spec.k:6`

- Kind: claim
- Lines: 6-40
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  claim [loop-invariant]:
    <k>
      #loop(list(REST:ValSeq), Name("current"), isSortedLoopBody)
      ~> Return(Name("result")) .Stmts
      ~> #endcall
      ~> .K
      =>
      scanCounts(INPUT, RESULT, REST)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "is_sorted" |-> closureVal("lst", isSortedFunctionBody, 0),
          parent(-1))
        1 |-> scope(
          "current"    |-> _CURRENT
          "lst"        |-> list(INPUT)
          "result"     |-> RESULT,
          parent(0))
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "is_sorted" |-> closureVal("lst", isSortedFunctionBody, 0),
          parent(-1))
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> 0 |-> list(sortVS(INPUT)) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
```

### K-0946: `spec.k:41`

- Kind: claim
- Lines: 41-69
- Origin: candidate proof-local
- Tags: none
- Disposition: PROOF_LOCAL: see the hand-audited per-item review.

```k
  claim [is-sorted]:
    <k>
      #loadAll(Module(
        FuncDef("is_sorted", Params("lst"), isSortedFunctionBody)
        .Stmts))
      ~> Call(Name("is_sorted"), list(INPUT:ValSeq), .Exprs)
      =>
      intendedSorted(INPUT)
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1))
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "is_sorted" |-> closureVal("lst", isSortedFunctionBody, 0),
          parent(-1))
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(sortVS(INPUT)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires nonNegativeInts(INPUT)
```


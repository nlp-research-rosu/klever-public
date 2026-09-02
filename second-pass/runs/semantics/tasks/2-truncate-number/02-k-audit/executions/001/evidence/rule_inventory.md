# Exhaustive K rule and declaration inventory

Generated independently from the trusted supplied semantics and the submitted proof/spec sources. `Entry slice` marks constructs that can participate in the single submitted claim; all other rules were checked for sort/guard/priority separation from that slice.

Total inventoried statements: **931**

| Source | Syntax | Rules | Configurations | Contexts | Claims |
|---|---:|---:|---:|---:|---:|
| `semantics.k` | 0 | 0 | 0 | 0 | 0 |
| `semantics/assert.k` | 0 | 3 | 0 | 0 | 0 |
| `semantics/bool.k` | 0 | 13 | 0 | 1 | 0 |
| `semantics/builtins.k` | 38 | 137 | 0 | 0 | 0 |
| `semantics/call.k` | 3 | 21 | 0 | 0 | 0 |
| `semantics/comprehension.k` | 3 | 7 | 0 | 0 | 0 |
| `semantics/concrete.k` | 5 | 16 | 0 | 0 | 0 |
| `semantics/controls.k` | 3 | 34 | 0 | 0 | 0 |
| `semantics/core.k` | 37 | 46 | 1 | 0 | 0 |
| `semantics/dict.k` | 12 | 28 | 0 | 0 | 0 |
| `semantics/float.k` | 34 | 121 | 0 | 0 | 0 |
| `semantics/functions.k` | 4 | 15 | 0 | 0 | 0 |
| `semantics/int.k` | 1 | 16 | 0 | 0 | 0 |
| `semantics/iter.k` | 1 | 0 | 0 | 0 | 0 |
| `semantics/list.k` | 5 | 27 | 0 | 0 | 0 |
| `semantics/methods.k` | 27 | 75 | 0 | 0 | 0 |
| `semantics/operators.k` | 0 | 10 | 0 | 2 | 0 |
| `semantics/range.k` | 2 | 6 | 0 | 0 | 0 |
| `semantics/set.k` | 6 | 12 | 0 | 0 | 0 |
| `semantics/sort.k` | 6 | 19 | 0 | 0 | 0 |
| `semantics/str.k` | 5 | 28 | 0 | 0 | 0 |
| `semantics/subscript.k` | 15 | 40 | 0 | 2 | 0 |
| `semantics/syntax.k` | 16 | 0 | 0 | 0 | 0 |
| `semantics/tuple.k` | 4 | 21 | 0 | 0 | 0 |
| `verification.k` | 1 | 1 | 0 | 0 | 0 |
| `spec.k` | 0 | 0 | 0 | 0 | 1 |

## Statement-by-statement inventory

### K-0001 — `semantics/assert.k:6`

- Lines: 6–7
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### K-0002 — `semantics/assert.k:8`

- Lines: 8–11
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### K-0003 — `semantics/assert.k:13`

- Lines: 13–15
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0004 — `semantics/bool.k:8`

- Lines: 8–8
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### K-0005 — `semantics/bool.k:10`

- Lines: 10–10
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### K-0006 — `semantics/bool.k:11`

- Lines: 11–11
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### K-0007 — `semantics/bool.k:16`

- Lines: 16–16
- Classification: evaluation context
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### K-0008 — `semantics/bool.k:17`

- Lines: 17–17
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### K-0009 — `semantics/bool.k:18`

- Lines: 18–19
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### K-0010 — `semantics/bool.k:20`

- Lines: 20–21
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### K-0011 — `semantics/bool.k:22`

- Lines: 22–23
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### K-0012 — `semantics/bool.k:24`

- Lines: 24–25
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

### K-0013 — `semantics/bool.k:29`

- Lines: 29–30
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### K-0014 — `semantics/bool.k:31`

- Lines: 31–34
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K-0015 — `semantics/bool.k:35`

- Lines: 35–38
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K-0016 — `semantics/bool.k:39`

- Lines: 39–42
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K-0017 — `semantics/bool.k:43`

- Lines: 43–46
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K-0018 — `semantics/builtins.k:17`

- Lines: 17–17
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### K-0019 — `semantics/builtins.k:20`

- Lines: 20–20
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= seqLen(Val) [function]
```

### K-0020 — `semantics/builtins.k:21`

- Lines: 21–21
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### K-0021 — `semantics/builtins.k:22`

- Lines: 22–22
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### K-0022 — `semantics/builtins.k:23`

- Lines: 23–23
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### K-0023 — `semantics/builtins.k:24`

- Lines: 24–24
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### K-0024 — `semantics/builtins.k:25`

- Lines: 25–25
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### K-0025 — `semantics/builtins.k:26`

- Lines: 26–26
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### K-0026 — `semantics/builtins.k:32`

- Lines: 32–32
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### K-0027 — `semantics/builtins.k:33`

- Lines: 33–33
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### K-0028 — `semantics/builtins.k:34`

- Lines: 34–34
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### K-0029 — `semantics/builtins.k:35`

- Lines: 35–35
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### K-0030 — `semantics/builtins.k:36`

- Lines: 36–36
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### K-0031 — `semantics/builtins.k:37`

- Lines: 37–37
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### K-0032 — `semantics/builtins.k:38`

- Lines: 38–38
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### K-0033 — `semantics/builtins.k:41`

- Lines: 41–41
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### K-0034 — `semantics/builtins.k:44`

- Lines: 44–44
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### K-0035 — `semantics/builtins.k:47`

- Lines: 47–47
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### K-0036 — `semantics/builtins.k:48`

- Lines: 48–48
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### K-0037 — `semantics/builtins.k:49`

- Lines: 49–49
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### K-0038 — `semantics/builtins.k:50`

- Lines: 50–52
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K-0039 — `semantics/builtins.k:54`

- Lines: 54–54
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= intOf(Val) [function]
```

### K-0040 — `semantics/builtins.k:55`

- Lines: 55–55
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intOf(I:Int)  => I
```

### K-0041 — `semantics/builtins.k:56`

- Lines: 56–56
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### K-0042 — `semantics/builtins.k:59`

- Lines: 59–59
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### K-0043 — `semantics/builtins.k:60`

- Lines: 60–60
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### K-0044 — `semantics/builtins.k:61`

- Lines: 61–61
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### K-0045 — `semantics/builtins.k:62`

- Lines: 62–63
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### K-0046 — `semantics/builtins.k:64`

- Lines: 64–65
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### K-0047 — `semantics/builtins.k:67`

- Lines: 67–67
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### K-0048 — `semantics/builtins.k:68`

- Lines: 68–68
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### K-0049 — `semantics/builtins.k:69`

- Lines: 69–69
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### K-0050 — `semantics/builtins.k:70`

- Lines: 70–71
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### K-0051 — `semantics/builtins.k:72`

- Lines: 72–73
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

### K-0052 — `semantics/builtins.k:76`

- Lines: 76–76
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### K-0053 — `semantics/builtins.k:77`

- Lines: 77–77
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### K-0054 — `semantics/builtins.k:78`

- Lines: 78–79
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K-0055 — `semantics/builtins.k:80`

- Lines: 80–80
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### K-0056 — `semantics/builtins.k:81`

- Lines: 81–81
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### K-0057 — `semantics/builtins.k:82`

- Lines: 82–84
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K-0058 — `semantics/builtins.k:86`

- Lines: 86–86
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### K-0059 — `semantics/builtins.k:87`

- Lines: 87–87
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### K-0060 — `semantics/builtins.k:88`

- Lines: 88–89
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K-0061 — `semantics/builtins.k:90`

- Lines: 90–90
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### K-0062 — `semantics/builtins.k:91`

- Lines: 91–91
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### K-0063 — `semantics/builtins.k:92`

- Lines: 92–94
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K-0064 — `semantics/builtins.k:97`

- Lines: 97–97
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### K-0065 — `semantics/builtins.k:98`

- Lines: 98–98
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### K-0066 — `semantics/builtins.k:99`

- Lines: 99–99
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule maxVals(M:Int, .Vals)           => M
```

### K-0067 — `semantics/builtins.k:100`

- Lines: 100–100
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### K-0068 — `semantics/builtins.k:102`

- Lines: 102–102
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### K-0069 — `semantics/builtins.k:103`

- Lines: 103–103
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### K-0070 — `semantics/builtins.k:104`

- Lines: 104–104
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule minVals(M:Int, .Vals)           => M
```

### K-0071 — `semantics/builtins.k:105`

- Lines: 105–105
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### K-0072 — `semantics/builtins.k:108`

- Lines: 108–109
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

### K-0073 — `semantics/builtins.k:111`

- Lines: 111–113
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### K-0074 — `semantics/builtins.k:114`

- Lines: 114–114
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### K-0075 — `semantics/builtins.k:115`

- Lines: 115–115
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### K-0076 — `semantics/builtins.k:116`

- Lines: 116–116
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### K-0077 — `semantics/builtins.k:117`

- Lines: 117–117
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### K-0078 — `semantics/builtins.k:118`

- Lines: 118–118
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### K-0079 — `semantics/builtins.k:119`

- Lines: 119–121
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

### K-0080 — `semantics/builtins.k:124`

- Lines: 124–125
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### K-0081 — `semantics/builtins.k:126`

- Lines: 126–126
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### K-0082 — `semantics/builtins.k:127`

- Lines: 127–127
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### K-0083 — `semantics/builtins.k:128`

- Lines: 128–129
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### K-0084 — `semantics/builtins.k:132`

- Lines: 132–133
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### K-0085 — `semantics/builtins.k:134`

- Lines: 134–134
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### K-0086 — `semantics/builtins.k:135`

- Lines: 135–135
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### K-0087 — `semantics/builtins.k:136`

- Lines: 136–136
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### K-0088 — `semantics/builtins.k:137`

- Lines: 137–137
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### K-0089 — `semantics/builtins.k:140`

- Lines: 140–140
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### K-0090 — `semantics/builtins.k:143`

- Lines: 143–143
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### K-0091 — `semantics/builtins.k:144`

- Lines: 144–145
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

### K-0092 — `semantics/builtins.k:148`

- Lines: 148–148
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### K-0093 — `semantics/builtins.k:149`

- Lines: 149–149
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### K-0094 — `semantics/builtins.k:152`

- Lines: 152–153
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

### K-0095 — `semantics/builtins.k:156`

- Lines: 156–157
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### K-0096 — `semantics/builtins.k:158`

- Lines: 158–158
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### K-0097 — `semantics/builtins.k:159`

- Lines: 159–159
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### K-0098 — `semantics/builtins.k:160`

- Lines: 160–160
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### K-0099 — `semantics/builtins.k:163`

- Lines: 163–163
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### K-0100 — `semantics/builtins.k:164`

- Lines: 164–164
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### K-0101 — `semantics/builtins.k:167`

- Lines: 167–168
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### K-0102 — `semantics/builtins.k:169`

- Lines: 169–169
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### K-0103 — `semantics/builtins.k:170`

- Lines: 170–170
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### K-0104 — `semantics/builtins.k:171`

- Lines: 171–172
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### K-0105 — `semantics/builtins.k:173`

- Lines: 173–173
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### K-0106 — `semantics/builtins.k:174`

- Lines: 174–174
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### K-0107 — `semantics/builtins.k:177`

- Lines: 177–177
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### K-0108 — `semantics/builtins.k:178`

- Lines: 178–178
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### K-0109 — `semantics/builtins.k:179`

- Lines: 179–180
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

### K-0110 — `semantics/builtins.k:187`

- Lines: 187–187
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### K-0111 — `semantics/builtins.k:188`

- Lines: 188–188
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### K-0112 — `semantics/builtins.k:189`

- Lines: 189–190
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### K-0113 — `semantics/builtins.k:192`

- Lines: 192–192
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### K-0114 — `semantics/builtins.k:194`

- Lines: 194–194
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### K-0115 — `semantics/builtins.k:195`

- Lines: 195–195
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K-0116 — `semantics/builtins.k:196`

- Lines: 196–196
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### K-0117 — `semantics/builtins.k:197`

- Lines: 197–197
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### K-0118 — `semantics/builtins.k:198`

- Lines: 198–198
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### K-0119 — `semantics/builtins.k:199`

- Lines: 199–199
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### K-0120 — `semantics/builtins.k:200`

- Lines: 200–200
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### K-0121 — `semantics/builtins.k:201`

- Lines: 201–201
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### K-0122 — `semantics/builtins.k:203`

- Lines: 203–203
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### K-0123 — `semantics/builtins.k:204`

- Lines: 204–204
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### K-0124 — `semantics/builtins.k:205`

- Lines: 205–205
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### K-0125 — `semantics/builtins.k:206`

- Lines: 206–206
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### K-0126 — `semantics/builtins.k:207`

- Lines: 207–207
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### K-0127 — `semantics/builtins.k:208`

- Lines: 208–208
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### K-0128 — `semantics/builtins.k:209`

- Lines: 209–209
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### K-0129 — `semantics/builtins.k:210`

- Lines: 210–210
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### K-0130 — `semantics/builtins.k:211`

- Lines: 211–211
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### K-0131 — `semantics/builtins.k:212`

- Lines: 212–212
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### K-0132 — `semantics/builtins.k:214`

- Lines: 214–215
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### K-0133 — `semantics/builtins.k:216`

- Lines: 216–216
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### K-0134 — `semantics/builtins.k:217`

- Lines: 217–217
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### K-0135 — `semantics/builtins.k:218`

- Lines: 218–218
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### K-0136 — `semantics/builtins.k:219`

- Lines: 219–220
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### K-0137 — `semantics/builtins.k:221`

- Lines: 221–222
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### K-0138 — `semantics/builtins.k:223`

- Lines: 223–223
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### K-0139 — `semantics/builtins.k:225`

- Lines: 225–225
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### K-0140 — `semantics/builtins.k:226`

- Lines: 226–226
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### K-0141 — `semantics/builtins.k:227`

- Lines: 227–227
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### K-0142 — `semantics/builtins.k:228`

- Lines: 228–228
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### K-0143 — `semantics/builtins.k:230`

- Lines: 230–230
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### K-0144 — `semantics/builtins.k:231`

- Lines: 231–231
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### K-0145 — `semantics/builtins.k:232`

- Lines: 232–232
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### K-0146 — `semantics/builtins.k:233`

- Lines: 233–233
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### K-0147 — `semantics/builtins.k:234`

- Lines: 234–234
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### K-0148 — `semantics/builtins.k:235`

- Lines: 235–235
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### K-0149 — `semantics/builtins.k:236`

- Lines: 236–236
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### K-0150 — `semantics/builtins.k:238`

- Lines: 238–238
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### K-0151 — `semantics/builtins.k:239`

- Lines: 239–239
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### K-0152 — `semantics/builtins.k:240`

- Lines: 240–240
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### K-0153 — `semantics/builtins.k:241`

- Lines: 241–242
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### K-0154 — `semantics/builtins.k:243`

- Lines: 243–243
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### K-0155 — `semantics/builtins.k:244`

- Lines: 244–244
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### K-0156 — `semantics/builtins.k:245`

- Lines: 245–245
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### K-0157 — `semantics/builtins.k:246`

- Lines: 246–246
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### K-0158 — `semantics/builtins.k:247`

- Lines: 247–247
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### K-0159 — `semantics/builtins.k:248`

- Lines: 248–248
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### K-0160 — `semantics/builtins.k:250`

- Lines: 250–250
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### K-0161 — `semantics/builtins.k:251`

- Lines: 251–251
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K-0162 — `semantics/builtins.k:252`

- Lines: 252–252
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K-0163 — `semantics/builtins.k:253`

- Lines: 253–253
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K-0164 — `semantics/builtins.k:254`

- Lines: 254–254
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K-0165 — `semantics/builtins.k:255`

- Lines: 255–255
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### K-0166 — `semantics/builtins.k:256`

- Lines: 256–256
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### K-0167 — `semantics/builtins.k:257`

- Lines: 257–259
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### K-0168 — `semantics/builtins.k:260`

- Lines: 260–262
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### K-0169 — `semantics/builtins.k:263`

- Lines: 263–264
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### K-0170 — `semantics/builtins.k:265`

- Lines: 265–265
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### K-0171 — `semantics/builtins.k:266`

- Lines: 266–266
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### K-0172 — `semantics/builtins.k:267`

- Lines: 267–267
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### K-0173 — `semantics/builtins.k:268`

- Lines: 268–268
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### K-0174 — `semantics/builtins.k:269`

- Lines: 269–269
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### K-0175 — `semantics/builtins.k:270`

- Lines: 270–270
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### K-0176 — `semantics/builtins.k:271`

- Lines: 271–271
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### K-0177 — `semantics/builtins.k:272`

- Lines: 272–272
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### K-0178 — `semantics/builtins.k:273`

- Lines: 273–273
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### K-0179 — `semantics/builtins.k:274`

- Lines: 274–274
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### K-0180 — `semantics/builtins.k:279`

- Lines: 279–279
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= "#md5"
```

### K-0181 — `semantics/builtins.k:280`

- Lines: 280–281
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### K-0182 — `semantics/builtins.k:282`

- Lines: 282–282
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### K-0183 — `semantics/builtins.k:283`

- Lines: 283–283
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= md5Obj(IntSeq)
```

### K-0184 — `semantics/builtins.k:284`

- Lines: 284–284
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### K-0185 — `semantics/builtins.k:285`

- Lines: 285–285
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### K-0186 — `semantics/builtins.k:291`

- Lines: 291–291
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### K-0187 — `semantics/builtins.k:292`

- Lines: 292–292
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### K-0188 — `semantics/builtins.k:293`

- Lines: 293–293
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### K-0189 — `semantics/builtins.k:294`

- Lines: 294–294
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isIntV(_:Int)         => true
```

### K-0190 — `semantics/builtins.k:295`

- Lines: 295–295
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isIntV(_:Val)         => false [owise]
```

### K-0191 — `semantics/builtins.k:296`

- Lines: 296–296
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isStrV(str(_:IntSeq)) => true
```

### K-0192 — `semantics/builtins.k:297`

- Lines: 297–297
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isStrV(_:Val)         => false [owise]
```

### K-0193 — `semantics/call.k:16`

- Lines: 16–16
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### K-0194 — `semantics/call.k:19`

- Lines: 19–19
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax KItem ::= #callee(Exprs)
```

### K-0195 — `semantics/call.k:20`

- Lines: 20–20
- Classification: ordinary operational semantic rule
- Attributes: owise
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### K-0196 — `semantics/call.k:21`

- Lines: 21–21
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### K-0197 — `semantics/call.k:24`

- Lines: 24–24
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### K-0198 — `semantics/call.k:26`

- Lines: 26–26
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### K-0199 — `semantics/call.k:27`

- Lines: 27–27
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### K-0200 — `semantics/call.k:28`

- Lines: 28–28
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### K-0201 — `semantics/call.k:29`

- Lines: 29–29
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### K-0202 — `semantics/call.k:30`

- Lines: 30–30
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### K-0203 — `semantics/call.k:31`

- Lines: 31–31
- Classification: ordinary operational semantic rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### K-0204 — `semantics/call.k:32`

- Lines: 32–32
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### K-0205 — `semantics/call.k:38`

- Lines: 38–41
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0206 — `semantics/call.k:42`

- Lines: 42–46
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### K-0207 — `semantics/call.k:47`

- Lines: 47–50
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0208 — `semantics/call.k:52`

- Lines: 52–52
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### K-0209 — `semantics/call.k:53`

- Lines: 53–55
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### K-0210 — `semantics/call.k:56`

- Lines: 56–60
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

### K-0211 — `semantics/call.k:63`

- Lines: 63–67
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### K-0212 — `semantics/call.k:69`

- Lines: 69–74
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K-0213 — `semantics/call.k:80`

- Lines: 80–85
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K-0214 — `semantics/call.k:87`

- Lines: 87–87
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### K-0215 — `semantics/call.k:88`

- Lines: 88–88
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### K-0216 — `semantics/call.k:89`

- Lines: 89–94
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K-0217 — `semantics/comprehension.k:11`

- Lines: 11–11
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K-0218 — `semantics/comprehension.k:12`

- Lines: 12–12
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K-0219 — `semantics/comprehension.k:14`

- Lines: 14–14
- Classification: local syntax/function declaration
- Attributes: macro
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### K-0220 — `semantics/comprehension.k:15`

- Lines: 15–16
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### K-0221 — `semantics/comprehension.k:18`

- Lines: 18–18
- Classification: local syntax/function declaration
- Attributes: macro, macro-rec
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### K-0222 — `semantics/comprehension.k:19`

- Lines: 19–20
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### K-0223 — `semantics/comprehension.k:21`

- Lines: 21–22
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### K-0224 — `semantics/comprehension.k:24`

- Lines: 24–24
- Classification: local syntax/function declaration
- Attributes: macro
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### K-0225 — `semantics/comprehension.k:25`

- Lines: 25–25
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### K-0226 — `semantics/comprehension.k:26`

- Lines: 26–26
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### K-0227 — `semantics/concrete.k:13`

- Lines: 13–15
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K-0228 — `semantics/concrete.k:16`

- Lines: 16–18
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K-0229 — `semantics/concrete.k:25`

- Lines: 25–25
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= kvP(Val, Val)
```

### K-0230 — `semantics/concrete.k:26`

- Lines: 26–27
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### K-0231 — `semantics/concrete.k:28`

- Lines: 28–30
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### K-0232 — `semantics/concrete.k:31`

- Lines: 31–33
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### K-0233 — `semantics/concrete.k:34`

- Lines: 34–35
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### K-0234 — `semantics/concrete.k:36`

- Lines: 36–37
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### K-0235 — `semantics/concrete.k:38`

- Lines: 38–40
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### K-0236 — `semantics/concrete.k:42`

- Lines: 42–42
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### K-0237 — `semantics/concrete.k:43`

- Lines: 43–43
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### K-0238 — `semantics/concrete.k:44`

- Lines: 44–46
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### K-0239 — `semantics/concrete.k:47`

- Lines: 47–49
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### K-0240 — `semantics/concrete.k:51`

- Lines: 51–51
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### K-0241 — `semantics/concrete.k:52`

- Lines: 52–52
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### K-0242 — `semantics/concrete.k:53`

- Lines: 53–53
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### K-0243 — `semantics/concrete.k:54`

- Lines: 54–54
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K-0244 — `semantics/concrete.k:56`

- Lines: 56–56
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### K-0245 — `semantics/concrete.k:57`

- Lines: 57–57
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### K-0246 — `semantics/concrete.k:58`

- Lines: 58–58
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### K-0247 — `semantics/concrete.k:59`

- Lines: 59–59
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### K-0248 — `semantics/controls.k:9`

- Lines: 9–11
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K-0249 — `semantics/controls.k:12`

- Lines: 12–18
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K-0250 — `semantics/controls.k:20`

- Lines: 20–23
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

### K-0251 — `semantics/controls.k:27`

- Lines: 27–31
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

### K-0252 — `semantics/controls.k:35`

- Lines: 35–35
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### K-0253 — `semantics/controls.k:36`

- Lines: 36–36
- Classification: ordinary operational semantic rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### K-0254 — `semantics/controls.k:37`

- Lines: 37–37
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### K-0255 — `semantics/controls.k:38`

- Lines: 38–38
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### K-0256 — `semantics/controls.k:39`

- Lines: 39–42
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### K-0257 — `semantics/controls.k:43`

- Lines: 43–44
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### K-0258 — `semantics/controls.k:48`

- Lines: 48–48
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### K-0259 — `semantics/controls.k:51`

- Lines: 51–51
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### K-0260 — `semantics/controls.k:52`

- Lines: 52–52
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### K-0261 — `semantics/controls.k:53`

- Lines: 53–53
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### K-0262 — `semantics/controls.k:54`

- Lines: 54–54
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### K-0263 — `semantics/controls.k:57`

- Lines: 57–58
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### K-0264 — `semantics/controls.k:59`

- Lines: 59–60
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

### K-0265 — `semantics/controls.k:65`

- Lines: 65–67
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### K-0266 — `semantics/controls.k:69`

- Lines: 69–69
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### K-0267 — `semantics/controls.k:71`

- Lines: 71–71
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### K-0268 — `semantics/controls.k:72`

- Lines: 72–72
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### K-0269 — `semantics/controls.k:73`

- Lines: 73–74
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### K-0270 — `semantics/controls.k:77`

- Lines: 77–77
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### K-0271 — `semantics/controls.k:78`

- Lines: 78–78
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### K-0272 — `semantics/controls.k:79`

- Lines: 79–80
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### K-0273 — `semantics/controls.k:81`

- Lines: 81–82
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

### K-0274 — `semantics/controls.k:85`

- Lines: 85–85
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K-0275 — `semantics/controls.k:86`

- Lines: 86–86
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Continue => #cont ... </k>
```

### K-0276 — `semantics/controls.k:87`

- Lines: 87–87
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Break => #brk ... </k>
```

### K-0277 — `semantics/controls.k:88`

- Lines: 88–88
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K-0278 — `semantics/controls.k:89`

- Lines: 89–89
- Classification: ordinary operational semantic rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### K-0279 — `semantics/controls.k:90`

- Lines: 90–90
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### K-0280 — `semantics/controls.k:91`

- Lines: 91–91
- Classification: ordinary operational semantic rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### K-0281 — `semantics/controls.k:95`

- Lines: 95–97
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0282 — `semantics/controls.k:98`

- Lines: 98–100
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0283 — `semantics/controls.k:101`

- Lines: 101–103
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0284 — `semantics/controls.k:106`

- Lines: 106–108
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0285 — `semantics/core.k:13`

- Lines: 13–13
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### K-0286 — `semantics/core.k:14`

- Lines: 14–14
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### K-0287 — `semantics/core.k:15`

- Lines: 15–15
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Str    ::= str(IntSeq)
```

### K-0288 — `semantics/core.k:18`

- Lines: 18–23
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### K-0289 — `semantics/core.k:25`

- Lines: 25–34
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

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

### K-0290 — `semantics/core.k:36`

- Lines: 36–36
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Parent   ::= "root" | parent(Int)
```

### K-0291 — `semantics/core.k:37`

- Lines: 37–37
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Scope    ::= scope(Map, Parent)
```

### K-0292 — `semantics/core.k:38`

- Lines: 38–38
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax KResult  ::= Val
```

### K-0293 — `semantics/core.k:39`

- Lines: 39–39
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### K-0294 — `semantics/core.k:40`

- Lines: 40–40
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Vals     ::= List{Val, ","}
```

### K-0295 — `semantics/core.k:41`

- Lines: 41–41
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### K-0296 — `semantics/core.k:42`

- Lines: 42–42
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### K-0297 — `semantics/core.k:49`

- Lines: 49–60
- Classification: configuration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

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

### K-0298 — `semantics/core.k:68`

- Lines: 68–68
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### K-0299 — `semantics/core.k:69`

- Lines: 69–69
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isRefV(ref(_:Int)) => true
```

### K-0300 — `semantics/core.k:70`

- Lines: 70–70
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isRefV(_:Val)      => false [owise]
```

### K-0301 — `semantics/core.k:75`

- Lines: 75–75
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax HeapVal ::= cellV(Val)
```

### K-0302 — `semantics/core.k:76`

- Lines: 76–76
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### K-0303 — `semantics/core.k:77`

- Lines: 77–77
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### K-0304 — `semantics/core.k:78`

- Lines: 78–78
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isCellRef(_:Val)          => false [owise]
```

### K-0305 — `semantics/core.k:85`

- Lines: 85–90
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

### K-0306 — `semantics/core.k:95`

- Lines: 95–95
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= kwV(String, Val)
```

### K-0307 — `semantics/core.k:96`

- Lines: 96–96
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #kwTag(String)
```

### K-0308 — `semantics/core.k:97`

- Lines: 97–97
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### K-0309 — `semantics/core.k:98`

- Lines: 98–99
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### K-0310 — `semantics/core.k:100`

- Lines: 100–100
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### K-0311 — `semantics/core.k:101`

- Lines: 101–101
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### K-0312 — `semantics/core.k:102`

- Lines: 102–102
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isKwV(_:Val)                => false [owise]
```

### K-0313 — `semantics/core.k:106`

- Lines: 106–106
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= cellsMark(ParamNames)
```

### K-0314 — `semantics/core.k:107`

- Lines: 107–107
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### K-0315 — `semantics/core.k:108`

- Lines: 108–108
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### K-0316 — `semantics/core.k:109`

- Lines: 109–109
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### K-0317 — `semantics/core.k:110`

- Lines: 110–110
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule pnMember(_:String, .ParamNames) => false
```

### K-0318 — `semantics/core.k:111`

- Lines: 111–111
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### K-0319 — `semantics/core.k:113`

- Lines: 113–113
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #cellW(Val, Val)
```

### K-0320 — `semantics/core.k:114`

- Lines: 114–115
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### K-0321 — `semantics/core.k:117`

- Lines: 117–117
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #alloc(Val)
```

### K-0322 — `semantics/core.k:118`

- Lines: 118–121
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K-0323 — `semantics/core.k:124`

- Lines: 124–124
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax KItem ::= #loadAll(Module)
```

### K-0324 — `semantics/core.k:125`

- Lines: 125–125
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### K-0325 — `semantics/core.k:126`

- Lines: 126–126
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### K-0326 — `semantics/core.k:127`

- Lines: 127–127
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> .Stmts => .K ... </k>
```

### K-0327 — `semantics/core.k:130`

- Lines: 130–130
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax KItem ::= #look(String, Int)
```

### K-0328 — `semantics/core.k:131`

- Lines: 131–131
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### K-0329 — `semantics/core.k:132`

- Lines: 132–134
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

### K-0330 — `semantics/core.k:145`

- Lines: 145–151
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### K-0331 — `semantics/core.k:152`

- Lines: 152–154
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

### K-0332 — `semantics/core.k:157`

- Lines: 157–157
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### K-0333 — `semantics/core.k:158`

- Lines: 158–181
- Classification: function/equational rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

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

### K-0334 — `semantics/core.k:185`

- Lines: 185–185
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax ApplyK ::= toCall(Val)
```

### K-0335 — `semantics/core.k:186`

- Lines: 186–188
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### K-0336 — `semantics/core.k:189`

- Lines: 189–189
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### K-0337 — `semantics/core.k:190`

- Lines: 190–190
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### K-0338 — `semantics/core.k:191`

- Lines: 191–191
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### K-0339 — `semantics/core.k:194`

- Lines: 194–194
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### K-0340 — `semantics/core.k:195`

- Lines: 195–195
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### K-0341 — `semantics/core.k:196`

- Lines: 196–196
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> NoneVal      => noneV ... </k>
```

### K-0342 — `semantics/core.k:199`

- Lines: 199–199
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= truthy(Val) [function]
```

### K-0343 — `semantics/core.k:200`

- Lines: 200–200
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule truthy(B:Bool)          => B
```

### K-0344 — `semantics/core.k:201`

- Lines: 201–201
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule truthy(noneV)           => false
```

### K-0345 — `semantics/core.k:202`

- Lines: 202–202
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### K-0346 — `semantics/core.k:203`

- Lines: 203–203
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### K-0347 — `semantics/core.k:204`

- Lines: 204–204
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### K-0348 — `semantics/core.k:205`

- Lines: 205–205
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### K-0349 — `semantics/core.k:208`

- Lines: 208–208
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### K-0350 — `semantics/core.k:209`

- Lines: 209–209
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### K-0351 — `semantics/core.k:210`

- Lines: 210–210
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### K-0352 — `semantics/core.k:213`

- Lines: 213–213
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### K-0353 — `semantics/core.k:214`

- Lines: 214–214
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### K-0354 — `semantics/core.k:215`

- Lines: 215–215
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### K-0355 — `semantics/core.k:217`

- Lines: 217–217
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### K-0356 — `semantics/core.k:218`

- Lines: 218–218
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### K-0357 — `semantics/core.k:219`

- Lines: 219–219
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### K-0358 — `semantics/core.k:223`

- Lines: 223–223
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### K-0359 — `semantics/core.k:224`

- Lines: 224–224
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule vsLen(.ValSeq)                => 0
```

### K-0360 — `semantics/core.k:225`

- Lines: 225–225
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### K-0361 — `semantics/core.k:227`

- Lines: 227–227
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### K-0362 — `semantics/core.k:228`

- Lines: 228–228
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isLen(.IntSeq)                => 0
```

### K-0363 — `semantics/core.k:229`

- Lines: 229–229
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### K-0364 — `semantics/core.k:233`

- Lines: 233–233
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### K-0365 — `semantics/core.k:234`

- Lines: 234–234
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### K-0366 — `semantics/core.k:235`

- Lines: 235–235
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### K-0367 — `semantics/core.k:236`

- Lines: 236–237
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### K-0368 — `semantics/core.k:238`

- Lines: 238–239
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### K-0369 — `semantics/dict.k:20`

- Lines: 20–20
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### K-0370 — `semantics/dict.k:23`

- Lines: 23–25
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### K-0371 — `semantics/dict.k:26`

- Lines: 26–26
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### K-0372 — `semantics/dict.k:27`

- Lines: 27–27
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### K-0373 — `semantics/dict.k:28`

- Lines: 28–29
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### K-0374 — `semantics/dict.k:30`

- Lines: 30–31
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### K-0375 — `semantics/dict.k:32`

- Lines: 32–33
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### K-0376 — `semantics/dict.k:37`

- Lines: 37–37
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### K-0377 — `semantics/dict.k:38`

- Lines: 38–38
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### K-0378 — `semantics/dict.k:39`

- Lines: 39–39
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### K-0379 — `semantics/dict.k:40`

- Lines: 40–40
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### K-0380 — `semantics/dict.k:43`

- Lines: 43–43
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### K-0381 — `semantics/dict.k:44`

- Lines: 44–44
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### K-0382 — `semantics/dict.k:45`

- Lines: 45–45
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### K-0383 — `semantics/dict.k:49`

- Lines: 49–49
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### K-0384 — `semantics/dict.k:50`

- Lines: 50–51
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### K-0385 — `semantics/dict.k:52`

- Lines: 52–53
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### K-0386 — `semantics/dict.k:54`

- Lines: 54–54
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### K-0387 — `semantics/dict.k:58`

- Lines: 58–60
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### K-0388 — `semantics/dict.k:63`

- Lines: 63–63
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### K-0389 — `semantics/dict.k:64`

- Lines: 64–64
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### K-0390 — `semantics/dict.k:65`

- Lines: 65–66
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### K-0391 — `semantics/dict.k:70`

- Lines: 70–70
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### K-0392 — `semantics/dict.k:71`

- Lines: 71–71
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### K-0393 — `semantics/dict.k:76`

- Lines: 76–76
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #dsetK(String, Val)
```

### K-0394 — `semantics/dict.k:77`

- Lines: 77–77
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### K-0395 — `semantics/dict.k:78`

- Lines: 78–81
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### K-0396 — `semantics/dict.k:82`

- Lines: 82–85
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### K-0397 — `semantics/dict.k:86`

- Lines: 86–86
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### K-0398 — `semantics/dict.k:87`

- Lines: 87–88
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### K-0399 — `semantics/dict.k:90`

- Lines: 90–90
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### K-0400 — `semantics/dict.k:91`

- Lines: 91–91
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K-0401 — `semantics/dict.k:92`

- Lines: 92–92
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### K-0402 — `semantics/dict.k:95`

- Lines: 95–96
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### K-0403 — `semantics/dict.k:97`

- Lines: 97–97
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### K-0404 — `semantics/dict.k:98`

- Lines: 98–98
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### K-0405 — `semantics/dict.k:99`

- Lines: 99–100
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### K-0406 — `semantics/dict.k:101`

- Lines: 101–101
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### K-0407 — `semantics/dict.k:102`

- Lines: 102–102
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### K-0408 — `semantics/dict.k:103`

- Lines: 103–103
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### K-0409 — `semantics/float.k:20`

- Lines: 20–20
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Val ::= Float
```

### K-0410 — `semantics/float.k:21`

- Lines: 21–21
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> Float(F:Float) => F ... </k>
```

### K-0411 — `semantics/float.k:24`

- Lines: 24–24
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### K-0412 — `semantics/float.k:25`

- Lines: 25–25
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### K-0413 — `semantics/float.k:27`

- Lines: 27–27
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### K-0414 — `semantics/float.k:30`

- Lines: 30–30
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### K-0415 — `semantics/float.k:31`

- Lines: 31–31
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### K-0416 — `semantics/float.k:32`

- Lines: 32–32
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### K-0417 — `semantics/float.k:37`

- Lines: 37–37
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### K-0418 — `semantics/float.k:38`

- Lines: 38–38
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### K-0419 — `semantics/float.k:39`

- Lines: 39–39
- Classification: function/equational rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### K-0420 — `semantics/float.k:43`

- Lines: 43–43
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### K-0421 — `semantics/float.k:44`

- Lines: 44–44
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### K-0422 — `semantics/float.k:50`

- Lines: 50–50
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### K-0423 — `semantics/float.k:51`

- Lines: 51–51
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### K-0424 — `semantics/float.k:52`

- Lines: 52–52
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### K-0425 — `semantics/float.k:54`

- Lines: 54–54
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### K-0426 — `semantics/float.k:55`

- Lines: 55–55
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### K-0427 — `semantics/float.k:56`

- Lines: 56–56
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### K-0428 — `semantics/float.k:61`

- Lines: 61–61
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Import(_:String) => .K ... </k>
```

### K-0429 — `semantics/float.k:65`

- Lines: 65–65
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= "#mathCeil"
```

### K-0430 — `semantics/float.k:66`

- Lines: 66–66
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### K-0431 — `semantics/float.k:67`

- Lines: 67–67
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### K-0432 — `semantics/float.k:70`

- Lines: 70–70
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= "#mathFloor"
```

### K-0433 — `semantics/float.k:71`

- Lines: 71–71
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### K-0434 — `semantics/float.k:72`

- Lines: 72–72
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### K-0435 — `semantics/float.k:73`

- Lines: 73–73
- Classification: local syntax/function declaration
- Attributes: function, total, symbol
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### K-0436 — `semantics/float.k:74`

- Lines: 74–74
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### K-0437 — `semantics/float.k:75`

- Lines: 75–75
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### K-0438 — `semantics/float.k:78`

- Lines: 78–78
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### K-0439 — `semantics/float.k:79`

- Lines: 79–79
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### K-0440 — `semantics/float.k:82`

- Lines: 82–82
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### K-0441 — `semantics/float.k:83`

- Lines: 83–83
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### K-0442 — `semantics/float.k:84`

- Lines: 84–84
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### K-0443 — `semantics/float.k:85`

- Lines: 85–85
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### K-0444 — `semantics/float.k:86`

- Lines: 86–86
- Classification: local syntax/function declaration
- Attributes: function, total, symbol
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### K-0445 — `semantics/float.k:87`

- Lines: 87–87
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule toF(F:Float) => F        [concrete]
```

### K-0446 — `semantics/float.k:88`

- Lines: 88–88
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### K-0447 — `semantics/float.k:93`

- Lines: 93–93
- Classification: local syntax/function declaration
- Attributes: function, total, symbol
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### K-0448 — `semantics/float.k:94`

- Lines: 94–94
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### K-0449 — `semantics/float.k:95`

- Lines: 95–95
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### K-0450 — `semantics/float.k:99`

- Lines: 99–99
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### K-0451 — `semantics/float.k:103`

- Lines: 103–103
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### K-0452 — `semantics/float.k:104`

- Lines: 104–104
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### K-0453 — `semantics/float.k:105`

- Lines: 105–105
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### K-0454 — `semantics/float.k:107`

- Lines: 107–107
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### K-0455 — `semantics/float.k:108`

- Lines: 108–108
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### K-0456 — `semantics/float.k:109`

- Lines: 109–109
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### K-0457 — `semantics/float.k:111`

- Lines: 111–111
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### K-0458 — `semantics/float.k:112`

- Lines: 112–112
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### K-0459 — `semantics/float.k:113`

- Lines: 113–113
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### K-0460 — `semantics/float.k:115`

- Lines: 115–115
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### K-0461 — `semantics/float.k:116`

- Lines: 116–116
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### K-0462 — `semantics/float.k:117`

- Lines: 117–117
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### K-0463 — `semantics/float.k:119`

- Lines: 119–119
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### K-0464 — `semantics/float.k:120`

- Lines: 120–120
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### K-0465 — `semantics/float.k:121`

- Lines: 121–121
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### K-0466 — `semantics/float.k:125`

- Lines: 125–125
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### K-0467 — `semantics/float.k:126`

- Lines: 126–126
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### K-0468 — `semantics/float.k:127`

- Lines: 127–127
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### K-0469 — `semantics/float.k:128`

- Lines: 128–128
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### K-0470 — `semantics/float.k:129`

- Lines: 129–129
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### K-0471 — `semantics/float.k:132`

- Lines: 132–132
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### K-0472 — `semantics/float.k:133`

- Lines: 133–133
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### K-0473 — `semantics/float.k:134`

- Lines: 134–134
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### K-0474 — `semantics/float.k:135`

- Lines: 135–135
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### K-0475 — `semantics/float.k:136`

- Lines: 136–136
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### K-0476 — `semantics/float.k:137`

- Lines: 137–137
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### K-0477 — `semantics/float.k:138`

- Lines: 138–138
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### K-0478 — `semantics/float.k:139`

- Lines: 139–139
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### K-0479 — `semantics/float.k:142`

- Lines: 142–142
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### K-0480 — `semantics/float.k:143`

- Lines: 143–143
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### K-0481 — `semantics/float.k:144`

- Lines: 144–144
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### K-0482 — `semantics/float.k:145`

- Lines: 145–145
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### K-0483 — `semantics/float.k:146`

- Lines: 146–146
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### K-0484 — `semantics/float.k:147`

- Lines: 147–147
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### K-0485 — `semantics/float.k:148`

- Lines: 148–148
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### K-0486 — `semantics/float.k:149`

- Lines: 149–149
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### K-0487 — `semantics/float.k:150`

- Lines: 150–150
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### K-0488 — `semantics/float.k:151`

- Lines: 151–151
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### K-0489 — `semantics/float.k:154`

- Lines: 154–154
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### K-0490 — `semantics/float.k:155`

- Lines: 155–155
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### K-0491 — `semantics/float.k:160`

- Lines: 160–160
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### K-0492 — `semantics/float.k:161`

- Lines: 161–161
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### K-0493 — `semantics/float.k:162`

- Lines: 162–164
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### K-0494 — `semantics/float.k:165`

- Lines: 165–165
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### K-0495 — `semantics/float.k:166`

- Lines: 166–166
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### K-0496 — `semantics/float.k:167`

- Lines: 167–167
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### K-0497 — `semantics/float.k:168`

- Lines: 168–168
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### K-0498 — `semantics/float.k:169`

- Lines: 169–169
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### K-0499 — `semantics/float.k:170`

- Lines: 170–170
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### K-0500 — `semantics/float.k:171`

- Lines: 171–172
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### K-0501 — `semantics/float.k:173`

- Lines: 173–173
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### K-0502 — `semantics/float.k:174`

- Lines: 174–174
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracPart(.IntSeq) => 0
```

### K-0503 — `semantics/float.k:175`

- Lines: 175–175
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### K-0504 — `semantics/float.k:176`

- Lines: 176–176
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### K-0505 — `semantics/float.k:177`

- Lines: 177–177
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### K-0506 — `semantics/float.k:178`

- Lines: 178–178
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### K-0507 — `semantics/float.k:179`

- Lines: 179–179
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### K-0508 — `semantics/float.k:180`

- Lines: 180–180
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracScale(.IntSeq) => 1
```

### K-0509 — `semantics/float.k:181`

- Lines: 181–181
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### K-0510 — `semantics/float.k:182`

- Lines: 182–182
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### K-0511 — `semantics/float.k:183`

- Lines: 183–183
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### K-0512 — `semantics/float.k:184`

- Lines: 184–184
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### K-0513 — `semantics/float.k:185`

- Lines: 185–185
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### K-0514 — `semantics/float.k:186`

- Lines: 186–186
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### K-0515 — `semantics/float.k:187`

- Lines: 187–187
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### K-0516 — `semantics/float.k:190`

- Lines: 190–190
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### K-0517 — `semantics/float.k:191`

- Lines: 191–191
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### K-0518 — `semantics/float.k:192`

- Lines: 192–192
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### K-0519 — `semantics/float.k:195`

- Lines: 195–195
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### K-0520 — `semantics/float.k:196`

- Lines: 196–196
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### K-0521 — `semantics/float.k:197`

- Lines: 197–197
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### K-0522 — `semantics/float.k:198`

- Lines: 198–198
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### K-0523 — `semantics/float.k:199`

- Lines: 199–199
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### K-0524 — `semantics/float.k:200`

- Lines: 200–200
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### K-0525 — `semantics/float.k:201`

- Lines: 201–201
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### K-0526 — `semantics/float.k:202`

- Lines: 202–202
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### K-0527 — `semantics/float.k:203`

- Lines: 203–203
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### K-0528 — `semantics/float.k:204`

- Lines: 204–204
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### K-0529 — `semantics/float.k:205`

- Lines: 205–205
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### K-0530 — `semantics/float.k:206`

- Lines: 206–206
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### K-0531 — `semantics/float.k:209`

- Lines: 209–209
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### K-0532 — `semantics/float.k:210`

- Lines: 210–210
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### K-0533 — `semantics/float.k:211`

- Lines: 211–211
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### K-0534 — `semantics/float.k:213`

- Lines: 213–213
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### K-0535 — `semantics/float.k:214`

- Lines: 214–214
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### K-0536 — `semantics/float.k:217`

- Lines: 217–217
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### K-0537 — `semantics/float.k:218`

- Lines: 218–222
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### K-0538 — `semantics/float.k:223`

- Lines: 223–223
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### K-0539 — `semantics/float.k:224`

- Lines: 224–226
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### K-0540 — `semantics/float.k:227`

- Lines: 227–227
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### K-0541 — `semantics/float.k:228`

- Lines: 228–228
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### K-0542 — `semantics/float.k:230`

- Lines: 230–230
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### K-0543 — `semantics/float.k:231`

- Lines: 231–231
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### K-0544 — `semantics/float.k:232`

- Lines: 232–232
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= "#mathSqrt"
```

### K-0545 — `semantics/float.k:233`

- Lines: 233–233
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### K-0546 — `semantics/float.k:234`

- Lines: 234–234
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### K-0547 — `semantics/float.k:235`

- Lines: 235–235
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### K-0548 — `semantics/float.k:243`

- Lines: 243–243
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### K-0549 — `semantics/float.k:244`

- Lines: 244–244
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K-0550 — `semantics/float.k:245`

- Lines: 245–245
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### K-0551 — `semantics/float.k:246`

- Lines: 246–246
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### K-0552 — `semantics/float.k:247`

- Lines: 247–248
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0553 — `semantics/float.k:250`

- Lines: 250–250
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### K-0554 — `semantics/float.k:251`

- Lines: 251–251
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K-0555 — `semantics/float.k:252`

- Lines: 252–252
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### K-0556 — `semantics/float.k:253`

- Lines: 253–253
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### K-0557 — `semantics/float.k:254`

- Lines: 254–255
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0558 — `semantics/float.k:261`

- Lines: 261–261
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### K-0559 — `semantics/float.k:262`

- Lines: 262–264
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### K-0560 — `semantics/float.k:265`

- Lines: 265–265
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### K-0561 — `semantics/float.k:266`

- Lines: 266–266
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### K-0562 — `semantics/float.k:267`

- Lines: 267–269
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K-0563 — `semantics/float.k:270`

- Lines: 270–272
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K-0564 — `semantics/functions.k:8`

- Lines: 8–11
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### K-0565 — `semantics/functions.k:14`

- Lines: 14–16
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### K-0566 — `semantics/functions.k:18`

- Lines: 18–18
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### K-0567 — `semantics/functions.k:19`

- Lines: 19–20
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### K-0568 — `semantics/functions.k:27`

- Lines: 27–27
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### K-0569 — `semantics/functions.k:31`

- Lines: 31–32
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### K-0570 — `semantics/functions.k:33`

- Lines: 33–35
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### K-0571 — `semantics/functions.k:36`

- Lines: 36–41
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K-0572 — `semantics/functions.k:42`

- Lines: 42–45
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### K-0573 — `semantics/functions.k:47`

- Lines: 47–49
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### K-0574 — `semantics/functions.k:50`

- Lines: 50–52
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### K-0575 — `semantics/functions.k:53`

- Lines: 53–58
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K-0576 — `semantics/functions.k:59`

- Lines: 59–60
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### K-0577 — `semantics/functions.k:63`

- Lines: 63–63
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### K-0578 — `semantics/functions.k:64`

- Lines: 64–66
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### K-0579 — `semantics/functions.k:68`

- Lines: 68–75
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

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

### K-0580 — `semantics/functions.k:78`

- Lines: 78–79
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### K-0581 — `semantics/functions.k:80`

- Lines: 80–81
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### K-0582 — `semantics/functions.k:85`

- Lines: 85–90
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### K-0583 — `semantics/int.k:7`

- Lines: 7–7
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### K-0584 — `semantics/int.k:9`

- Lines: 9–9
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### K-0585 — `semantics/int.k:11`

- Lines: 11–11
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### K-0586 — `semantics/int.k:12`

- Lines: 12–12
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### K-0587 — `semantics/int.k:13`

- Lines: 13–13
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### K-0588 — `semantics/int.k:14`

- Lines: 14–14
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### K-0589 — `semantics/int.k:15`

- Lines: 15–15
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### K-0590 — `semantics/int.k:16`

- Lines: 16–16
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### K-0591 — `semantics/int.k:17`

- Lines: 17–17
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### K-0592 — `semantics/int.k:19`

- Lines: 19–19
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### K-0593 — `semantics/int.k:20`

- Lines: 20–20
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### K-0594 — `semantics/int.k:22`

- Lines: 22–22
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### K-0595 — `semantics/int.k:23`

- Lines: 23–23
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### K-0596 — `semantics/int.k:24`

- Lines: 24–24
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### K-0597 — `semantics/int.k:25`

- Lines: 25–25
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### K-0598 — `semantics/int.k:26`

- Lines: 26–26
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### K-0599 — `semantics/int.k:27`

- Lines: 27–27
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### K-0600 — `semantics/iter.k:8`

- Lines: 8–8
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### K-0601 — `semantics/list.k:9`

- Lines: 9–9
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### K-0602 — `semantics/list.k:10`

- Lines: 10–10
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### K-0603 — `semantics/list.k:13`

- Lines: 13–13
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ApplyK ::= "toList"
```

### K-0604 — `semantics/list.k:14`

- Lines: 14–14
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### K-0605 — `semantics/list.k:15`

- Lines: 15–15
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### K-0606 — `semantics/list.k:18`

- Lines: 18–18
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### K-0607 — `semantics/list.k:19`

- Lines: 19–19
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### K-0608 — `semantics/list.k:20`

- Lines: 20–20
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### K-0609 — `semantics/list.k:24`

- Lines: 24–25
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### K-0610 — `semantics/list.k:27`

- Lines: 27–27
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### K-0611 — `semantics/list.k:28`

- Lines: 28–28
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### K-0612 — `semantics/list.k:33`

- Lines: 33–33
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### K-0613 — `semantics/list.k:34`

- Lines: 34–34
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule hasRefVS(.ValSeq)                => false
```

### K-0614 — `semantics/list.k:35`

- Lines: 35–35
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### K-0615 — `semantics/list.k:37`

- Lines: 37–38
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### K-0616 — `semantics/list.k:39`

- Lines: 39–39
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### K-0617 — `semantics/list.k:40`

- Lines: 40–40
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### K-0618 — `semantics/list.k:41`

- Lines: 41–41
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### K-0619 — `semantics/list.k:42`

- Lines: 42–43
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### K-0620 — `semantics/list.k:45`

- Lines: 45–46
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### K-0621 — `semantics/list.k:47`

- Lines: 47–48
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### K-0622 — `semantics/list.k:49`

- Lines: 49–49
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### K-0623 — `semantics/list.k:50`

- Lines: 50–50
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### K-0624 — `semantics/list.k:53`

- Lines: 53–55
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### K-0625 — `semantics/list.k:58`

- Lines: 58–58
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### K-0626 — `semantics/list.k:59`

- Lines: 59–59
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### K-0627 — `semantics/list.k:60`

- Lines: 60–60
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### K-0628 — `semantics/list.k:61`

- Lines: 61–61
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### K-0629 — `semantics/list.k:62`

- Lines: 62–62
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### K-0630 — `semantics/list.k:63`

- Lines: 63–64
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### K-0631 — `semantics/list.k:65`

- Lines: 65–66
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### K-0632 — `semantics/list.k:67`

- Lines: 67–67
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### K-0633 — `semantics/methods.k:10`

- Lines: 10–10
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### K-0634 — `semantics/methods.k:13`

- Lines: 13–13
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### K-0635 — `semantics/methods.k:14`

- Lines: 14–14
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### K-0636 — `semantics/methods.k:15`

- Lines: 15–15
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### K-0637 — `semantics/methods.k:16`

- Lines: 16–16
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### K-0638 — `semantics/methods.k:19`

- Lines: 19–19
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### K-0639 — `semantics/methods.k:20`

- Lines: 20–20
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### K-0640 — `semantics/methods.k:21`

- Lines: 21–21
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### K-0641 — `semantics/methods.k:26`

- Lines: 26–26
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### K-0642 — `semantics/methods.k:27`

- Lines: 27–27
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### K-0643 — `semantics/methods.k:28`

- Lines: 28–28
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### K-0644 — `semantics/methods.k:29`

- Lines: 29–29
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### K-0645 — `semantics/methods.k:30`

- Lines: 30–31
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### K-0646 — `semantics/methods.k:34`

- Lines: 34–34
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### K-0647 — `semantics/methods.k:35`

- Lines: 35–35
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### K-0648 — `semantics/methods.k:36`

- Lines: 36–36
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### K-0649 — `semantics/methods.k:37`

- Lines: 37–38
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### K-0650 — `semantics/methods.k:39`

- Lines: 39–40
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### K-0651 — `semantics/methods.k:41`

- Lines: 41–41
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### K-0652 — `semantics/methods.k:42`

- Lines: 42–42
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### K-0653 — `semantics/methods.k:43`

- Lines: 43–43
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### K-0654 — `semantics/methods.k:44`

- Lines: 44–44
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### K-0655 — `semantics/methods.k:47`

- Lines: 47–47
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### K-0656 — `semantics/methods.k:48`

- Lines: 48–48
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### K-0657 — `semantics/methods.k:49`

- Lines: 49–49
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### K-0658 — `semantics/methods.k:50`

- Lines: 50–50
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### K-0659 — `semantics/methods.k:51`

- Lines: 51–51
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### K-0660 — `semantics/methods.k:52`

- Lines: 52–52
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### K-0661 — `semantics/methods.k:53`

- Lines: 53–53
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### K-0662 — `semantics/methods.k:54`

- Lines: 54–54
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### K-0663 — `semantics/methods.k:55`

- Lines: 55–55
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### K-0664 — `semantics/methods.k:58`

- Lines: 58–58
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### K-0665 — `semantics/methods.k:61`

- Lines: 61–61
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### K-0666 — `semantics/methods.k:64`

- Lines: 64–64
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### K-0667 — `semantics/methods.k:65`

- Lines: 65–65
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### K-0668 — `semantics/methods.k:66`

- Lines: 66–66
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### K-0669 — `semantics/methods.k:67`

- Lines: 67–67
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### K-0670 — `semantics/methods.k:68`

- Lines: 68–68
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### K-0671 — `semantics/methods.k:72`

- Lines: 72–74
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### K-0672 — `semantics/methods.k:75`

- Lines: 75–75
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### K-0673 — `semantics/methods.k:76`

- Lines: 76–76
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### K-0674 — `semantics/methods.k:77`

- Lines: 77–78
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### K-0675 — `semantics/methods.k:79`

- Lines: 79–80
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

### K-0676 — `semantics/methods.k:82`

- Lines: 82–82
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### K-0677 — `semantics/methods.k:83`

- Lines: 83–83
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### K-0678 — `semantics/methods.k:84`

- Lines: 84–84
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### K-0679 — `semantics/methods.k:85`

- Lines: 85–85
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### K-0680 — `semantics/methods.k:86`

- Lines: 86–86
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### K-0681 — `semantics/methods.k:89`

- Lines: 89–91
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### K-0682 — `semantics/methods.k:94`

- Lines: 94–96
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### K-0683 — `semantics/methods.k:97`

- Lines: 97–97
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### K-0684 — `semantics/methods.k:98`

- Lines: 98–98
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### K-0685 — `semantics/methods.k:99`

- Lines: 99–100
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### K-0686 — `semantics/methods.k:101`

- Lines: 101–102
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### K-0687 — `semantics/methods.k:104`

- Lines: 104–105
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### K-0688 — `semantics/methods.k:106`

- Lines: 106–106
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### K-0689 — `semantics/methods.k:107`

- Lines: 107–107
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### K-0690 — `semantics/methods.k:108`

- Lines: 108–108
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### K-0691 — `semantics/methods.k:109`

- Lines: 109–109
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### K-0692 — `semantics/methods.k:112`

- Lines: 112–112
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### K-0693 — `semantics/methods.k:113`

- Lines: 113–113
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### K-0694 — `semantics/methods.k:115`

- Lines: 115–115
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### K-0695 — `semantics/methods.k:116`

- Lines: 116–116
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### K-0696 — `semantics/methods.k:118`

- Lines: 118–118
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### K-0697 — `semantics/methods.k:119`

- Lines: 119–119
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### K-0698 — `semantics/methods.k:121`

- Lines: 121–121
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### K-0699 — `semantics/methods.k:122`

- Lines: 122–122
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K-0700 — `semantics/methods.k:124`

- Lines: 124–124
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### K-0701 — `semantics/methods.k:125`

- Lines: 125–125
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule hasUpper(.IntSeq) => false
```

### K-0702 — `semantics/methods.k:126`

- Lines: 126–126
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### K-0703 — `semantics/methods.k:128`

- Lines: 128–128
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### K-0704 — `semantics/methods.k:129`

- Lines: 129–129
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule hasLower(.IntSeq) => false
```

### K-0705 — `semantics/methods.k:130`

- Lines: 130–130
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### K-0706 — `semantics/methods.k:132`

- Lines: 132–132
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### K-0707 — `semantics/methods.k:133`

- Lines: 133–133
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule allAlpha(.IntSeq) => true
```

### K-0708 — `semantics/methods.k:134`

- Lines: 134–134
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### K-0709 — `semantics/methods.k:136`

- Lines: 136–136
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### K-0710 — `semantics/methods.k:137`

- Lines: 137–137
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule allDigit(.IntSeq) => true
```

### K-0711 — `semantics/methods.k:138`

- Lines: 138–138
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### K-0712 — `semantics/methods.k:140`

- Lines: 140–140
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### K-0713 — `semantics/methods.k:142`

- Lines: 142–142
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K-0714 — `semantics/methods.k:143`

- Lines: 143–143
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule lowerC(C:Int) => C         [owise]
```

### K-0715 — `semantics/methods.k:145`

- Lines: 145–145
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= upperC(Int) [function, total]
```

### K-0716 — `semantics/methods.k:146`

- Lines: 146–146
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K-0717 — `semantics/methods.k:147`

- Lines: 147–147
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule upperC(C:Int) => C         [owise]
```

### K-0718 — `semantics/methods.k:149`

- Lines: 149–149
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= swapC(Int) [function, total]
```

### K-0719 — `semantics/methods.k:150`

- Lines: 150–150
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K-0720 — `semantics/methods.k:151`

- Lines: 151–151
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K-0721 — `semantics/methods.k:152`

- Lines: 152–152
- Classification: function/equational rule
- Attributes: owise
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule swapC(C:Int) => C         [owise]
```

### K-0722 — `semantics/methods.k:154`

- Lines: 154–154
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### K-0723 — `semantics/methods.k:155`

- Lines: 155–155
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### K-0724 — `semantics/methods.k:156`

- Lines: 156–156
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### K-0725 — `semantics/methods.k:158`

- Lines: 158–158
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### K-0726 — `semantics/methods.k:159`

- Lines: 159–159
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### K-0727 — `semantics/methods.k:160`

- Lines: 160–160
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### K-0728 — `semantics/methods.k:162`

- Lines: 162–162
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### K-0729 — `semantics/methods.k:163`

- Lines: 163–163
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### K-0730 — `semantics/methods.k:164`

- Lines: 164–164
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### K-0731 — `semantics/methods.k:166`

- Lines: 166–166
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### K-0732 — `semantics/methods.k:167`

- Lines: 167–167
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### K-0733 — `semantics/methods.k:168`

- Lines: 168–168
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0734 — `semantics/methods.k:169`

- Lines: 169–169
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### K-0735 — `semantics/operators.k:10`

- Lines: 10–10
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### K-0736 — `semantics/operators.k:12`

- Lines: 12–12
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### K-0737 — `semantics/operators.k:15`

- Lines: 15–15
- Classification: evaluation context
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  context Compare(HOLE, _)
```

### K-0738 — `semantics/operators.k:16`

- Lines: 16–16
- Classification: evaluation context
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### K-0739 — `semantics/operators.k:17`

- Lines: 17–17
- Classification: ordinary operational semantic rule
- Attributes: owise
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### K-0740 — `semantics/operators.k:19`

- Lines: 19–19
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### K-0741 — `semantics/operators.k:20`

- Lines: 20–20
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### K-0742 — `semantics/operators.k:25`

- Lines: 25–27
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0743 — `semantics/operators.k:28`

- Lines: 28–31
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

### K-0744 — `semantics/operators.k:34`

- Lines: 34–37
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### K-0745 — `semantics/operators.k:38`

- Lines: 38–42
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### K-0746 — `semantics/operators.k:44`

- Lines: 44–46
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0747 — `semantics/range.k:9`

- Lines: 9–9
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### K-0748 — `semantics/range.k:10`

- Lines: 10–10
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### K-0749 — `semantics/range.k:12`

- Lines: 12–12
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### K-0750 — `semantics/range.k:13`

- Lines: 13–14
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### K-0751 — `semantics/range.k:15`

- Lines: 15–16
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### K-0752 — `semantics/range.k:17`

- Lines: 17–18
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### K-0753 — `semantics/range.k:20`

- Lines: 20–22
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### K-0754 — `semantics/range.k:23`

- Lines: 23–24
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### K-0755 — `semantics/set.k:8`

- Lines: 8–8
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= setV(IntSeq)
```

### K-0756 — `semantics/set.k:11`

- Lines: 11–11
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### K-0757 — `semantics/set.k:12`

- Lines: 12–12
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### K-0758 — `semantics/set.k:13`

- Lines: 13–13
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### K-0759 — `semantics/set.k:16`

- Lines: 16–17
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### K-0760 — `semantics/set.k:18`

- Lines: 18–18
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### K-0761 — `semantics/set.k:19`

- Lines: 19–19
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### K-0762 — `semantics/set.k:20`

- Lines: 20–21
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### K-0763 — `semantics/set.k:22`

- Lines: 22–23
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### K-0764 — `semantics/set.k:25`

- Lines: 25–25
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### K-0765 — `semantics/set.k:26`

- Lines: 26–26
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### K-0766 — `semantics/set.k:27`

- Lines: 27–27
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### K-0767 — `semantics/set.k:31`

- Lines: 31–31
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### K-0768 — `semantics/set.k:32`

- Lines: 32–32
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### K-0769 — `semantics/set.k:33`

- Lines: 33–33
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### K-0770 — `semantics/set.k:35`

- Lines: 35–35
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### K-0771 — `semantics/set.k:36`

- Lines: 36–36
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### K-0772 — `semantics/set.k:39`

- Lines: 39–39
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### K-0773 — `semantics/sort.k:18`

- Lines: 18–18
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### K-0774 — `semantics/sort.k:19`

- Lines: 19–19
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### K-0775 — `semantics/sort.k:20`

- Lines: 20–20
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### K-0776 — `semantics/sort.k:21`

- Lines: 21–21
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### K-0777 — `semantics/sort.k:22`

- Lines: 22–22
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### K-0778 — `semantics/sort.k:23`

- Lines: 23–23
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### K-0779 — `semantics/sort.k:24`

- Lines: 24–24
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### K-0780 — `semantics/sort.k:26`

- Lines: 26–26
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### K-0781 — `semantics/sort.k:27`

- Lines: 27–27
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### K-0782 — `semantics/sort.k:28`

- Lines: 28–28
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### K-0783 — `semantics/sort.k:29`

- Lines: 29–30
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### K-0784 — `semantics/sort.k:31`

- Lines: 31–32
- Classification: function/equational rule; concrete-only equation
- Attributes: concrete
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### K-0785 — `semantics/sort.k:36`

- Lines: 36–37
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### K-0786 — `semantics/sort.k:40`

- Lines: 40–42
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### K-0787 — `semantics/sort.k:49`

- Lines: 49–49
- Classification: local syntax/function declaration
- Attributes: function, total, symbol, no-evaluators
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### K-0788 — `semantics/sort.k:51`

- Lines: 51–52
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### K-0789 — `semantics/sort.k:53`

- Lines: 53–53
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### K-0790 — `semantics/sort.k:54`

- Lines: 54–54
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### K-0791 — `semantics/sort.k:55`

- Lines: 55–55
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### K-0792 — `semantics/sort.k:57`

- Lines: 57–57
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### K-0793 — `semantics/sort.k:58`

- Lines: 58–58
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule condRev(S:ValSeq, false) => S
```

### K-0794 — `semantics/sort.k:59`

- Lines: 59–59
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### K-0795 — `semantics/sort.k:61`

- Lines: 61–62
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### K-0796 — `semantics/sort.k:63`

- Lines: 63–64
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### K-0797 — `semantics/sort.k:65`

- Lines: 65–66
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

### K-0798 — `semantics/str.k:8`

- Lines: 8–8
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### K-0799 — `semantics/str.k:9`

- Lines: 9–10
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### K-0800 — `semantics/str.k:13`

- Lines: 13–13
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### K-0801 — `semantics/str.k:14`

- Lines: 14–14
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### K-0802 — `semantics/str.k:15`

- Lines: 15–15
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strToCodes("") => .IntSeq
```

### K-0803 — `semantics/str.k:16`

- Lines: 16–17
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### K-0804 — `semantics/str.k:20`

- Lines: 20–20
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### K-0805 — `semantics/str.k:21`

- Lines: 21–21
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### K-0806 — `semantics/str.k:22`

- Lines: 22–22
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### K-0807 — `semantics/str.k:24`

- Lines: 24–24
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### K-0808 — `semantics/str.k:25`

- Lines: 25–25
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### K-0809 — `semantics/str.k:26`

- Lines: 26–26
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### K-0810 — `semantics/str.k:29`

- Lines: 29–29
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### K-0811 — `semantics/str.k:30`

- Lines: 30–30
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### K-0812 — `semantics/str.k:32`

- Lines: 32–32
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### K-0813 — `semantics/str.k:33`

- Lines: 33–33
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### K-0814 — `semantics/str.k:34`

- Lines: 34–34
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0815 — `semantics/str.k:35`

- Lines: 35–35
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### K-0816 — `semantics/str.k:37`

- Lines: 37–37
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### K-0817 — `semantics/str.k:38`

- Lines: 38–38
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### K-0818 — `semantics/str.k:39`

- Lines: 39–39
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### K-0819 — `semantics/str.k:40`

- Lines: 40–41
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

### K-0820 — `semantics/str.k:48`

- Lines: 48–48
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### K-0821 — `semantics/str.k:49`

- Lines: 49–49
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### K-0822 — `semantics/str.k:50`

- Lines: 50–50
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### K-0823 — `semantics/str.k:51`

- Lines: 51–51
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K-0824 — `semantics/str.k:52`

- Lines: 52–52
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### K-0825 — `semantics/str.k:53`

- Lines: 53–53
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### K-0826 — `semantics/str.k:54`

- Lines: 54–54
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### K-0827 — `semantics/str.k:56`

- Lines: 56–56
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K-0828 — `semantics/str.k:57`

- Lines: 57–57
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### K-0829 — `semantics/str.k:58`

- Lines: 58–58
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### K-0830 — `semantics/str.k:59`

- Lines: 59–59
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### K-0831 — `semantics/subscript.k:11`

- Lines: 11–11
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### K-0832 — `semantics/subscript.k:12`

- Lines: 12–12
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### K-0833 — `semantics/subscript.k:13`

- Lines: 13–14
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K-0834 — `semantics/subscript.k:16`

- Lines: 16–16
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### K-0835 — `semantics/subscript.k:17`

- Lines: 17–17
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### K-0836 — `semantics/subscript.k:18`

- Lines: 18–19
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K-0837 — `semantics/subscript.k:21`

- Lines: 21–21
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### K-0838 — `semantics/subscript.k:22`

- Lines: 22–22
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K-0839 — `semantics/subscript.k:23`

- Lines: 23–23
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### K-0840 — `semantics/subscript.k:27`

- Lines: 27–27
- Classification: evaluation context
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  context Subscript(HOLE, _)
```

### K-0841 — `semantics/subscript.k:28`

- Lines: 28–28
- Classification: evaluation context
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  context Subscript(_:Val, HOLE:Expr)
```

### K-0842 — `semantics/subscript.k:31`

- Lines: 31–33
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0843 — `semantics/subscript.k:35`

- Lines: 35–35
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### K-0844 — `semantics/subscript.k:37`

- Lines: 37–37
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### K-0845 — `semantics/subscript.k:38`

- Lines: 38–38
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K-0846 — `semantics/subscript.k:39`

- Lines: 39–39
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K-0847 — `semantics/subscript.k:40`

- Lines: 40–41
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### K-0848 — `semantics/subscript.k:44`

- Lines: 44–47
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### K-0849 — `semantics/subscript.k:49`

- Lines: 49–49
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### K-0850 — `semantics/subscript.k:50`

- Lines: 50–50
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### K-0851 — `semantics/subscript.k:51`

- Lines: 51–51
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### K-0852 — `semantics/subscript.k:52`

- Lines: 52–52
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### K-0853 — `semantics/subscript.k:54`

- Lines: 54–54
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### K-0854 — `semantics/subscript.k:55`

- Lines: 55–55
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### K-0855 — `semantics/subscript.k:56`

- Lines: 56–56
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### K-0856 — `semantics/subscript.k:58`

- Lines: 58–60
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### K-0857 — `semantics/subscript.k:61`

- Lines: 61–61
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### K-0858 — `semantics/subscript.k:63`

- Lines: 63–63
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### K-0859 — `semantics/subscript.k:64`

- Lines: 64–65
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K-0860 — `semantics/subscript.k:66`

- Lines: 66–67
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K-0861 — `semantics/subscript.k:68`

- Lines: 68–69
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### K-0862 — `semantics/subscript.k:72`

- Lines: 72–72
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### K-0863 — `semantics/subscript.k:73`

- Lines: 73–73
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStep(noB)          => 1
```

### K-0864 — `semantics/subscript.k:74`

- Lines: 74–74
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStep(someB(S:Int)) => S
```

### K-0865 — `semantics/subscript.k:76`

- Lines: 76–76
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### K-0866 — `semantics/subscript.k:77`

- Lines: 77–78
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### K-0867 — `semantics/subscript.k:79`

- Lines: 79–80
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### K-0868 — `semantics/subscript.k:81`

- Lines: 81–81
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K-0869 — `semantics/subscript.k:83`

- Lines: 83–83
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### K-0870 — `semantics/subscript.k:84`

- Lines: 84–85
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### K-0871 — `semantics/subscript.k:86`

- Lines: 86–87
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### K-0872 — `semantics/subscript.k:88`

- Lines: 88–88
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K-0873 — `semantics/subscript.k:90`

- Lines: 90–90
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### K-0874 — `semantics/subscript.k:91`

- Lines: 91–92
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### K-0875 — `semantics/subscript.k:93`

- Lines: 93–94
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### K-0876 — `semantics/subscript.k:96`

- Lines: 96–96
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### K-0877 — `semantics/subscript.k:97`

- Lines: 97–98
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### K-0878 — `semantics/subscript.k:99`

- Lines: 99–100
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### K-0879 — `semantics/subscript.k:102`

- Lines: 102–102
- Classification: local syntax/function declaration
- Attributes: function, total
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### K-0880 — `semantics/subscript.k:103`

- Lines: 103–104
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### K-0881 — `semantics/subscript.k:105`

- Lines: 105–106
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

### K-0882 — `semantics/subscript.k:109`

- Lines: 109–109
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### K-0883 — `semantics/subscript.k:110`

- Lines: 110–112
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K-0884 — `semantics/subscript.k:113`

- Lines: 113–114
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K-0885 — `semantics/subscript.k:116`

- Lines: 116–116
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### K-0886 — `semantics/subscript.k:117`

- Lines: 117–119
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K-0887 — `semantics/subscript.k:120`

- Lines: 120–121
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K-0888 — `semantics/syntax.k:9`

- Lines: 9–30
- Classification: local syntax/function declaration
- Attributes: macro, strict, seqstrict
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

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

### K-0889 — `semantics/syntax.k:32`

- Lines: 32–32
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### K-0890 — `semantics/syntax.k:33`

- Lines: 33–33
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### K-0891 — `semantics/syntax.k:34`

- Lines: 34–34
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Entries  ::= List{Entry, ","}
```

### K-0892 — `semantics/syntax.k:35`

- Lines: 35–35
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### K-0893 — `semantics/syntax.k:36`

- Lines: 36–36
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax CompFors ::= List{CompFor, ""}
```

### K-0894 — `semantics/syntax.k:37`

- Lines: 37–37
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Exprs    ::= List{Expr, ","}
```

### K-0895 — `semantics/syntax.k:38`

- Lines: 38–38
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### K-0896 — `semantics/syntax.k:39`

- Lines: 39–39
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Bound    ::= Expr | "NoBound"
```

### K-0897 — `semantics/syntax.k:41`

- Lines: 41–54
- Classification: local syntax/function declaration
- Attributes: strict
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

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

### K-0898 — `semantics/syntax.k:56`

- Lines: 56–56
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### K-0899 — `semantics/syntax.k:57`

- Lines: 57–57
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### K-0900 — `semantics/syntax.k:58`

- Lines: 58–58
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### K-0901 — `semantics/syntax.k:59`

- Lines: 59–59
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### K-0902 — `semantics/syntax.k:60`

- Lines: 60–60
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax ParamNames ::= List{String, ","}
```

### K-0903 — `semantics/syntax.k:61`

- Lines: 61–61
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — checked on the entry execution slice for binding, evaluation order, control/state footprint, and result flow

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### K-0904 — `semantics/tuple.k:10`

- Lines: 10–10
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### K-0905 — `semantics/tuple.k:11`

- Lines: 11–11
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### K-0906 — `semantics/tuple.k:14`

- Lines: 14–14
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax ApplyK ::= "toTuple"
```

### K-0907 — `semantics/tuple.k:15`

- Lines: 15–15
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### K-0908 — `semantics/tuple.k:16`

- Lines: 16–16
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### K-0909 — `semantics/tuple.k:18`

- Lines: 18–18
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### K-0910 — `semantics/tuple.k:20`

- Lines: 20–20
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### K-0911 — `semantics/tuple.k:21`

- Lines: 21–21
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### K-0912 — `semantics/tuple.k:23`

- Lines: 23–23
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### K-0913 — `semantics/tuple.k:24`

- Lines: 24–24
- Classification: local syntax/function declaration
- Attributes: function
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### K-0914 — `semantics/tuple.k:25`

- Lines: 25–25
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### K-0915 — `semantics/tuple.k:26`

- Lines: 26–27
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### K-0916 — `semantics/tuple.k:28`

- Lines: 28–28
- Classification: function/equational rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### K-0917 — `semantics/tuple.k:31`

- Lines: 31–31
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### K-0918 — `semantics/tuple.k:32`

- Lines: 32–34
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K-0919 — `semantics/tuple.k:35`

- Lines: 35–41
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K-0920 — `semantics/tuple.k:42`

- Lines: 42–42
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K-0921 — `semantics/tuple.k:43`

- Lines: 43–43
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K-0922 — `semantics/tuple.k:44`

- Lines: 44–46
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0923 — `semantics/tuple.k:49`

- Lines: 49–49
- Classification: local syntax/function declaration
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### K-0924 — `semantics/tuple.k:50`

- Lines: 50–50
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K-0925 — `semantics/tuple.k:51`

- Lines: 51–51
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K-0926 — `semantics/tuple.k:52`

- Lines: 52–54
- Classification: ordinary operational semantic rule; priority rule
- Attributes: priority
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K-0927 — `semantics/tuple.k:55`

- Lines: 55–56
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### K-0928 — `semantics/tuple.k:57`

- Lines: 57–57
- Classification: ordinary operational semantic rule
- Attributes: none
- Entry slice: no
- Audit decision: ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; guard/sort/priority reviewed and no match or dependency on this entry claim

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### K-0929 — `verification.k:8`

- Lines: 8–8
- Classification: local syntax/function declaration
- Attributes: macro
- Entry slice: yes
- Audit decision: ACCEPT_USED — exact submitted AST macro; expands syntax and leaves all program control/value computation to fixed semantics

```k
  syntax Module ::= "solutionProgram" [macro]
```

### K-0930 — `verification.k:9`

- Lines: 9–12
- Classification: function/equational rule
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_USED — exact submitted AST macro; expands syntax and leaves all program control/value computation to fixed semantics

```k
  rule solutionProgram
    => Module(
         FuncDef("truncate_number", Params("number"),
           Return(BinOp("%", Name("number"), Float(1.0)))))
```

### K-0931 — `spec.k:10`

- Lines: 10–32
- Classification: positive reachability claim
- Attributes: none
- Entry slice: yes
- Audit decision: ACCEPT_WITH_BOUNDARY — satisfiable and result-constraining; the floatMod-to-human-decimal bridge remains a named primitive contract

```k
  claim
    <k> #loadAll(solutionProgram)
         ~> Call(Name("truncate_number"), (Float(N:Float), .Exprs))
      => floatMod(N, 1.0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => 0 |-> scope(
           "truncate_number" |-> closureVal(
             ("number", .ParamNames),
             Return(BinOp("%", Name("number"), Float(1.0))) .Stmts,
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


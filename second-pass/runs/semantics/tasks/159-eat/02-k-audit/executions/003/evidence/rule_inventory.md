# Exhaustive K source inventory

This inventory covers every source-level `syntax`, `configuration`, `context`, `rule`, and `claim` declaration in the supplied semantics tree and candidate `verification.k`. Generated strictness rules and K builtin definitions are recorded separately as toolchain trust.

## Totals

- `attr:concrete`: 35
- `attr:function`: 147
- `attr:macro`: 4
- `attr:macro-rec`: 1
- `attr:no-evaluators`: 22
- `attr:owise`: 26
- `attr:priority`: 45
- `attr:seqstrict`: 1
- `attr:strict`: 2
- `attr:symbol`: 25
- `attr:total`: 107
- `configuration`: 1
- `context`: 5
- `rule`: 696
- `syntax`: 228

## Per-file counts

| File | Syntax | Configuration | Context | Rule | Claim | Opaque | Priority | Concrete |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `/candidate/reference-semantics/semantics/assert.k` | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 |
| `/candidate/reference-semantics/semantics/bool.k` | 0 | 0 | 1 | 13 | 0 | 0 | 5 | 0 |
| `/candidate/reference-semantics/semantics/builtins.k` | 38 | 0 | 0 | 137 | 0 | 1 | 1 | 0 |
| `/candidate/reference-semantics/semantics/call.k` | 3 | 0 | 0 | 21 | 0 | 0 | 5 | 0 |
| `/candidate/reference-semantics/semantics/comprehension.k` | 3 | 0 | 0 | 7 | 0 | 0 | 0 | 0 |
| `/candidate/reference-semantics/semantics/concrete.k` | 5 | 0 | 0 | 16 | 0 | 0 | 2 | 0 |
| `/candidate/reference-semantics/semantics/controls.k` | 3 | 0 | 0 | 34 | 0 | 0 | 6 | 0 |
| `/candidate/reference-semantics/semantics/core.k` | 37 | 1 | 0 | 46 | 0 | 0 | 2 | 0 |
| `/candidate/reference-semantics/semantics/dict.k` | 12 | 0 | 0 | 28 | 0 | 0 | 2 | 0 |
| `/candidate/reference-semantics/semantics/float.k` | 34 | 0 | 0 | 121 | 0 | 19 | 4 | 26 |
| `/candidate/reference-semantics/semantics/functions.k` | 4 | 0 | 0 | 15 | 0 | 0 | 1 | 0 |
| `/candidate/reference-semantics/semantics/int.k` | 1 | 0 | 0 | 16 | 0 | 0 | 0 | 0 |
| `/candidate/reference-semantics/semantics/iter.k` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `/candidate/reference-semantics/semantics/list.k` | 5 | 0 | 0 | 27 | 0 | 0 | 2 | 0 |
| `/candidate/reference-semantics/semantics/methods.k` | 27 | 0 | 0 | 75 | 0 | 0 | 3 | 0 |
| `/candidate/reference-semantics/semantics/operators.k` | 0 | 0 | 2 | 10 | 0 | 0 | 5 | 0 |
| `/candidate/reference-semantics/semantics/range.k` | 2 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| `/candidate/reference-semantics/semantics/set.k` | 6 | 0 | 0 | 12 | 0 | 0 | 0 | 0 |
| `/candidate/reference-semantics/semantics/sort.k` | 6 | 0 | 0 | 19 | 0 | 2 | 1 | 9 |
| `/candidate/reference-semantics/semantics/str.k` | 5 | 0 | 0 | 28 | 0 | 0 | 0 | 0 |
| `/candidate/reference-semantics/semantics/subscript.k` | 15 | 0 | 2 | 40 | 0 | 0 | 2 | 0 |
| `/candidate/reference-semantics/semantics/syntax.k` | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `/candidate/reference-semantics/semantics/tuple.k` | 4 | 0 | 0 | 21 | 0 | 0 | 3 | 0 |
| `/candidate/reference-semantics/semantics.k` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `/candidate/verification.k` | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

## Entries

### K0001 — `/candidate/reference-semantics/semantics/assert.k:6`

- Kind: `rule`; attributes: `none`; lines: 6–7.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### K0002 — `/candidate/reference-semantics/semantics/assert.k:8`

- Kind: `rule`; attributes: `none`; lines: 8–11.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### K0003 — `/candidate/reference-semantics/semantics/assert.k:13`

- Kind: `rule`; attributes: `priority`; lines: 13–15.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0004 — `/candidate/reference-semantics/semantics/bool.k:8`

- Kind: `rule`; attributes: `none`; lines: 8–8.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### K0005 — `/candidate/reference-semantics/semantics/bool.k:10`

- Kind: `rule`; attributes: `none`; lines: 10–10.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### K0006 — `/candidate/reference-semantics/semantics/bool.k:11`

- Kind: `rule`; attributes: `none`; lines: 11–11.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### K0007 — `/candidate/reference-semantics/semantics/bool.k:16`

- Kind: `context`; attributes: `none`; lines: 16–16.
- Decision: FIXED_EVALUATION_CONTEXT: not exercised by eat unless noted in path map.

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### K0008 — `/candidate/reference-semantics/semantics/bool.k:17`

- Kind: `rule`; attributes: `none`; lines: 17–17.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### K0009 — `/candidate/reference-semantics/semantics/bool.k:18`

- Kind: `rule`; attributes: `none`; lines: 18–19.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### K0010 — `/candidate/reference-semantics/semantics/bool.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–21.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### K0011 — `/candidate/reference-semantics/semantics/bool.k:22`

- Kind: `rule`; attributes: `none`; lines: 22–23.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### K0012 — `/candidate/reference-semantics/semantics/bool.k:24`

- Kind: `rule`; attributes: `none`; lines: 24–25.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

### K0013 — `/candidate/reference-semantics/semantics/bool.k:29`

- Kind: `rule`; attributes: `priority`; lines: 29–30.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### K0014 — `/candidate/reference-semantics/semantics/bool.k:31`

- Kind: `rule`; attributes: `priority`; lines: 31–34.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K0015 — `/candidate/reference-semantics/semantics/bool.k:35`

- Kind: `rule`; attributes: `priority`; lines: 35–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K0016 — `/candidate/reference-semantics/semantics/bool.k:39`

- Kind: `rule`; attributes: `priority`; lines: 39–42.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### K0017 — `/candidate/reference-semantics/semantics/bool.k:43`

- Kind: `rule`; attributes: `priority`; lines: 43–46.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### K0018 — `/candidate/reference-semantics/semantics/builtins.k:17`

- Kind: `syntax`; attributes: `function`; lines: 17–17.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### K0019 — `/candidate/reference-semantics/semantics/builtins.k:20`

- Kind: `syntax`; attributes: `function`; lines: 20–20.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= seqLen(Val) [function]
```

### K0020 — `/candidate/reference-semantics/semantics/builtins.k:21`

- Kind: `rule`; attributes: `none`; lines: 21–21.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### K0021 — `/candidate/reference-semantics/semantics/builtins.k:22`

- Kind: `rule`; attributes: `none`; lines: 22–22.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### K0022 — `/candidate/reference-semantics/semantics/builtins.k:23`

- Kind: `rule`; attributes: `none`; lines: 23–23.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### K0023 — `/candidate/reference-semantics/semantics/builtins.k:24`

- Kind: `rule`; attributes: `none`; lines: 24–24.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### K0024 — `/candidate/reference-semantics/semantics/builtins.k:25`

- Kind: `rule`; attributes: `none`; lines: 25–25.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### K0025 — `/candidate/reference-semantics/semantics/builtins.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### K0026 — `/candidate/reference-semantics/semantics/builtins.k:32`

- Kind: `rule`; attributes: `none`; lines: 32–32.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### K0027 — `/candidate/reference-semantics/semantics/builtins.k:33`

- Kind: `rule`; attributes: `none`; lines: 33–33.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### K0028 — `/candidate/reference-semantics/semantics/builtins.k:34`

- Kind: `rule`; attributes: `none`; lines: 34–34.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### K0029 — `/candidate/reference-semantics/semantics/builtins.k:35`

- Kind: `rule`; attributes: `none`; lines: 35–35.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### K0030 — `/candidate/reference-semantics/semantics/builtins.k:36`

- Kind: `syntax`; attributes: `function, total`; lines: 36–36.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### K0031 — `/candidate/reference-semantics/semantics/builtins.k:37`

- Kind: `rule`; attributes: `none`; lines: 37–37.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### K0032 — `/candidate/reference-semantics/semantics/builtins.k:38`

- Kind: `rule`; attributes: `none`; lines: 38–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### K0033 — `/candidate/reference-semantics/semantics/builtins.k:41`

- Kind: `rule`; attributes: `none`; lines: 41–41.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### K0034 — `/candidate/reference-semantics/semantics/builtins.k:44`

- Kind: `rule`; attributes: `none`; lines: 44–44.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### K0035 — `/candidate/reference-semantics/semantics/builtins.k:47`

- Kind: `syntax`; attributes: `none`; lines: 47–47.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### K0036 — `/candidate/reference-semantics/semantics/builtins.k:48`

- Kind: `rule`; attributes: `none`; lines: 48–48.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### K0037 — `/candidate/reference-semantics/semantics/builtins.k:49`

- Kind: `rule`; attributes: `none`; lines: 49–49.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### K0038 — `/candidate/reference-semantics/semantics/builtins.k:50`

- Kind: `rule`; attributes: `none`; lines: 50–52.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K0039 — `/candidate/reference-semantics/semantics/builtins.k:54`

- Kind: `syntax`; attributes: `function`; lines: 54–54.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= intOf(Val) [function]
```

### K0040 — `/candidate/reference-semantics/semantics/builtins.k:55`

- Kind: `rule`; attributes: `none`; lines: 55–55.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intOf(I:Int)  => I
```

### K0041 — `/candidate/reference-semantics/semantics/builtins.k:56`

- Kind: `rule`; attributes: `none`; lines: 56–56.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### K0042 — `/candidate/reference-semantics/semantics/builtins.k:59`

- Kind: `syntax`; attributes: `none`; lines: 59–59.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### K0043 — `/candidate/reference-semantics/semantics/builtins.k:60`

- Kind: `rule`; attributes: `none`; lines: 60–60.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### K0044 — `/candidate/reference-semantics/semantics/builtins.k:61`

- Kind: `rule`; attributes: `none`; lines: 61–61.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### K0045 — `/candidate/reference-semantics/semantics/builtins.k:62`

- Kind: `rule`; attributes: `none`; lines: 62–63.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### K0046 — `/candidate/reference-semantics/semantics/builtins.k:64`

- Kind: `rule`; attributes: `none`; lines: 64–65.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### K0047 — `/candidate/reference-semantics/semantics/builtins.k:67`

- Kind: `syntax`; attributes: `none`; lines: 67–67.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### K0048 — `/candidate/reference-semantics/semantics/builtins.k:68`

- Kind: `rule`; attributes: `none`; lines: 68–68.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### K0049 — `/candidate/reference-semantics/semantics/builtins.k:69`

- Kind: `rule`; attributes: `none`; lines: 69–69.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### K0050 — `/candidate/reference-semantics/semantics/builtins.k:70`

- Kind: `rule`; attributes: `none`; lines: 70–71.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### K0051 — `/candidate/reference-semantics/semantics/builtins.k:72`

- Kind: `rule`; attributes: `none`; lines: 72–73.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

### K0052 — `/candidate/reference-semantics/semantics/builtins.k:76`

- Kind: `syntax`; attributes: `none`; lines: 76–76.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### K0053 — `/candidate/reference-semantics/semantics/builtins.k:77`

- Kind: `rule`; attributes: `none`; lines: 77–77.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### K0054 — `/candidate/reference-semantics/semantics/builtins.k:78`

- Kind: `rule`; attributes: `none`; lines: 78–79.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K0055 — `/candidate/reference-semantics/semantics/builtins.k:80`

- Kind: `rule`; attributes: `none`; lines: 80–80.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### K0056 — `/candidate/reference-semantics/semantics/builtins.k:81`

- Kind: `rule`; attributes: `none`; lines: 81–81.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### K0057 — `/candidate/reference-semantics/semantics/builtins.k:82`

- Kind: `rule`; attributes: `none`; lines: 82–84.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K0058 — `/candidate/reference-semantics/semantics/builtins.k:86`

- Kind: `syntax`; attributes: `none`; lines: 86–86.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### K0059 — `/candidate/reference-semantics/semantics/builtins.k:87`

- Kind: `rule`; attributes: `none`; lines: 87–87.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### K0060 — `/candidate/reference-semantics/semantics/builtins.k:88`

- Kind: `rule`; attributes: `none`; lines: 88–89.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### K0061 — `/candidate/reference-semantics/semantics/builtins.k:90`

- Kind: `rule`; attributes: `none`; lines: 90–90.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### K0062 — `/candidate/reference-semantics/semantics/builtins.k:91`

- Kind: `rule`; attributes: `none`; lines: 91–91.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### K0063 — `/candidate/reference-semantics/semantics/builtins.k:92`

- Kind: `rule`; attributes: `none`; lines: 92–94.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### K0064 — `/candidate/reference-semantics/semantics/builtins.k:97`

- Kind: `syntax`; attributes: `function`; lines: 97–97.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### K0065 — `/candidate/reference-semantics/semantics/builtins.k:98`

- Kind: `rule`; attributes: `none`; lines: 98–98.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### K0066 — `/candidate/reference-semantics/semantics/builtins.k:99`

- Kind: `rule`; attributes: `none`; lines: 99–99.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule maxVals(M:Int, .Vals)           => M
```

### K0067 — `/candidate/reference-semantics/semantics/builtins.k:100`

- Kind: `rule`; attributes: `none`; lines: 100–100.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### K0068 — `/candidate/reference-semantics/semantics/builtins.k:102`

- Kind: `syntax`; attributes: `function`; lines: 102–102.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### K0069 — `/candidate/reference-semantics/semantics/builtins.k:103`

- Kind: `rule`; attributes: `none`; lines: 103–103.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### K0070 — `/candidate/reference-semantics/semantics/builtins.k:104`

- Kind: `rule`; attributes: `none`; lines: 104–104.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule minVals(M:Int, .Vals)           => M
```

### K0071 — `/candidate/reference-semantics/semantics/builtins.k:105`

- Kind: `rule`; attributes: `none`; lines: 105–105.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### K0072 — `/candidate/reference-semantics/semantics/builtins.k:108`

- Kind: `rule`; attributes: `none`; lines: 108–109.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

### K0073 — `/candidate/reference-semantics/semantics/builtins.k:111`

- Kind: `rule`; attributes: `none`; lines: 111–113.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### K0074 — `/candidate/reference-semantics/semantics/builtins.k:114`

- Kind: `syntax`; attributes: `function, total`; lines: 114–114.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### K0075 — `/candidate/reference-semantics/semantics/builtins.k:115`

- Kind: `rule`; attributes: `none`; lines: 115–115.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### K0076 — `/candidate/reference-semantics/semantics/builtins.k:116`

- Kind: `rule`; attributes: `none`; lines: 116–116.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### K0077 — `/candidate/reference-semantics/semantics/builtins.k:117`

- Kind: `syntax`; attributes: `function, total`; lines: 117–117.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### K0078 — `/candidate/reference-semantics/semantics/builtins.k:118`

- Kind: `rule`; attributes: `none`; lines: 118–118.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### K0079 — `/candidate/reference-semantics/semantics/builtins.k:119`

- Kind: `rule`; attributes: `none`; lines: 119–121.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

### K0080 — `/candidate/reference-semantics/semantics/builtins.k:124`

- Kind: `rule`; attributes: `none`; lines: 124–125.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### K0081 — `/candidate/reference-semantics/semantics/builtins.k:126`

- Kind: `syntax`; attributes: `function, total`; lines: 126–126.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### K0082 — `/candidate/reference-semantics/semantics/builtins.k:127`

- Kind: `rule`; attributes: `none`; lines: 127–127.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### K0083 — `/candidate/reference-semantics/semantics/builtins.k:128`

- Kind: `rule`; attributes: `none`; lines: 128–129.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### K0084 — `/candidate/reference-semantics/semantics/builtins.k:132`

- Kind: `rule`; attributes: `none`; lines: 132–133.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### K0085 — `/candidate/reference-semantics/semantics/builtins.k:134`

- Kind: `syntax`; attributes: `function, total`; lines: 134–134.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### K0086 — `/candidate/reference-semantics/semantics/builtins.k:135`

- Kind: `rule`; attributes: `none`; lines: 135–135.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### K0087 — `/candidate/reference-semantics/semantics/builtins.k:136`

- Kind: `rule`; attributes: `none`; lines: 136–136.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### K0088 — `/candidate/reference-semantics/semantics/builtins.k:137`

- Kind: `rule`; attributes: `none`; lines: 137–137.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### K0089 — `/candidate/reference-semantics/semantics/builtins.k:140`

- Kind: `rule`; attributes: `none`; lines: 140–140.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### K0090 — `/candidate/reference-semantics/semantics/builtins.k:143`

- Kind: `rule`; attributes: `none`; lines: 143–143.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### K0091 — `/candidate/reference-semantics/semantics/builtins.k:144`

- Kind: `rule`; attributes: `none`; lines: 144–145.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

### K0092 — `/candidate/reference-semantics/semantics/builtins.k:148`

- Kind: `rule`; attributes: `none`; lines: 148–148.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### K0093 — `/candidate/reference-semantics/semantics/builtins.k:149`

- Kind: `rule`; attributes: `none`; lines: 149–149.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### K0094 — `/candidate/reference-semantics/semantics/builtins.k:152`

- Kind: `rule`; attributes: `none`; lines: 152–153.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

### K0095 — `/candidate/reference-semantics/semantics/builtins.k:156`

- Kind: `rule`; attributes: `none`; lines: 156–157.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### K0096 — `/candidate/reference-semantics/semantics/builtins.k:158`

- Kind: `syntax`; attributes: `function, total`; lines: 158–158.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### K0097 — `/candidate/reference-semantics/semantics/builtins.k:159`

- Kind: `rule`; attributes: `none`; lines: 159–159.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### K0098 — `/candidate/reference-semantics/semantics/builtins.k:160`

- Kind: `rule`; attributes: `none`; lines: 160–160.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### K0099 — `/candidate/reference-semantics/semantics/builtins.k:163`

- Kind: `rule`; attributes: `none`; lines: 163–163.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### K0100 — `/candidate/reference-semantics/semantics/builtins.k:164`

- Kind: `rule`; attributes: `none`; lines: 164–164.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### K0101 — `/candidate/reference-semantics/semantics/builtins.k:167`

- Kind: `rule`; attributes: `none`; lines: 167–168.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### K0102 — `/candidate/reference-semantics/semantics/builtins.k:169`

- Kind: `rule`; attributes: `none`; lines: 169–169.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### K0103 — `/candidate/reference-semantics/semantics/builtins.k:170`

- Kind: `rule`; attributes: `none`; lines: 170–170.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### K0104 — `/candidate/reference-semantics/semantics/builtins.k:171`

- Kind: `rule`; attributes: `none`; lines: 171–172.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### K0105 — `/candidate/reference-semantics/semantics/builtins.k:173`

- Kind: `rule`; attributes: `none`; lines: 173–173.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### K0106 — `/candidate/reference-semantics/semantics/builtins.k:174`

- Kind: `rule`; attributes: `none`; lines: 174–174.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### K0107 — `/candidate/reference-semantics/semantics/builtins.k:177`

- Kind: `rule`; attributes: `none`; lines: 177–177.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### K0108 — `/candidate/reference-semantics/semantics/builtins.k:178`

- Kind: `rule`; attributes: `none`; lines: 178–178.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### K0109 — `/candidate/reference-semantics/semantics/builtins.k:179`

- Kind: `rule`; attributes: `none`; lines: 179–180.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

### K0110 — `/candidate/reference-semantics/semantics/builtins.k:187`

- Kind: `rule`; attributes: `none`; lines: 187–187.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### K0111 — `/candidate/reference-semantics/semantics/builtins.k:188`

- Kind: `syntax`; attributes: `function`; lines: 188–188.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### K0112 — `/candidate/reference-semantics/semantics/builtins.k:189`

- Kind: `rule`; attributes: `none`; lines: 189–190.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### K0113 — `/candidate/reference-semantics/semantics/builtins.k:192`

- Kind: `syntax`; attributes: `none`; lines: 192–192.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### K0114 — `/candidate/reference-semantics/semantics/builtins.k:194`

- Kind: `syntax`; attributes: `function, total`; lines: 194–194.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### K0115 — `/candidate/reference-semantics/semantics/builtins.k:195`

- Kind: `rule`; attributes: `none`; lines: 195–195.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K0116 — `/candidate/reference-semantics/semantics/builtins.k:196`

- Kind: `syntax`; attributes: `function, total`; lines: 196–196.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### K0117 — `/candidate/reference-semantics/semantics/builtins.k:197`

- Kind: `rule`; attributes: `none`; lines: 197–197.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### K0118 — `/candidate/reference-semantics/semantics/builtins.k:198`

- Kind: `rule`; attributes: `owise`; lines: 198–198.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### K0119 — `/candidate/reference-semantics/semantics/builtins.k:199`

- Kind: `syntax`; attributes: `function, total`; lines: 199–199.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### K0120 — `/candidate/reference-semantics/semantics/builtins.k:200`

- Kind: `rule`; attributes: `none`; lines: 200–200.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### K0121 — `/candidate/reference-semantics/semantics/builtins.k:201`

- Kind: `rule`; attributes: `owise`; lines: 201–201.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### K0122 — `/candidate/reference-semantics/semantics/builtins.k:203`

- Kind: `syntax`; attributes: `function, total`; lines: 203–203.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### K0123 — `/candidate/reference-semantics/semantics/builtins.k:204`

- Kind: `rule`; attributes: `none`; lines: 204–204.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### K0124 — `/candidate/reference-semantics/semantics/builtins.k:205`

- Kind: `rule`; attributes: `none`; lines: 205–205.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### K0125 — `/candidate/reference-semantics/semantics/builtins.k:206`

- Kind: `rule`; attributes: `none`; lines: 206–206.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### K0126 — `/candidate/reference-semantics/semantics/builtins.k:207`

- Kind: `rule`; attributes: `none`; lines: 207–207.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### K0127 — `/candidate/reference-semantics/semantics/builtins.k:208`

- Kind: `rule`; attributes: `none`; lines: 208–208.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### K0128 — `/candidate/reference-semantics/semantics/builtins.k:209`

- Kind: `rule`; attributes: `none`; lines: 209–209.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### K0129 — `/candidate/reference-semantics/semantics/builtins.k:210`

- Kind: `rule`; attributes: `none`; lines: 210–210.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### K0130 — `/candidate/reference-semantics/semantics/builtins.k:211`

- Kind: `rule`; attributes: `none`; lines: 211–211.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### K0131 — `/candidate/reference-semantics/semantics/builtins.k:212`

- Kind: `rule`; attributes: `none`; lines: 212–212.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### K0132 — `/candidate/reference-semantics/semantics/builtins.k:214`

- Kind: `syntax`; attributes: `function, total`; lines: 214–215.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### K0133 — `/candidate/reference-semantics/semantics/builtins.k:216`

- Kind: `rule`; attributes: `none`; lines: 216–216.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### K0134 — `/candidate/reference-semantics/semantics/builtins.k:217`

- Kind: `rule`; attributes: `none`; lines: 217–217.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### K0135 — `/candidate/reference-semantics/semantics/builtins.k:218`

- Kind: `rule`; attributes: `none`; lines: 218–218.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### K0136 — `/candidate/reference-semantics/semantics/builtins.k:219`

- Kind: `rule`; attributes: `none`; lines: 219–220.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### K0137 — `/candidate/reference-semantics/semantics/builtins.k:221`

- Kind: `rule`; attributes: `none`; lines: 221–222.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### K0138 — `/candidate/reference-semantics/semantics/builtins.k:223`

- Kind: `rule`; attributes: `owise`; lines: 223–223.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### K0139 — `/candidate/reference-semantics/semantics/builtins.k:225`

- Kind: `syntax`; attributes: `none`; lines: 225–225.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### K0140 — `/candidate/reference-semantics/semantics/builtins.k:226`

- Kind: `syntax`; attributes: `function, total`; lines: 226–226.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### K0141 — `/candidate/reference-semantics/semantics/builtins.k:227`

- Kind: `rule`; attributes: `none`; lines: 227–227.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### K0142 — `/candidate/reference-semantics/semantics/builtins.k:228`

- Kind: `rule`; attributes: `owise`; lines: 228–228.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### K0143 — `/candidate/reference-semantics/semantics/builtins.k:230`

- Kind: `syntax`; attributes: `function, total`; lines: 230–230.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### K0144 — `/candidate/reference-semantics/semantics/builtins.k:231`

- Kind: `rule`; attributes: `none`; lines: 231–231.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### K0145 — `/candidate/reference-semantics/semantics/builtins.k:232`

- Kind: `rule`; attributes: `none`; lines: 232–232.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### K0146 — `/candidate/reference-semantics/semantics/builtins.k:233`

- Kind: `rule`; attributes: `none`; lines: 233–233.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### K0147 — `/candidate/reference-semantics/semantics/builtins.k:234`

- Kind: `rule`; attributes: `none`; lines: 234–234.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### K0148 — `/candidate/reference-semantics/semantics/builtins.k:235`

- Kind: `rule`; attributes: `none`; lines: 235–235.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### K0149 — `/candidate/reference-semantics/semantics/builtins.k:236`

- Kind: `rule`; attributes: `owise`; lines: 236–236.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### K0150 — `/candidate/reference-semantics/semantics/builtins.k:238`

- Kind: `syntax`; attributes: `function, total`; lines: 238–238.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### K0151 — `/candidate/reference-semantics/semantics/builtins.k:239`

- Kind: `rule`; attributes: `none`; lines: 239–239.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### K0152 — `/candidate/reference-semantics/semantics/builtins.k:240`

- Kind: `rule`; attributes: `none`; lines: 240–240.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### K0153 — `/candidate/reference-semantics/semantics/builtins.k:241`

- Kind: `rule`; attributes: `none`; lines: 241–242.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### K0154 — `/candidate/reference-semantics/semantics/builtins.k:243`

- Kind: `rule`; attributes: `owise`; lines: 243–243.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### K0155 — `/candidate/reference-semantics/semantics/builtins.k:244`

- Kind: `syntax`; attributes: `function, total`; lines: 244–244.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### K0156 — `/candidate/reference-semantics/semantics/builtins.k:245`

- Kind: `rule`; attributes: `none`; lines: 245–245.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### K0157 — `/candidate/reference-semantics/semantics/builtins.k:246`

- Kind: `rule`; attributes: `none`; lines: 246–246.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### K0158 — `/candidate/reference-semantics/semantics/builtins.k:247`

- Kind: `syntax`; attributes: `function, total`; lines: 247–247.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### K0159 — `/candidate/reference-semantics/semantics/builtins.k:248`

- Kind: `rule`; attributes: `none`; lines: 248–248.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### K0160 — `/candidate/reference-semantics/semantics/builtins.k:250`

- Kind: `syntax`; attributes: `function, total`; lines: 250–250.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### K0161 — `/candidate/reference-semantics/semantics/builtins.k:251`

- Kind: `rule`; attributes: `none`; lines: 251–251.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K0162 — `/candidate/reference-semantics/semantics/builtins.k:252`

- Kind: `rule`; attributes: `none`; lines: 252–252.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K0163 — `/candidate/reference-semantics/semantics/builtins.k:253`

- Kind: `rule`; attributes: `none`; lines: 253–253.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### K0164 — `/candidate/reference-semantics/semantics/builtins.k:254`

- Kind: `rule`; attributes: `none`; lines: 254–254.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### K0165 — `/candidate/reference-semantics/semantics/builtins.k:255`

- Kind: `syntax`; attributes: `function, total`; lines: 255–255.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### K0166 — `/candidate/reference-semantics/semantics/builtins.k:256`

- Kind: `rule`; attributes: `none`; lines: 256–256.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### K0167 — `/candidate/reference-semantics/semantics/builtins.k:257`

- Kind: `rule`; attributes: `none`; lines: 257–259.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### K0168 — `/candidate/reference-semantics/semantics/builtins.k:260`

- Kind: `rule`; attributes: `none`; lines: 260–262.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### K0169 — `/candidate/reference-semantics/semantics/builtins.k:263`

- Kind: `rule`; attributes: `owise`; lines: 263–264.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### K0170 — `/candidate/reference-semantics/semantics/builtins.k:265`

- Kind: `syntax`; attributes: `function, total`; lines: 265–265.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### K0171 — `/candidate/reference-semantics/semantics/builtins.k:266`

- Kind: `rule`; attributes: `none`; lines: 266–266.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### K0172 — `/candidate/reference-semantics/semantics/builtins.k:267`

- Kind: `rule`; attributes: `none`; lines: 267–267.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### K0173 — `/candidate/reference-semantics/semantics/builtins.k:268`

- Kind: `rule`; attributes: `owise`; lines: 268–268.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### K0174 — `/candidate/reference-semantics/semantics/builtins.k:269`

- Kind: `syntax`; attributes: `function, total`; lines: 269–269.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### K0175 — `/candidate/reference-semantics/semantics/builtins.k:270`

- Kind: `rule`; attributes: `none`; lines: 270–270.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### K0176 — `/candidate/reference-semantics/semantics/builtins.k:271`

- Kind: `rule`; attributes: `none`; lines: 271–271.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### K0177 — `/candidate/reference-semantics/semantics/builtins.k:272`

- Kind: `syntax`; attributes: `function, total`; lines: 272–272.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### K0178 — `/candidate/reference-semantics/semantics/builtins.k:273`

- Kind: `rule`; attributes: `none`; lines: 273–273.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### K0179 — `/candidate/reference-semantics/semantics/builtins.k:274`

- Kind: `rule`; attributes: `none`; lines: 274–274.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### K0180 — `/candidate/reference-semantics/semantics/builtins.k:279`

- Kind: `syntax`; attributes: `none`; lines: 279–279.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= "#md5"
```

### K0181 — `/candidate/reference-semantics/semantics/builtins.k:280`

- Kind: `rule`; attributes: `priority`; lines: 280–281.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### K0182 — `/candidate/reference-semantics/semantics/builtins.k:282`

- Kind: `rule`; attributes: `none`; lines: 282–282.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### K0183 — `/candidate/reference-semantics/semantics/builtins.k:283`

- Kind: `syntax`; attributes: `none`; lines: 283–283.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= md5Obj(IntSeq)
```

### K0184 — `/candidate/reference-semantics/semantics/builtins.k:284`

- Kind: `rule`; attributes: `none`; lines: 284–284.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### K0185 — `/candidate/reference-semantics/semantics/builtins.k:285`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 285–285.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### K0186 — `/candidate/reference-semantics/semantics/builtins.k:291`

- Kind: `rule`; attributes: `none`; lines: 291–291.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### K0187 — `/candidate/reference-semantics/semantics/builtins.k:292`

- Kind: `rule`; attributes: `none`; lines: 292–292.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### K0188 — `/candidate/reference-semantics/semantics/builtins.k:293`

- Kind: `syntax`; attributes: `function`; lines: 293–293.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### K0189 — `/candidate/reference-semantics/semantics/builtins.k:294`

- Kind: `rule`; attributes: `none`; lines: 294–294.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isIntV(_:Int)         => true
```

### K0190 — `/candidate/reference-semantics/semantics/builtins.k:295`

- Kind: `rule`; attributes: `owise`; lines: 295–295.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isIntV(_:Val)         => false [owise]
```

### K0191 — `/candidate/reference-semantics/semantics/builtins.k:296`

- Kind: `rule`; attributes: `none`; lines: 296–296.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isStrV(str(_:IntSeq)) => true
```

### K0192 — `/candidate/reference-semantics/semantics/builtins.k:297`

- Kind: `rule`; attributes: `owise`; lines: 297–297.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isStrV(_:Val)         => false [owise]
```

### K0193 — `/candidate/reference-semantics/semantics/call.k:16`

- Kind: `rule`; attributes: `none`; lines: 16–16.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### K0194 — `/candidate/reference-semantics/semantics/call.k:19`

- Kind: `syntax`; attributes: `none`; lines: 19–19.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax KItem ::= #callee(Exprs)
```

### K0195 — `/candidate/reference-semantics/semantics/call.k:20`

- Kind: `rule`; attributes: `owise`; lines: 20–20.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### K0196 — `/candidate/reference-semantics/semantics/call.k:21`

- Kind: `rule`; attributes: `none`; lines: 21–21.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### K0197 — `/candidate/reference-semantics/semantics/call.k:24`

- Kind: `rule`; attributes: `none`; lines: 24–24.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### K0198 — `/candidate/reference-semantics/semantics/call.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### K0199 — `/candidate/reference-semantics/semantics/call.k:27`

- Kind: `rule`; attributes: `none`; lines: 27–27.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### K0200 — `/candidate/reference-semantics/semantics/call.k:28`

- Kind: `rule`; attributes: `none`; lines: 28–28.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### K0201 — `/candidate/reference-semantics/semantics/call.k:29`

- Kind: `rule`; attributes: `none`; lines: 29–29.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### K0202 — `/candidate/reference-semantics/semantics/call.k:30`

- Kind: `rule`; attributes: `none`; lines: 30–30.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### K0203 — `/candidate/reference-semantics/semantics/call.k:31`

- Kind: `rule`; attributes: `owise`; lines: 31–31.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### K0204 — `/candidate/reference-semantics/semantics/call.k:32`

- Kind: `rule`; attributes: `none`; lines: 32–32.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### K0205 — `/candidate/reference-semantics/semantics/call.k:38`

- Kind: `rule`; attributes: `priority`; lines: 38–41.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0206 — `/candidate/reference-semantics/semantics/call.k:42`

- Kind: `rule`; attributes: `priority`; lines: 42–46.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### K0207 — `/candidate/reference-semantics/semantics/call.k:47`

- Kind: `rule`; attributes: `priority`; lines: 47–50.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0208 — `/candidate/reference-semantics/semantics/call.k:52`

- Kind: `syntax`; attributes: `function, total`; lines: 52–52.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### K0209 — `/candidate/reference-semantics/semantics/call.k:53`

- Kind: `rule`; attributes: `none`; lines: 53–55.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### K0210 — `/candidate/reference-semantics/semantics/call.k:56`

- Kind: `rule`; attributes: `priority`; lines: 56–60.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

### K0211 — `/candidate/reference-semantics/semantics/call.k:63`

- Kind: `rule`; attributes: `priority`; lines: 63–67.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### K0212 — `/candidate/reference-semantics/semantics/call.k:69`

- Kind: `rule`; attributes: `none`; lines: 69–74.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K0213 — `/candidate/reference-semantics/semantics/call.k:80`

- Kind: `rule`; attributes: `none`; lines: 80–85.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### K0214 — `/candidate/reference-semantics/semantics/call.k:87`

- Kind: `syntax`; attributes: `none`; lines: 87–87.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### K0215 — `/candidate/reference-semantics/semantics/call.k:88`

- Kind: `rule`; attributes: `none`; lines: 88–88.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### K0216 — `/candidate/reference-semantics/semantics/call.k:89`

- Kind: `rule`; attributes: `none`; lines: 89–94.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K0217 — `/candidate/reference-semantics/semantics/comprehension.k:11`

- Kind: `rule`; attributes: `none`; lines: 11–11.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K0218 — `/candidate/reference-semantics/semantics/comprehension.k:12`

- Kind: `rule`; attributes: `none`; lines: 12–12.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### K0219 — `/candidate/reference-semantics/semantics/comprehension.k:14`

- Kind: `syntax`; attributes: `macro`; lines: 14–14.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### K0220 — `/candidate/reference-semantics/semantics/comprehension.k:15`

- Kind: `rule`; attributes: `none`; lines: 15–16.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### K0221 — `/candidate/reference-semantics/semantics/comprehension.k:18`

- Kind: `syntax`; attributes: `macro, macro-rec`; lines: 18–18.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### K0222 — `/candidate/reference-semantics/semantics/comprehension.k:19`

- Kind: `rule`; attributes: `none`; lines: 19–20.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### K0223 — `/candidate/reference-semantics/semantics/comprehension.k:21`

- Kind: `rule`; attributes: `none`; lines: 21–22.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### K0224 — `/candidate/reference-semantics/semantics/comprehension.k:24`

- Kind: `syntax`; attributes: `macro`; lines: 24–24.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### K0225 — `/candidate/reference-semantics/semantics/comprehension.k:25`

- Kind: `rule`; attributes: `none`; lines: 25–25.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### K0226 — `/candidate/reference-semantics/semantics/comprehension.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### K0227 — `/candidate/reference-semantics/semantics/concrete.k:13`

- Kind: `rule`; attributes: `none`; lines: 13–15.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K0228 — `/candidate/reference-semantics/semantics/concrete.k:16`

- Kind: `rule`; attributes: `none`; lines: 16–18.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### K0229 — `/candidate/reference-semantics/semantics/concrete.k:25`

- Kind: `syntax`; attributes: `none`; lines: 25–25.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  syntax Val ::= kvP(Val, Val)
```

### K0230 — `/candidate/reference-semantics/semantics/concrete.k:26`

- Kind: `syntax`; attributes: `none`; lines: 26–27.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### K0231 — `/candidate/reference-semantics/semantics/concrete.k:28`

- Kind: `rule`; attributes: `priority`; lines: 28–30.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### K0232 — `/candidate/reference-semantics/semantics/concrete.k:31`

- Kind: `rule`; attributes: `priority`; lines: 31–33.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### K0233 — `/candidate/reference-semantics/semantics/concrete.k:34`

- Kind: `rule`; attributes: `none`; lines: 34–35.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### K0234 — `/candidate/reference-semantics/semantics/concrete.k:36`

- Kind: `rule`; attributes: `none`; lines: 36–37.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### K0235 — `/candidate/reference-semantics/semantics/concrete.k:38`

- Kind: `rule`; attributes: `none`; lines: 38–40.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### K0236 — `/candidate/reference-semantics/semantics/concrete.k:42`

- Kind: `syntax`; attributes: `function`; lines: 42–42.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### K0237 — `/candidate/reference-semantics/semantics/concrete.k:43`

- Kind: `rule`; attributes: `none`; lines: 43–43.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### K0238 — `/candidate/reference-semantics/semantics/concrete.k:44`

- Kind: `rule`; attributes: `none`; lines: 44–46.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### K0239 — `/candidate/reference-semantics/semantics/concrete.k:47`

- Kind: `rule`; attributes: `none`; lines: 47–49.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### K0240 — `/candidate/reference-semantics/semantics/concrete.k:51`

- Kind: `syntax`; attributes: `function`; lines: 51–51.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### K0241 — `/candidate/reference-semantics/semantics/concrete.k:52`

- Kind: `rule`; attributes: `none`; lines: 52–52.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### K0242 — `/candidate/reference-semantics/semantics/concrete.k:53`

- Kind: `rule`; attributes: `none`; lines: 53–53.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### K0243 — `/candidate/reference-semantics/semantics/concrete.k:54`

- Kind: `rule`; attributes: `none`; lines: 54–54.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K0244 — `/candidate/reference-semantics/semantics/concrete.k:56`

- Kind: `syntax`; attributes: `function, total`; lines: 56–56.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### K0245 — `/candidate/reference-semantics/semantics/concrete.k:57`

- Kind: `rule`; attributes: `none`; lines: 57–57.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### K0246 — `/candidate/reference-semantics/semantics/concrete.k:58`

- Kind: `rule`; attributes: `none`; lines: 58–58.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### K0247 — `/candidate/reference-semantics/semantics/concrete.k:59`

- Kind: `rule`; attributes: `owise`; lines: 59–59.
- Decision: CONCRETE_ONLY: excluded from the Haskell proof module MPY.

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### K0248 — `/candidate/reference-semantics/semantics/controls.k:9`

- Kind: `rule`; attributes: `none`; lines: 9–11.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K0249 — `/candidate/reference-semantics/semantics/controls.k:12`

- Kind: `rule`; attributes: `priority`; lines: 12–18.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K0250 — `/candidate/reference-semantics/semantics/controls.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–23.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

### K0251 — `/candidate/reference-semantics/semantics/controls.k:27`

- Kind: `rule`; attributes: `priority`; lines: 27–31.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

### K0252 — `/candidate/reference-semantics/semantics/controls.k:35`

- Kind: `rule`; attributes: `none`; lines: 35–35.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### K0253 — `/candidate/reference-semantics/semantics/controls.k:36`

- Kind: `rule`; attributes: `owise`; lines: 36–36.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### K0254 — `/candidate/reference-semantics/semantics/controls.k:37`

- Kind: `syntax`; attributes: `none`; lines: 37–37.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### K0255 — `/candidate/reference-semantics/semantics/controls.k:38`

- Kind: `rule`; attributes: `none`; lines: 38–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### K0256 — `/candidate/reference-semantics/semantics/controls.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–42.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### K0257 — `/candidate/reference-semantics/semantics/controls.k:43`

- Kind: `rule`; attributes: `none`; lines: 43–44.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### K0258 — `/candidate/reference-semantics/semantics/controls.k:48`

- Kind: `rule`; attributes: `none`; lines: 48–48.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### K0259 — `/candidate/reference-semantics/semantics/controls.k:51`

- Kind: `syntax`; attributes: `none`; lines: 51–51.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### K0260 — `/candidate/reference-semantics/semantics/controls.k:52`

- Kind: `rule`; attributes: `none`; lines: 52–52.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### K0261 — `/candidate/reference-semantics/semantics/controls.k:53`

- Kind: `rule`; attributes: `none`; lines: 53–53.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### K0262 — `/candidate/reference-semantics/semantics/controls.k:54`

- Kind: `rule`; attributes: `none`; lines: 54–54.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### K0263 — `/candidate/reference-semantics/semantics/controls.k:57`

- Kind: `rule`; attributes: `none`; lines: 57–58.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### K0264 — `/candidate/reference-semantics/semantics/controls.k:59`

- Kind: `rule`; attributes: `none`; lines: 59–60.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

### K0265 — `/candidate/reference-semantics/semantics/controls.k:65`

- Kind: `syntax`; attributes: `none`; lines: 65–67.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### K0266 — `/candidate/reference-semantics/semantics/controls.k:69`

- Kind: `rule`; attributes: `none`; lines: 69–69.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### K0267 — `/candidate/reference-semantics/semantics/controls.k:71`

- Kind: `rule`; attributes: `none`; lines: 71–71.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### K0268 — `/candidate/reference-semantics/semantics/controls.k:72`

- Kind: `rule`; attributes: `none`; lines: 72–72.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### K0269 — `/candidate/reference-semantics/semantics/controls.k:73`

- Kind: `rule`; attributes: `none`; lines: 73–74.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### K0270 — `/candidate/reference-semantics/semantics/controls.k:77`

- Kind: `rule`; attributes: `none`; lines: 77–77.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### K0271 — `/candidate/reference-semantics/semantics/controls.k:78`

- Kind: `rule`; attributes: `none`; lines: 78–78.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### K0272 — `/candidate/reference-semantics/semantics/controls.k:79`

- Kind: `rule`; attributes: `none`; lines: 79–80.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### K0273 — `/candidate/reference-semantics/semantics/controls.k:81`

- Kind: `rule`; attributes: `none`; lines: 81–82.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

### K0274 — `/candidate/reference-semantics/semantics/controls.k:85`

- Kind: `rule`; attributes: `none`; lines: 85–85.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K0275 — `/candidate/reference-semantics/semantics/controls.k:86`

- Kind: `rule`; attributes: `none`; lines: 86–86.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Continue => #cont ... </k>
```

### K0276 — `/candidate/reference-semantics/semantics/controls.k:87`

- Kind: `rule`; attributes: `none`; lines: 87–87.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Break => #brk ... </k>
```

### K0277 — `/candidate/reference-semantics/semantics/controls.k:88`

- Kind: `rule`; attributes: `none`; lines: 88–88.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### K0278 — `/candidate/reference-semantics/semantics/controls.k:89`

- Kind: `rule`; attributes: `owise`; lines: 89–89.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### K0279 — `/candidate/reference-semantics/semantics/controls.k:90`

- Kind: `rule`; attributes: `none`; lines: 90–90.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### K0280 — `/candidate/reference-semantics/semantics/controls.k:91`

- Kind: `rule`; attributes: `owise`; lines: 91–91.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### K0281 — `/candidate/reference-semantics/semantics/controls.k:95`

- Kind: `rule`; attributes: `priority`; lines: 95–97.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0282 — `/candidate/reference-semantics/semantics/controls.k:98`

- Kind: `rule`; attributes: `priority`; lines: 98–100.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0283 — `/candidate/reference-semantics/semantics/controls.k:101`

- Kind: `rule`; attributes: `priority`; lines: 101–103.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0284 — `/candidate/reference-semantics/semantics/controls.k:106`

- Kind: `rule`; attributes: `priority`; lines: 106–108.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0285 — `/candidate/reference-semantics/semantics/core.k:13`

- Kind: `syntax`; attributes: `none`; lines: 13–13.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### K0286 — `/candidate/reference-semantics/semantics/core.k:14`

- Kind: `syntax`; attributes: `none`; lines: 14–14.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### K0287 — `/candidate/reference-semantics/semantics/core.k:15`

- Kind: `syntax`; attributes: `none`; lines: 15–15.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Str    ::= str(IntSeq)
```

### K0288 — `/candidate/reference-semantics/semantics/core.k:18`

- Kind: `syntax`; attributes: `none`; lines: 18–23.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### K0289 — `/candidate/reference-semantics/semantics/core.k:25`

- Kind: `syntax`; attributes: `function`; lines: 25–34.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

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

### K0290 — `/candidate/reference-semantics/semantics/core.k:36`

- Kind: `syntax`; attributes: `none`; lines: 36–36.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Parent   ::= "root" | parent(Int)
```

### K0291 — `/candidate/reference-semantics/semantics/core.k:37`

- Kind: `syntax`; attributes: `none`; lines: 37–37.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Scope    ::= scope(Map, Parent)
```

### K0292 — `/candidate/reference-semantics/semantics/core.k:38`

- Kind: `syntax`; attributes: `none`; lines: 38–38.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KResult  ::= Val
```

### K0293 — `/candidate/reference-semantics/semantics/core.k:39`

- Kind: `syntax`; attributes: `none`; lines: 39–39.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### K0294 — `/candidate/reference-semantics/semantics/core.k:40`

- Kind: `syntax`; attributes: `none`; lines: 40–40.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Vals     ::= List{Val, ","}
```

### K0295 — `/candidate/reference-semantics/semantics/core.k:41`

- Kind: `syntax`; attributes: `none`; lines: 41–41.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### K0296 — `/candidate/reference-semantics/semantics/core.k:42`

- Kind: `syntax`; attributes: `none`; lines: 42–42.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### K0297 — `/candidate/reference-semantics/semantics/core.k:49`

- Kind: `configuration`; attributes: `none`; lines: 49–60.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

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

### K0298 — `/candidate/reference-semantics/semantics/core.k:68`

- Kind: `syntax`; attributes: `function, total`; lines: 68–68.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### K0299 — `/candidate/reference-semantics/semantics/core.k:69`

- Kind: `rule`; attributes: `none`; lines: 69–69.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isRefV(ref(_:Int)) => true
```

### K0300 — `/candidate/reference-semantics/semantics/core.k:70`

- Kind: `rule`; attributes: `owise`; lines: 70–70.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isRefV(_:Val)      => false [owise]
```

### K0301 — `/candidate/reference-semantics/semantics/core.k:75`

- Kind: `syntax`; attributes: `none`; lines: 75–75.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax HeapVal ::= cellV(Val)
```

### K0302 — `/candidate/reference-semantics/semantics/core.k:76`

- Kind: `syntax`; attributes: `function, total`; lines: 76–76.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### K0303 — `/candidate/reference-semantics/semantics/core.k:77`

- Kind: `rule`; attributes: `none`; lines: 77–77.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### K0304 — `/candidate/reference-semantics/semantics/core.k:78`

- Kind: `rule`; attributes: `owise`; lines: 78–78.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isCellRef(_:Val)          => false [owise]
```

### K0305 — `/candidate/reference-semantics/semantics/core.k:85`

- Kind: `rule`; attributes: `priority`; lines: 85–90.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

### K0306 — `/candidate/reference-semantics/semantics/core.k:95`

- Kind: `syntax`; attributes: `none`; lines: 95–95.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= kwV(String, Val)
```

### K0307 — `/candidate/reference-semantics/semantics/core.k:96`

- Kind: `syntax`; attributes: `none`; lines: 96–96.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #kwTag(String)
```

### K0308 — `/candidate/reference-semantics/semantics/core.k:97`

- Kind: `rule`; attributes: `none`; lines: 97–97.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### K0309 — `/candidate/reference-semantics/semantics/core.k:98`

- Kind: `rule`; attributes: `none`; lines: 98–99.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### K0310 — `/candidate/reference-semantics/semantics/core.k:100`

- Kind: `syntax`; attributes: `function, total`; lines: 100–100.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### K0311 — `/candidate/reference-semantics/semantics/core.k:101`

- Kind: `rule`; attributes: `none`; lines: 101–101.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### K0312 — `/candidate/reference-semantics/semantics/core.k:102`

- Kind: `rule`; attributes: `owise`; lines: 102–102.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isKwV(_:Val)                => false [owise]
```

### K0313 — `/candidate/reference-semantics/semantics/core.k:106`

- Kind: `syntax`; attributes: `none`; lines: 106–106.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= cellsMark(ParamNames)
```

### K0314 — `/candidate/reference-semantics/semantics/core.k:107`

- Kind: `syntax`; attributes: `function`; lines: 107–107.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### K0315 — `/candidate/reference-semantics/semantics/core.k:108`

- Kind: `rule`; attributes: `none`; lines: 108–108.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### K0316 — `/candidate/reference-semantics/semantics/core.k:109`

- Kind: `syntax`; attributes: `function, total`; lines: 109–109.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### K0317 — `/candidate/reference-semantics/semantics/core.k:110`

- Kind: `rule`; attributes: `none`; lines: 110–110.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule pnMember(_:String, .ParamNames) => false
```

### K0318 — `/candidate/reference-semantics/semantics/core.k:111`

- Kind: `rule`; attributes: `none`; lines: 111–111.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### K0319 — `/candidate/reference-semantics/semantics/core.k:113`

- Kind: `syntax`; attributes: `none`; lines: 113–113.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #cellW(Val, Val)
```

### K0320 — `/candidate/reference-semantics/semantics/core.k:114`

- Kind: `rule`; attributes: `none`; lines: 114–115.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### K0321 — `/candidate/reference-semantics/semantics/core.k:117`

- Kind: `syntax`; attributes: `none`; lines: 117–117.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax KItem ::= #alloc(Val)
```

### K0322 — `/candidate/reference-semantics/semantics/core.k:118`

- Kind: `rule`; attributes: `none`; lines: 118–121.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### K0323 — `/candidate/reference-semantics/semantics/core.k:124`

- Kind: `syntax`; attributes: `none`; lines: 124–124.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax KItem ::= #loadAll(Module)
```

### K0324 — `/candidate/reference-semantics/semantics/core.k:125`

- Kind: `rule`; attributes: `none`; lines: 125–125.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### K0325 — `/candidate/reference-semantics/semantics/core.k:126`

- Kind: `rule`; attributes: `none`; lines: 126–126.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### K0326 — `/candidate/reference-semantics/semantics/core.k:127`

- Kind: `rule`; attributes: `none`; lines: 127–127.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> .Stmts => .K ... </k>
```

### K0327 — `/candidate/reference-semantics/semantics/core.k:130`

- Kind: `syntax`; attributes: `none`; lines: 130–130.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax KItem ::= #look(String, Int)
```

### K0328 — `/candidate/reference-semantics/semantics/core.k:131`

- Kind: `rule`; attributes: `none`; lines: 131–131.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### K0329 — `/candidate/reference-semantics/semantics/core.k:132`

- Kind: `rule`; attributes: `none`; lines: 132–134.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

### K0330 — `/candidate/reference-semantics/semantics/core.k:145`

- Kind: `rule`; attributes: `priority`; lines: 145–151.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### K0331 — `/candidate/reference-semantics/semantics/core.k:152`

- Kind: `rule`; attributes: `none`; lines: 152–154.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

### K0332 — `/candidate/reference-semantics/semantics/core.k:157`

- Kind: `syntax`; attributes: `function, total`; lines: 157–157.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### K0333 — `/candidate/reference-semantics/semantics/core.k:158`

- Kind: `rule`; attributes: `none`; lines: 158–181.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

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

### K0334 — `/candidate/reference-semantics/semantics/core.k:185`

- Kind: `syntax`; attributes: `none`; lines: 185–185.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax ApplyK ::= toCall(Val)
```

### K0335 — `/candidate/reference-semantics/semantics/core.k:186`

- Kind: `syntax`; attributes: `none`; lines: 186–188.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### K0336 — `/candidate/reference-semantics/semantics/core.k:189`

- Kind: `rule`; attributes: `none`; lines: 189–189.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### K0337 — `/candidate/reference-semantics/semantics/core.k:190`

- Kind: `rule`; attributes: `none`; lines: 190–190.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### K0338 — `/candidate/reference-semantics/semantics/core.k:191`

- Kind: `rule`; attributes: `none`; lines: 191–191.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### K0339 — `/candidate/reference-semantics/semantics/core.k:194`

- Kind: `rule`; attributes: `none`; lines: 194–194.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### K0340 — `/candidate/reference-semantics/semantics/core.k:195`

- Kind: `rule`; attributes: `none`; lines: 195–195.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### K0341 — `/candidate/reference-semantics/semantics/core.k:196`

- Kind: `rule`; attributes: `none`; lines: 196–196.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> NoneVal      => noneV ... </k>
```

### K0342 — `/candidate/reference-semantics/semantics/core.k:199`

- Kind: `syntax`; attributes: `function`; lines: 199–199.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= truthy(Val) [function]
```

### K0343 — `/candidate/reference-semantics/semantics/core.k:200`

- Kind: `rule`; attributes: `none`; lines: 200–200.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule truthy(B:Bool)          => B
```

### K0344 — `/candidate/reference-semantics/semantics/core.k:201`

- Kind: `rule`; attributes: `none`; lines: 201–201.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule truthy(noneV)           => false
```

### K0345 — `/candidate/reference-semantics/semantics/core.k:202`

- Kind: `rule`; attributes: `none`; lines: 202–202.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### K0346 — `/candidate/reference-semantics/semantics/core.k:203`

- Kind: `rule`; attributes: `none`; lines: 203–203.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### K0347 — `/candidate/reference-semantics/semantics/core.k:204`

- Kind: `rule`; attributes: `none`; lines: 204–204.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### K0348 — `/candidate/reference-semantics/semantics/core.k:205`

- Kind: `rule`; attributes: `none`; lines: 205–205.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### K0349 — `/candidate/reference-semantics/semantics/core.k:208`

- Kind: `syntax`; attributes: `function`; lines: 208–208.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### K0350 — `/candidate/reference-semantics/semantics/core.k:209`

- Kind: `syntax`; attributes: `function`; lines: 209–209.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### K0351 — `/candidate/reference-semantics/semantics/core.k:210`

- Kind: `syntax`; attributes: `function`; lines: 210–210.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### K0352 — `/candidate/reference-semantics/semantics/core.k:213`

- Kind: `syntax`; attributes: `function, total`; lines: 213–213.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### K0353 — `/candidate/reference-semantics/semantics/core.k:214`

- Kind: `rule`; attributes: `none`; lines: 214–214.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### K0354 — `/candidate/reference-semantics/semantics/core.k:215`

- Kind: `rule`; attributes: `none`; lines: 215–215.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### K0355 — `/candidate/reference-semantics/semantics/core.k:217`

- Kind: `syntax`; attributes: `function, total`; lines: 217–217.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### K0356 — `/candidate/reference-semantics/semantics/core.k:218`

- Kind: `rule`; attributes: `none`; lines: 218–218.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### K0357 — `/candidate/reference-semantics/semantics/core.k:219`

- Kind: `rule`; attributes: `none`; lines: 219–219.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### K0358 — `/candidate/reference-semantics/semantics/core.k:223`

- Kind: `syntax`; attributes: `function, total`; lines: 223–223.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### K0359 — `/candidate/reference-semantics/semantics/core.k:224`

- Kind: `rule`; attributes: `none`; lines: 224–224.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule vsLen(.ValSeq)                => 0
```

### K0360 — `/candidate/reference-semantics/semantics/core.k:225`

- Kind: `rule`; attributes: `none`; lines: 225–225.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### K0361 — `/candidate/reference-semantics/semantics/core.k:227`

- Kind: `syntax`; attributes: `function, total`; lines: 227–227.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### K0362 — `/candidate/reference-semantics/semantics/core.k:228`

- Kind: `rule`; attributes: `none`; lines: 228–228.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isLen(.IntSeq)                => 0
```

### K0363 — `/candidate/reference-semantics/semantics/core.k:229`

- Kind: `rule`; attributes: `none`; lines: 229–229.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### K0364 — `/candidate/reference-semantics/semantics/core.k:233`

- Kind: `syntax`; attributes: `function, total`; lines: 233–233.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### K0365 — `/candidate/reference-semantics/semantics/core.k:234`

- Kind: `rule`; attributes: `none`; lines: 234–234.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### K0366 — `/candidate/reference-semantics/semantics/core.k:235`

- Kind: `rule`; attributes: `none`; lines: 235–235.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### K0367 — `/candidate/reference-semantics/semantics/core.k:236`

- Kind: `rule`; attributes: `none`; lines: 236–237.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### K0368 — `/candidate/reference-semantics/semantics/core.k:238`

- Kind: `rule`; attributes: `none`; lines: 238–239.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### K0369 — `/candidate/reference-semantics/semantics/dict.k:20`

- Kind: `syntax`; attributes: `none`; lines: 20–20.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### K0370 — `/candidate/reference-semantics/semantics/dict.k:23`

- Kind: `syntax`; attributes: `none`; lines: 23–25.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### K0371 — `/candidate/reference-semantics/semantics/dict.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### K0372 — `/candidate/reference-semantics/semantics/dict.k:27`

- Kind: `rule`; attributes: `none`; lines: 27–27.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### K0373 — `/candidate/reference-semantics/semantics/dict.k:28`

- Kind: `rule`; attributes: `none`; lines: 28–29.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### K0374 — `/candidate/reference-semantics/semantics/dict.k:30`

- Kind: `rule`; attributes: `none`; lines: 30–31.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### K0375 — `/candidate/reference-semantics/semantics/dict.k:32`

- Kind: `rule`; attributes: `none`; lines: 32–33.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### K0376 — `/candidate/reference-semantics/semantics/dict.k:37`

- Kind: `syntax`; attributes: `function, total`; lines: 37–37.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### K0377 — `/candidate/reference-semantics/semantics/dict.k:38`

- Kind: `rule`; attributes: `none`; lines: 38–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### K0378 — `/candidate/reference-semantics/semantics/dict.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–39.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### K0379 — `/candidate/reference-semantics/semantics/dict.k:40`

- Kind: `rule`; attributes: `none`; lines: 40–40.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### K0380 — `/candidate/reference-semantics/semantics/dict.k:43`

- Kind: `syntax`; attributes: `function, total`; lines: 43–43.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### K0381 — `/candidate/reference-semantics/semantics/dict.k:44`

- Kind: `rule`; attributes: `none`; lines: 44–44.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### K0382 — `/candidate/reference-semantics/semantics/dict.k:45`

- Kind: `rule`; attributes: `none`; lines: 45–45.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### K0383 — `/candidate/reference-semantics/semantics/dict.k:49`

- Kind: `syntax`; attributes: `function, total`; lines: 49–49.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### K0384 — `/candidate/reference-semantics/semantics/dict.k:50`

- Kind: `rule`; attributes: `none`; lines: 50–51.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### K0385 — `/candidate/reference-semantics/semantics/dict.k:52`

- Kind: `rule`; attributes: `none`; lines: 52–53.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### K0386 — `/candidate/reference-semantics/semantics/dict.k:54`

- Kind: `rule`; attributes: `owise`; lines: 54–54.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### K0387 — `/candidate/reference-semantics/semantics/dict.k:58`

- Kind: `rule`; attributes: `priority`; lines: 58–60.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### K0388 — `/candidate/reference-semantics/semantics/dict.k:63`

- Kind: `rule`; attributes: `none`; lines: 63–63.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### K0389 — `/candidate/reference-semantics/semantics/dict.k:64`

- Kind: `syntax`; attributes: `function`; lines: 64–64.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### K0390 — `/candidate/reference-semantics/semantics/dict.k:65`

- Kind: `rule`; attributes: `priority`; lines: 65–66.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### K0391 — `/candidate/reference-semantics/semantics/dict.k:70`

- Kind: `syntax`; attributes: `function`; lines: 70–70.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### K0392 — `/candidate/reference-semantics/semantics/dict.k:71`

- Kind: `rule`; attributes: `none`; lines: 71–71.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### K0393 — `/candidate/reference-semantics/semantics/dict.k:76`

- Kind: `syntax`; attributes: `none`; lines: 76–76.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #dsetK(String, Val)
```

### K0394 — `/candidate/reference-semantics/semantics/dict.k:77`

- Kind: `rule`; attributes: `none`; lines: 77–77.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### K0395 — `/candidate/reference-semantics/semantics/dict.k:78`

- Kind: `rule`; attributes: `none`; lines: 78–81.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### K0396 — `/candidate/reference-semantics/semantics/dict.k:82`

- Kind: `rule`; attributes: `none`; lines: 82–85.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### K0397 — `/candidate/reference-semantics/semantics/dict.k:86`

- Kind: `syntax`; attributes: `none`; lines: 86–86.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### K0398 — `/candidate/reference-semantics/semantics/dict.k:87`

- Kind: `rule`; attributes: `none`; lines: 87–88.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### K0399 — `/candidate/reference-semantics/semantics/dict.k:90`

- Kind: `syntax`; attributes: `function, total`; lines: 90–90.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### K0400 — `/candidate/reference-semantics/semantics/dict.k:91`

- Kind: `rule`; attributes: `none`; lines: 91–91.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K0401 — `/candidate/reference-semantics/semantics/dict.k:92`

- Kind: `rule`; attributes: `none`; lines: 92–92.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### K0402 — `/candidate/reference-semantics/semantics/dict.k:95`

- Kind: `rule`; attributes: `none`; lines: 95–96.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### K0403 — `/candidate/reference-semantics/semantics/dict.k:97`

- Kind: `syntax`; attributes: `function`; lines: 97–97.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### K0404 — `/candidate/reference-semantics/semantics/dict.k:98`

- Kind: `rule`; attributes: `none`; lines: 98–98.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### K0405 — `/candidate/reference-semantics/semantics/dict.k:99`

- Kind: `rule`; attributes: `none`; lines: 99–100.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### K0406 — `/candidate/reference-semantics/semantics/dict.k:101`

- Kind: `syntax`; attributes: `function`; lines: 101–101.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### K0407 — `/candidate/reference-semantics/semantics/dict.k:102`

- Kind: `rule`; attributes: `none`; lines: 102–102.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### K0408 — `/candidate/reference-semantics/semantics/dict.k:103`

- Kind: `rule`; attributes: `none`; lines: 103–103.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### K0409 — `/candidate/reference-semantics/semantics/float.k:20`

- Kind: `syntax`; attributes: `none`; lines: 20–20.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= Float
```

### K0410 — `/candidate/reference-semantics/semantics/float.k:21`

- Kind: `rule`; attributes: `none`; lines: 21–21.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Float(F:Float) => F ... </k>
```

### K0411 — `/candidate/reference-semantics/semantics/float.k:24`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 24–24.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### K0412 — `/candidate/reference-semantics/semantics/float.k:25`

- Kind: `rule`; attributes: `concrete`; lines: 25–25.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### K0413 — `/candidate/reference-semantics/semantics/float.k:27`

- Kind: `rule`; attributes: `none`; lines: 27–27.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### K0414 — `/candidate/reference-semantics/semantics/float.k:30`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 30–30.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### K0415 — `/candidate/reference-semantics/semantics/float.k:31`

- Kind: `rule`; attributes: `concrete`; lines: 31–31.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### K0416 — `/candidate/reference-semantics/semantics/float.k:32`

- Kind: `rule`; attributes: `none`; lines: 32–32.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### K0417 — `/candidate/reference-semantics/semantics/float.k:37`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 37–37.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### K0418 — `/candidate/reference-semantics/semantics/float.k:38`

- Kind: `rule`; attributes: `concrete`; lines: 38–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### K0419 — `/candidate/reference-semantics/semantics/float.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–39.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### K0420 — `/candidate/reference-semantics/semantics/float.k:43`

- Kind: `rule`; attributes: `none`; lines: 43–43.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### K0421 — `/candidate/reference-semantics/semantics/float.k:44`

- Kind: `rule`; attributes: `none`; lines: 44–44.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### K0422 — `/candidate/reference-semantics/semantics/float.k:50`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 50–50.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### K0423 — `/candidate/reference-semantics/semantics/float.k:51`

- Kind: `rule`; attributes: `concrete`; lines: 51–51.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### K0424 — `/candidate/reference-semantics/semantics/float.k:52`

- Kind: `rule`; attributes: `none`; lines: 52–52.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### K0425 — `/candidate/reference-semantics/semantics/float.k:54`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 54–54.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### K0426 — `/candidate/reference-semantics/semantics/float.k:55`

- Kind: `rule`; attributes: `concrete`; lines: 55–55.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### K0427 — `/candidate/reference-semantics/semantics/float.k:56`

- Kind: `rule`; attributes: `none`; lines: 56–56.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### K0428 — `/candidate/reference-semantics/semantics/float.k:61`

- Kind: `rule`; attributes: `none`; lines: 61–61.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Import(_:String) => .K ... </k>
```

### K0429 — `/candidate/reference-semantics/semantics/float.k:65`

- Kind: `syntax`; attributes: `none`; lines: 65–65.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= "#mathCeil"
```

### K0430 — `/candidate/reference-semantics/semantics/float.k:66`

- Kind: `rule`; attributes: `priority`; lines: 66–66.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### K0431 — `/candidate/reference-semantics/semantics/float.k:67`

- Kind: `rule`; attributes: `none`; lines: 67–67.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### K0432 — `/candidate/reference-semantics/semantics/float.k:70`

- Kind: `syntax`; attributes: `none`; lines: 70–70.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= "#mathFloor"
```

### K0433 — `/candidate/reference-semantics/semantics/float.k:71`

- Kind: `rule`; attributes: `priority`; lines: 71–71.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### K0434 — `/candidate/reference-semantics/semantics/float.k:72`

- Kind: `rule`; attributes: `none`; lines: 72–72.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### K0435 — `/candidate/reference-semantics/semantics/float.k:73`

- Kind: `syntax`; attributes: `function, total, symbol`; lines: 73–73.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### K0436 — `/candidate/reference-semantics/semantics/float.k:74`

- Kind: `rule`; attributes: `concrete`; lines: 74–74.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### K0437 — `/candidate/reference-semantics/semantics/float.k:75`

- Kind: `rule`; attributes: `concrete`; lines: 75–75.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### K0438 — `/candidate/reference-semantics/semantics/float.k:78`

- Kind: `rule`; attributes: `none`; lines: 78–78.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### K0439 — `/candidate/reference-semantics/semantics/float.k:79`

- Kind: `rule`; attributes: `none`; lines: 79–79.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### K0440 — `/candidate/reference-semantics/semantics/float.k:82`

- Kind: `syntax`; attributes: `none`; lines: 82–82.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### K0441 — `/candidate/reference-semantics/semantics/float.k:83`

- Kind: `rule`; attributes: `priority`; lines: 83–83.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### K0442 — `/candidate/reference-semantics/semantics/float.k:84`

- Kind: `rule`; attributes: `none`; lines: 84–84.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### K0443 — `/candidate/reference-semantics/semantics/float.k:85`

- Kind: `rule`; attributes: `none`; lines: 85–85.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### K0444 — `/candidate/reference-semantics/semantics/float.k:86`

- Kind: `syntax`; attributes: `function, total, symbol`; lines: 86–86.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### K0445 — `/candidate/reference-semantics/semantics/float.k:87`

- Kind: `rule`; attributes: `concrete`; lines: 87–87.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule toF(F:Float) => F        [concrete]
```

### K0446 — `/candidate/reference-semantics/semantics/float.k:88`

- Kind: `rule`; attributes: `concrete`; lines: 88–88.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### K0447 — `/candidate/reference-semantics/semantics/float.k:93`

- Kind: `syntax`; attributes: `function, total, symbol`; lines: 93–93.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### K0448 — `/candidate/reference-semantics/semantics/float.k:94`

- Kind: `rule`; attributes: `concrete`; lines: 94–94.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### K0449 — `/candidate/reference-semantics/semantics/float.k:95`

- Kind: `rule`; attributes: `concrete`; lines: 95–95.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### K0450 — `/candidate/reference-semantics/semantics/float.k:99`

- Kind: `rule`; attributes: `none`; lines: 99–99.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### K0451 — `/candidate/reference-semantics/semantics/float.k:103`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 103–103.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### K0452 — `/candidate/reference-semantics/semantics/float.k:104`

- Kind: `rule`; attributes: `concrete`; lines: 104–104.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### K0453 — `/candidate/reference-semantics/semantics/float.k:105`

- Kind: `rule`; attributes: `none`; lines: 105–105.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### K0454 — `/candidate/reference-semantics/semantics/float.k:107`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 107–107.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### K0455 — `/candidate/reference-semantics/semantics/float.k:108`

- Kind: `rule`; attributes: `concrete`; lines: 108–108.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### K0456 — `/candidate/reference-semantics/semantics/float.k:109`

- Kind: `rule`; attributes: `none`; lines: 109–109.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### K0457 — `/candidate/reference-semantics/semantics/float.k:111`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 111–111.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### K0458 — `/candidate/reference-semantics/semantics/float.k:112`

- Kind: `rule`; attributes: `concrete`; lines: 112–112.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### K0459 — `/candidate/reference-semantics/semantics/float.k:113`

- Kind: `rule`; attributes: `none`; lines: 113–113.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### K0460 — `/candidate/reference-semantics/semantics/float.k:115`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 115–115.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### K0461 — `/candidate/reference-semantics/semantics/float.k:116`

- Kind: `rule`; attributes: `concrete`; lines: 116–116.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### K0462 — `/candidate/reference-semantics/semantics/float.k:117`

- Kind: `rule`; attributes: `none`; lines: 117–117.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### K0463 — `/candidate/reference-semantics/semantics/float.k:119`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 119–119.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### K0464 — `/candidate/reference-semantics/semantics/float.k:120`

- Kind: `rule`; attributes: `concrete`; lines: 120–120.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### K0465 — `/candidate/reference-semantics/semantics/float.k:121`

- Kind: `rule`; attributes: `none`; lines: 121–121.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### K0466 — `/candidate/reference-semantics/semantics/float.k:125`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 125–125.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### K0467 — `/candidate/reference-semantics/semantics/float.k:126`

- Kind: `rule`; attributes: `concrete`; lines: 126–126.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### K0468 — `/candidate/reference-semantics/semantics/float.k:127`

- Kind: `rule`; attributes: `none`; lines: 127–127.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### K0469 — `/candidate/reference-semantics/semantics/float.k:128`

- Kind: `rule`; attributes: `none`; lines: 128–128.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### K0470 — `/candidate/reference-semantics/semantics/float.k:129`

- Kind: `rule`; attributes: `none`; lines: 129–129.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### K0471 — `/candidate/reference-semantics/semantics/float.k:132`

- Kind: `rule`; attributes: `none`; lines: 132–132.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### K0472 — `/candidate/reference-semantics/semantics/float.k:133`

- Kind: `rule`; attributes: `none`; lines: 133–133.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### K0473 — `/candidate/reference-semantics/semantics/float.k:134`

- Kind: `rule`; attributes: `none`; lines: 134–134.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### K0474 — `/candidate/reference-semantics/semantics/float.k:135`

- Kind: `rule`; attributes: `none`; lines: 135–135.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### K0475 — `/candidate/reference-semantics/semantics/float.k:136`

- Kind: `rule`; attributes: `none`; lines: 136–136.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### K0476 — `/candidate/reference-semantics/semantics/float.k:137`

- Kind: `rule`; attributes: `none`; lines: 137–137.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### K0477 — `/candidate/reference-semantics/semantics/float.k:138`

- Kind: `rule`; attributes: `none`; lines: 138–138.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### K0478 — `/candidate/reference-semantics/semantics/float.k:139`

- Kind: `rule`; attributes: `none`; lines: 139–139.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### K0479 — `/candidate/reference-semantics/semantics/float.k:142`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 142–142.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### K0480 — `/candidate/reference-semantics/semantics/float.k:143`

- Kind: `rule`; attributes: `concrete`; lines: 143–143.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### K0481 — `/candidate/reference-semantics/semantics/float.k:144`

- Kind: `rule`; attributes: `none`; lines: 144–144.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### K0482 — `/candidate/reference-semantics/semantics/float.k:145`

- Kind: `rule`; attributes: `none`; lines: 145–145.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### K0483 — `/candidate/reference-semantics/semantics/float.k:146`

- Kind: `rule`; attributes: `none`; lines: 146–146.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### K0484 — `/candidate/reference-semantics/semantics/float.k:147`

- Kind: `rule`; attributes: `none`; lines: 147–147.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### K0485 — `/candidate/reference-semantics/semantics/float.k:148`

- Kind: `rule`; attributes: `none`; lines: 148–148.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### K0486 — `/candidate/reference-semantics/semantics/float.k:149`

- Kind: `rule`; attributes: `none`; lines: 149–149.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### K0487 — `/candidate/reference-semantics/semantics/float.k:150`

- Kind: `rule`; attributes: `none`; lines: 150–150.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### K0488 — `/candidate/reference-semantics/semantics/float.k:151`

- Kind: `rule`; attributes: `none`; lines: 151–151.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### K0489 — `/candidate/reference-semantics/semantics/float.k:154`

- Kind: `rule`; attributes: `none`; lines: 154–154.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### K0490 — `/candidate/reference-semantics/semantics/float.k:155`

- Kind: `rule`; attributes: `none`; lines: 155–155.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### K0491 — `/candidate/reference-semantics/semantics/float.k:160`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 160–160.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### K0492 — `/candidate/reference-semantics/semantics/float.k:161`

- Kind: `rule`; attributes: `concrete`; lines: 161–161.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### K0493 — `/candidate/reference-semantics/semantics/float.k:162`

- Kind: `rule`; attributes: `concrete`; lines: 162–164.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### K0494 — `/candidate/reference-semantics/semantics/float.k:165`

- Kind: `syntax`; attributes: `function`; lines: 165–165.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### K0495 — `/candidate/reference-semantics/semantics/float.k:166`

- Kind: `rule`; attributes: `none`; lines: 166–166.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### K0496 — `/candidate/reference-semantics/semantics/float.k:167`

- Kind: `syntax`; attributes: `function, total`; lines: 167–167.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### K0497 — `/candidate/reference-semantics/semantics/float.k:168`

- Kind: `rule`; attributes: `none`; lines: 168–168.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### K0498 — `/candidate/reference-semantics/semantics/float.k:169`

- Kind: `rule`; attributes: `none`; lines: 169–169.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### K0499 — `/candidate/reference-semantics/semantics/float.k:170`

- Kind: `rule`; attributes: `none`; lines: 170–170.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### K0500 — `/candidate/reference-semantics/semantics/float.k:171`

- Kind: `rule`; attributes: `none`; lines: 171–172.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### K0501 — `/candidate/reference-semantics/semantics/float.k:173`

- Kind: `syntax`; attributes: `function, total`; lines: 173–173.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### K0502 — `/candidate/reference-semantics/semantics/float.k:174`

- Kind: `rule`; attributes: `none`; lines: 174–174.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracPart(.IntSeq) => 0
```

### K0503 — `/candidate/reference-semantics/semantics/float.k:175`

- Kind: `rule`; attributes: `none`; lines: 175–175.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### K0504 — `/candidate/reference-semantics/semantics/float.k:176`

- Kind: `rule`; attributes: `none`; lines: 176–176.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### K0505 — `/candidate/reference-semantics/semantics/float.k:177`

- Kind: `rule`; attributes: `none`; lines: 177–177.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### K0506 — `/candidate/reference-semantics/semantics/float.k:178`

- Kind: `rule`; attributes: `none`; lines: 178–178.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### K0507 — `/candidate/reference-semantics/semantics/float.k:179`

- Kind: `syntax`; attributes: `function, total`; lines: 179–179.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### K0508 — `/candidate/reference-semantics/semantics/float.k:180`

- Kind: `rule`; attributes: `none`; lines: 180–180.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracScale(.IntSeq) => 1
```

### K0509 — `/candidate/reference-semantics/semantics/float.k:181`

- Kind: `rule`; attributes: `none`; lines: 181–181.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### K0510 — `/candidate/reference-semantics/semantics/float.k:182`

- Kind: `rule`; attributes: `none`; lines: 182–182.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### K0511 — `/candidate/reference-semantics/semantics/float.k:183`

- Kind: `rule`; attributes: `none`; lines: 183–183.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### K0512 — `/candidate/reference-semantics/semantics/float.k:184`

- Kind: `rule`; attributes: `none`; lines: 184–184.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### K0513 — `/candidate/reference-semantics/semantics/float.k:185`

- Kind: `rule`; attributes: `none`; lines: 185–185.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### K0514 — `/candidate/reference-semantics/semantics/float.k:186`

- Kind: `rule`; attributes: `none`; lines: 186–186.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### K0515 — `/candidate/reference-semantics/semantics/float.k:187`

- Kind: `rule`; attributes: `none`; lines: 187–187.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### K0516 — `/candidate/reference-semantics/semantics/float.k:190`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 190–190.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### K0517 — `/candidate/reference-semantics/semantics/float.k:191`

- Kind: `rule`; attributes: `concrete`; lines: 191–191.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### K0518 — `/candidate/reference-semantics/semantics/float.k:192`

- Kind: `rule`; attributes: `none`; lines: 192–192.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### K0519 — `/candidate/reference-semantics/semantics/float.k:195`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 195–195.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### K0520 — `/candidate/reference-semantics/semantics/float.k:196`

- Kind: `rule`; attributes: `concrete`; lines: 196–196.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### K0521 — `/candidate/reference-semantics/semantics/float.k:197`

- Kind: `rule`; attributes: `none`; lines: 197–197.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### K0522 — `/candidate/reference-semantics/semantics/float.k:198`

- Kind: `rule`; attributes: `none`; lines: 198–198.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### K0523 — `/candidate/reference-semantics/semantics/float.k:199`

- Kind: `rule`; attributes: `none`; lines: 199–199.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### K0524 — `/candidate/reference-semantics/semantics/float.k:200`

- Kind: `rule`; attributes: `none`; lines: 200–200.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### K0525 — `/candidate/reference-semantics/semantics/float.k:201`

- Kind: `rule`; attributes: `none`; lines: 201–201.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### K0526 — `/candidate/reference-semantics/semantics/float.k:202`

- Kind: `rule`; attributes: `none`; lines: 202–202.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### K0527 — `/candidate/reference-semantics/semantics/float.k:203`

- Kind: `rule`; attributes: `none`; lines: 203–203.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### K0528 — `/candidate/reference-semantics/semantics/float.k:204`

- Kind: `rule`; attributes: `none`; lines: 204–204.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### K0529 — `/candidate/reference-semantics/semantics/float.k:205`

- Kind: `rule`; attributes: `none`; lines: 205–205.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### K0530 — `/candidate/reference-semantics/semantics/float.k:206`

- Kind: `rule`; attributes: `none`; lines: 206–206.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### K0531 — `/candidate/reference-semantics/semantics/float.k:209`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 209–209.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### K0532 — `/candidate/reference-semantics/semantics/float.k:210`

- Kind: `rule`; attributes: `concrete`; lines: 210–210.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### K0533 — `/candidate/reference-semantics/semantics/float.k:211`

- Kind: `rule`; attributes: `none`; lines: 211–211.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### K0534 — `/candidate/reference-semantics/semantics/float.k:213`

- Kind: `rule`; attributes: `none`; lines: 213–213.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### K0535 — `/candidate/reference-semantics/semantics/float.k:214`

- Kind: `rule`; attributes: `none`; lines: 214–214.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### K0536 — `/candidate/reference-semantics/semantics/float.k:217`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 217–217.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### K0537 — `/candidate/reference-semantics/semantics/float.k:218`

- Kind: `rule`; attributes: `concrete`; lines: 218–222.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### K0538 — `/candidate/reference-semantics/semantics/float.k:223`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 223–223.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### K0539 — `/candidate/reference-semantics/semantics/float.k:224`

- Kind: `rule`; attributes: `concrete`; lines: 224–226.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### K0540 — `/candidate/reference-semantics/semantics/float.k:227`

- Kind: `rule`; attributes: `none`; lines: 227–227.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### K0541 — `/candidate/reference-semantics/semantics/float.k:228`

- Kind: `rule`; attributes: `none`; lines: 228–228.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### K0542 — `/candidate/reference-semantics/semantics/float.k:230`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 230–230.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### K0543 — `/candidate/reference-semantics/semantics/float.k:231`

- Kind: `rule`; attributes: `concrete`; lines: 231–231.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### K0544 — `/candidate/reference-semantics/semantics/float.k:232`

- Kind: `syntax`; attributes: `none`; lines: 232–232.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= "#mathSqrt"
```

### K0545 — `/candidate/reference-semantics/semantics/float.k:233`

- Kind: `rule`; attributes: `priority`; lines: 233–233.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### K0546 — `/candidate/reference-semantics/semantics/float.k:234`

- Kind: `rule`; attributes: `none`; lines: 234–234.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### K0547 — `/candidate/reference-semantics/semantics/float.k:235`

- Kind: `rule`; attributes: `none`; lines: 235–235.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### K0548 — `/candidate/reference-semantics/semantics/float.k:243`

- Kind: `syntax`; attributes: `none`; lines: 243–243.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### K0549 — `/candidate/reference-semantics/semantics/float.k:244`

- Kind: `rule`; attributes: `none`; lines: 244–244.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K0550 — `/candidate/reference-semantics/semantics/float.k:245`

- Kind: `rule`; attributes: `none`; lines: 245–245.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### K0551 — `/candidate/reference-semantics/semantics/float.k:246`

- Kind: `rule`; attributes: `none`; lines: 246–246.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### K0552 — `/candidate/reference-semantics/semantics/float.k:247`

- Kind: `rule`; attributes: `none`; lines: 247–248.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K0553 — `/candidate/reference-semantics/semantics/float.k:250`

- Kind: `syntax`; attributes: `none`; lines: 250–250.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### K0554 — `/candidate/reference-semantics/semantics/float.k:251`

- Kind: `rule`; attributes: `none`; lines: 251–251.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### K0555 — `/candidate/reference-semantics/semantics/float.k:252`

- Kind: `rule`; attributes: `none`; lines: 252–252.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### K0556 — `/candidate/reference-semantics/semantics/float.k:253`

- Kind: `rule`; attributes: `none`; lines: 253–253.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### K0557 — `/candidate/reference-semantics/semantics/float.k:254`

- Kind: `rule`; attributes: `none`; lines: 254–255.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K0558 — `/candidate/reference-semantics/semantics/float.k:261`

- Kind: `syntax`; attributes: `none`; lines: 261–261.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### K0559 — `/candidate/reference-semantics/semantics/float.k:262`

- Kind: `rule`; attributes: `none`; lines: 262–264.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### K0560 — `/candidate/reference-semantics/semantics/float.k:265`

- Kind: `rule`; attributes: `none`; lines: 265–265.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### K0561 — `/candidate/reference-semantics/semantics/float.k:266`

- Kind: `rule`; attributes: `none`; lines: 266–266.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### K0562 — `/candidate/reference-semantics/semantics/float.k:267`

- Kind: `rule`; attributes: `none`; lines: 267–269.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### K0563 — `/candidate/reference-semantics/semantics/float.k:270`

- Kind: `rule`; attributes: `none`; lines: 270–272.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### K0564 — `/candidate/reference-semantics/semantics/functions.k:8`

- Kind: `syntax`; attributes: `none`; lines: 8–11.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### K0565 — `/candidate/reference-semantics/semantics/functions.k:14`

- Kind: `rule`; attributes: `none`; lines: 14–16.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### K0566 — `/candidate/reference-semantics/semantics/functions.k:18`

- Kind: `syntax`; attributes: `none`; lines: 18–18.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### K0567 — `/candidate/reference-semantics/semantics/functions.k:19`

- Kind: `rule`; attributes: `none`; lines: 19–20.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### K0568 — `/candidate/reference-semantics/semantics/functions.k:27`

- Kind: `syntax`; attributes: `none`; lines: 27–27.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### K0569 — `/candidate/reference-semantics/semantics/functions.k:31`

- Kind: `syntax`; attributes: `none`; lines: 31–32.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### K0570 — `/candidate/reference-semantics/semantics/functions.k:33`

- Kind: `rule`; attributes: `none`; lines: 33–35.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### K0571 — `/candidate/reference-semantics/semantics/functions.k:36`

- Kind: `rule`; attributes: `none`; lines: 36–41.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K0572 — `/candidate/reference-semantics/semantics/functions.k:42`

- Kind: `rule`; attributes: `none`; lines: 42–45.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### K0573 — `/candidate/reference-semantics/semantics/functions.k:47`

- Kind: `rule`; attributes: `none`; lines: 47–49.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### K0574 — `/candidate/reference-semantics/semantics/functions.k:50`

- Kind: `rule`; attributes: `none`; lines: 50–52.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### K0575 — `/candidate/reference-semantics/semantics/functions.k:53`

- Kind: `rule`; attributes: `none`; lines: 53–58.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### K0576 — `/candidate/reference-semantics/semantics/functions.k:59`

- Kind: `rule`; attributes: `none`; lines: 59–60.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### K0577 — `/candidate/reference-semantics/semantics/functions.k:63`

- Kind: `rule`; attributes: `none`; lines: 63–63.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### K0578 — `/candidate/reference-semantics/semantics/functions.k:64`

- Kind: `rule`; attributes: `none`; lines: 64–66.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### K0579 — `/candidate/reference-semantics/semantics/functions.k:68`

- Kind: `rule`; attributes: `priority`; lines: 68–75.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

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

### K0580 — `/candidate/reference-semantics/semantics/functions.k:78`

- Kind: `rule`; attributes: `none`; lines: 78–79.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### K0581 — `/candidate/reference-semantics/semantics/functions.k:80`

- Kind: `rule`; attributes: `none`; lines: 80–81.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### K0582 — `/candidate/reference-semantics/semantics/functions.k:85`

- Kind: `rule`; attributes: `none`; lines: 85–90.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### K0583 — `/candidate/reference-semantics/semantics/int.k:7`

- Kind: `rule`; attributes: `none`; lines: 7–7.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### K0584 — `/candidate/reference-semantics/semantics/int.k:9`

- Kind: `rule`; attributes: `none`; lines: 9–9.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### K0585 — `/candidate/reference-semantics/semantics/int.k:11`

- Kind: `rule`; attributes: `none`; lines: 11–11.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### K0586 — `/candidate/reference-semantics/semantics/int.k:12`

- Kind: `rule`; attributes: `none`; lines: 12–12.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### K0587 — `/candidate/reference-semantics/semantics/int.k:13`

- Kind: `rule`; attributes: `none`; lines: 13–13.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### K0588 — `/candidate/reference-semantics/semantics/int.k:14`

- Kind: `rule`; attributes: `none`; lines: 14–14.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### K0589 — `/candidate/reference-semantics/semantics/int.k:15`

- Kind: `rule`; attributes: `none`; lines: 15–15.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### K0590 — `/candidate/reference-semantics/semantics/int.k:16`

- Kind: `rule`; attributes: `none`; lines: 16–16.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### K0591 — `/candidate/reference-semantics/semantics/int.k:17`

- Kind: `rule`; attributes: `none`; lines: 17–17.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### K0592 — `/candidate/reference-semantics/semantics/int.k:19`

- Kind: `syntax`; attributes: `function`; lines: 19–19.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### K0593 — `/candidate/reference-semantics/semantics/int.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–20.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### K0594 — `/candidate/reference-semantics/semantics/int.k:22`

- Kind: `rule`; attributes: `none`; lines: 22–22.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### K0595 — `/candidate/reference-semantics/semantics/int.k:23`

- Kind: `rule`; attributes: `none`; lines: 23–23.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### K0596 — `/candidate/reference-semantics/semantics/int.k:24`

- Kind: `rule`; attributes: `none`; lines: 24–24.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### K0597 — `/candidate/reference-semantics/semantics/int.k:25`

- Kind: `rule`; attributes: `none`; lines: 25–25.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### K0598 — `/candidate/reference-semantics/semantics/int.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### K0599 — `/candidate/reference-semantics/semantics/int.k:27`

- Kind: `rule`; attributes: `none`; lines: 27–27.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### K0600 — `/candidate/reference-semantics/semantics/iter.k:8`

- Kind: `syntax`; attributes: `none`; lines: 8–8.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### K0601 — `/candidate/reference-semantics/semantics/list.k:9`

- Kind: `rule`; attributes: `none`; lines: 9–9.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### K0602 — `/candidate/reference-semantics/semantics/list.k:10`

- Kind: `rule`; attributes: `none`; lines: 10–10.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### K0603 — `/candidate/reference-semantics/semantics/list.k:13`

- Kind: `syntax`; attributes: `none`; lines: 13–13.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ApplyK ::= "toList"
```

### K0604 — `/candidate/reference-semantics/semantics/list.k:14`

- Kind: `rule`; attributes: `none`; lines: 14–14.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### K0605 — `/candidate/reference-semantics/semantics/list.k:15`

- Kind: `rule`; attributes: `none`; lines: 15–15.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### K0606 — `/candidate/reference-semantics/semantics/list.k:18`

- Kind: `syntax`; attributes: `function, total`; lines: 18–18.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### K0607 — `/candidate/reference-semantics/semantics/list.k:19`

- Kind: `rule`; attributes: `none`; lines: 19–19.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### K0608 — `/candidate/reference-semantics/semantics/list.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–20.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### K0609 — `/candidate/reference-semantics/semantics/list.k:24`

- Kind: `rule`; attributes: `priority`; lines: 24–25.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### K0610 — `/candidate/reference-semantics/semantics/list.k:27`

- Kind: `rule`; attributes: `none`; lines: 27–27.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### K0611 — `/candidate/reference-semantics/semantics/list.k:28`

- Kind: `rule`; attributes: `none`; lines: 28–28.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### K0612 — `/candidate/reference-semantics/semantics/list.k:33`

- Kind: `syntax`; attributes: `function, total`; lines: 33–33.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### K0613 — `/candidate/reference-semantics/semantics/list.k:34`

- Kind: `rule`; attributes: `none`; lines: 34–34.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule hasRefVS(.ValSeq)                => false
```

### K0614 — `/candidate/reference-semantics/semantics/list.k:35`

- Kind: `rule`; attributes: `none`; lines: 35–35.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### K0615 — `/candidate/reference-semantics/semantics/list.k:37`

- Kind: `syntax`; attributes: `function`; lines: 37–38.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### K0616 — `/candidate/reference-semantics/semantics/list.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–39.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### K0617 — `/candidate/reference-semantics/semantics/list.k:40`

- Kind: `rule`; attributes: `none`; lines: 40–40.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### K0618 — `/candidate/reference-semantics/semantics/list.k:41`

- Kind: `rule`; attributes: `none`; lines: 41–41.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### K0619 — `/candidate/reference-semantics/semantics/list.k:42`

- Kind: `rule`; attributes: `none`; lines: 42–43.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### K0620 — `/candidate/reference-semantics/semantics/list.k:45`

- Kind: `rule`; attributes: `none`; lines: 45–46.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### K0621 — `/candidate/reference-semantics/semantics/list.k:47`

- Kind: `rule`; attributes: `none`; lines: 47–48.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### K0622 — `/candidate/reference-semantics/semantics/list.k:49`

- Kind: `rule`; attributes: `none`; lines: 49–49.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### K0623 — `/candidate/reference-semantics/semantics/list.k:50`

- Kind: `rule`; attributes: `owise`; lines: 50–50.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### K0624 — `/candidate/reference-semantics/semantics/list.k:53`

- Kind: `rule`; attributes: `priority`; lines: 53–55.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### K0625 — `/candidate/reference-semantics/semantics/list.k:58`

- Kind: `syntax`; attributes: `none`; lines: 58–58.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### K0626 — `/candidate/reference-semantics/semantics/list.k:59`

- Kind: `rule`; attributes: `none`; lines: 59–59.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### K0627 — `/candidate/reference-semantics/semantics/list.k:60`

- Kind: `rule`; attributes: `none`; lines: 60–60.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### K0628 — `/candidate/reference-semantics/semantics/list.k:61`

- Kind: `rule`; attributes: `none`; lines: 61–61.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### K0629 — `/candidate/reference-semantics/semantics/list.k:62`

- Kind: `rule`; attributes: `none`; lines: 62–62.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### K0630 — `/candidate/reference-semantics/semantics/list.k:63`

- Kind: `rule`; attributes: `none`; lines: 63–64.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### K0631 — `/candidate/reference-semantics/semantics/list.k:65`

- Kind: `rule`; attributes: `none`; lines: 65–66.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### K0632 — `/candidate/reference-semantics/semantics/list.k:67`

- Kind: `rule`; attributes: `none`; lines: 67–67.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### K0633 — `/candidate/reference-semantics/semantics/methods.k:10`

- Kind: `syntax`; attributes: `function`; lines: 10–10.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### K0634 — `/candidate/reference-semantics/semantics/methods.k:13`

- Kind: `rule`; attributes: `none`; lines: 13–13.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### K0635 — `/candidate/reference-semantics/semantics/methods.k:14`

- Kind: `rule`; attributes: `none`; lines: 14–14.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### K0636 — `/candidate/reference-semantics/semantics/methods.k:15`

- Kind: `rule`; attributes: `none`; lines: 15–15.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### K0637 — `/candidate/reference-semantics/semantics/methods.k:16`

- Kind: `rule`; attributes: `none`; lines: 16–16.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### K0638 — `/candidate/reference-semantics/semantics/methods.k:19`

- Kind: `rule`; attributes: `none`; lines: 19–19.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### K0639 — `/candidate/reference-semantics/semantics/methods.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–20.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### K0640 — `/candidate/reference-semantics/semantics/methods.k:21`

- Kind: `rule`; attributes: `none`; lines: 21–21.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### K0641 — `/candidate/reference-semantics/semantics/methods.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### K0642 — `/candidate/reference-semantics/semantics/methods.k:27`

- Kind: `syntax`; attributes: `function, total`; lines: 27–27.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### K0643 — `/candidate/reference-semantics/semantics/methods.k:28`

- Kind: `rule`; attributes: `none`; lines: 28–28.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### K0644 — `/candidate/reference-semantics/semantics/methods.k:29`

- Kind: `rule`; attributes: `none`; lines: 29–29.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### K0645 — `/candidate/reference-semantics/semantics/methods.k:30`

- Kind: `rule`; attributes: `none`; lines: 30–31.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### K0646 — `/candidate/reference-semantics/semantics/methods.k:34`

- Kind: `rule`; attributes: `none`; lines: 34–34.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### K0647 — `/candidate/reference-semantics/semantics/methods.k:35`

- Kind: `syntax`; attributes: `function`; lines: 35–35.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### K0648 — `/candidate/reference-semantics/semantics/methods.k:36`

- Kind: `rule`; attributes: `none`; lines: 36–36.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### K0649 — `/candidate/reference-semantics/semantics/methods.k:37`

- Kind: `rule`; attributes: `none`; lines: 37–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### K0650 — `/candidate/reference-semantics/semantics/methods.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–40.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### K0651 — `/candidate/reference-semantics/semantics/methods.k:41`

- Kind: `syntax`; attributes: `function, total`; lines: 41–41.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### K0652 — `/candidate/reference-semantics/semantics/methods.k:42`

- Kind: `rule`; attributes: `none`; lines: 42–42.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### K0653 — `/candidate/reference-semantics/semantics/methods.k:43`

- Kind: `rule`; attributes: `owise`; lines: 43–43.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### K0654 — `/candidate/reference-semantics/semantics/methods.k:44`

- Kind: `rule`; attributes: `none`; lines: 44–44.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### K0655 — `/candidate/reference-semantics/semantics/methods.k:47`

- Kind: `rule`; attributes: `none`; lines: 47–47.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### K0656 — `/candidate/reference-semantics/semantics/methods.k:48`

- Kind: `syntax`; attributes: `function, total`; lines: 48–48.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### K0657 — `/candidate/reference-semantics/semantics/methods.k:49`

- Kind: `rule`; attributes: `none`; lines: 49–49.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### K0658 — `/candidate/reference-semantics/semantics/methods.k:50`

- Kind: `rule`; attributes: `none`; lines: 50–50.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### K0659 — `/candidate/reference-semantics/semantics/methods.k:51`

- Kind: `rule`; attributes: `none`; lines: 51–51.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### K0660 — `/candidate/reference-semantics/semantics/methods.k:52`

- Kind: `syntax`; attributes: `function, total`; lines: 52–52.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### K0661 — `/candidate/reference-semantics/semantics/methods.k:53`

- Kind: `rule`; attributes: `none`; lines: 53–53.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### K0662 — `/candidate/reference-semantics/semantics/methods.k:54`

- Kind: `rule`; attributes: `none`; lines: 54–54.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### K0663 — `/candidate/reference-semantics/semantics/methods.k:55`

- Kind: `rule`; attributes: `none`; lines: 55–55.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### K0664 — `/candidate/reference-semantics/semantics/methods.k:58`

- Kind: `rule`; attributes: `none`; lines: 58–58.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### K0665 — `/candidate/reference-semantics/semantics/methods.k:61`

- Kind: `rule`; attributes: `none`; lines: 61–61.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### K0666 — `/candidate/reference-semantics/semantics/methods.k:64`

- Kind: `rule`; attributes: `none`; lines: 64–64.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### K0667 — `/candidate/reference-semantics/semantics/methods.k:65`

- Kind: `syntax`; attributes: `function, total`; lines: 65–65.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### K0668 — `/candidate/reference-semantics/semantics/methods.k:66`

- Kind: `rule`; attributes: `none`; lines: 66–66.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### K0669 — `/candidate/reference-semantics/semantics/methods.k:67`

- Kind: `rule`; attributes: `none`; lines: 67–67.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### K0670 — `/candidate/reference-semantics/semantics/methods.k:68`

- Kind: `rule`; attributes: `none`; lines: 68–68.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### K0671 — `/candidate/reference-semantics/semantics/methods.k:72`

- Kind: `rule`; attributes: `priority`; lines: 72–74.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### K0672 — `/candidate/reference-semantics/semantics/methods.k:75`

- Kind: `syntax`; attributes: `function`; lines: 75–75.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### K0673 — `/candidate/reference-semantics/semantics/methods.k:76`

- Kind: `rule`; attributes: `none`; lines: 76–76.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### K0674 — `/candidate/reference-semantics/semantics/methods.k:77`

- Kind: `rule`; attributes: `none`; lines: 77–78.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### K0675 — `/candidate/reference-semantics/semantics/methods.k:79`

- Kind: `rule`; attributes: `none`; lines: 79–80.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

### K0676 — `/candidate/reference-semantics/semantics/methods.k:82`

- Kind: `syntax`; attributes: `function`; lines: 82–82.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### K0677 — `/candidate/reference-semantics/semantics/methods.k:83`

- Kind: `rule`; attributes: `none`; lines: 83–83.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### K0678 — `/candidate/reference-semantics/semantics/methods.k:84`

- Kind: `rule`; attributes: `none`; lines: 84–84.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### K0679 — `/candidate/reference-semantics/semantics/methods.k:85`

- Kind: `syntax`; attributes: `function, total`; lines: 85–85.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### K0680 — `/candidate/reference-semantics/semantics/methods.k:86`

- Kind: `rule`; attributes: `none`; lines: 86–86.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### K0681 — `/candidate/reference-semantics/semantics/methods.k:89`

- Kind: `rule`; attributes: `priority`; lines: 89–91.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### K0682 — `/candidate/reference-semantics/semantics/methods.k:94`

- Kind: `rule`; attributes: `priority`; lines: 94–96.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### K0683 — `/candidate/reference-semantics/semantics/methods.k:97`

- Kind: `syntax`; attributes: `function`; lines: 97–97.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### K0684 — `/candidate/reference-semantics/semantics/methods.k:98`

- Kind: `rule`; attributes: `none`; lines: 98–98.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### K0685 — `/candidate/reference-semantics/semantics/methods.k:99`

- Kind: `rule`; attributes: `none`; lines: 99–100.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### K0686 — `/candidate/reference-semantics/semantics/methods.k:101`

- Kind: `rule`; attributes: `none`; lines: 101–102.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### K0687 — `/candidate/reference-semantics/semantics/methods.k:104`

- Kind: `rule`; attributes: `none`; lines: 104–105.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### K0688 — `/candidate/reference-semantics/semantics/methods.k:106`

- Kind: `syntax`; attributes: `function, total`; lines: 106–106.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### K0689 — `/candidate/reference-semantics/semantics/methods.k:107`

- Kind: `rule`; attributes: `none`; lines: 107–107.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### K0690 — `/candidate/reference-semantics/semantics/methods.k:108`

- Kind: `rule`; attributes: `none`; lines: 108–108.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### K0691 — `/candidate/reference-semantics/semantics/methods.k:109`

- Kind: `rule`; attributes: `none`; lines: 109–109.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### K0692 — `/candidate/reference-semantics/semantics/methods.k:112`

- Kind: `syntax`; attributes: `function, total`; lines: 112–112.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### K0693 — `/candidate/reference-semantics/semantics/methods.k:113`

- Kind: `rule`; attributes: `none`; lines: 113–113.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### K0694 — `/candidate/reference-semantics/semantics/methods.k:115`

- Kind: `syntax`; attributes: `function, total`; lines: 115–115.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### K0695 — `/candidate/reference-semantics/semantics/methods.k:116`

- Kind: `rule`; attributes: `none`; lines: 116–116.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### K0696 — `/candidate/reference-semantics/semantics/methods.k:118`

- Kind: `syntax`; attributes: `function, total`; lines: 118–118.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### K0697 — `/candidate/reference-semantics/semantics/methods.k:119`

- Kind: `rule`; attributes: `none`; lines: 119–119.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### K0698 — `/candidate/reference-semantics/semantics/methods.k:121`

- Kind: `syntax`; attributes: `function, total`; lines: 121–121.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### K0699 — `/candidate/reference-semantics/semantics/methods.k:122`

- Kind: `rule`; attributes: `none`; lines: 122–122.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### K0700 — `/candidate/reference-semantics/semantics/methods.k:124`

- Kind: `syntax`; attributes: `function, total`; lines: 124–124.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### K0701 — `/candidate/reference-semantics/semantics/methods.k:125`

- Kind: `rule`; attributes: `none`; lines: 125–125.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule hasUpper(.IntSeq) => false
```

### K0702 — `/candidate/reference-semantics/semantics/methods.k:126`

- Kind: `rule`; attributes: `none`; lines: 126–126.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### K0703 — `/candidate/reference-semantics/semantics/methods.k:128`

- Kind: `syntax`; attributes: `function, total`; lines: 128–128.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### K0704 — `/candidate/reference-semantics/semantics/methods.k:129`

- Kind: `rule`; attributes: `none`; lines: 129–129.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule hasLower(.IntSeq) => false
```

### K0705 — `/candidate/reference-semantics/semantics/methods.k:130`

- Kind: `rule`; attributes: `none`; lines: 130–130.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### K0706 — `/candidate/reference-semantics/semantics/methods.k:132`

- Kind: `syntax`; attributes: `function, total`; lines: 132–132.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### K0707 — `/candidate/reference-semantics/semantics/methods.k:133`

- Kind: `rule`; attributes: `none`; lines: 133–133.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule allAlpha(.IntSeq) => true
```

### K0708 — `/candidate/reference-semantics/semantics/methods.k:134`

- Kind: `rule`; attributes: `none`; lines: 134–134.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### K0709 — `/candidate/reference-semantics/semantics/methods.k:136`

- Kind: `syntax`; attributes: `function, total`; lines: 136–136.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### K0710 — `/candidate/reference-semantics/semantics/methods.k:137`

- Kind: `rule`; attributes: `none`; lines: 137–137.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule allDigit(.IntSeq) => true
```

### K0711 — `/candidate/reference-semantics/semantics/methods.k:138`

- Kind: `rule`; attributes: `none`; lines: 138–138.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### K0712 — `/candidate/reference-semantics/semantics/methods.k:140`

- Kind: `syntax`; attributes: `function, total`; lines: 140–140.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### K0713 — `/candidate/reference-semantics/semantics/methods.k:142`

- Kind: `rule`; attributes: `none`; lines: 142–142.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K0714 — `/candidate/reference-semantics/semantics/methods.k:143`

- Kind: `rule`; attributes: `owise`; lines: 143–143.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule lowerC(C:Int) => C         [owise]
```

### K0715 — `/candidate/reference-semantics/semantics/methods.k:145`

- Kind: `syntax`; attributes: `function, total`; lines: 145–145.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= upperC(Int) [function, total]
```

### K0716 — `/candidate/reference-semantics/semantics/methods.k:146`

- Kind: `rule`; attributes: `none`; lines: 146–146.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K0717 — `/candidate/reference-semantics/semantics/methods.k:147`

- Kind: `rule`; attributes: `owise`; lines: 147–147.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule upperC(C:Int) => C         [owise]
```

### K0718 — `/candidate/reference-semantics/semantics/methods.k:149`

- Kind: `syntax`; attributes: `function, total`; lines: 149–149.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= swapC(Int) [function, total]
```

### K0719 — `/candidate/reference-semantics/semantics/methods.k:150`

- Kind: `rule`; attributes: `none`; lines: 150–150.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### K0720 — `/candidate/reference-semantics/semantics/methods.k:151`

- Kind: `rule`; attributes: `none`; lines: 151–151.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### K0721 — `/candidate/reference-semantics/semantics/methods.k:152`

- Kind: `rule`; attributes: `owise`; lines: 152–152.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule swapC(C:Int) => C         [owise]
```

### K0722 — `/candidate/reference-semantics/semantics/methods.k:154`

- Kind: `syntax`; attributes: `function, total`; lines: 154–154.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### K0723 — `/candidate/reference-semantics/semantics/methods.k:155`

- Kind: `rule`; attributes: `none`; lines: 155–155.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### K0724 — `/candidate/reference-semantics/semantics/methods.k:156`

- Kind: `rule`; attributes: `none`; lines: 156–156.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### K0725 — `/candidate/reference-semantics/semantics/methods.k:158`

- Kind: `syntax`; attributes: `function, total`; lines: 158–158.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### K0726 — `/candidate/reference-semantics/semantics/methods.k:159`

- Kind: `rule`; attributes: `none`; lines: 159–159.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### K0727 — `/candidate/reference-semantics/semantics/methods.k:160`

- Kind: `rule`; attributes: `none`; lines: 160–160.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### K0728 — `/candidate/reference-semantics/semantics/methods.k:162`

- Kind: `syntax`; attributes: `function, total`; lines: 162–162.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### K0729 — `/candidate/reference-semantics/semantics/methods.k:163`

- Kind: `rule`; attributes: `none`; lines: 163–163.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### K0730 — `/candidate/reference-semantics/semantics/methods.k:164`

- Kind: `rule`; attributes: `none`; lines: 164–164.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### K0731 — `/candidate/reference-semantics/semantics/methods.k:166`

- Kind: `syntax`; attributes: `function, total`; lines: 166–166.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### K0732 — `/candidate/reference-semantics/semantics/methods.k:167`

- Kind: `rule`; attributes: `none`; lines: 167–167.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### K0733 — `/candidate/reference-semantics/semantics/methods.k:168`

- Kind: `rule`; attributes: `none`; lines: 168–168.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K0734 — `/candidate/reference-semantics/semantics/methods.k:169`

- Kind: `rule`; attributes: `none`; lines: 169–169.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### K0735 — `/candidate/reference-semantics/semantics/operators.k:10`

- Kind: `rule`; attributes: `none`; lines: 10–10.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### K0736 — `/candidate/reference-semantics/semantics/operators.k:12`

- Kind: `rule`; attributes: `none`; lines: 12–12.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### K0737 — `/candidate/reference-semantics/semantics/operators.k:15`

- Kind: `context`; attributes: `none`; lines: 15–15.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  context Compare(HOLE, _)
```

### K0738 — `/candidate/reference-semantics/semantics/operators.k:16`

- Kind: `context`; attributes: `none`; lines: 16–16.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### K0739 — `/candidate/reference-semantics/semantics/operators.k:17`

- Kind: `rule`; attributes: `owise`; lines: 17–17.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### K0740 — `/candidate/reference-semantics/semantics/operators.k:19`

- Kind: `rule`; attributes: `none`; lines: 19–19.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### K0741 — `/candidate/reference-semantics/semantics/operators.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–20.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### K0742 — `/candidate/reference-semantics/semantics/operators.k:25`

- Kind: `rule`; attributes: `priority`; lines: 25–27.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0743 — `/candidate/reference-semantics/semantics/operators.k:28`

- Kind: `rule`; attributes: `priority`; lines: 28–31.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

### K0744 — `/candidate/reference-semantics/semantics/operators.k:34`

- Kind: `rule`; attributes: `priority`; lines: 34–37.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### K0745 — `/candidate/reference-semantics/semantics/operators.k:38`

- Kind: `rule`; attributes: `priority`; lines: 38–42.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### K0746 — `/candidate/reference-semantics/semantics/operators.k:44`

- Kind: `rule`; attributes: `priority`; lines: 44–46.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0747 — `/candidate/reference-semantics/semantics/range.k:9`

- Kind: `syntax`; attributes: `function, total`; lines: 9–9.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### K0748 — `/candidate/reference-semantics/semantics/range.k:10`

- Kind: `rule`; attributes: `none`; lines: 10–10.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### K0749 — `/candidate/reference-semantics/semantics/range.k:12`

- Kind: `syntax`; attributes: `function`; lines: 12–12.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### K0750 — `/candidate/reference-semantics/semantics/range.k:13`

- Kind: `rule`; attributes: `none`; lines: 13–14.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### K0751 — `/candidate/reference-semantics/semantics/range.k:15`

- Kind: `rule`; attributes: `none`; lines: 15–16.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### K0752 — `/candidate/reference-semantics/semantics/range.k:17`

- Kind: `rule`; attributes: `none`; lines: 17–18.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### K0753 — `/candidate/reference-semantics/semantics/range.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–22.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### K0754 — `/candidate/reference-semantics/semantics/range.k:23`

- Kind: `rule`; attributes: `none`; lines: 23–24.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### K0755 — `/candidate/reference-semantics/semantics/set.k:8`

- Kind: `syntax`; attributes: `none`; lines: 8–8.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= setV(IntSeq)
```

### K0756 — `/candidate/reference-semantics/semantics/set.k:11`

- Kind: `syntax`; attributes: `function, total`; lines: 11–11.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### K0757 — `/candidate/reference-semantics/semantics/set.k:12`

- Kind: `rule`; attributes: `none`; lines: 12–12.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### K0758 — `/candidate/reference-semantics/semantics/set.k:13`

- Kind: `rule`; attributes: `none`; lines: 13–13.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### K0759 — `/candidate/reference-semantics/semantics/set.k:16`

- Kind: `syntax`; attributes: `function, total`; lines: 16–17.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### K0760 — `/candidate/reference-semantics/semantics/set.k:18`

- Kind: `rule`; attributes: `none`; lines: 18–18.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### K0761 — `/candidate/reference-semantics/semantics/set.k:19`

- Kind: `rule`; attributes: `none`; lines: 19–19.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### K0762 — `/candidate/reference-semantics/semantics/set.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–21.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### K0763 — `/candidate/reference-semantics/semantics/set.k:22`

- Kind: `rule`; attributes: `none`; lines: 22–23.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### K0764 — `/candidate/reference-semantics/semantics/set.k:25`

- Kind: `syntax`; attributes: `function, total`; lines: 25–25.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### K0765 — `/candidate/reference-semantics/semantics/set.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### K0766 — `/candidate/reference-semantics/semantics/set.k:27`

- Kind: `rule`; attributes: `none`; lines: 27–27.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### K0767 — `/candidate/reference-semantics/semantics/set.k:31`

- Kind: `syntax`; attributes: `function, total`; lines: 31–31.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### K0768 — `/candidate/reference-semantics/semantics/set.k:32`

- Kind: `rule`; attributes: `none`; lines: 32–32.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### K0769 — `/candidate/reference-semantics/semantics/set.k:33`

- Kind: `rule`; attributes: `none`; lines: 33–33.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### K0770 — `/candidate/reference-semantics/semantics/set.k:35`

- Kind: `syntax`; attributes: `function, total`; lines: 35–35.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### K0771 — `/candidate/reference-semantics/semantics/set.k:36`

- Kind: `rule`; attributes: `none`; lines: 36–36.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### K0772 — `/candidate/reference-semantics/semantics/set.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–39.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### K0773 — `/candidate/reference-semantics/semantics/sort.k:18`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 18–18.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### K0774 — `/candidate/reference-semantics/semantics/sort.k:19`

- Kind: `syntax`; attributes: `function`; lines: 19–19.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### K0775 — `/candidate/reference-semantics/semantics/sort.k:20`

- Kind: `rule`; attributes: `concrete`; lines: 20–20.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### K0776 — `/candidate/reference-semantics/semantics/sort.k:21`

- Kind: `rule`; attributes: `concrete`; lines: 21–21.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### K0777 — `/candidate/reference-semantics/semantics/sort.k:22`

- Kind: `rule`; attributes: `concrete`; lines: 22–22.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### K0778 — `/candidate/reference-semantics/semantics/sort.k:23`

- Kind: `rule`; attributes: `concrete`; lines: 23–23.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### K0779 — `/candidate/reference-semantics/semantics/sort.k:24`

- Kind: `rule`; attributes: `concrete`; lines: 24–24.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### K0780 — `/candidate/reference-semantics/semantics/sort.k:26`

- Kind: `syntax`; attributes: `function`; lines: 26–26.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### K0781 — `/candidate/reference-semantics/semantics/sort.k:27`

- Kind: `rule`; attributes: `concrete`; lines: 27–27.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### K0782 — `/candidate/reference-semantics/semantics/sort.k:28`

- Kind: `rule`; attributes: `concrete`; lines: 28–28.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### K0783 — `/candidate/reference-semantics/semantics/sort.k:29`

- Kind: `rule`; attributes: `concrete`; lines: 29–30.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### K0784 — `/candidate/reference-semantics/semantics/sort.k:31`

- Kind: `rule`; attributes: `concrete`; lines: 31–32.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### K0785 — `/candidate/reference-semantics/semantics/sort.k:36`

- Kind: `rule`; attributes: `none`; lines: 36–37.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### K0786 — `/candidate/reference-semantics/semantics/sort.k:40`

- Kind: `rule`; attributes: `priority`; lines: 40–42.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### K0787 — `/candidate/reference-semantics/semantics/sort.k:49`

- Kind: `syntax`; attributes: `function, total, no-evaluators, symbol`; lines: 49–49.
- Decision: FIXED_OPAQUE_PRIMITIVE: supplied semantics trust boundary; not reachable from eat.

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### K0788 — `/candidate/reference-semantics/semantics/sort.k:51`

- Kind: `syntax`; attributes: `function, total`; lines: 51–52.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### K0789 — `/candidate/reference-semantics/semantics/sort.k:53`

- Kind: `rule`; attributes: `none`; lines: 53–53.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### K0790 — `/candidate/reference-semantics/semantics/sort.k:54`

- Kind: `rule`; attributes: `none`; lines: 54–54.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### K0791 — `/candidate/reference-semantics/semantics/sort.k:55`

- Kind: `rule`; attributes: `none`; lines: 55–55.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### K0792 — `/candidate/reference-semantics/semantics/sort.k:57`

- Kind: `syntax`; attributes: `function, total`; lines: 57–57.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### K0793 — `/candidate/reference-semantics/semantics/sort.k:58`

- Kind: `rule`; attributes: `none`; lines: 58–58.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule condRev(S:ValSeq, false) => S
```

### K0794 — `/candidate/reference-semantics/semantics/sort.k:59`

- Kind: `rule`; attributes: `none`; lines: 59–59.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### K0795 — `/candidate/reference-semantics/semantics/sort.k:61`

- Kind: `rule`; attributes: `none`; lines: 61–62.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### K0796 — `/candidate/reference-semantics/semantics/sort.k:63`

- Kind: `rule`; attributes: `none`; lines: 63–64.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### K0797 — `/candidate/reference-semantics/semantics/sort.k:65`

- Kind: `rule`; attributes: `none`; lines: 65–66.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

### K0798 — `/candidate/reference-semantics/semantics/str.k:8`

- Kind: `rule`; attributes: `none`; lines: 8–8.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### K0799 — `/candidate/reference-semantics/semantics/str.k:9`

- Kind: `rule`; attributes: `none`; lines: 9–10.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### K0800 — `/candidate/reference-semantics/semantics/str.k:13`

- Kind: `syntax`; attributes: `function`; lines: 13–13.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### K0801 — `/candidate/reference-semantics/semantics/str.k:14`

- Kind: `rule`; attributes: `none`; lines: 14–14.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### K0802 — `/candidate/reference-semantics/semantics/str.k:15`

- Kind: `rule`; attributes: `none`; lines: 15–15.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strToCodes("") => .IntSeq
```

### K0803 — `/candidate/reference-semantics/semantics/str.k:16`

- Kind: `rule`; attributes: `none`; lines: 16–17.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### K0804 — `/candidate/reference-semantics/semantics/str.k:20`

- Kind: `syntax`; attributes: `function, total`; lines: 20–20.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### K0805 — `/candidate/reference-semantics/semantics/str.k:21`

- Kind: `rule`; attributes: `none`; lines: 21–21.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### K0806 — `/candidate/reference-semantics/semantics/str.k:22`

- Kind: `rule`; attributes: `none`; lines: 22–22.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### K0807 — `/candidate/reference-semantics/semantics/str.k:24`

- Kind: `rule`; attributes: `none`; lines: 24–24.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### K0808 — `/candidate/reference-semantics/semantics/str.k:25`

- Kind: `rule`; attributes: `none`; lines: 25–25.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### K0809 — `/candidate/reference-semantics/semantics/str.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–26.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### K0810 — `/candidate/reference-semantics/semantics/str.k:29`

- Kind: `rule`; attributes: `none`; lines: 29–29.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### K0811 — `/candidate/reference-semantics/semantics/str.k:30`

- Kind: `rule`; attributes: `none`; lines: 30–30.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### K0812 — `/candidate/reference-semantics/semantics/str.k:32`

- Kind: `syntax`; attributes: `function, total`; lines: 32–32.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### K0813 — `/candidate/reference-semantics/semantics/str.k:33`

- Kind: `rule`; attributes: `none`; lines: 33–33.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### K0814 — `/candidate/reference-semantics/semantics/str.k:34`

- Kind: `rule`; attributes: `none`; lines: 34–34.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K0815 — `/candidate/reference-semantics/semantics/str.k:35`

- Kind: `rule`; attributes: `none`; lines: 35–35.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### K0816 — `/candidate/reference-semantics/semantics/str.k:37`

- Kind: `syntax`; attributes: `function, total`; lines: 37–37.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### K0817 — `/candidate/reference-semantics/semantics/str.k:38`

- Kind: `rule`; attributes: `none`; lines: 38–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### K0818 — `/candidate/reference-semantics/semantics/str.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–39.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### K0819 — `/candidate/reference-semantics/semantics/str.k:40`

- Kind: `rule`; attributes: `none`; lines: 40–41.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

### K0820 — `/candidate/reference-semantics/semantics/str.k:48`

- Kind: `syntax`; attributes: `function, total`; lines: 48–48.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### K0821 — `/candidate/reference-semantics/semantics/str.k:49`

- Kind: `rule`; attributes: `none`; lines: 49–49.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### K0822 — `/candidate/reference-semantics/semantics/str.k:50`

- Kind: `rule`; attributes: `none`; lines: 50–50.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### K0823 — `/candidate/reference-semantics/semantics/str.k:51`

- Kind: `rule`; attributes: `none`; lines: 51–51.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### K0824 — `/candidate/reference-semantics/semantics/str.k:52`

- Kind: `rule`; attributes: `none`; lines: 52–52.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### K0825 — `/candidate/reference-semantics/semantics/str.k:53`

- Kind: `rule`; attributes: `none`; lines: 53–53.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### K0826 — `/candidate/reference-semantics/semantics/str.k:54`

- Kind: `rule`; attributes: `none`; lines: 54–54.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### K0827 — `/candidate/reference-semantics/semantics/str.k:56`

- Kind: `rule`; attributes: `none`; lines: 56–56.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### K0828 — `/candidate/reference-semantics/semantics/str.k:57`

- Kind: `rule`; attributes: `none`; lines: 57–57.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### K0829 — `/candidate/reference-semantics/semantics/str.k:58`

- Kind: `rule`; attributes: `none`; lines: 58–58.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### K0830 — `/candidate/reference-semantics/semantics/str.k:59`

- Kind: `rule`; attributes: `none`; lines: 59–59.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### K0831 — `/candidate/reference-semantics/semantics/subscript.k:11`

- Kind: `syntax`; attributes: `function, total`; lines: 11–11.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### K0832 — `/candidate/reference-semantics/semantics/subscript.k:12`

- Kind: `rule`; attributes: `none`; lines: 12–12.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### K0833 — `/candidate/reference-semantics/semantics/subscript.k:13`

- Kind: `rule`; attributes: `none`; lines: 13–14.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K0834 — `/candidate/reference-semantics/semantics/subscript.k:16`

- Kind: `syntax`; attributes: `function`; lines: 16–16.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### K0835 — `/candidate/reference-semantics/semantics/subscript.k:17`

- Kind: `rule`; attributes: `none`; lines: 17–17.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### K0836 — `/candidate/reference-semantics/semantics/subscript.k:18`

- Kind: `rule`; attributes: `none`; lines: 18–19.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### K0837 — `/candidate/reference-semantics/semantics/subscript.k:21`

- Kind: `syntax`; attributes: `function, total`; lines: 21–21.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### K0838 — `/candidate/reference-semantics/semantics/subscript.k:22`

- Kind: `rule`; attributes: `none`; lines: 22–22.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### K0839 — `/candidate/reference-semantics/semantics/subscript.k:23`

- Kind: `rule`; attributes: `none`; lines: 23–23.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### K0840 — `/candidate/reference-semantics/semantics/subscript.k:27`

- Kind: `context`; attributes: `none`; lines: 27–27.
- Decision: FIXED_EVALUATION_CONTEXT: not exercised by eat unless noted in path map.

```k
  context Subscript(HOLE, _)
```

### K0841 — `/candidate/reference-semantics/semantics/subscript.k:28`

- Kind: `context`; attributes: `none`; lines: 28–28.
- Decision: FIXED_EVALUATION_CONTEXT: not exercised by eat unless noted in path map.

```k
  context Subscript(_:Val, HOLE:Expr)
```

### K0842 — `/candidate/reference-semantics/semantics/subscript.k:31`

- Kind: `rule`; attributes: `priority`; lines: 31–33.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0843 — `/candidate/reference-semantics/semantics/subscript.k:35`

- Kind: `rule`; attributes: `none`; lines: 35–35.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### K0844 — `/candidate/reference-semantics/semantics/subscript.k:37`

- Kind: `syntax`; attributes: `function`; lines: 37–37.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### K0845 — `/candidate/reference-semantics/semantics/subscript.k:38`

- Kind: `rule`; attributes: `none`; lines: 38–38.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K0846 — `/candidate/reference-semantics/semantics/subscript.k:39`

- Kind: `rule`; attributes: `none`; lines: 39–39.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### K0847 — `/candidate/reference-semantics/semantics/subscript.k:40`

- Kind: `rule`; attributes: `none`; lines: 40–41.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### K0848 — `/candidate/reference-semantics/semantics/subscript.k:44`

- Kind: `syntax`; attributes: `none`; lines: 44–47.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### K0849 — `/candidate/reference-semantics/semantics/subscript.k:49`

- Kind: `syntax`; attributes: `none`; lines: 49–49.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### K0850 — `/candidate/reference-semantics/semantics/subscript.k:50`

- Kind: `rule`; attributes: `none`; lines: 50–50.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### K0851 — `/candidate/reference-semantics/semantics/subscript.k:51`

- Kind: `rule`; attributes: `none`; lines: 51–51.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### K0852 — `/candidate/reference-semantics/semantics/subscript.k:52`

- Kind: `rule`; attributes: `none`; lines: 52–52.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### K0853 — `/candidate/reference-semantics/semantics/subscript.k:54`

- Kind: `rule`; attributes: `none`; lines: 54–54.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### K0854 — `/candidate/reference-semantics/semantics/subscript.k:55`

- Kind: `rule`; attributes: `none`; lines: 55–55.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### K0855 — `/candidate/reference-semantics/semantics/subscript.k:56`

- Kind: `rule`; attributes: `none`; lines: 56–56.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### K0856 — `/candidate/reference-semantics/semantics/subscript.k:58`

- Kind: `rule`; attributes: `priority`; lines: 58–60.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### K0857 — `/candidate/reference-semantics/semantics/subscript.k:61`

- Kind: `rule`; attributes: `none`; lines: 61–61.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### K0858 — `/candidate/reference-semantics/semantics/subscript.k:63`

- Kind: `syntax`; attributes: `function`; lines: 63–63.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### K0859 — `/candidate/reference-semantics/semantics/subscript.k:64`

- Kind: `rule`; attributes: `none`; lines: 64–65.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K0860 — `/candidate/reference-semantics/semantics/subscript.k:66`

- Kind: `rule`; attributes: `none`; lines: 66–67.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### K0861 — `/candidate/reference-semantics/semantics/subscript.k:68`

- Kind: `rule`; attributes: `none`; lines: 68–69.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### K0862 — `/candidate/reference-semantics/semantics/subscript.k:72`

- Kind: `syntax`; attributes: `function, total`; lines: 72–72.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### K0863 — `/candidate/reference-semantics/semantics/subscript.k:73`

- Kind: `rule`; attributes: `none`; lines: 73–73.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStep(noB)          => 1
```

### K0864 — `/candidate/reference-semantics/semantics/subscript.k:74`

- Kind: `rule`; attributes: `none`; lines: 74–74.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStep(someB(S:Int)) => S
```

### K0865 — `/candidate/reference-semantics/semantics/subscript.k:76`

- Kind: `syntax`; attributes: `function`; lines: 76–76.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### K0866 — `/candidate/reference-semantics/semantics/subscript.k:77`

- Kind: `rule`; attributes: `none`; lines: 77–78.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### K0867 — `/candidate/reference-semantics/semantics/subscript.k:79`

- Kind: `rule`; attributes: `none`; lines: 79–80.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### K0868 — `/candidate/reference-semantics/semantics/subscript.k:81`

- Kind: `rule`; attributes: `none`; lines: 81–81.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K0869 — `/candidate/reference-semantics/semantics/subscript.k:83`

- Kind: `syntax`; attributes: `function`; lines: 83–83.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### K0870 — `/candidate/reference-semantics/semantics/subscript.k:84`

- Kind: `rule`; attributes: `none`; lines: 84–85.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### K0871 — `/candidate/reference-semantics/semantics/subscript.k:86`

- Kind: `rule`; attributes: `none`; lines: 86–87.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### K0872 — `/candidate/reference-semantics/semantics/subscript.k:88`

- Kind: `rule`; attributes: `none`; lines: 88–88.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### K0873 — `/candidate/reference-semantics/semantics/subscript.k:90`

- Kind: `syntax`; attributes: `function, total`; lines: 90–90.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### K0874 — `/candidate/reference-semantics/semantics/subscript.k:91`

- Kind: `rule`; attributes: `none`; lines: 91–92.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### K0875 — `/candidate/reference-semantics/semantics/subscript.k:93`

- Kind: `rule`; attributes: `none`; lines: 93–94.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### K0876 — `/candidate/reference-semantics/semantics/subscript.k:96`

- Kind: `syntax`; attributes: `function, total`; lines: 96–96.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### K0877 — `/candidate/reference-semantics/semantics/subscript.k:97`

- Kind: `rule`; attributes: `none`; lines: 97–98.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### K0878 — `/candidate/reference-semantics/semantics/subscript.k:99`

- Kind: `rule`; attributes: `none`; lines: 99–100.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### K0879 — `/candidate/reference-semantics/semantics/subscript.k:102`

- Kind: `syntax`; attributes: `function, total`; lines: 102–102.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### K0880 — `/candidate/reference-semantics/semantics/subscript.k:103`

- Kind: `rule`; attributes: `none`; lines: 103–104.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### K0881 — `/candidate/reference-semantics/semantics/subscript.k:105`

- Kind: `rule`; attributes: `none`; lines: 105–106.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

### K0882 — `/candidate/reference-semantics/semantics/subscript.k:109`

- Kind: `syntax`; attributes: `function`; lines: 109–109.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### K0883 — `/candidate/reference-semantics/semantics/subscript.k:110`

- Kind: `rule`; attributes: `none`; lines: 110–112.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K0884 — `/candidate/reference-semantics/semantics/subscript.k:113`

- Kind: `rule`; attributes: `none`; lines: 113–114.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K0885 — `/candidate/reference-semantics/semantics/subscript.k:116`

- Kind: `syntax`; attributes: `function`; lines: 116–116.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### K0886 — `/candidate/reference-semantics/semantics/subscript.k:117`

- Kind: `rule`; attributes: `none`; lines: 117–119.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### K0887 — `/candidate/reference-semantics/semantics/subscript.k:120`

- Kind: `rule`; attributes: `none`; lines: 120–121.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### K0888 — `/candidate/reference-semantics/semantics/syntax.k:9`

- Kind: `syntax`; attributes: `macro, strict, seqstrict`; lines: 9–30.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

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

### K0889 — `/candidate/reference-semantics/semantics/syntax.k:32`

- Kind: `syntax`; attributes: `none`; lines: 32–32.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### K0890 — `/candidate/reference-semantics/semantics/syntax.k:33`

- Kind: `syntax`; attributes: `none`; lines: 33–33.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### K0891 — `/candidate/reference-semantics/semantics/syntax.k:34`

- Kind: `syntax`; attributes: `none`; lines: 34–34.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Entries  ::= List{Entry, ","}
```

### K0892 — `/candidate/reference-semantics/semantics/syntax.k:35`

- Kind: `syntax`; attributes: `none`; lines: 35–35.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### K0893 — `/candidate/reference-semantics/semantics/syntax.k:36`

- Kind: `syntax`; attributes: `none`; lines: 36–36.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax CompFors ::= List{CompFor, ""}
```

### K0894 — `/candidate/reference-semantics/semantics/syntax.k:37`

- Kind: `syntax`; attributes: `none`; lines: 37–37.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Exprs    ::= List{Expr, ","}
```

### K0895 — `/candidate/reference-semantics/semantics/syntax.k:38`

- Kind: `syntax`; attributes: `none`; lines: 38–38.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### K0896 — `/candidate/reference-semantics/semantics/syntax.k:39`

- Kind: `syntax`; attributes: `none`; lines: 39–39.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Bound    ::= Expr | "NoBound"
```

### K0897 — `/candidate/reference-semantics/semantics/syntax.k:41`

- Kind: `syntax`; attributes: `strict`; lines: 41–54.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

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

### K0898 — `/candidate/reference-semantics/semantics/syntax.k:56`

- Kind: `syntax`; attributes: `none`; lines: 56–56.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### K0899 — `/candidate/reference-semantics/semantics/syntax.k:57`

- Kind: `syntax`; attributes: `none`; lines: 57–57.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### K0900 — `/candidate/reference-semantics/semantics/syntax.k:58`

- Kind: `syntax`; attributes: `none`; lines: 58–58.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### K0901 — `/candidate/reference-semantics/semantics/syntax.k:59`

- Kind: `syntax`; attributes: `none`; lines: 59–59.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### K0902 — `/candidate/reference-semantics/semantics/syntax.k:60`

- Kind: `syntax`; attributes: `none`; lines: 60–60.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ParamNames ::= List{String, ","}
```

### K0903 — `/candidate/reference-semantics/semantics/syntax.k:61`

- Kind: `syntax`; attributes: `none`; lines: 61–61.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### K0904 — `/candidate/reference-semantics/semantics/tuple.k:10`

- Kind: `rule`; attributes: `none`; lines: 10–10.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### K0905 — `/candidate/reference-semantics/semantics/tuple.k:11`

- Kind: `rule`; attributes: `none`; lines: 11–11.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### K0906 — `/candidate/reference-semantics/semantics/tuple.k:14`

- Kind: `syntax`; attributes: `none`; lines: 14–14.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax ApplyK ::= "toTuple"
```

### K0907 — `/candidate/reference-semantics/semantics/tuple.k:15`

- Kind: `rule`; attributes: `none`; lines: 15–15.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### K0908 — `/candidate/reference-semantics/semantics/tuple.k:16`

- Kind: `rule`; attributes: `none`; lines: 16–16.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### K0909 — `/candidate/reference-semantics/semantics/tuple.k:18`

- Kind: `rule`; attributes: `none`; lines: 18–18.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### K0910 — `/candidate/reference-semantics/semantics/tuple.k:20`

- Kind: `rule`; attributes: `none`; lines: 20–20.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### K0911 — `/candidate/reference-semantics/semantics/tuple.k:21`

- Kind: `rule`; attributes: `none`; lines: 21–21.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### K0912 — `/candidate/reference-semantics/semantics/tuple.k:23`

- Kind: `rule`; attributes: `none`; lines: 23–23.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### K0913 — `/candidate/reference-semantics/semantics/tuple.k:24`

- Kind: `syntax`; attributes: `function`; lines: 24–24.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### K0914 — `/candidate/reference-semantics/semantics/tuple.k:25`

- Kind: `rule`; attributes: `none`; lines: 25–25.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### K0915 — `/candidate/reference-semantics/semantics/tuple.k:26`

- Kind: `rule`; attributes: `none`; lines: 26–27.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### K0916 — `/candidate/reference-semantics/semantics/tuple.k:28`

- Kind: `rule`; attributes: `none`; lines: 28–28.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### K0917 — `/candidate/reference-semantics/semantics/tuple.k:31`

- Kind: `syntax`; attributes: `none`; lines: 31–31.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### K0918 — `/candidate/reference-semantics/semantics/tuple.k:32`

- Kind: `rule`; attributes: `none`; lines: 32–34.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### K0919 — `/candidate/reference-semantics/semantics/tuple.k:35`

- Kind: `rule`; attributes: `priority`; lines: 35–41.
- Decision: REACHABLE_FRAGMENT_REVIEWED: operational/equational rule agrees with the submitted constructor path and integer/list mathematics.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### K0920 — `/candidate/reference-semantics/semantics/tuple.k:42`

- Kind: `rule`; attributes: `none`; lines: 42–42.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K0921 — `/candidate/reference-semantics/semantics/tuple.k:43`

- Kind: `rule`; attributes: `none`; lines: 43–43.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K0922 — `/candidate/reference-semantics/semantics/tuple.k:44`

- Kind: `rule`; attributes: `priority`; lines: 44–46.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0923 — `/candidate/reference-semantics/semantics/tuple.k:49`

- Kind: `syntax`; attributes: `none`; lines: 49–49.
- Decision: FIXED_DECLARATION: typing/grammar only; no conclusion introduced.

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### K0924 — `/candidate/reference-semantics/semantics/tuple.k:50`

- Kind: `rule`; attributes: `none`; lines: 50–50.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### K0925 — `/candidate/reference-semantics/semantics/tuple.k:51`

- Kind: `rule`; attributes: `none`; lines: 51–51.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### K0926 — `/candidate/reference-semantics/semantics/tuple.k:52`

- Kind: `rule`; attributes: `priority`; lines: 52–54.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### K0927 — `/candidate/reference-semantics/semantics/tuple.k:55`

- Kind: `rule`; attributes: `none`; lines: 55–56.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### K0928 — `/candidate/reference-semantics/semantics/tuple.k:57`

- Kind: `rule`; attributes: `none`; lines: 57–57.
- Decision: FIXED_UNUSED_FRAGMENT: no matching reachable redex in eat; inspected without a false-conclusion witness on the intended domain.

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### K0929 — `/candidate/verification.k:9`

- Kind: `syntax`; attributes: `function`; lines: 9–9.
- Decision: PROOF_LOCAL_NAME: eatClosure is a definitional Val symbol.

```k
  syntax Val ::= "eatClosure" [function]
```

### K0930 — `/candidate/verification.k:11`

- Kind: `rule`; attributes: `none`; lines: 11–27.
- Decision: SUPPORTED_PROOF_LOCAL_EQUATION: exact translator-derived closure constructor; checked by pinning claim.

```k
  rule eatClosure
    => closureVal(
         ("number", "need", "remaining"),
         If(
           Compare(Name("need"), CmpOp("<=", Name("remaining"))),
           Return(
             ListExpr(
               BinOp("+", Name("number"), Name("need")),
               BinOp("-", Name("remaining"), Name("need"))))
           .Stmts,
           .Stmts)
         Return(
           ListExpr(
             BinOp("+", Name("number"), Name("remaining")),
             Int(0)))
         .Stmts,
         0)
```

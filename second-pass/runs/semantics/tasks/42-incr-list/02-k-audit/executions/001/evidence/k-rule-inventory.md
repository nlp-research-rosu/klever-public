# Exhaustive local K declaration and rule inventory

Generated from the fresh scratch source. Each local `syntax`, `rule`, `claim`, `configuration`, and `context` block is included with its exact source line and reviewer disposition.

Counts: claim=2, configuration=1, context=5, rule=704, syntax=231

## `reference-semantics/semantics/assert.k`

### I0001 — rule, lines 6-6

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assert(V:Val) => .K ... </k>
```

### I0002 — rule, lines 8-10

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
```

### I0003 — rule, lines 13-15

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/bool.k`

### I0004 — rule, lines 8-8

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### I0005 — rule, lines 10-10

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### I0006 — rule, lines 11-11

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### I0007 — context, lines 16-16

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### I0008 — rule, lines 17-17

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### I0009 — rule, lines 18-18

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
```

### I0010 — rule, lines 20-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### I0011 — rule, lines 22-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### I0012 — rule, lines 24-24

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
```

### I0013 — rule, lines 29-30

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### I0014 — rule, lines 31-32

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0015 — rule, lines 35-36

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0016 — rule, lines 39-40

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0017 — rule, lines 43-44

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

## `reference-semantics/semantics/builtins.k`

### I0018 — syntax, lines 17-17

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### I0019 — syntax, lines 20-20

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= seqLen(Val) [function]
```

### I0020 — rule, lines 21-21

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### I0021 — rule, lines 22-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### I0022 — rule, lines 23-23

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### I0023 — rule, lines 24-24

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### I0024 — rule, lines 25-25

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### I0025 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### I0026 — rule, lines 32-32

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### I0027 — rule, lines 33-33

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### I0028 — rule, lines 34-34

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### I0029 — rule, lines 35-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### I0030 — syntax, lines 36-36

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### I0031 — rule, lines 37-37

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### I0032 — rule, lines 38-38

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### I0033 — rule, lines 41-41

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### I0034 — rule, lines 44-44

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### I0035 — syntax, lines 47-47

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### I0036 — rule, lines 48-48

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### I0037 — rule, lines 49-49

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### I0038 — rule, lines 50-51

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
```

### I0039 — syntax, lines 54-54

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= intOf(Val) [function]
```

### I0040 — rule, lines 55-55

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intOf(I:Int)  => I
```

### I0041 — rule, lines 56-56

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### I0042 — syntax, lines 59-59

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### I0043 — rule, lines 60-60

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### I0044 — rule, lines 61-61

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### I0045 — rule, lines 62-62

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
```

### I0046 — rule, lines 64-64

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
```

### I0047 — syntax, lines 67-67

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### I0048 — rule, lines 68-68

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### I0049 — rule, lines 69-69

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### I0050 — rule, lines 70-70

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
```

### I0051 — rule, lines 72-72

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
```

### I0052 — syntax, lines 76-76

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### I0053 — rule, lines 77-77

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### I0054 — rule, lines 78-78

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
```

### I0055 — rule, lines 80-80

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### I0056 — rule, lines 81-81

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### I0057 — rule, lines 82-83

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
```

### I0058 — syntax, lines 86-86

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### I0059 — rule, lines 87-87

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### I0060 — rule, lines 88-88

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
```

### I0061 — rule, lines 90-90

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### I0062 — rule, lines 91-91

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### I0063 — rule, lines 92-93

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
```

### I0064 — syntax, lines 97-97

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### I0065 — rule, lines 98-98

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### I0066 — rule, lines 99-99

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule maxVals(M:Int, .Vals)           => M
```

### I0067 — rule, lines 100-100

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### I0068 — syntax, lines 102-102

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### I0069 — rule, lines 103-103

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### I0070 — rule, lines 104-104

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule minVals(M:Int, .Vals)           => M
```

### I0071 — rule, lines 105-105

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### I0072 — rule, lines 108-108

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
```

### I0073 — rule, lines 111-112

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
```

### I0074 — syntax, lines 114-114

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### I0075 — rule, lines 115-115

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### I0076 — rule, lines 116-116

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### I0077 — syntax, lines 117-117

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### I0078 — rule, lines 118-118

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### I0079 — rule, lines 119-120

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
```

### I0080 — rule, lines 124-125

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### I0081 — syntax, lines 126-126

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### I0082 — rule, lines 127-127

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### I0083 — rule, lines 128-129

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### I0084 — rule, lines 132-133

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### I0085 — syntax, lines 134-134

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### I0086 — rule, lines 135-135

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### I0087 — rule, lines 136-136

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### I0088 — rule, lines 137-137

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### I0089 — rule, lines 140-140

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### I0090 — rule, lines 143-143

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### I0091 — rule, lines 144-144

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
```

### I0092 — rule, lines 148-148

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### I0093 — rule, lines 149-149

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### I0094 — rule, lines 152-152

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
```

### I0095 — rule, lines 156-156

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
```

### I0096 — syntax, lines 158-158

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### I0097 — rule, lines 159-159

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### I0098 — rule, lines 160-160

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### I0099 — rule, lines 163-163

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### I0100 — rule, lines 164-164

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### I0101 — rule, lines 167-168

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### I0102 — rule, lines 169-169

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### I0103 — rule, lines 170-170

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### I0104 — rule, lines 171-172

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### I0105 — rule, lines 173-173

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### I0106 — rule, lines 174-174

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### I0107 — rule, lines 177-177

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### I0108 — rule, lines 178-178

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### I0109 — rule, lines 179-179

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
```

### I0110 — rule, lines 187-187

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### I0111 — syntax, lines 188-188

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### I0112 — rule, lines 189-190

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### I0113 — syntax, lines 192-192

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### I0114 — syntax, lines 194-194

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### I0115 — rule, lines 195-195

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### I0116 — syntax, lines 196-196

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### I0117 — rule, lines 197-197

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### I0118 — rule, lines 198-198

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### I0119 — syntax, lines 199-199

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### I0120 — rule, lines 200-200

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### I0121 — rule, lines 201-201

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### I0122 — syntax, lines 203-203

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### I0123 — rule, lines 204-204

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### I0124 — rule, lines 205-205

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### I0125 — rule, lines 206-206

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### I0126 — rule, lines 207-207

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### I0127 — rule, lines 208-208

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### I0128 — rule, lines 209-209

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### I0129 — rule, lines 210-210

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### I0130 — rule, lines 211-211

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### I0131 — rule, lines 212-212

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### I0132 — syntax, lines 214-215

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### I0133 — rule, lines 216-216

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### I0134 — rule, lines 217-217

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### I0135 — rule, lines 218-218

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### I0136 — rule, lines 219-219

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
```

### I0137 — rule, lines 221-221

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
```

### I0138 — rule, lines 223-223

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### I0139 — syntax, lines 225-225

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### I0140 — syntax, lines 226-226

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### I0141 — rule, lines 227-227

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### I0142 — rule, lines 228-228

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### I0143 — syntax, lines 230-230

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### I0144 — rule, lines 231-231

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### I0145 — rule, lines 232-232

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### I0146 — rule, lines 233-233

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### I0147 — rule, lines 234-234

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### I0148 — rule, lines 235-235

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### I0149 — rule, lines 236-236

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### I0150 — syntax, lines 238-238

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### I0151 — rule, lines 239-239

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### I0152 — rule, lines 240-240

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### I0153 — rule, lines 241-241

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
```

### I0154 — rule, lines 243-243

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### I0155 — syntax, lines 244-244

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### I0156 — rule, lines 245-245

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### I0157 — rule, lines 246-246

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### I0158 — syntax, lines 247-247

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### I0159 — rule, lines 248-248

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### I0160 — syntax, lines 250-250

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### I0161 — rule, lines 251-251

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### I0162 — rule, lines 252-252

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### I0163 — rule, lines 253-253

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### I0164 — rule, lines 254-254

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### I0165 — syntax, lines 255-255

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### I0166 — rule, lines 256-256

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### I0167 — rule, lines 257-258

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
```

### I0168 — rule, lines 260-261

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
```

### I0169 — rule, lines 263-264

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### I0170 — syntax, lines 265-265

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### I0171 — rule, lines 266-266

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### I0172 — rule, lines 267-267

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### I0173 — rule, lines 268-268

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### I0174 — syntax, lines 269-269

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### I0175 — rule, lines 270-270

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### I0176 — rule, lines 271-271

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### I0177 — syntax, lines 272-272

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### I0178 — rule, lines 273-273

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### I0179 — rule, lines 274-274

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### I0180 — syntax, lines 279-279

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= "#md5"
```

### I0181 — rule, lines 280-281

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### I0182 — rule, lines 282-282

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### I0183 — syntax, lines 283-283

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= md5Obj(IntSeq)
```

### I0184 — rule, lines 284-284

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### I0185 — syntax, lines 285-285

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### I0186 — rule, lines 291-291

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### I0187 — rule, lines 292-292

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### I0188 — syntax, lines 293-293

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### I0189 — rule, lines 294-294

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isIntV(_:Int)         => true
```

### I0190 — rule, lines 295-295

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isIntV(_:Val)         => false [owise]
```

### I0191 — rule, lines 296-296

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isStrV(str(_:IntSeq)) => true
```

### I0192 — rule, lines 297-297

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isStrV(_:Val)         => false [owise]
```

## `reference-semantics/semantics/call.k`

### I0193 — rule, lines 16-16

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### I0194 — syntax, lines 19-19

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= #callee(Exprs)
```

### I0195 — rule, lines 20-20

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### I0196 — rule, lines 21-21

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### I0197 — rule, lines 24-24

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### I0198 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### I0199 — rule, lines 27-27

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### I0200 — rule, lines 28-28

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### I0201 — rule, lines 29-29

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### I0202 — rule, lines 30-30

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### I0203 — rule, lines 31-31

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### I0204 — rule, lines 32-32

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### I0205 — rule, lines 38-41

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0206 — rule, lines 42-44

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0207 — rule, lines 47-50

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0208 — syntax, lines 52-52

- Attributes/class: function, total
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### I0209 — rule, lines 53-55

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### I0210 — rule, lines 56-58

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0211 — rule, lines 63-65

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0212 — rule, lines 69-74

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### I0213 — rule, lines 80-85

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### I0214 — syntax, lines 87-87

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### I0215 — rule, lines 88-88

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### I0216 — rule, lines 89-93

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

## `reference-semantics/semantics/comprehension.k`

### I0217 — rule, lines 11-11

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### I0218 — rule, lines 12-12

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### I0219 — syntax, lines 14-14

- Attributes/class: macro
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### I0220 — rule, lines 15-16

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### I0221 — syntax, lines 18-18

- Attributes/class: macro, macro-rec
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### I0222 — rule, lines 19-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### I0223 — rule, lines 21-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### I0224 — syntax, lines 24-24

- Attributes/class: macro
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### I0225 — rule, lines 25-25

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### I0226 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## `reference-semantics/semantics/concrete.k`

### I0227 — rule, lines 13-14

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### I0228 — rule, lines 16-17

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### I0229 — syntax, lines 25-25

- Attributes/class: none
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  syntax Val ::= kvP(Val, Val)
```

### I0230 — syntax, lines 26-27

- Attributes/class: none
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### I0231 — rule, lines 28-30

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### I0232 — rule, lines 31-33

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### I0233 — rule, lines 34-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### I0234 — rule, lines 36-37

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### I0235 — rule, lines 38-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
```

### I0236 — syntax, lines 42-42

- Attributes/class: function
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### I0237 — rule, lines 43-43

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### I0238 — rule, lines 44-45

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
```

### I0239 — rule, lines 47-48

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
```

### I0240 — syntax, lines 51-51

- Attributes/class: function
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### I0241 — rule, lines 52-52

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### I0242 — rule, lines 53-53

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### I0243 — rule, lines 54-54

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### I0244 — syntax, lines 56-56

- Attributes/class: function, total
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### I0245 — rule, lines 57-57

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### I0246 — rule, lines 58-58

- Attributes/class: ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### I0247 — rule, lines 59-59

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot contribute to proof closure

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## `reference-semantics/semantics/controls.k`

### I0248 — rule, lines 9-11

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### I0249 — rule, lines 12-14

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### I0250 — rule, lines 20-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
```

### I0251 — rule, lines 27-29

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### I0252 — rule, lines 35-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### I0253 — rule, lines 36-36

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### I0254 — syntax, lines 37-37

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### I0255 — rule, lines 38-38

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### I0256 — rule, lines 39-41

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
```

### I0257 — rule, lines 43-43

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
```

### I0258 — rule, lines 48-48

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### I0259 — syntax, lines 51-51

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### I0260 — rule, lines 52-52

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### I0261 — rule, lines 53-53

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### I0262 — rule, lines 54-54

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### I0263 — rule, lines 57-57

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
```

### I0264 — rule, lines 59-59

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
```

### I0265 — syntax, lines 65-67

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### I0266 — rule, lines 69-69

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### I0267 — rule, lines 71-71

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### I0268 — rule, lines 72-72

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### I0269 — rule, lines 73-74

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### I0270 — rule, lines 77-77

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### I0271 — rule, lines 78-78

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### I0272 — rule, lines 79-79

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
```

### I0273 — rule, lines 81-81

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
```

### I0274 — rule, lines 85-85

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### I0275 — rule, lines 86-86

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Continue => #cont ... </k>
```

### I0276 — rule, lines 87-87

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Break => #brk ... </k>
```

### I0277 — rule, lines 88-88

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### I0278 — rule, lines 89-89

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### I0279 — rule, lines 90-90

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### I0280 — rule, lines 91-91

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### I0281 — rule, lines 95-97

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0282 — rule, lines 98-100

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0283 — rule, lines 101-103

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0284 — rule, lines 106-108

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/core.k`

### I0285 — syntax, lines 13-13

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### I0286 — syntax, lines 14-14

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### I0287 — syntax, lines 15-15

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Str    ::= str(IntSeq)
```

### I0288 — syntax, lines 18-23

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### I0289 — syntax, lines 25-34

- Attributes/class: function
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

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

### I0290 — syntax, lines 36-36

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Parent   ::= "root" | parent(Int)
```

### I0291 — syntax, lines 37-37

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Scope    ::= scope(Map, Parent)
```

### I0292 — syntax, lines 38-38

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KResult  ::= Val
```

### I0293 — syntax, lines 39-39

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### I0294 — syntax, lines 40-40

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Vals     ::= List{Val, ","}
```

### I0295 — syntax, lines 41-41

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### I0296 — syntax, lines 42-42

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### I0297 — configuration, lines 49-60

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

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

### I0298 — syntax, lines 68-68

- Attributes/class: function, total
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### I0299 — rule, lines 69-69

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isRefV(ref(_:Int)) => true
```

### I0300 — rule, lines 70-70

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isRefV(_:Val)      => false [owise]
```

### I0301 — syntax, lines 75-75

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax HeapVal ::= cellV(Val)
```

### I0302 — syntax, lines 76-76

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### I0303 — rule, lines 77-77

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### I0304 — rule, lines 78-78

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isCellRef(_:Val)          => false [owise]
```

### I0305 — rule, lines 85-88

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### I0306 — syntax, lines 95-95

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= kwV(String, Val)
```

### I0307 — syntax, lines 96-96

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #kwTag(String)
```

### I0308 — rule, lines 97-97

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### I0309 — rule, lines 98-98

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
```

### I0310 — syntax, lines 100-100

- Attributes/class: function, total
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### I0311 — rule, lines 101-101

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### I0312 — rule, lines 102-102

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isKwV(_:Val)                => false [owise]
```

### I0313 — syntax, lines 106-106

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= cellsMark(ParamNames)
```

### I0314 — syntax, lines 107-107

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### I0315 — rule, lines 108-108

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### I0316 — syntax, lines 109-109

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### I0317 — rule, lines 110-110

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule pnMember(_:String, .ParamNames) => false
```

### I0318 — rule, lines 111-111

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### I0319 — syntax, lines 113-113

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #cellW(Val, Val)
```

### I0320 — rule, lines 114-115

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### I0321 — syntax, lines 117-117

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= #alloc(Val)
```

### I0322 — rule, lines 118-120

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

### I0323 — syntax, lines 124-124

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= #loadAll(Module)
```

### I0324 — rule, lines 125-125

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### I0325 — rule, lines 126-126

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### I0326 — rule, lines 127-127

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> .Stmts => .K ... </k>
```

### I0327 — syntax, lines 130-130

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= #look(String, Int)
```

### I0328 — rule, lines 131-131

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### I0329 — rule, lines 132-133

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
```

### I0330 — rule, lines 145-147

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### I0331 — rule, lines 152-153

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
```

### I0332 — syntax, lines 157-157

- Attributes/class: function, total
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### I0333 — rule, lines 158-181

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

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

### I0334 — syntax, lines 185-185

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax ApplyK ::= toCall(Val)
```

### I0335 — syntax, lines 186-188

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### I0336 — rule, lines 189-189

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### I0337 — rule, lines 190-190

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### I0338 — rule, lines 191-191

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### I0339 — rule, lines 194-194

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### I0340 — rule, lines 195-195

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### I0341 — rule, lines 196-196

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> NoneVal      => noneV ... </k>
```

### I0342 — syntax, lines 199-199

- Attributes/class: function
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Bool ::= truthy(Val) [function]
```

### I0343 — rule, lines 200-200

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule truthy(B:Bool)          => B
```

### I0344 — rule, lines 201-201

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule truthy(noneV)           => false
```

### I0345 — rule, lines 202-202

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### I0346 — rule, lines 203-203

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### I0347 — rule, lines 204-204

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### I0348 — rule, lines 205-205

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### I0349 — syntax, lines 208-208

- Attributes/class: function
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### I0350 — syntax, lines 209-209

- Attributes/class: function
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### I0351 — syntax, lines 210-210

- Attributes/class: function
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### I0352 — syntax, lines 213-213

- Attributes/class: function, total
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### I0353 — rule, lines 214-214

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### I0354 — rule, lines 215-215

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### I0355 — syntax, lines 217-217

- Attributes/class: function, total
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### I0356 — rule, lines 218-218

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### I0357 — rule, lines 219-219

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### I0358 — syntax, lines 223-223

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### I0359 — rule, lines 224-224

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule vsLen(.ValSeq)                => 0
```

### I0360 — rule, lines 225-225

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### I0361 — syntax, lines 227-227

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### I0362 — rule, lines 228-228

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isLen(.IntSeq)                => 0
```

### I0363 — rule, lines 229-229

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### I0364 — syntax, lines 233-233

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### I0365 — rule, lines 234-234

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### I0366 — rule, lines 235-235

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### I0367 — rule, lines 236-236

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
```

### I0368 — rule, lines 238-238

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
```

## `reference-semantics/semantics/dict.k`

### I0369 — syntax, lines 20-20

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### I0370 — syntax, lines 23-25

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### I0371 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### I0372 — rule, lines 27-27

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### I0373 — rule, lines 28-29

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### I0374 — rule, lines 30-31

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### I0375 — rule, lines 32-33

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### I0376 — syntax, lines 37-37

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### I0377 — rule, lines 38-38

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### I0378 — rule, lines 39-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### I0379 — rule, lines 40-40

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### I0380 — syntax, lines 43-43

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### I0381 — rule, lines 44-44

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### I0382 — rule, lines 45-45

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### I0383 — syntax, lines 49-49

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### I0384 — rule, lines 50-50

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
```

### I0385 — rule, lines 52-52

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
```

### I0386 — rule, lines 54-54

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### I0387 — rule, lines 58-60

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### I0388 — rule, lines 63-63

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### I0389 — syntax, lines 64-64

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### I0390 — rule, lines 65-66

- Attributes/class: priority(45), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### I0391 — syntax, lines 70-70

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### I0392 — rule, lines 71-71

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### I0393 — syntax, lines 76-76

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #dsetK(String, Val)
```

### I0394 — rule, lines 77-77

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### I0395 — rule, lines 78-80

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
```

### I0396 — rule, lines 82-84

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### I0397 — syntax, lines 86-86

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### I0398 — rule, lines 87-88

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### I0399 — syntax, lines 90-90

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### I0400 — rule, lines 91-91

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### I0401 — rule, lines 92-92

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### I0402 — rule, lines 95-96

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### I0403 — syntax, lines 97-97

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### I0404 — rule, lines 98-98

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### I0405 — rule, lines 99-100

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### I0406 — syntax, lines 101-101

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### I0407 — rule, lines 102-102

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### I0408 — rule, lines 103-103

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## `reference-semantics/semantics/float.k`

### I0409 — syntax, lines 20-20

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= Float
```

### I0410 — rule, lines 21-21

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Float(F:Float) => F ... </k>
```

### I0411 — syntax, lines 24-24

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### I0412 — rule, lines 25-25

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### I0413 — rule, lines 27-27

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### I0414 — syntax, lines 30-30

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### I0415 — rule, lines 31-31

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### I0416 — rule, lines 32-32

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### I0417 — syntax, lines 37-37

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### I0418 — rule, lines 38-38

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### I0419 — rule, lines 39-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### I0420 — rule, lines 43-43

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### I0421 — rule, lines 44-44

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### I0422 — syntax, lines 50-50

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### I0423 — rule, lines 51-51

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### I0424 — rule, lines 52-52

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### I0425 — syntax, lines 54-54

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### I0426 — rule, lines 55-55

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### I0427 — rule, lines 56-56

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### I0428 — rule, lines 61-61

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Import(_:String) => .K ... </k>
```

### I0429 — syntax, lines 65-65

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= "#mathCeil"
```

### I0430 — rule, lines 66-66

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### I0431 — rule, lines 67-67

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### I0432 — syntax, lines 70-70

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= "#mathFloor"
```

### I0433 — rule, lines 71-71

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### I0434 — rule, lines 72-72

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### I0435 — syntax, lines 73-73

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### I0436 — rule, lines 74-74

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### I0437 — rule, lines 75-75

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### I0438 — rule, lines 78-78

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### I0439 — rule, lines 79-79

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### I0440 — syntax, lines 82-82

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### I0441 — rule, lines 83-83

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### I0442 — rule, lines 84-84

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### I0443 — rule, lines 85-85

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### I0444 — syntax, lines 86-86

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### I0445 — rule, lines 87-87

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule toF(F:Float) => F        [concrete]
```

### I0446 — rule, lines 88-88

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### I0447 — syntax, lines 93-93

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### I0448 — rule, lines 94-94

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### I0449 — rule, lines 95-95

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### I0450 — rule, lines 99-99

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### I0451 — syntax, lines 103-103

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### I0452 — rule, lines 104-104

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### I0453 — rule, lines 105-105

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### I0454 — syntax, lines 107-107

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### I0455 — rule, lines 108-108

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### I0456 — rule, lines 109-109

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### I0457 — syntax, lines 111-111

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### I0458 — rule, lines 112-112

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### I0459 — rule, lines 113-113

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### I0460 — syntax, lines 115-115

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### I0461 — rule, lines 116-116

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### I0462 — rule, lines 117-117

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### I0463 — syntax, lines 119-119

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### I0464 — rule, lines 120-120

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### I0465 — rule, lines 121-121

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### I0466 — syntax, lines 125-125

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### I0467 — rule, lines 126-126

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### I0468 — rule, lines 127-127

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### I0469 — rule, lines 128-128

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### I0470 — rule, lines 129-129

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### I0471 — rule, lines 132-132

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### I0472 — rule, lines 133-133

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### I0473 — rule, lines 134-134

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### I0474 — rule, lines 135-135

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### I0475 — rule, lines 136-136

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### I0476 — rule, lines 137-137

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### I0477 — rule, lines 138-138

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### I0478 — rule, lines 139-139

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### I0479 — syntax, lines 142-142

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### I0480 — rule, lines 143-143

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### I0481 — rule, lines 144-144

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### I0482 — rule, lines 145-145

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### I0483 — rule, lines 146-146

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### I0484 — rule, lines 147-147

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### I0485 — rule, lines 148-148

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### I0486 — rule, lines 149-149

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### I0487 — rule, lines 150-150

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### I0488 — rule, lines 151-151

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### I0489 — rule, lines 154-154

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### I0490 — rule, lines 155-155

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### I0491 — syntax, lines 160-160

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### I0492 — rule, lines 161-161

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### I0493 — rule, lines 162-163

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
```

### I0494 — syntax, lines 165-165

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### I0495 — rule, lines 166-166

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### I0496 — syntax, lines 167-167

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### I0497 — rule, lines 168-168

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### I0498 — rule, lines 169-169

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### I0499 — rule, lines 170-170

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### I0500 — rule, lines 171-171

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
```

### I0501 — syntax, lines 173-173

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### I0502 — rule, lines 174-174

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracPart(.IntSeq) => 0
```

### I0503 — rule, lines 175-175

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### I0504 — rule, lines 176-176

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### I0505 — rule, lines 177-177

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### I0506 — rule, lines 178-178

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### I0507 — syntax, lines 179-179

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### I0508 — rule, lines 180-180

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracScale(.IntSeq) => 1
```

### I0509 — rule, lines 181-181

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### I0510 — rule, lines 182-182

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### I0511 — rule, lines 183-183

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### I0512 — rule, lines 184-184

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### I0513 — rule, lines 185-185

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### I0514 — rule, lines 186-186

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### I0515 — rule, lines 187-187

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### I0516 — syntax, lines 190-190

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### I0517 — rule, lines 191-191

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### I0518 — rule, lines 192-192

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### I0519 — syntax, lines 195-195

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### I0520 — rule, lines 196-196

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### I0521 — rule, lines 197-197

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### I0522 — rule, lines 198-198

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### I0523 — rule, lines 199-199

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### I0524 — rule, lines 200-200

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### I0525 — rule, lines 201-201

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### I0526 — rule, lines 202-202

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### I0527 — rule, lines 203-203

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### I0528 — rule, lines 204-204

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### I0529 — rule, lines 205-205

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### I0530 — rule, lines 206-206

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### I0531 — syntax, lines 209-209

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### I0532 — rule, lines 210-210

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### I0533 — rule, lines 211-211

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### I0534 — rule, lines 213-213

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### I0535 — rule, lines 214-214

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### I0536 — syntax, lines 217-217

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### I0537 — rule, lines 218-222

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### I0538 — syntax, lines 223-223

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### I0539 — rule, lines 224-226

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### I0540 — rule, lines 227-227

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### I0541 — rule, lines 228-228

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### I0542 — syntax, lines 230-230

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### I0543 — rule, lines 231-231

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### I0544 — syntax, lines 232-232

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= "#mathSqrt"
```

### I0545 — rule, lines 233-233

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### I0546 — rule, lines 234-234

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### I0547 — rule, lines 235-235

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### I0548 — syntax, lines 243-243

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### I0549 — rule, lines 244-244

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### I0550 — rule, lines 245-245

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### I0551 — rule, lines 246-246

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### I0552 — rule, lines 247-247

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
```

### I0553 — syntax, lines 250-250

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### I0554 — rule, lines 251-251

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### I0555 — rule, lines 252-252

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### I0556 — rule, lines 253-253

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### I0557 — rule, lines 254-254

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
```

### I0558 — syntax, lines 261-261

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### I0559 — rule, lines 262-263

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
```

### I0560 — rule, lines 265-265

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### I0561 — rule, lines 266-266

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### I0562 — rule, lines 267-268

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
```

### I0563 — rule, lines 270-271

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
```

## `reference-semantics/semantics/functions.k`

### I0564 — syntax, lines 8-11

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### I0565 — rule, lines 14-16

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### I0566 — syntax, lines 18-18

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### I0567 — rule, lines 19-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### I0568 — syntax, lines 27-27

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### I0569 — syntax, lines 31-32

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### I0570 — rule, lines 33-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### I0571 — rule, lines 36-40

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### I0572 — rule, lines 42-45

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### I0573 — rule, lines 47-49

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### I0574 — rule, lines 50-52

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### I0575 — rule, lines 53-57

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### I0576 — rule, lines 59-60

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### I0577 — rule, lines 63-63

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### I0578 — rule, lines 64-66

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### I0579 — rule, lines 68-71

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### I0580 — rule, lines 78-79

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### I0581 — rule, lines 80-81

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### I0582 — rule, lines 85-90

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## `reference-semantics/semantics/int.k`

### I0583 — rule, lines 7-7

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### I0584 — rule, lines 9-9

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### I0585 — rule, lines 11-11

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### I0586 — rule, lines 12-12

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### I0587 — rule, lines 13-13

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### I0588 — rule, lines 14-14

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### I0589 — rule, lines 15-15

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### I0590 — rule, lines 16-16

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### I0591 — rule, lines 17-17

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### I0592 — syntax, lines 19-19

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### I0593 — rule, lines 20-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### I0594 — rule, lines 22-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### I0595 — rule, lines 23-23

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### I0596 — rule, lines 24-24

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### I0597 — rule, lines 25-25

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### I0598 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### I0599 — rule, lines 27-27

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## `reference-semantics/semantics/iter.k`

### I0600 — syntax, lines 8-8

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## `reference-semantics/semantics/list.k`

### I0601 — rule, lines 9-9

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### I0602 — rule, lines 10-10

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### I0603 — syntax, lines 13-13

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax ApplyK ::= "toList"
```

### I0604 — rule, lines 14-14

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### I0605 — rule, lines 15-15

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### I0606 — syntax, lines 18-18

- Attributes/class: function, total
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### I0607 — rule, lines 19-19

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### I0608 — rule, lines 20-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### I0609 — rule, lines 24-25

- Attributes/class: priority(45), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### I0610 — rule, lines 27-27

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### I0611 — rule, lines 28-28

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### I0612 — syntax, lines 33-33

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### I0613 — rule, lines 34-34

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule hasRefVS(.ValSeq)                => false
```

### I0614 — rule, lines 35-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### I0615 — syntax, lines 37-38

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### I0616 — rule, lines 39-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### I0617 — rule, lines 40-40

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### I0618 — rule, lines 41-41

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### I0619 — rule, lines 42-43

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### I0620 — rule, lines 45-45

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
```

### I0621 — rule, lines 47-47

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
```

### I0622 — rule, lines 49-49

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### I0623 — rule, lines 50-50

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### I0624 — rule, lines 53-55

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### I0625 — syntax, lines 58-58

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### I0626 — rule, lines 59-59

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### I0627 — rule, lines 60-60

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### I0628 — rule, lines 61-61

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### I0629 — rule, lines 62-62

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### I0630 — rule, lines 63-63

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
```

### I0631 — rule, lines 65-65

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
```

### I0632 — rule, lines 67-67

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## `reference-semantics/semantics/methods.k`

### I0633 — syntax, lines 10-10

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### I0634 — rule, lines 13-13

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### I0635 — rule, lines 14-14

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### I0636 — rule, lines 15-15

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### I0637 — rule, lines 16-16

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### I0638 — rule, lines 19-19

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### I0639 — rule, lines 20-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### I0640 — rule, lines 21-21

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### I0641 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### I0642 — syntax, lines 27-27

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### I0643 — rule, lines 28-28

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### I0644 — rule, lines 29-29

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### I0645 — rule, lines 30-31

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### I0646 — rule, lines 34-34

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### I0647 — syntax, lines 35-35

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### I0648 — rule, lines 36-36

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### I0649 — rule, lines 37-37

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
```

### I0650 — rule, lines 39-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
```

### I0651 — syntax, lines 41-41

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### I0652 — rule, lines 42-42

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### I0653 — rule, lines 43-43

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### I0654 — rule, lines 44-44

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### I0655 — rule, lines 47-47

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### I0656 — syntax, lines 48-48

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### I0657 — rule, lines 49-49

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### I0658 — rule, lines 50-50

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### I0659 — rule, lines 51-51

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### I0660 — syntax, lines 52-52

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### I0661 — rule, lines 53-53

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### I0662 — rule, lines 54-54

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### I0663 — rule, lines 55-55

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### I0664 — rule, lines 58-58

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### I0665 — rule, lines 61-61

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### I0666 — rule, lines 64-64

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### I0667 — syntax, lines 65-65

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### I0668 — rule, lines 66-66

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### I0669 — rule, lines 67-67

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### I0670 — rule, lines 68-68

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### I0671 — rule, lines 72-74

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### I0672 — syntax, lines 75-75

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### I0673 — rule, lines 76-76

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### I0674 — rule, lines 77-77

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
```

### I0675 — rule, lines 79-79

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
```

### I0676 — syntax, lines 82-82

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### I0677 — rule, lines 83-83

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### I0678 — rule, lines 84-84

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### I0679 — syntax, lines 85-85

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### I0680 — rule, lines 86-86

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### I0681 — rule, lines 89-91

- Attributes/class: priority(39), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### I0682 — rule, lines 94-96

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### I0683 — syntax, lines 97-97

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### I0684 — rule, lines 98-98

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### I0685 — rule, lines 99-99

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
```

### I0686 — rule, lines 101-101

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
```

### I0687 — rule, lines 104-105

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### I0688 — syntax, lines 106-106

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### I0689 — rule, lines 107-107

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### I0690 — rule, lines 108-108

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### I0691 — rule, lines 109-109

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### I0692 — syntax, lines 112-112

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### I0693 — rule, lines 113-113

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### I0694 — syntax, lines 115-115

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### I0695 — rule, lines 116-116

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### I0696 — syntax, lines 118-118

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### I0697 — rule, lines 119-119

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### I0698 — syntax, lines 121-121

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### I0699 — rule, lines 122-122

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### I0700 — syntax, lines 124-124

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### I0701 — rule, lines 125-125

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule hasUpper(.IntSeq) => false
```

### I0702 — rule, lines 126-126

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### I0703 — syntax, lines 128-128

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### I0704 — rule, lines 129-129

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule hasLower(.IntSeq) => false
```

### I0705 — rule, lines 130-130

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### I0706 — syntax, lines 132-132

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### I0707 — rule, lines 133-133

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule allAlpha(.IntSeq) => true
```

### I0708 — rule, lines 134-134

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### I0709 — syntax, lines 136-136

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### I0710 — rule, lines 137-137

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule allDigit(.IntSeq) => true
```

### I0711 — rule, lines 138-138

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### I0712 — syntax, lines 140-140

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### I0713 — rule, lines 142-142

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### I0714 — rule, lines 143-143

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule lowerC(C:Int) => C         [owise]
```

### I0715 — syntax, lines 145-145

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= upperC(Int) [function, total]
```

### I0716 — rule, lines 146-146

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### I0717 — rule, lines 147-147

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule upperC(C:Int) => C         [owise]
```

### I0718 — syntax, lines 149-149

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= swapC(Int) [function, total]
```

### I0719 — rule, lines 150-150

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### I0720 — rule, lines 151-151

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### I0721 — rule, lines 152-152

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule swapC(C:Int) => C         [owise]
```

### I0722 — syntax, lines 154-154

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### I0723 — rule, lines 155-155

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### I0724 — rule, lines 156-156

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### I0725 — syntax, lines 158-158

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### I0726 — rule, lines 159-159

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### I0727 — rule, lines 160-160

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### I0728 — syntax, lines 162-162

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### I0729 — rule, lines 163-163

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### I0730 — rule, lines 164-164

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### I0731 — syntax, lines 166-166

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### I0732 — rule, lines 167-167

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### I0733 — rule, lines 168-168

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### I0734 — rule, lines 169-169

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## `reference-semantics/semantics/operators.k`

### I0735 — rule, lines 10-10

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### I0736 — rule, lines 12-12

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### I0737 — context, lines 15-15

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  context Compare(HOLE, _)
```

### I0738 — context, lines 16-16

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### I0739 — rule, lines 17-17

- Attributes/class: owise, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### I0740 — rule, lines 19-19

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### I0741 — rule, lines 20-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### I0742 — rule, lines 25-27

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0743 — rule, lines 28-29

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0744 — rule, lines 34-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0745 — rule, lines 38-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### I0746 — rule, lines 44-46

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/range.k`

### I0747 — syntax, lines 9-9

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### I0748 — rule, lines 10-10

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### I0749 — syntax, lines 12-12

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### I0750 — rule, lines 13-13

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
```

### I0751 — rule, lines 15-15

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
```

### I0752 — rule, lines 17-17

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
```

### I0753 — rule, lines 20-21

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
```

### I0754 — rule, lines 23-23

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
```

## `reference-semantics/semantics/set.k`

### I0755 — syntax, lines 8-8

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= setV(IntSeq)
```

### I0756 — syntax, lines 11-11

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### I0757 — rule, lines 12-12

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### I0758 — rule, lines 13-13

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### I0759 — syntax, lines 16-17

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### I0760 — rule, lines 18-18

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### I0761 — rule, lines 19-19

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### I0762 — rule, lines 20-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
```

### I0763 — rule, lines 22-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
```

### I0764 — syntax, lines 25-25

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### I0765 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### I0766 — rule, lines 27-27

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### I0767 — syntax, lines 31-31

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### I0768 — rule, lines 32-32

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### I0769 — rule, lines 33-33

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### I0770 — syntax, lines 35-35

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### I0771 — rule, lines 36-36

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### I0772 — rule, lines 39-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## `reference-semantics/semantics/sort.k`

### I0773 — syntax, lines 18-18

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### I0774 — syntax, lines 19-19

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### I0775 — rule, lines 20-20

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### I0776 — rule, lines 21-21

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### I0777 — rule, lines 22-22

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### I0778 — rule, lines 23-23

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### I0779 — rule, lines 24-24

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### I0780 — syntax, lines 26-26

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### I0781 — rule, lines 27-27

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### I0782 — rule, lines 28-28

- Attributes/class: concrete, ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### I0783 — rule, lines 29-29

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
```

### I0784 — rule, lines 31-31

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
```

### I0785 — rule, lines 36-37

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### I0786 — rule, lines 40-42

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### I0787 — syntax, lines 49-49

- Attributes/class: function, total, opaque-symbol
- Disposition: ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from solution.mpy reaches it, so it cannot affect either claim

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### I0788 — syntax, lines 51-52

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### I0789 — rule, lines 53-53

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### I0790 — rule, lines 54-54

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### I0791 — rule, lines 55-55

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### I0792 — syntax, lines 57-57

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### I0793 — rule, lines 58-58

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule condRev(S:ValSeq, false) => S
```

### I0794 — rule, lines 59-59

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### I0795 — rule, lines 61-62

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### I0796 — rule, lines 63-64

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### I0797 — rule, lines 65-66

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

## `reference-semantics/semantics/str.k`

### I0798 — rule, lines 8-8

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### I0799 — rule, lines 9-10

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### I0800 — syntax, lines 13-13

- Attributes/class: function
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### I0801 — rule, lines 14-14

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### I0802 — rule, lines 15-15

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule strToCodes("") => .IntSeq
```

### I0803 — rule, lines 16-16

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
```

### I0804 — syntax, lines 20-20

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### I0805 — rule, lines 21-21

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### I0806 — rule, lines 22-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### I0807 — rule, lines 24-24

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### I0808 — rule, lines 25-25

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### I0809 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### I0810 — rule, lines 29-29

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### I0811 — rule, lines 30-30

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### I0812 — syntax, lines 32-32

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### I0813 — rule, lines 33-33

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### I0814 — rule, lines 34-34

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### I0815 — rule, lines 35-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### I0816 — syntax, lines 37-37

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### I0817 — rule, lines 38-38

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### I0818 — rule, lines 39-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### I0819 — rule, lines 40-40

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
```

### I0820 — syntax, lines 48-48

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### I0821 — rule, lines 49-49

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### I0822 — rule, lines 50-50

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### I0823 — rule, lines 51-51

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### I0824 — rule, lines 52-52

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### I0825 — rule, lines 53-53

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### I0826 — rule, lines 54-54

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### I0827 — rule, lines 56-56

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### I0828 — rule, lines 57-57

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### I0829 — rule, lines 58-58

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### I0830 — rule, lines 59-59

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## `reference-semantics/semantics/subscript.k`

### I0831 — syntax, lines 11-11

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### I0832 — rule, lines 12-12

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### I0833 — rule, lines 13-13

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
```

### I0834 — syntax, lines 16-16

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### I0835 — rule, lines 17-17

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### I0836 — rule, lines 18-18

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
```

### I0837 — syntax, lines 21-21

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### I0838 — rule, lines 22-22

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### I0839 — rule, lines 23-23

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### I0840 — context, lines 27-27

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  context Subscript(HOLE, _)
```

### I0841 — context, lines 28-28

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  context Subscript(_:Val, HOLE:Expr)
```

### I0842 — rule, lines 31-33

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0843 — rule, lines 35-35

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### I0844 — syntax, lines 37-37

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### I0845 — rule, lines 38-38

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### I0846 — rule, lines 39-39

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### I0847 — rule, lines 40-41

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### I0848 — syntax, lines 44-47

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### I0849 — syntax, lines 49-49

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### I0850 — rule, lines 50-50

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### I0851 — rule, lines 51-51

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### I0852 — rule, lines 52-52

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### I0853 — rule, lines 54-54

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### I0854 — rule, lines 55-55

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### I0855 — rule, lines 56-56

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### I0856 — rule, lines 58-60

- Attributes/class: priority(45), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### I0857 — rule, lines 61-61

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### I0858 — syntax, lines 63-63

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### I0859 — rule, lines 64-65

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### I0860 — rule, lines 66-67

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### I0861 — rule, lines 68-69

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### I0862 — syntax, lines 72-72

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### I0863 — rule, lines 73-73

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStep(noB)          => 1
```

### I0864 — rule, lines 74-74

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStep(someB(S:Int)) => S
```

### I0865 — syntax, lines 76-76

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### I0866 — rule, lines 77-77

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
```

### I0867 — rule, lines 79-79

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
```

### I0868 — rule, lines 81-81

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### I0869 — syntax, lines 83-83

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### I0870 — rule, lines 84-84

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
```

### I0871 — rule, lines 86-86

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
```

### I0872 — rule, lines 88-88

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### I0873 — syntax, lines 90-90

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### I0874 — rule, lines 91-91

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
```

### I0875 — rule, lines 93-93

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
```

### I0876 — syntax, lines 96-96

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### I0877 — rule, lines 97-97

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule clampLo(J:Int, _STEP:Int) => J
```

### I0878 — rule, lines 99-99

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
```

### I0879 — syntax, lines 102-102

- Attributes/class: function, total
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### I0880 — rule, lines 103-103

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
```

### I0881 — rule, lines 105-105

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
```

### I0882 — syntax, lines 109-109

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### I0883 — rule, lines 110-111

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
```

### I0884 — rule, lines 113-113

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
```

### I0885 — syntax, lines 116-116

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### I0886 — rule, lines 117-118

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
```

### I0887 — rule, lines 120-120

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
```

## `reference-semantics/semantics/syntax.k`

### I0888 — syntax, lines 9-30

- Attributes/class: macro, strict, seqstrict
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

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

### I0889 — syntax, lines 32-32

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### I0890 — syntax, lines 33-33

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### I0891 — syntax, lines 34-34

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Entries  ::= List{Entry, ","}
```

### I0892 — syntax, lines 35-35

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### I0893 — syntax, lines 36-36

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax CompFors ::= List{CompFor, ""}
```

### I0894 — syntax, lines 37-37

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Exprs    ::= List{Expr, ","}
```

### I0895 — syntax, lines 38-38

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### I0896 — syntax, lines 39-39

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Bound    ::= Expr | "NoBound"
```

### I0897 — syntax, lines 41-54

- Attributes/class: strict
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

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

### I0898 — syntax, lines 56-56

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### I0899 — syntax, lines 57-57

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### I0900 — syntax, lines 58-58

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### I0901 — syntax, lines 59-59

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### I0902 — syntax, lines 60-60

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax ParamNames ::= List{String, ","}
```

### I0903 — syntax, lines 61-61

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## `reference-semantics/semantics/tuple.k`

### I0904 — rule, lines 10-10

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### I0905 — rule, lines 11-11

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### I0906 — syntax, lines 14-14

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax ApplyK ::= "toTuple"
```

### I0907 — rule, lines 15-15

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### I0908 — rule, lines 16-16

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### I0909 — rule, lines 18-18

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### I0910 — rule, lines 20-20

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### I0911 — rule, lines 21-21

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### I0912 — rule, lines 23-23

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### I0913 — syntax, lines 24-24

- Attributes/class: function
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### I0914 — rule, lines 25-25

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### I0915 — rule, lines 26-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
```

### I0916 — rule, lines 28-28

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### I0917 — syntax, lines 31-31

- Attributes/class: none
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### I0918 — rule, lines 32-34

- Attributes/class: ordinary-rule
- Disposition: ACCEPT REACHABLE — fixed supplied operational/definitional semantics; binding, order, state, control, and overlaps checked on the real path

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### I0919 — rule, lines 35-37

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### I0920 — rule, lines 42-42

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### I0921 — rule, lines 43-43

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### I0922 — rule, lines 44-46

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0923 — syntax, lines 49-49

- Attributes/class: none
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### I0924 — rule, lines 50-50

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### I0925 — rule, lines 51-51

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### I0926 — rule, lines 52-54

- Attributes/class: priority(40), ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### I0927 — rule, lines 55-56

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### I0928 — rule, lines 57-57

- Attributes/class: ordinary-rule
- Disposition: ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent from solution.mpy; no matching term can arise on either reviewed claim

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## `reference-semantics/semantics.k`

No local syntax/rule/claim/configuration/context declarations.

## `verification.k`

### I0929 — syntax, lines 7-7

- Attributes/class: function, total
- Disposition: ACCEPT — proof-local declaration supporting the reviewed rules

```k
  syntax Module ::= "solutionProgram" [function, total]
```

### I0930 — rule, lines 8-18

- Attributes/class: ordinary-rule
- Disposition: ACCEPT — truthful terminating definition; complete for its declared domain

```k
  rule solutionProgram =>
    Module(
      FuncDef("incr_list", Params("l"),
        Expr(Str("Return list with elements incremented by 1."))
        Assign(Name("result"), ListExpr(.Exprs))
        For(Name("x"), Name("l"),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              BinOp("+", Name("x"), Int(1)))))
        Return(Name("result"))))
```

### I0931 — syntax, lines 22-23

- Attributes/class: function, total
- Disposition: ACCEPT — proof-local declaration supporting the reviewed rules

```k
  syntax ValSeq ::= intVals(IntSeq)
                  | incrVals(IntSeq) [function, total]
```

### I0932 — rule, lines 24-24

- Attributes/class: ordinary-rule
- Disposition: ACCEPT — truthful terminating definition; complete for its declared domain

```k
  rule incrVals(.IntSeq) => .ValSeq
```

### I0933 — rule, lines 25-26

- Attributes/class: ordinary-rule
- Disposition: ACCEPT — truthful terminating definition; complete for its declared domain

```k
  rule incrVals(iCons(I:Int, IS:IntSeq)) =>
    vCons(I +Int 1, incrVals(IS))
```

### I0934 — rule, lines 30-30

- Attributes/class: ordinary-rule
- Disposition: ACCEPT — definitional iterator equations for the fresh intVals input embedding; exact #iterNext context, exhaustive IntSeq constructors, no state/control changes

```k
  rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>
```

### I0935 — rule, lines 31-32

- Attributes/class: ordinary-rule
- Disposition: ACCEPT — definitional iterator equations for the fresh intVals input embedding; exact #iterNext context, exhaustive IntSeq constructors, no state/control changes

```k
  rule <k> #iterNext(list(intVals(iCons(I:Int, IS:IntSeq))))
        => #iterYield(I, list(intVals(IS))) ... </k>
```

### I0936 — syntax, lines 34-34

- Attributes/class: function, total
- Disposition: ACCEPT — proof-local declaration supporting the reviewed rules

```k
  syntax Stmts ::= "incrLoopBody" [function, total]
```

### I0937 — rule, lines 35-40

- Attributes/class: ordinary-rule
- Disposition: ACCEPT — truthful terminating definition; complete for its declared domain

```k
  rule incrLoopBody =>
    Expr(
      Call(
        Attribute(Name("result"), "append"),
        BinOp("+", Name("x"), Int(1))))
    .Stmts
```

### I0938 — rule, lines 44-46

- Attributes/class: simplification
- Disposition: ACCEPT — standard right-association/right-identity laws for finite sequences

```k
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]
```

### I0939 — rule, lines 47-48

- Attributes/class: simplification
- Disposition: ACCEPT — standard right-association/right-identity laws for finite sequences

```k
  rule valSeqConcat(A:ValSeq, .ValSeq) => A
    [simplification]
```

### I0940 — syntax, lines 52-52

- Attributes/class: none
- Disposition: ACCEPT — proof-local declaration supporting the reviewed rules

```k
  syntax KItem ::= "#observeResult"
```

### I0941 — rule, lines 53-54

- Attributes/class: ordinary-rule
- Disposition: ACCEPT — proof-harness observer; exact ref then marker context, reads the addressed heap value and preserves the remaining continuation/cells

```k
  rule <k> ref(H:Int) ~> #observeResult => V ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

## `spec.k`

### I0942 — claim, lines 8-27

- Attributes/class: none
- Disposition: TARGET CLAIM — adequacy and closure reviewed separately

```k
  claim [incr-loop]:
    <k>
      #loop(list(intVals(IS:IntSeq)), Name("x"), incrLoopBody)
      ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(("l" |-> _INPUT:Val)
                   ("result" |-> ref(H:Int))
                   ("x" |-> (_OLD_X:Val => ?_FINAL_X:Val)),
                   _PAR:Parent)
       _REST_SCOPES:Map)
    </scopes>
    <heap>
      H |-> list(
        PREFIX:ValSeq
        => valSeqConcat(PREFIX, incrVals(IS)))
      _REST_HEAP:Map
    </heap>
```

### I0943 — claim, lines 30-50

- Attributes/class: none
- Disposition: TARGET CLAIM — adequacy and closure reviewed separately

```k
  claim [incr-list]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("incr_list"), list(intVals(IS:IntSeq)))
      ~> #observeResult
      => list(?RESULT:ValSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?_FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_FINAL_HEAP:Map </heap>
    <heapLoc> 0 => ?_FINAL_HEAP_LOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    ensures ?RESULT ==K incrVals(IS)
    [depends(incr-loop)]
```

TOTAL_INVENTORY_ITEMS=943

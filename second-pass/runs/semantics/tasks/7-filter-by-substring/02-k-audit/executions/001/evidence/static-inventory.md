# Exhaustive K declaration inventory

This lexical inventory covers the supplied semantics, every supplied helper
K file, `verification.k`, and `spec.k`. Source blocks are copied from the
scratch tree; trust and soundness decisions are in `REVIEW.md`.

```json
{
  "class_counts": {
    "claim": 2,
    "concrete-rule": 35,
    "configuration": 1,
    "context": 5,
    "function-declaration": 149,
    "macro-syntax": 7,
    "ordinary-rule": 710,
    "owise-rule": 26,
    "priority-rule": 47,
    "proof-opaque-symbol-declaration": 22,
    "rule": 712,
    "simplification-rule": 2,
    "symbol-declaration": 25,
    "syntax": 237,
    "total-declaration": 110
  },
  "file_counts": {
    "reference-semantics/semantics/assert.k": 3,
    "reference-semantics/semantics/bool.k": 14,
    "reference-semantics/semantics/builtins.k": 175,
    "reference-semantics/semantics/call.k": 24,
    "reference-semantics/semantics/comprehension.k": 10,
    "reference-semantics/semantics/concrete.k": 21,
    "reference-semantics/semantics/controls.k": 37,
    "reference-semantics/semantics/core.k": 84,
    "reference-semantics/semantics/dict.k": 40,
    "reference-semantics/semantics/float.k": 155,
    "reference-semantics/semantics/functions.k": 19,
    "reference-semantics/semantics/int.k": 17,
    "reference-semantics/semantics/iter.k": 1,
    "reference-semantics/semantics/list.k": 32,
    "reference-semantics/semantics/methods.k": 102,
    "reference-semantics/semantics/operators.k": 12,
    "reference-semantics/semantics/range.k": 8,
    "reference-semantics/semantics/set.k": 18,
    "reference-semantics/semantics/sort.k": 25,
    "reference-semantics/semantics/str.k": 33,
    "reference-semantics/semantics/subscript.k": 57,
    "reference-semantics/semantics/syntax.k": 16,
    "reference-semantics/semantics/tuple.k": 25,
    "spec.k": 2,
    "verification.k": 27
  },
  "kind_counts": {
    "claim": 2,
    "configuration": 1,
    "context": 5,
    "rule": 712,
    "syntax": 237
  },
  "record_count": 957
}
```

## `reference-semantics/semantics/assert.k`

### D0001 — lines 6–7

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### D0002 — lines 8–11

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### D0003 — lines 13–15

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/bool.k`

### D0004 — lines 8–8

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### D0005 — lines 10–10

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### D0006 — lines 11–11

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### D0007 — lines 16–16

Kind/classes: `context`; context. Attributes: none.

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### D0008 — lines 17–17

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### D0009 — lines 18–19

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### D0010 — lines 20–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### D0011 — lines 22–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### D0012 — lines 24–25

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

### D0013 — lines 29–30

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### D0014 — lines 31–34

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### D0015 — lines 35–38

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### D0016 — lines 39–42

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### D0017 — lines 43–46

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## `reference-semantics/semantics/builtins.k`

### D0018 — lines 17–17

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### D0019 — lines 20–20

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= seqLen(Val) [function]
```

### D0020 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### D0021 — lines 22–22

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### D0022 — lines 23–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### D0023 — lines 24–24

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### D0024 — lines 25–25

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### D0025 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### D0026 — lines 32–32

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### D0027 — lines 33–33

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### D0028 — lines 34–34

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### D0029 — lines 35–35

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### D0030 — lines 36–36

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### D0031 — lines 37–37

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### D0032 — lines 38–38

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### D0033 — lines 41–41

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### D0034 — lines 44–44

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### D0035 — lines 47–47

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### D0036 — lines 48–48

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### D0037 — lines 49–49

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### D0038 — lines 50–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### D0039 — lines 54–54

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= intOf(Val) [function]
```

### D0040 — lines 55–55

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intOf(I:Int)  => I
```

### D0041 — lines 56–56

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### D0042 — lines 59–59

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### D0043 — lines 60–60

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### D0044 — lines 61–61

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### D0045 — lines 62–63

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### D0046 — lines 64–65

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### D0047 — lines 67–67

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### D0048 — lines 68–68

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### D0049 — lines 69–69

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### D0050 — lines 70–71

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### D0051 — lines 72–73

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

### D0052 — lines 76–76

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### D0053 — lines 77–77

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### D0054 — lines 78–79

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### D0055 — lines 80–80

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### D0056 — lines 81–81

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### D0057 — lines 82–84

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### D0058 — lines 86–86

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### D0059 — lines 87–87

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### D0060 — lines 88–89

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### D0061 — lines 90–90

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### D0062 — lines 91–91

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### D0063 — lines 92–94

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### D0064 — lines 97–97

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### D0065 — lines 98–98

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### D0066 — lines 99–99

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule maxVals(M:Int, .Vals)           => M
```

### D0067 — lines 100–100

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### D0068 — lines 102–102

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### D0069 — lines 103–103

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### D0070 — lines 104–104

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule minVals(M:Int, .Vals)           => M
```

### D0071 — lines 105–105

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### D0072 — lines 108–109

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

### D0073 — lines 111–113

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### D0074 — lines 114–114

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### D0075 — lines 115–115

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### D0076 — lines 116–116

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### D0077 — lines 117–117

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### D0078 — lines 118–118

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### D0079 — lines 119–121

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

### D0080 — lines 124–125

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### D0081 — lines 126–126

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### D0082 — lines 127–127

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### D0083 — lines 128–129

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### D0084 — lines 132–133

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### D0085 — lines 134–134

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### D0086 — lines 135–135

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### D0087 — lines 136–136

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### D0088 — lines 137–137

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### D0089 — lines 140–140

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### D0090 — lines 143–143

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### D0091 — lines 144–145

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

### D0092 — lines 148–148

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### D0093 — lines 149–149

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### D0094 — lines 152–153

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

### D0095 — lines 156–157

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### D0096 — lines 158–158

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### D0097 — lines 159–159

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### D0098 — lines 160–160

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### D0099 — lines 163–163

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### D0100 — lines 164–164

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### D0101 — lines 167–168

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### D0102 — lines 169–169

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### D0103 — lines 170–170

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### D0104 — lines 171–172

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### D0105 — lines 173–173

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### D0106 — lines 174–174

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### D0107 — lines 177–177

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### D0108 — lines 178–178

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### D0109 — lines 179–180

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

### D0110 — lines 187–187

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### D0111 — lines 188–188

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### D0112 — lines 189–190

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### D0113 — lines 192–192

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### D0114 — lines 194–194

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### D0115 — lines 195–195

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### D0116 — lines 196–196

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### D0117 — lines 197–197

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### D0118 — lines 198–198

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### D0119 — lines 199–199

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### D0120 — lines 200–200

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### D0121 — lines 201–201

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### D0122 — lines 203–203

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### D0123 — lines 204–204

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### D0124 — lines 205–205

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### D0125 — lines 206–206

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### D0126 — lines 207–207

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### D0127 — lines 208–208

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### D0128 — lines 209–209

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### D0129 — lines 210–210

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### D0130 — lines 211–211

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### D0131 — lines 212–212

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### D0132 — lines 214–215

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### D0133 — lines 216–216

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### D0134 — lines 217–217

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### D0135 — lines 218–218

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### D0136 — lines 219–220

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### D0137 — lines 221–222

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### D0138 — lines 223–223

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### D0139 — lines 225–225

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### D0140 — lines 226–226

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### D0141 — lines 227–227

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### D0142 — lines 228–228

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### D0143 — lines 230–230

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### D0144 — lines 231–231

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### D0145 — lines 232–232

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### D0146 — lines 233–233

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### D0147 — lines 234–234

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### D0148 — lines 235–235

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### D0149 — lines 236–236

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### D0150 — lines 238–238

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### D0151 — lines 239–239

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### D0152 — lines 240–240

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### D0153 — lines 241–242

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### D0154 — lines 243–243

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### D0155 — lines 244–244

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### D0156 — lines 245–245

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### D0157 — lines 246–246

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### D0158 — lines 247–247

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### D0159 — lines 248–248

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### D0160 — lines 250–250

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### D0161 — lines 251–251

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### D0162 — lines 252–252

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### D0163 — lines 253–253

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### D0164 — lines 254–254

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### D0165 — lines 255–255

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### D0166 — lines 256–256

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### D0167 — lines 257–259

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### D0168 — lines 260–262

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### D0169 — lines 263–264

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### D0170 — lines 265–265

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### D0171 — lines 266–266

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### D0172 — lines 267–267

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### D0173 — lines 268–268

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### D0174 — lines 269–269

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### D0175 — lines 270–270

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### D0176 — lines 271–271

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### D0177 — lines 272–272

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### D0178 — lines 273–273

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### D0179 — lines 274–274

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### D0180 — lines 279–279

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= "#md5"
```

### D0181 — lines 280–281

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### D0182 — lines 282–282

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### D0183 — lines 283–283

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= md5Obj(IntSeq)
```

### D0184 — lines 284–284

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### D0185 — lines 285–285

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(md5hexCodes), total.

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### D0186 — lines 291–291

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### D0187 — lines 292–292

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### D0188 — lines 293–293

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### D0189 — lines 294–294

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isIntV(_:Int)         => true
```

### D0190 — lines 295–295

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule isIntV(_:Val)         => false [owise]
```

### D0191 — lines 296–296

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isStrV(str(_:IntSeq)) => true
```

### D0192 — lines 297–297

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule isStrV(_:Val)         => false [owise]
```

## `reference-semantics/semantics/call.k`

### D0193 — lines 16–16

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### D0194 — lines 19–19

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #callee(Exprs)
```

### D0195 — lines 20–20

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### D0196 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### D0197 — lines 24–24

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### D0198 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### D0199 — lines 27–27

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### D0200 — lines 28–28

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### D0201 — lines 29–29

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### D0202 — lines 30–30

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### D0203 — lines 31–31

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### D0204 — lines 32–32

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### D0205 — lines 38–41

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0206 — lines 42–46

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### D0207 — lines 47–50

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0208 — lines 52–52

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### D0209 — lines 53–55

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### D0210 — lines 56–60

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

### D0211 — lines 63–67

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### D0212 — lines 69–74

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### D0213 — lines 80–85

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### D0214 — lines 87–87

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### D0215 — lines 88–88

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### D0216 — lines 89–94

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## `reference-semantics/semantics/comprehension.k`

### D0217 — lines 11–11

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### D0218 — lines 12–12

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### D0219 — lines 14–14

Kind/classes: `syntax`; syntax, macro-syntax. Attributes: macro.

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### D0220 — lines 15–16

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### D0221 — lines 18–18

Kind/classes: `syntax`; syntax, macro-syntax. Attributes: macro.

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### D0222 — lines 19–20

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### D0223 — lines 21–22

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### D0224 — lines 24–24

Kind/classes: `syntax`; syntax, macro-syntax. Attributes: macro.

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### D0225 — lines 25–25

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### D0226 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## `reference-semantics/semantics/concrete.k`

### D0227 — lines 13–15

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### D0228 — lines 16–18

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### D0229 — lines 25–25

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= kvP(Val, Val)
```

### D0230 — lines 26–27

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### D0231 — lines 28–30

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### D0232 — lines 31–33

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### D0233 — lines 34–35

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### D0234 — lines 36–37

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### D0235 — lines 38–40

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### D0236 — lines 42–42

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### D0237 — lines 43–43

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### D0238 — lines 44–46

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### D0239 — lines 47–49

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### D0240 — lines 51–51

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### D0241 — lines 52–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### D0242 — lines 53–53

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### D0243 — lines 54–54

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### D0244 — lines 56–56

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### D0245 — lines 57–57

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### D0246 — lines 58–58

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### D0247 — lines 59–59

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## `reference-semantics/semantics/controls.k`

### D0248 — lines 9–11

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### D0249 — lines 12–18

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### D0250 — lines 20–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

### D0251 — lines 27–31

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

### D0252 — lines 35–35

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### D0253 — lines 36–36

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### D0254 — lines 37–37

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### D0255 — lines 38–38

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### D0256 — lines 39–42

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### D0257 — lines 43–44

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### D0258 — lines 48–48

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### D0259 — lines 51–51

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### D0260 — lines 52–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### D0261 — lines 53–53

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### D0262 — lines 54–54

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### D0263 — lines 57–58

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### D0264 — lines 59–60

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

### D0265 — lines 65–67

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### D0266 — lines 69–69

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### D0267 — lines 71–71

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### D0268 — lines 72–72

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### D0269 — lines 73–74

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### D0270 — lines 77–77

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### D0271 — lines 78–78

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### D0272 — lines 79–80

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### D0273 — lines 81–82

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

### D0274 — lines 85–85

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### D0275 — lines 86–86

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Continue => #cont ... </k>
```

### D0276 — lines 87–87

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Break => #brk ... </k>
```

### D0277 — lines 88–88

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### D0278 — lines 89–89

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### D0279 — lines 90–90

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### D0280 — lines 91–91

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### D0281 — lines 95–97

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0282 — lines 98–100

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0283 — lines 101–103

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0284 — lines 106–108

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/core.k`

### D0285 — lines 13–13

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### D0286 — lines 14–14

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### D0287 — lines 15–15

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Str    ::= str(IntSeq)
```

### D0288 — lines 18–23

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### D0289 — lines 25–34

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

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

### D0290 — lines 36–36

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Parent   ::= "root" | parent(Int)
```

### D0291 — lines 37–37

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Scope    ::= scope(Map, Parent)
```

### D0292 — lines 38–38

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KResult  ::= Val
```

### D0293 — lines 39–39

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### D0294 — lines 40–40

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Vals     ::= List{Val, ","}
```

### D0295 — lines 41–41

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### D0296 — lines 42–42

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### D0297 — lines 49–60

Kind/classes: `configuration`; configuration. Attributes: none.

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

### D0298 — lines 68–68

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### D0299 — lines 69–69

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isRefV(ref(_:Int)) => true
```

### D0300 — lines 70–70

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule isRefV(_:Val)      => false [owise]
```

### D0301 — lines 75–75

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax HeapVal ::= cellV(Val)
```

### D0302 — lines 76–76

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### D0303 — lines 77–77

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### D0304 — lines 78–78

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule isCellRef(_:Val)          => false [owise]
```

### D0305 — lines 85–90

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

### D0306 — lines 95–95

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= kwV(String, Val)
```

### D0307 — lines 96–96

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #kwTag(String)
```

### D0308 — lines 97–97

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### D0309 — lines 98–99

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### D0310 — lines 100–100

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### D0311 — lines 101–101

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### D0312 — lines 102–102

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule isKwV(_:Val)                => false [owise]
```

### D0313 — lines 106–106

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= cellsMark(ParamNames)
```

### D0314 — lines 107–107

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### D0315 — lines 108–108

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### D0316 — lines 109–109

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### D0317 — lines 110–110

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule pnMember(_:String, .ParamNames) => false
```

### D0318 — lines 111–111

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### D0319 — lines 113–113

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #cellW(Val, Val)
```

### D0320 — lines 114–115

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### D0321 — lines 117–117

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #alloc(Val)
```

### D0322 — lines 118–121

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### D0323 — lines 124–124

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #loadAll(Module)
```

### D0324 — lines 125–125

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### D0325 — lines 126–126

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### D0326 — lines 127–127

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> .Stmts => .K ... </k>
```

### D0327 — lines 130–130

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #look(String, Int)
```

### D0328 — lines 131–131

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### D0329 — lines 132–134

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

### D0330 — lines 145–151

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### D0331 — lines 152–154

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

### D0332 — lines 157–157

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### D0333 — lines 158–181

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

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

### D0334 — lines 185–185

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax ApplyK ::= toCall(Val)
```

### D0335 — lines 186–188

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### D0336 — lines 189–189

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### D0337 — lines 190–190

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### D0338 — lines 191–191

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### D0339 — lines 194–194

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### D0340 — lines 195–195

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### D0341 — lines 196–196

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> NoneVal      => noneV ... </k>
```

### D0342 — lines 199–199

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Bool ::= truthy(Val) [function]
```

### D0343 — lines 200–200

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule truthy(B:Bool)          => B
```

### D0344 — lines 201–201

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule truthy(noneV)           => false
```

### D0345 — lines 202–202

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### D0346 — lines 203–203

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### D0347 — lines 204–204

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### D0348 — lines 205–205

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### D0349 — lines 208–208

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### D0350 — lines 209–209

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### D0351 — lines 210–210

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### D0352 — lines 213–213

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### D0353 — lines 214–214

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### D0354 — lines 215–215

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### D0355 — lines 217–217

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### D0356 — lines 218–218

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### D0357 — lines 219–219

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### D0358 — lines 223–223

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### D0359 — lines 224–224

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule vsLen(.ValSeq)                => 0
```

### D0360 — lines 225–225

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### D0361 — lines 227–227

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### D0362 — lines 228–228

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isLen(.IntSeq)                => 0
```

### D0363 — lines 229–229

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### D0364 — lines 233–233

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### D0365 — lines 234–234

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### D0366 — lines 235–235

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### D0367 — lines 236–237

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### D0368 — lines 238–239

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

## `reference-semantics/semantics/dict.k`

### D0369 — lines 20–20

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### D0370 — lines 23–25

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### D0371 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### D0372 — lines 27–27

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### D0373 — lines 28–29

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### D0374 — lines 30–31

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### D0375 — lines 32–33

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### D0376 — lines 37–37

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### D0377 — lines 38–38

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### D0378 — lines 39–39

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### D0379 — lines 40–40

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### D0380 — lines 43–43

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### D0381 — lines 44–44

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### D0382 — lines 45–45

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### D0383 — lines 49–49

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### D0384 — lines 50–51

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### D0385 — lines 52–53

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### D0386 — lines 54–54

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### D0387 — lines 58–60

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### D0388 — lines 63–63

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### D0389 — lines 64–64

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### D0390 — lines 65–66

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(45).

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### D0391 — lines 70–70

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### D0392 — lines 71–71

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### D0393 — lines 76–76

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #dsetK(String, Val)
```

### D0394 — lines 77–77

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### D0395 — lines 78–81

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### D0396 — lines 82–85

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### D0397 — lines 86–86

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### D0398 — lines 87–88

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### D0399 — lines 90–90

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### D0400 — lines 91–91

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### D0401 — lines 92–92

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### D0402 — lines 95–96

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### D0403 — lines 97–97

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### D0404 — lines 98–98

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### D0405 — lines 99–100

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### D0406 — lines 101–101

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### D0407 — lines 102–102

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### D0408 — lines 103–103

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## `reference-semantics/semantics/float.k`

### D0409 — lines 20–20

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= Float
```

### D0410 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Float(F:Float) => F ... </k>
```

### D0411 — lines 24–24

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(intFloatDiv), total.

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### D0412 — lines 25–25

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### D0413 — lines 27–27

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### D0414 — lines 30–30

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(divII), total.

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### D0415 — lines 31–31

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### D0416 — lines 32–32

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### D0417 — lines 37–37

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(floatMod), total.

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### D0418 — lines 38–38

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### D0419 — lines 39–39

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### D0420 — lines 43–43

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### D0421 — lines 44–44

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### D0422 — lines 50–50

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(floatLt), total.

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### D0423 — lines 51–51

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### D0424 — lines 52–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### D0425 — lines 54–54

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(absF), total.

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### D0426 — lines 55–55

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### D0427 — lines 56–56

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### D0428 — lines 61–61

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Import(_:String) => .K ... </k>
```

### D0429 — lines 65–65

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= "#mathCeil"
```

### D0430 — lines 66–66

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### D0431 — lines 67–67

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### D0432 — lines 70–70

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= "#mathFloor"
```

### D0433 — lines 71–71

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### D0434 — lines 72–72

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### D0435 — lines 73–73

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration. Attributes: function, symbol(floorFI), total.

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### D0436 — lines 74–74

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### D0437 — lines 75–75

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### D0438 — lines 78–78

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### D0439 — lines 79–79

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### D0440 — lines 82–82

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### D0441 — lines 83–83

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### D0442 — lines 84–84

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### D0443 — lines 85–85

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### D0444 — lines 86–86

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration. Attributes: function, symbol(toF), total.

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### D0445 — lines 87–87

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule toF(F:Float) => F        [concrete]
```

### D0446 — lines 88–88

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### D0447 — lines 93–93

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration. Attributes: function, symbol(ceilF), total.

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### D0448 — lines 94–94

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### D0449 — lines 95–95

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### D0450 — lines 99–99

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### D0451 — lines 103–103

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(subF), total.

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### D0452 — lines 104–104

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### D0453 — lines 105–105

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### D0454 — lines 107–107

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(divF), total.

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### D0455 — lines 108–108

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### D0456 — lines 109–109

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### D0457 — lines 111–111

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(addF), total.

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### D0458 — lines 112–112

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### D0459 — lines 113–113

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### D0460 — lines 115–115

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(mulF), total.

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### D0461 — lines 116–116

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### D0462 — lines 117–117

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### D0463 — lines 119–119

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(powF), total.

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### D0464 — lines 120–120

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### D0465 — lines 121–121

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### D0466 — lines 125–125

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(gtF), total.

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### D0467 — lines 126–126

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### D0468 — lines 127–127

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### D0469 — lines 128–128

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### D0470 — lines 129–129

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### D0471 — lines 132–132

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### D0472 — lines 133–133

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### D0473 — lines 134–134

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### D0474 — lines 135–135

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### D0475 — lines 136–136

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### D0476 — lines 137–137

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### D0477 — lines 138–138

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### D0478 — lines 139–139

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### D0479 — lines 142–142

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(eqF), total.

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### D0480 — lines 143–143

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### D0481 — lines 144–144

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### D0482 — lines 145–145

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### D0483 — lines 146–146

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### D0484 — lines 147–147

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### D0485 — lines 148–148

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### D0486 — lines 149–149

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### D0487 — lines 150–150

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### D0488 — lines 151–151

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### D0489 — lines 154–154

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### D0490 — lines 155–155

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### D0491 — lines 160–160

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(decStrToF), total.

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### D0492 — lines 161–161

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### D0493 — lines 162–164

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### D0494 — lines 165–165

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### D0495 — lines 166–166

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### D0496 — lines 167–167

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### D0497 — lines 168–168

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### D0498 — lines 169–169

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### D0499 — lines 170–170

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### D0500 — lines 171–172

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### D0501 — lines 173–173

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### D0502 — lines 174–174

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracPart(.IntSeq) => 0
```

### D0503 — lines 175–175

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### D0504 — lines 176–176

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### D0505 — lines 177–177

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### D0506 — lines 178–178

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### D0507 — lines 179–179

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### D0508 — lines 180–180

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracScale(.IntSeq) => 1
```

### D0509 — lines 181–181

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### D0510 — lines 182–182

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### D0511 — lines 183–183

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### D0512 — lines 184–184

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### D0513 — lines 185–185

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### D0514 — lines 186–186

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### D0515 — lines 187–187

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### D0516 — lines 190–190

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(divFloatIntV), total.

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### D0517 — lines 191–191

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### D0518 — lines 192–192

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### D0519 — lines 195–195

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(intToF), total.

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### D0520 — lines 196–196

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### D0521 — lines 197–197

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### D0522 — lines 198–198

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### D0523 — lines 199–199

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### D0524 — lines 200–200

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### D0525 — lines 201–201

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### D0526 — lines 202–202

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### D0527 — lines 203–203

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### D0528 — lines 204–204

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### D0529 — lines 205–205

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### D0530 — lines 206–206

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### D0531 — lines 209–209

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(truncF), total.

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### D0532 — lines 210–210

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### D0533 — lines 211–211

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### D0534 — lines 213–213

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### D0535 — lines 214–214

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### D0536 — lines 217–217

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(roundF), total.

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### D0537 — lines 218–222

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### D0538 — lines 223–223

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(roundFN), total.

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### D0539 — lines 224–226

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### D0540 — lines 227–227

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### D0541 — lines 228–228

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### D0542 — lines 230–230

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(sqrtF), total.

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### D0543 — lines 231–231

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### D0544 — lines 232–232

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= "#mathSqrt"
```

### D0545 — lines 233–233

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### D0546 — lines 234–234

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### D0547 — lines 235–235

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### D0548 — lines 243–243

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### D0549 — lines 244–244

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### D0550 — lines 245–245

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### D0551 — lines 246–246

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### D0552 — lines 247–248

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### D0553 — lines 250–250

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### D0554 — lines 251–251

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### D0555 — lines 252–252

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### D0556 — lines 253–253

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### D0557 — lines 254–255

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### D0558 — lines 261–261

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### D0559 — lines 262–264

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### D0560 — lines 265–265

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### D0561 — lines 266–266

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### D0562 — lines 267–269

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### D0563 — lines 270–272

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

## `reference-semantics/semantics/functions.k`

### D0564 — lines 8–11

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### D0565 — lines 14–16

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### D0566 — lines 18–18

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### D0567 — lines 19–20

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### D0568 — lines 27–27

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### D0569 — lines 31–32

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### D0570 — lines 33–35

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### D0571 — lines 36–41

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### D0572 — lines 42–45

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### D0573 — lines 47–49

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### D0574 — lines 50–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### D0575 — lines 53–58

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### D0576 — lines 59–60

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### D0577 — lines 63–63

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### D0578 — lines 64–66

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### D0579 — lines 68–75

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

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

### D0580 — lines 78–79

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### D0581 — lines 80–81

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### D0582 — lines 85–90

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## `reference-semantics/semantics/int.k`

### D0583 — lines 7–7

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### D0584 — lines 9–9

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### D0585 — lines 11–11

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### D0586 — lines 12–12

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### D0587 — lines 13–13

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### D0588 — lines 14–14

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### D0589 — lines 15–15

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### D0590 — lines 16–16

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### D0591 — lines 17–17

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### D0592 — lines 19–19

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### D0593 — lines 20–20

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### D0594 — lines 22–22

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### D0595 — lines 23–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### D0596 — lines 24–24

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### D0597 — lines 25–25

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### D0598 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### D0599 — lines 27–27

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## `reference-semantics/semantics/iter.k`

### D0600 — lines 8–8

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## `reference-semantics/semantics/list.k`

### D0601 — lines 9–9

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### D0602 — lines 10–10

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### D0603 — lines 13–13

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax ApplyK ::= "toList"
```

### D0604 — lines 14–14

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### D0605 — lines 15–15

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### D0606 — lines 18–18

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### D0607 — lines 19–19

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### D0608 — lines 20–20

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### D0609 — lines 24–25

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(45).

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### D0610 — lines 27–27

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### D0611 — lines 28–28

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### D0612 — lines 33–33

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### D0613 — lines 34–34

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule hasRefVS(.ValSeq)                => false
```

### D0614 — lines 35–35

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### D0615 — lines 37–38

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### D0616 — lines 39–39

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### D0617 — lines 40–40

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### D0618 — lines 41–41

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### D0619 — lines 42–43

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### D0620 — lines 45–46

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### D0621 — lines 47–48

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### D0622 — lines 49–49

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### D0623 — lines 50–50

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### D0624 — lines 53–55

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### D0625 — lines 58–58

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### D0626 — lines 59–59

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### D0627 — lines 60–60

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### D0628 — lines 61–61

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### D0629 — lines 62–62

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### D0630 — lines 63–64

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### D0631 — lines 65–66

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### D0632 — lines 67–67

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## `reference-semantics/semantics/methods.k`

### D0633 — lines 10–10

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### D0634 — lines 13–13

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### D0635 — lines 14–14

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### D0636 — lines 15–15

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### D0637 — lines 16–16

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### D0638 — lines 19–19

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### D0639 — lines 20–20

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### D0640 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### D0641 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### D0642 — lines 27–27

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### D0643 — lines 28–28

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### D0644 — lines 29–29

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### D0645 — lines 30–31

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### D0646 — lines 34–34

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### D0647 — lines 35–35

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### D0648 — lines 36–36

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### D0649 — lines 37–38

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### D0650 — lines 39–40

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### D0651 — lines 41–41

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### D0652 — lines 42–42

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### D0653 — lines 43–43

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### D0654 — lines 44–44

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### D0655 — lines 47–47

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### D0656 — lines 48–48

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### D0657 — lines 49–49

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### D0658 — lines 50–50

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### D0659 — lines 51–51

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### D0660 — lines 52–52

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### D0661 — lines 53–53

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### D0662 — lines 54–54

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### D0663 — lines 55–55

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### D0664 — lines 58–58

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### D0665 — lines 61–61

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### D0666 — lines 64–64

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### D0667 — lines 65–65

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### D0668 — lines 66–66

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### D0669 — lines 67–67

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### D0670 — lines 68–68

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### D0671 — lines 72–74

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### D0672 — lines 75–75

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function, token.

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### D0673 — lines 76–76

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### D0674 — lines 77–78

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### D0675 — lines 79–80

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

### D0676 — lines 82–82

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### D0677 — lines 83–83

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### D0678 — lines 84–84

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### D0679 — lines 85–85

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### D0680 — lines 86–86

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### D0681 — lines 89–91

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(39).

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### D0682 — lines 94–96

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### D0683 — lines 97–97

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function, token.

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### D0684 — lines 98–98

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### D0685 — lines 99–100

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### D0686 — lines 101–102

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### D0687 — lines 104–105

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### D0688 — lines 106–106

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### D0689 — lines 107–107

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### D0690 — lines 108–108

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### D0691 — lines 109–109

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### D0692 — lines 112–112

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### D0693 — lines 113–113

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### D0694 — lines 115–115

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### D0695 — lines 116–116

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### D0696 — lines 118–118

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### D0697 — lines 119–119

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### D0698 — lines 121–121

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### D0699 — lines 122–122

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### D0700 — lines 124–124

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### D0701 — lines 125–125

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule hasUpper(.IntSeq) => false
```

### D0702 — lines 126–126

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### D0703 — lines 128–128

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### D0704 — lines 129–129

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule hasLower(.IntSeq) => false
```

### D0705 — lines 130–130

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### D0706 — lines 132–132

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### D0707 — lines 133–133

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule allAlpha(.IntSeq) => true
```

### D0708 — lines 134–134

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### D0709 — lines 136–136

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### D0710 — lines 137–137

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule allDigit(.IntSeq) => true
```

### D0711 — lines 138–138

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### D0712 — lines 140–140

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### D0713 — lines 142–142

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### D0714 — lines 143–143

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule lowerC(C:Int) => C         [owise]
```

### D0715 — lines 145–145

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= upperC(Int) [function, total]
```

### D0716 — lines 146–146

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### D0717 — lines 147–147

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule upperC(C:Int) => C         [owise]
```

### D0718 — lines 149–149

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= swapC(Int) [function, total]
```

### D0719 — lines 150–150

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### D0720 — lines 151–151

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### D0721 — lines 152–152

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule swapC(C:Int) => C         [owise]
```

### D0722 — lines 154–154

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### D0723 — lines 155–155

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### D0724 — lines 156–156

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### D0725 — lines 158–158

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### D0726 — lines 159–159

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### D0727 — lines 160–160

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### D0728 — lines 162–162

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### D0729 — lines 163–163

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### D0730 — lines 164–164

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### D0731 — lines 166–166

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### D0732 — lines 167–167

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### D0733 — lines 168–168

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### D0734 — lines 169–169

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## `reference-semantics/semantics/operators.k`

### D0735 — lines 10–10

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### D0736 — lines 12–12

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### D0737 — lines 15–15

Kind/classes: `context`; context. Attributes: none.

```k
  context Compare(HOLE, _)
```

### D0738 — lines 16–16

Kind/classes: `context`; context. Attributes: none.

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### D0739 — lines 17–17

Kind/classes: `rule`; rule, ordinary-rule, owise-rule. Attributes: owise.

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### D0740 — lines 19–19

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### D0741 — lines 20–20

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### D0742 — lines 25–27

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0743 — lines 28–31

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

### D0744 — lines 34–37

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### D0745 — lines 38–42

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### D0746 — lines 44–46

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/range.k`

### D0747 — lines 9–9

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### D0748 — lines 10–10

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### D0749 — lines 12–12

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### D0750 — lines 13–14

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### D0751 — lines 15–16

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### D0752 — lines 17–18

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### D0753 — lines 20–22

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### D0754 — lines 23–24

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

## `reference-semantics/semantics/set.k`

### D0755 — lines 8–8

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Val ::= setV(IntSeq)
```

### D0756 — lines 11–11

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### D0757 — lines 12–12

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### D0758 — lines 13–13

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### D0759 — lines 16–17

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### D0760 — lines 18–18

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### D0761 — lines 19–19

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### D0762 — lines 20–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### D0763 — lines 22–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### D0764 — lines 25–25

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### D0765 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### D0766 — lines 27–27

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### D0767 — lines 31–31

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### D0768 — lines 32–32

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### D0769 — lines 33–33

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### D0770 — lines 35–35

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### D0771 — lines 36–36

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### D0772 — lines 39–39

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## `reference-semantics/semantics/sort.k`

### D0773 — lines 18–18

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(sortVS), total.

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### D0774 — lines 19–19

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### D0775 — lines 20–20

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### D0776 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### D0777 — lines 22–22

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### D0778 — lines 23–23

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### D0779 — lines 24–24

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### D0780 — lines 26–26

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### D0781 — lines 27–27

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### D0782 — lines 28–28

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### D0783 — lines 29–30

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### D0784 — lines 31–32

Kind/classes: `rule`; rule, ordinary-rule, concrete-rule. Attributes: concrete.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### D0785 — lines 36–37

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### D0786 — lines 40–42

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### D0787 — lines 49–49

Kind/classes: `syntax`; syntax, function-declaration, total-declaration, symbol-declaration, proof-opaque-symbol-declaration. Attributes: function, no-evaluators, symbol(sortKeyVS), total.

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### D0788 — lines 51–52

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### D0789 — lines 53–53

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### D0790 — lines 54–54

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### D0791 — lines 55–55

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### D0792 — lines 57–57

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### D0793 — lines 58–58

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule condRev(S:ValSeq, false) => S
```

### D0794 — lines 59–59

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### D0795 — lines 61–62

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### D0796 — lines 63–64

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### D0797 — lines 65–66

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

## `reference-semantics/semantics/str.k`

### D0798 — lines 8–8

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### D0799 — lines 9–10

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### D0800 — lines 13–13

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### D0801 — lines 14–14

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### D0802 — lines 15–15

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strToCodes("") => .IntSeq
```

### D0803 — lines 16–17

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### D0804 — lines 20–20

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### D0805 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### D0806 — lines 22–22

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### D0807 — lines 24–24

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### D0808 — lines 25–25

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### D0809 — lines 26–26

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### D0810 — lines 29–29

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### D0811 — lines 30–30

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### D0812 — lines 32–32

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### D0813 — lines 33–33

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### D0814 — lines 34–34

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### D0815 — lines 35–35

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### D0816 — lines 37–37

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### D0817 — lines 38–38

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### D0818 — lines 39–39

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### D0819 — lines 40–41

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

### D0820 — lines 48–48

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### D0821 — lines 49–49

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### D0822 — lines 50–50

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### D0823 — lines 51–51

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### D0824 — lines 52–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### D0825 — lines 53–53

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### D0826 — lines 54–54

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### D0827 — lines 56–56

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### D0828 — lines 57–57

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### D0829 — lines 58–58

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### D0830 — lines 59–59

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## `reference-semantics/semantics/subscript.k`

### D0831 — lines 11–11

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### D0832 — lines 12–12

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### D0833 — lines 13–14

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### D0834 — lines 16–16

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### D0835 — lines 17–17

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### D0836 — lines 18–19

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### D0837 — lines 21–21

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### D0838 — lines 22–22

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### D0839 — lines 23–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### D0840 — lines 27–27

Kind/classes: `context`; context. Attributes: none.

```k
  context Subscript(HOLE, _)
```

### D0841 — lines 28–28

Kind/classes: `context`; context. Attributes: none.

```k
  context Subscript(_:Val, HOLE:Expr)
```

### D0842 — lines 31–33

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0843 — lines 35–35

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### D0844 — lines 37–37

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### D0845 — lines 38–38

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### D0846 — lines 39–39

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### D0847 — lines 40–41

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### D0848 — lines 44–47

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### D0849 — lines 49–49

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### D0850 — lines 50–50

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### D0851 — lines 51–51

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### D0852 — lines 52–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### D0853 — lines 54–54

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### D0854 — lines 55–55

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### D0855 — lines 56–56

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### D0856 — lines 58–60

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(45).

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### D0857 — lines 61–61

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### D0858 — lines 63–63

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### D0859 — lines 64–65

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### D0860 — lines 66–67

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### D0861 — lines 68–69

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### D0862 — lines 72–72

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### D0863 — lines 73–73

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStep(noB)          => 1
```

### D0864 — lines 74–74

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStep(someB(S:Int)) => S
```

### D0865 — lines 76–76

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### D0866 — lines 77–78

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### D0867 — lines 79–80

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### D0868 — lines 81–81

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### D0869 — lines 83–83

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### D0870 — lines 84–85

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### D0871 — lines 86–87

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### D0872 — lines 88–88

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### D0873 — lines 90–90

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### D0874 — lines 91–92

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### D0875 — lines 93–94

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### D0876 — lines 96–96

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### D0877 — lines 97–98

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### D0878 — lines 99–100

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### D0879 — lines 102–102

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### D0880 — lines 103–104

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### D0881 — lines 105–106

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

### D0882 — lines 109–109

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### D0883 — lines 110–112

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### D0884 — lines 113–114

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### D0885 — lines 116–116

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### D0886 — lines 117–119

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### D0887 — lines 120–121

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## `reference-semantics/semantics/syntax.k`

### D0888 — lines 9–30

Kind/classes: `syntax`; syntax, macro-syntax. Attributes: macro, seqstrict, strict.

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

### D0889 — lines 32–32

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### D0890 — lines 33–33

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### D0891 — lines 34–34

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Entries  ::= List{Entry, ","}
```

### D0892 — lines 35–35

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### D0893 — lines 36–36

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax CompFors ::= List{CompFor, ""}
```

### D0894 — lines 37–37

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Exprs    ::= List{Expr, ","}
```

### D0895 — lines 38–38

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### D0896 — lines 39–39

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Bound    ::= Expr | "NoBound"
```

### D0897 — lines 41–54

Kind/classes: `syntax`; syntax. Attributes: strict.

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

### D0898 — lines 56–56

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### D0899 — lines 57–57

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### D0900 — lines 58–58

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### D0901 — lines 59–59

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### D0902 — lines 60–60

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax ParamNames ::= List{String, ","}
```

### D0903 — lines 61–61

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## `reference-semantics/semantics/tuple.k`

### D0904 — lines 10–10

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### D0905 — lines 11–11

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### D0906 — lines 14–14

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax ApplyK ::= "toTuple"
```

### D0907 — lines 15–15

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### D0908 — lines 16–16

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### D0909 — lines 18–18

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### D0910 — lines 20–20

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### D0911 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### D0912 — lines 23–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### D0913 — lines 24–24

Kind/classes: `syntax`; syntax, function-declaration. Attributes: function.

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### D0914 — lines 25–25

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### D0915 — lines 26–27

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### D0916 — lines 28–28

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### D0917 — lines 31–31

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### D0918 — lines 32–34

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### D0919 — lines 35–41

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### D0920 — lines 42–42

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### D0921 — lines 43–43

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### D0922 — lines 44–46

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0923 — lines 49–49

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### D0924 — lines 50–50

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### D0925 — lines 51–51

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### D0926 — lines 52–54

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### D0927 — lines 55–56

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### D0928 — lines 57–57

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## `verification.k`

### D0929 — lines 7–8

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax StrSeq ::= ".StrSeq"
                  | ssCons(IntSeq, StrSeq)
```

### D0930 — lines 12–12

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax ValSeq ::= strVals(StrSeq)
```

### D0931 — lines 13–13

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strVals(.StrSeq) => .ValSeq
```

### D0932 — lines 14–15

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule strVals(ssCons(S:IntSeq, SS:StrSeq))
    => vCons(str(S), strVals(SS))
```

### D0933 — lines 17–17

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #strIterNext(StrSeq)
```

### D0934 — lines 18–20

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> #iterNext(list(strVals(SS:StrSeq)))
        => #strIterNext(SS) ... </k>
    [priority(40)]
```

### D0935 — lines 21–21

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #strIterNext(.StrSeq) => #iterDone ... </k>
```

### D0936 — lines 22–23

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #strIterNext(ssCons(S:IntSeq, SS:StrSeq))
        => #iterYield(str(S), list(strVals(SS))) ... </k>
```

### D0937 — lines 26–26

Kind/classes: `syntax`; syntax. Attributes: none.

```k
  syntax KItem ::= #strContainsBool(IntSeq, IntSeq)
```

### D0938 — lines 27–29

Kind/classes: `rule`; rule, ordinary-rule, priority-rule. Attributes: priority(40).

```k
  rule <k> Compare(str(P:IntSeq), CmpOp("in", str(S:IntSeq)))
        => #strContainsBool(P, S) ... </k>
    [priority(40)]
```

### D0939 — lines 30–31

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #strContainsBool(P:IntSeq, S:IntSeq) => true ... </k>
    requires strContains(P, S) ==Bool true
```

### D0940 — lines 32–33

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule <k> #strContainsBool(P:IntSeq, S:IntSeq) => false ... </k>
    requires strContains(P, S) ==Bool false
```

### D0941 — lines 37–37

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= filterAccStrings(ValSeq, IntSeq, StrSeq) [function, total]
```

### D0942 — lines 38–38

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule filterAccStrings(ACC:ValSeq, _:IntSeq, .StrSeq) => ACC
```

### D0943 — lines 39–43

Kind/classes: `rule`; rule, simplification-rule. Attributes: simplification.

```k
  rule filterAccStrings(ACC:ValSeq, P:IntSeq,
                        ssCons(S:IntSeq, SS:StrSeq))
    => filterAccStrings(valSeqConcat(ACC, vCons(str(S), .ValSeq)), P, SS)
    requires strContains(P, S) ==Bool true
    [simplification]
```

### D0944 — lines 44–48

Kind/classes: `rule`; rule, simplification-rule. Attributes: simplification.

```k
  rule filterAccStrings(ACC:ValSeq, P:IntSeq,
                        ssCons(S:IntSeq, SS:StrSeq))
    => filterAccStrings(ACC, P, SS)
    requires strContains(P, S) ==Bool false
    [simplification]
```

### D0945 — lines 50–50

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax ValSeq ::= filterStrings(IntSeq, StrSeq) [function, total]
```

### D0946 — lines 51–52

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule filterStrings(P:IntSeq, SS:StrSeq)
    => filterAccStrings(.ValSeq, P, SS)
```

### D0947 — lines 54–54

Kind/classes: `syntax`; syntax, function-declaration, total-declaration. Attributes: function, total.

```k
  syntax IntSeq ::= lastCodes(IntSeq, StrSeq) [function, total]
```

### D0948 — lines 55–55

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule lastCodes(S:IntSeq, .StrSeq) => S
```

### D0949 — lines 56–57

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule lastCodes(_:IntSeq, ssCons(S:IntSeq, SS:StrSeq))
    => lastCodes(S, SS)
```

### D0950 — lines 60–60

Kind/classes: `syntax`; syntax, macro-syntax. Attributes: macro.

```k
  syntax Stmts ::= "filterLoopBody" [macro]
```

### D0951 — lines 61–64

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule filterLoopBody
    => If(Compare(Name("substring"), CmpOp("in", Name("string"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("string"))) .Stmts,
          .Stmts)
```

### D0952 — lines 66–66

Kind/classes: `syntax`; syntax, macro-syntax. Attributes: macro.

```k
  syntax Stmts ::= "filterBody" [macro]
```

### D0953 — lines 67–70

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule filterBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("string"), Name("strings"), filterLoopBody)
       Return(Name("result"))
```

### D0954 — lines 72–72

Kind/classes: `syntax`; syntax, macro-syntax. Attributes: macro.

```k
  syntax Module ::= "filterProgram" [macro]
```

### D0955 — lines 73–76

Kind/classes: `rule`; rule, ordinary-rule. Attributes: none.

```k
  rule filterProgram
    => Module(ImportFrom("typing", "List")
              FuncDef("filter_by_substring", Params("strings", "substring"),
                      filterBody))
```

## `spec.k`

### D0956 — lines 9–31

Kind/classes: `claim`; claim. Attributes: none.

```k
  claim
    <k> #loop(list(strVals(SS:StrSeq)), Name("string"), filterLoopBody)
         ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        (.Map [ "strings" <- list(strVals(ORIG:StrSeq)) ]
              [ "substring" <- str(P:IntSeq) ]
              [ "result" <- ref(H:Int) ]
              [ "string" <- str(CUR:IntSeq) ])
        =>
        (.Map [ "strings" <- list(strVals(ORIG)) ]
              [ "substring" <- str(P) ]
              [ "result" <- ref(H) ]
              [ "string" <- str(lastCodes(CUR, SS)) ]),
        parent(0)) ...
    </scopes>
    <heap>
      ... H:Int |-> list(ACC:ValSeq
                         => filterAccStrings(ACC, P, SS)) ...
    </heap>
```

### D0957 — lines 35–57

Kind/classes: `claim`; claim. Attributes: none.

```k
  claim
    <k> #loadAll(filterProgram)
         ~> Call(Name("filter_by_substring"),
                 (list(strVals(SS:StrSeq)), str(P:IntSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(("filter_by_substring"
                    |-> closureVal(("strings", "substring"), filterBody, 0)),
                   parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (0 |-> list(filterStrings(P, SS))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
```

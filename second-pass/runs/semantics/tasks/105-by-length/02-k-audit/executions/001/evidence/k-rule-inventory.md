# Exhaustive K declaration and rule inventory

Generated from the clean scratch copy. Every declaration block is shown with its complete source text and line range.

## `reference-semantics/semantics/assert.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-ASSERT
```

### imports at lines 4-5

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### rule at lines 6-7

Attributes/classifiers: none

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### rule at lines 8-12

Attributes/classifiers: none

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### rule at lines 13-15

Attributes/classifiers: priority

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### endmodule at lines 16-16

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/bool.k`

### module at lines 5-5

Attributes/classifiers: none

```k
module MPY-BOOL
```

### imports at lines 6-7

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### rule at lines 8-9

Attributes/classifiers: none

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### rule at lines 10-10

Attributes/classifiers: none

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### rule at lines 11-15

Attributes/classifiers: none

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### context at lines 16-16

Attributes/classifiers: none

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### rule at lines 17-17

Attributes/classifiers: none

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### rule at lines 18-19

Attributes/classifiers: none

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### rule at lines 20-21

Attributes/classifiers: none

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### rule at lines 22-23

Attributes/classifiers: none

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### rule at lines 24-28

Attributes/classifiers: none

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### rule at lines 29-30

Attributes/classifiers: priority

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### rule at lines 31-34

Attributes/classifiers: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### rule at lines 35-38

Attributes/classifiers: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### rule at lines 39-42

Attributes/classifiers: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### rule at lines 43-46

Attributes/classifiers: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### endmodule at lines 47-47

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/builtins.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-BUILTINS
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports MPY-STR
```

### imports at lines 6-6

Attributes/classifiers: none

```k
  imports MPY-SET
```

### imports at lines 7-7

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### imports at lines 8-8

Attributes/classifiers: none

```k
  imports MPY-RANGE
```

### imports at lines 9-9

Attributes/classifiers: none

```k
  imports MPY-INT
```

### imports at lines 10-16

Attributes/classifiers: none

```k
  imports MPY-METHODS

  // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup

  // Call routing + argument evaluation live in call.k, which also routes the fold
  // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to
  // applyBuiltin. This module owns applyBuiltin + the fold implementations.
```

### syntax at lines 17-19

Attributes/classifiers: function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### syntax at lines 20-20

Attributes/classifiers: function

```k
  syntax Int ::= seqLen(Val) [function]
```

### rule at lines 21-21

Attributes/classifiers: none

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### rule at lines 22-22

Attributes/classifiers: none

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### rule at lines 23-23

Attributes/classifiers: none

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### rule at lines 24-24

Attributes/classifiers: none

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### rule at lines 25-25

Attributes/classifiers: none

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### rule at lines 26-31

Attributes/classifiers: none

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### rule at lines 32-32

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### rule at lines 33-33

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### rule at lines 34-34

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### rule at lines 35-35

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### syntax at lines 36-36

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### rule at lines 37-37

Attributes/classifiers: none

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### rule at lines 38-40

Attributes/classifiers: none

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### rule at lines 41-43

Attributes/classifiers: none

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### rule at lines 44-46

Attributes/classifiers: none

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### syntax at lines 47-47

Attributes/classifiers: none

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### rule at lines 48-48

Attributes/classifiers: none

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### rule at lines 49-49

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### rule at lines 50-53

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### syntax at lines 54-54

Attributes/classifiers: function

```k
  syntax Int ::= intOf(Val) [function]
```

### rule at lines 55-55

Attributes/classifiers: none

```k
  rule intOf(I:Int)  => I
```

### rule at lines 56-58

Attributes/classifiers: none

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### syntax at lines 59-59

Attributes/classifiers: none

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### rule at lines 60-60

Attributes/classifiers: none

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### rule at lines 61-61

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### rule at lines 62-63

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### rule at lines 64-66

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### syntax at lines 67-67

Attributes/classifiers: none

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### rule at lines 68-68

Attributes/classifiers: none

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### rule at lines 69-69

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### rule at lines 70-71

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### rule at lines 72-75

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### syntax at lines 76-76

Attributes/classifiers: none

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### rule at lines 77-77

Attributes/classifiers: none

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### rule at lines 78-79

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### rule at lines 80-80

Attributes/classifiers: none

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### rule at lines 81-81

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### rule at lines 82-85

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### syntax at lines 86-86

Attributes/classifiers: none

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### rule at lines 87-87

Attributes/classifiers: none

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### rule at lines 88-89

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### rule at lines 90-90

Attributes/classifiers: none

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### rule at lines 91-91

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### rule at lines 92-96

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### syntax at lines 97-97

Attributes/classifiers: function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### rule at lines 98-98

Attributes/classifiers: none

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### rule at lines 99-99

Attributes/classifiers: none

```k
  rule maxVals(M:Int, .Vals)           => M
```

### rule at lines 100-101

Attributes/classifiers: none

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### syntax at lines 102-102

Attributes/classifiers: function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### rule at lines 103-103

Attributes/classifiers: none

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### rule at lines 104-104

Attributes/classifiers: none

```k
  rule minVals(M:Int, .Vals)           => M
```

### rule at lines 105-107

Attributes/classifiers: none

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### rule at lines 108-110

Attributes/classifiers: none

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### rule at lines 111-113

Attributes/classifiers: none

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### syntax at lines 114-114

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### rule at lines 115-115

Attributes/classifiers: none

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### rule at lines 116-116

Attributes/classifiers: none

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### syntax at lines 117-117

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### rule at lines 118-118

Attributes/classifiers: none

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### rule at lines 119-123

Attributes/classifiers: none

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### rule at lines 124-125

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### syntax at lines 126-126

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### rule at lines 127-127

Attributes/classifiers: none

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### rule at lines 128-131

Attributes/classifiers: none

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### rule at lines 132-133

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### syntax at lines 134-134

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### rule at lines 135-135

Attributes/classifiers: none

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### rule at lines 136-136

Attributes/classifiers: none

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### rule at lines 137-139

Attributes/classifiers: none

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### rule at lines 140-142

Attributes/classifiers: none

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### rule at lines 143-143

Attributes/classifiers: none

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### rule at lines 144-147

Attributes/classifiers: none

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### rule at lines 148-148

Attributes/classifiers: none

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### rule at lines 149-151

Attributes/classifiers: none

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### rule at lines 152-155

Attributes/classifiers: none

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### rule at lines 156-157

Attributes/classifiers: none

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### syntax at lines 158-158

Attributes/classifiers: function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### rule at lines 159-159

Attributes/classifiers: none

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### rule at lines 160-162

Attributes/classifiers: none

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### rule at lines 163-163

Attributes/classifiers: none

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### rule at lines 164-166

Attributes/classifiers: none

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### rule at lines 167-168

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### rule at lines 169-169

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### rule at lines 170-170

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### rule at lines 171-172

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### rule at lines 173-173

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### rule at lines 174-176

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### rule at lines 177-177

Attributes/classifiers: none

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### rule at lines 178-178

Attributes/classifiers: none

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### rule at lines 179-186

Attributes/classifiers: concrete

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### rule at lines 187-187

Attributes/classifiers: none

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### syntax at lines 188-188

Attributes/classifiers: function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### rule at lines 189-191

Attributes/classifiers: none

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### syntax at lines 192-193

Attributes/classifiers: none

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### syntax at lines 194-194

Attributes/classifiers: function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### rule at lines 195-195

Attributes/classifiers: none

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax at lines 196-196

Attributes/classifiers: function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### rule at lines 197-197

Attributes/classifiers: none

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### rule at lines 198-198

Attributes/classifiers: owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### syntax at lines 199-199

Attributes/classifiers: function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### rule at lines 200-200

Attributes/classifiers: none

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### rule at lines 201-202

Attributes/classifiers: owise

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### syntax at lines 203-203

Attributes/classifiers: function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### rule at lines 204-204

Attributes/classifiers: none

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### rule at lines 205-205

Attributes/classifiers: none

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### rule at lines 206-206

Attributes/classifiers: none

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### rule at lines 207-207

Attributes/classifiers: none

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### rule at lines 208-208

Attributes/classifiers: none

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### rule at lines 209-209

Attributes/classifiers: none

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### rule at lines 210-210

Attributes/classifiers: none

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### rule at lines 211-211

Attributes/classifiers: none

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### rule at lines 212-213

Attributes/classifiers: none

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### syntax at lines 214-215

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### rule at lines 216-216

Attributes/classifiers: none

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### rule at lines 217-217

Attributes/classifiers: none

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### rule at lines 218-218

Attributes/classifiers: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### rule at lines 219-220

Attributes/classifiers: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### rule at lines 221-222

Attributes/classifiers: none

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### rule at lines 223-224

Attributes/classifiers: owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### syntax at lines 225-225

Attributes/classifiers: none

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### syntax at lines 226-226

Attributes/classifiers: function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### rule at lines 227-227

Attributes/classifiers: none

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### rule at lines 228-229

Attributes/classifiers: owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### syntax at lines 230-230

Attributes/classifiers: function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### rule at lines 231-231

Attributes/classifiers: none

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### rule at lines 232-232

Attributes/classifiers: none

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### rule at lines 233-233

Attributes/classifiers: none

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### rule at lines 234-234

Attributes/classifiers: none

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### rule at lines 235-235

Attributes/classifiers: none

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### rule at lines 236-237

Attributes/classifiers: owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### syntax at lines 238-238

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### rule at lines 239-239

Attributes/classifiers: none

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### rule at lines 240-240

Attributes/classifiers: none

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### rule at lines 241-242

Attributes/classifiers: none

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### rule at lines 243-243

Attributes/classifiers: owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### syntax at lines 244-244

Attributes/classifiers: function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### rule at lines 245-245

Attributes/classifiers: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### rule at lines 246-246

Attributes/classifiers: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### syntax at lines 247-247

Attributes/classifiers: function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### rule at lines 248-249

Attributes/classifiers: none

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### syntax at lines 250-250

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### rule at lines 251-251

Attributes/classifiers: none

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule at lines 252-252

Attributes/classifiers: none

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### rule at lines 253-253

Attributes/classifiers: none

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule at lines 254-254

Attributes/classifiers: none

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### syntax at lines 255-255

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### rule at lines 256-256

Attributes/classifiers: none

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### rule at lines 257-259

Attributes/classifiers: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### rule at lines 260-262

Attributes/classifiers: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### rule at lines 263-264

Attributes/classifiers: owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### syntax at lines 265-265

Attributes/classifiers: function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### rule at lines 266-266

Attributes/classifiers: none

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### rule at lines 267-267

Attributes/classifiers: none

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### rule at lines 268-268

Attributes/classifiers: owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### syntax at lines 269-269

Attributes/classifiers: function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### rule at lines 270-270

Attributes/classifiers: none

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### rule at lines 271-271

Attributes/classifiers: none

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### syntax at lines 272-272

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### rule at lines 273-273

Attributes/classifiers: none

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### rule at lines 274-278

Attributes/classifiers: concrete

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### syntax at lines 279-279

Attributes/classifiers: none

```k
  syntax KItem ::= "#md5"
```

### rule at lines 280-281

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### rule at lines 282-282

Attributes/classifiers: none

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### syntax at lines 283-283

Attributes/classifiers: none

```k
  syntax Val ::= md5Obj(IntSeq)
```

### rule at lines 284-284

Attributes/classifiers: none

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### syntax at lines 285-290

Attributes/classifiers: function, total, symbol, no-evaluators, owise

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### rule at lines 291-291

Attributes/classifiers: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### rule at lines 292-292

Attributes/classifiers: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### syntax at lines 293-293

Attributes/classifiers: function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### rule at lines 294-294

Attributes/classifiers: none

```k
  rule isIntV(_:Int)         => true
```

### rule at lines 295-295

Attributes/classifiers: owise

```k
  rule isIntV(_:Val)         => false [owise]
```

### rule at lines 296-296

Attributes/classifiers: none

```k
  rule isStrV(str(_:IntSeq)) => true
```

### rule at lines 297-297

Attributes/classifiers: owise

```k
  rule isStrV(_:Val)         => false [owise]
```

### endmodule at lines 298-298

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/call.k`

### module at lines 10-10

Attributes/classifiers: none

```k
module MPY-CALL
```

### imports at lines 11-11

Attributes/classifiers: none

```k
  imports MPY-METHODS
```

### imports at lines 12-12

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### imports at lines 13-15

Attributes/classifiers: none

```k
  imports MPY-FUNCTIONS

  // a cooled attribute is a bound method value
```

### rule at lines 16-18

Attributes/classifiers: owise

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### syntax at lines 19-19

Attributes/classifiers: none

```k
  syntax KItem ::= #callee(Exprs)
```

### rule at lines 20-20

Attributes/classifiers: owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### rule at lines 21-23

Attributes/classifiers: none

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### rule at lines 24-25

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### rule at lines 26-26

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### rule at lines 27-27

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### rule at lines 28-28

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### rule at lines 29-29

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### rule at lines 30-30

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### rule at lines 31-31

Attributes/classifiers: owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### rule at lines 32-37

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### rule at lines 38-41

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at lines 42-46

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### rule at lines 47-51

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### syntax at lines 52-52

Attributes/classifiers: function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### rule at lines 53-55

Attributes/classifiers: none

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### rule at lines 56-62

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### rule at lines 63-68

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### rule at lines 69-79

Attributes/classifiers: none

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

### rule at lines 80-86

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### syntax at lines 87-87

Attributes/classifiers: none

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### rule at lines 88-88

Attributes/classifiers: none

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### rule at lines 89-94

Attributes/classifiers: none

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### endmodule at lines 95-95

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/comprehension.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-COMPREHENSION
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports MPY-OPERATORS
```

### imports at lines 6-6

Attributes/classifiers: none

```k
  imports MPY-LIST
```

### imports at lines 7-7

Attributes/classifiers: none

```k
  imports MPY-CONTROLS
```

### imports at lines 8-10

Attributes/classifiers: none

```k
  imports MPY-FUNCTIONS

  // A comprehension is pure syntactic sugar
```

### rule at lines 11-11

Attributes/classifiers: none

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### rule at lines 12-13

Attributes/classifiers: none

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### syntax at lines 14-14

Attributes/classifiers: macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### rule at lines 15-17

Attributes/classifiers: none

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### syntax at lines 18-18

Attributes/classifiers: macro-rec

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### rule at lines 19-20

Attributes/classifiers: none

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### rule at lines 21-23

Attributes/classifiers: none

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### syntax at lines 24-24

Attributes/classifiers: macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### rule at lines 25-25

Attributes/classifiers: none

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### rule at lines 26-26

Attributes/classifiers: none

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### endmodule at lines 27-27

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/concrete.k`

### module at lines 8-8

Attributes/classifiers: none

```k
module MPY-CONCRETE
```

### imports at lines 9-12

Attributes/classifiers: none

```k
  imports MPY

  // deep equality for list compares whose elements are heap objects
  // (list-of-lists): Python == is structural at every depth.
```

### rule at lines 13-15

Attributes/classifiers: none

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### rule at lines 16-24

Attributes/classifiers: priority, concrete

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

### syntax at lines 25-25

Attributes/classifiers: none

```k
  syntax Val ::= kvP(Val, Val)
```

### syntax at lines 26-27

Attributes/classifiers: none

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### rule at lines 28-30

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### rule at lines 31-33

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### rule at lines 34-35

Attributes/classifiers: none

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### rule at lines 36-37

Attributes/classifiers: none

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### rule at lines 38-41

Attributes/classifiers: none

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### syntax at lines 42-42

Attributes/classifiers: function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### rule at lines 43-43

Attributes/classifiers: none

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### rule at lines 44-46

Attributes/classifiers: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### rule at lines 47-50

Attributes/classifiers: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### syntax at lines 51-51

Attributes/classifiers: function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### rule at lines 52-52

Attributes/classifiers: none

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### rule at lines 53-53

Attributes/classifiers: none

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### rule at lines 54-55

Attributes/classifiers: none

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### syntax at lines 56-56

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### rule at lines 57-57

Attributes/classifiers: none

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### rule at lines 58-58

Attributes/classifiers: none

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### rule at lines 59-59

Attributes/classifiers: owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### endmodule at lines 60-60

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/controls.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-CONTROLS
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports MPY-TUPLE
```

### imports at lines 6-8

Attributes/classifiers: none

```k
  imports MPY-ITER

  // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==
```

### rule at lines 9-11

Attributes/classifiers: none

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule at lines 12-19

Attributes/classifiers: priority

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### rule at lines 20-26

Attributes/classifiers: none

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### rule at lines 27-34

Attributes/classifiers: priority

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### rule at lines 35-35

Attributes/classifiers: none

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### rule at lines 36-36

Attributes/classifiers: owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### syntax at lines 37-37

Attributes/classifiers: none

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### rule at lines 38-38

Attributes/classifiers: none

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### rule at lines 39-42

Attributes/classifiers: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### rule at lines 43-47

Attributes/classifiers: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### rule at lines 48-50

Attributes/classifiers: none

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### syntax at lines 51-51

Attributes/classifiers: none

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### rule at lines 52-52

Attributes/classifiers: none

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### rule at lines 53-53

Attributes/classifiers: none

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### rule at lines 54-56

Attributes/classifiers: none

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### rule at lines 57-58

Attributes/classifiers: none

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### rule at lines 59-64

Attributes/classifiers: none

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### syntax at lines 65-68

Attributes/classifiers: none

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### rule at lines 69-70

Attributes/classifiers: none

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### rule at lines 71-71

Attributes/classifiers: none

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### rule at lines 72-72

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### rule at lines 73-76

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### rule at lines 77-77

Attributes/classifiers: none

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### rule at lines 78-78

Attributes/classifiers: none

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### rule at lines 79-80

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### rule at lines 81-84

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### rule at lines 85-85

Attributes/classifiers: none

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule at lines 86-86

Attributes/classifiers: none

```k
  rule <k> Continue => #cont ... </k>
```

### rule at lines 87-87

Attributes/classifiers: none

```k
  rule <k> Break => #brk ... </k>
```

### rule at lines 88-88

Attributes/classifiers: none

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule at lines 89-89

Attributes/classifiers: owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### rule at lines 90-90

Attributes/classifiers: none

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### rule at lines 91-94

Attributes/classifiers: priority, owise

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### rule at lines 95-97

Attributes/classifiers: priority

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at lines 98-100

Attributes/classifiers: priority

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at lines 101-105

Attributes/classifiers: priority

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### rule at lines 106-108

Attributes/classifiers: priority

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### endmodule at lines 109-109

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/core.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-CORE
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-SYNTAX
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports INT
```

### imports at lines 6-6

Attributes/classifiers: none

```k
  imports BOOL
```

### imports at lines 7-7

Attributes/classifiers: none

```k
  imports STRING
```

### imports at lines 8-8

Attributes/classifiers: none

```k
  imports MAP
```

### imports at lines 9-9

Attributes/classifiers: none

```k
  imports LIST
```

### imports at lines 10-12

Attributes/classifiers: none

```k
  imports K-EQUAL

  // ==== values, the algebraic lists, and the scope heap =====================
```

### syntax at lines 13-13

Attributes/classifiers: none

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### syntax at lines 14-14

Attributes/classifiers: none

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### syntax at lines 15-17

Attributes/classifiers: none

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### syntax at lines 18-24

Attributes/classifiers: none

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### syntax at lines 25-35

Attributes/classifiers: function

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

### syntax at lines 36-36

Attributes/classifiers: none

```k
  syntax Parent   ::= "root" | parent(Int)
```

### syntax at lines 37-37

Attributes/classifiers: none

```k
  syntax Scope    ::= scope(Map, Parent)
```

### syntax at lines 38-38

Attributes/classifiers: none

```k
  syntax KResult  ::= Val
```

### syntax at lines 39-39

Attributes/classifiers: none

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### syntax at lines 40-40

Attributes/classifiers: none

```k
  syntax Vals     ::= List{Val, ","}
```

### syntax at lines 41-41

Attributes/classifiers: none

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### syntax at lines 42-48

Attributes/classifiers: none

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### configuration at lines 49-67

Attributes/classifiers: none

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

### syntax at lines 68-68

Attributes/classifiers: function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### rule at lines 69-69

Attributes/classifiers: none

```k
  rule isRefV(ref(_:Int)) => true
```

### rule at lines 70-74

Attributes/classifiers: owise

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### syntax at lines 75-75

Attributes/classifiers: none

```k
  syntax HeapVal ::= cellV(Val)
```

### syntax at lines 76-76

Attributes/classifiers: function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### rule at lines 77-77

Attributes/classifiers: none

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### rule at lines 78-84

Attributes/classifiers: function, owise

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### rule at lines 85-94

Attributes/classifiers: priority

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

### syntax at lines 95-95

Attributes/classifiers: none

```k
  syntax Val ::= kwV(String, Val)
```

### syntax at lines 96-96

Attributes/classifiers: none

```k
  syntax KItem ::= #kwTag(String)
```

### rule at lines 97-97

Attributes/classifiers: none

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### rule at lines 98-99

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### syntax at lines 100-100

Attributes/classifiers: function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### rule at lines 101-101

Attributes/classifiers: none

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### rule at lines 102-105

Attributes/classifiers: owise

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### syntax at lines 106-106

Attributes/classifiers: none

```k
  syntax Val ::= cellsMark(ParamNames)
```

### syntax at lines 107-107

Attributes/classifiers: function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### rule at lines 108-108

Attributes/classifiers: none

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### syntax at lines 109-109

Attributes/classifiers: function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### rule at lines 110-110

Attributes/classifiers: none

```k
  rule pnMember(_:String, .ParamNames) => false
```

### rule at lines 111-112

Attributes/classifiers: none

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### syntax at lines 113-113

Attributes/classifiers: none

```k
  syntax KItem ::= #cellW(Val, Val)
```

### rule at lines 114-116

Attributes/classifiers: none

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### syntax at lines 117-117

Attributes/classifiers: none

```k
  syntax KItem ::= #alloc(Val)
```

### rule at lines 118-123

Attributes/classifiers: none

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### syntax at lines 124-124

Attributes/classifiers: none

```k
  syntax KItem ::= #loadAll(Module)
```

### rule at lines 125-125

Attributes/classifiers: none

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### rule at lines 126-126

Attributes/classifiers: none

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### rule at lines 127-129

Attributes/classifiers: none

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### syntax at lines 130-130

Attributes/classifiers: none

```k
  syntax KItem ::= #look(String, Int)
```

### rule at lines 131-131

Attributes/classifiers: none

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### rule at lines 132-144

Attributes/classifiers: function, priority, concrete

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

### rule at lines 145-151

Attributes/classifiers: priority

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### rule at lines 152-156

Attributes/classifiers: none

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### syntax at lines 157-157

Attributes/classifiers: function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### rule at lines 158-184

Attributes/classifiers: none

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

### syntax at lines 185-185

Attributes/classifiers: none

```k
  syntax ApplyK ::= toCall(Val)
```

### syntax at lines 186-188

Attributes/classifiers: none

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### rule at lines 189-189

Attributes/classifiers: none

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### rule at lines 190-190

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### rule at lines 191-193

Attributes/classifiers: none

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### rule at lines 194-194

Attributes/classifiers: none

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### rule at lines 195-195

Attributes/classifiers: none

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### rule at lines 196-198

Attributes/classifiers: none

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### syntax at lines 199-199

Attributes/classifiers: function

```k
  syntax Bool ::= truthy(Val) [function]
```

### rule at lines 200-200

Attributes/classifiers: none

```k
  rule truthy(B:Bool)          => B
```

### rule at lines 201-201

Attributes/classifiers: none

```k
  rule truthy(noneV)           => false
```

### rule at lines 202-202

Attributes/classifiers: none

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### rule at lines 203-203

Attributes/classifiers: none

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### rule at lines 204-204

Attributes/classifiers: none

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### rule at lines 205-207

Attributes/classifiers: none

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### syntax at lines 208-208

Attributes/classifiers: function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### syntax at lines 209-209

Attributes/classifiers: function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### syntax at lines 210-212

Attributes/classifiers: function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### syntax at lines 213-213

Attributes/classifiers: function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### rule at lines 214-214

Attributes/classifiers: none

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### rule at lines 215-216

Attributes/classifiers: none

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### syntax at lines 217-217

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### rule at lines 218-218

Attributes/classifiers: none

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### rule at lines 219-222

Attributes/classifiers: none

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### syntax at lines 223-223

Attributes/classifiers: function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### rule at lines 224-224

Attributes/classifiers: none

```k
  rule vsLen(.ValSeq)                => 0
```

### rule at lines 225-226

Attributes/classifiers: none

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### syntax at lines 227-227

Attributes/classifiers: function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### rule at lines 228-228

Attributes/classifiers: none

```k
  rule isLen(.IntSeq)                => 0
```

### rule at lines 229-232

Attributes/classifiers: none

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### syntax at lines 233-233

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### rule at lines 234-234

Attributes/classifiers: none

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### rule at lines 235-235

Attributes/classifiers: none

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### rule at lines 236-237

Attributes/classifiers: none

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### rule at lines 238-239

Attributes/classifiers: none

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### endmodule at lines 240-240

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/dict.k`

### module at lines 13-13

Attributes/classifiers: none

```k
module MPY-DICT
```

### imports at lines 14-14

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 15-15

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### imports at lines 16-16

Attributes/classifiers: none

```k
  imports MPY-METHODS
```

### imports at lines 17-19

Attributes/classifiers: none

```k
  imports MPY-LIST

  // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).
```

### syntax at lines 20-22

Attributes/classifiers: none

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### syntax at lines 23-25

Attributes/classifiers: none

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### rule at lines 26-26

Attributes/classifiers: none

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### rule at lines 27-27

Attributes/classifiers: none

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### rule at lines 28-29

Attributes/classifiers: none

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### rule at lines 30-31

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### rule at lines 32-36

Attributes/classifiers: total, concrete

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### syntax at lines 37-37

Attributes/classifiers: function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### rule at lines 38-38

Attributes/classifiers: none

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### rule at lines 39-39

Attributes/classifiers: none

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### rule at lines 40-42

Attributes/classifiers: none

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### syntax at lines 43-43

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### rule at lines 44-44

Attributes/classifiers: none

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### rule at lines 45-48

Attributes/classifiers: owise

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### syntax at lines 49-49

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### rule at lines 50-51

Attributes/classifiers: none

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### rule at lines 52-53

Attributes/classifiers: none

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### rule at lines 54-57

Attributes/classifiers: owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### rule at lines 58-62

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### rule at lines 63-63

Attributes/classifiers: none

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### syntax at lines 64-64

Attributes/classifiers: function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### rule at lines 65-69

Attributes/classifiers: priority

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### syntax at lines 70-70

Attributes/classifiers: function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### rule at lines 71-75

Attributes/classifiers: none

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### syntax at lines 76-76

Attributes/classifiers: none

```k
  syntax KItem ::= #dsetK(String, Val)
```

### rule at lines 77-77

Attributes/classifiers: none

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### rule at lines 78-81

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### rule at lines 82-85

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### syntax at lines 86-86

Attributes/classifiers: none

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### rule at lines 87-89

Attributes/classifiers: none

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### syntax at lines 90-90

Attributes/classifiers: function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### rule at lines 91-91

Attributes/classifiers: none

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule at lines 92-94

Attributes/classifiers: none

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### rule at lines 95-96

Attributes/classifiers: none

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### syntax at lines 97-97

Attributes/classifiers: function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### rule at lines 98-98

Attributes/classifiers: none

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### rule at lines 99-100

Attributes/classifiers: none

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### syntax at lines 101-101

Attributes/classifiers: function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### rule at lines 102-102

Attributes/classifiers: none

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### rule at lines 103-103

Attributes/classifiers: none

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### endmodule at lines 104-104

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/float.k`

### module at lines 14-14

Attributes/classifiers: none

```k
module MPY-FLOAT
```

### imports at lines 15-15

Attributes/classifiers: none

```k
  imports MPY-OPERATORS
```

### imports at lines 16-16

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### imports at lines 17-19

Attributes/classifiers: none

```k
  imports FLOAT

  // Float is a value; the float literal evaluates to the K Float.
```

### syntax at lines 20-20

Attributes/classifiers: none

```k
  syntax Val ::= Float
```

### rule at lines 21-23

Attributes/classifiers: no-evaluators, concrete

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### syntax at lines 24-24

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### rule at lines 25-26

Attributes/classifiers: concrete

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### rule at lines 27-29

Attributes/classifiers: concrete

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### syntax at lines 30-30

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### rule at lines 31-31

Attributes/classifiers: concrete

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### rule at lines 32-36

Attributes/classifiers: concrete

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### syntax at lines 37-37

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### rule at lines 38-38

Attributes/classifiers: concrete

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### rule at lines 39-42

Attributes/classifiers: concrete

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### rule at lines 43-43

Attributes/classifiers: none

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### rule at lines 44-49

Attributes/classifiers: no-evaluators, concrete

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### syntax at lines 50-50

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### rule at lines 51-51

Attributes/classifiers: concrete

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### rule at lines 52-53

Attributes/classifiers: none

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### syntax at lines 54-54

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### rule at lines 55-55

Attributes/classifiers: concrete

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### rule at lines 56-60

Attributes/classifiers: none

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### rule at lines 61-64

Attributes/classifiers: priority

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### syntax at lines 65-65

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathCeil"
```

### rule at lines 66-66

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### rule at lines 67-69

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### syntax at lines 70-70

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathFloor"
```

### rule at lines 71-71

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### rule at lines 72-72

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### syntax at lines 73-73

Attributes/classifiers: function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### rule at lines 74-74

Attributes/classifiers: concrete

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### rule at lines 75-77

Attributes/classifiers: concrete

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### rule at lines 78-78

Attributes/classifiers: none

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### rule at lines 79-81

Attributes/classifiers: none

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### syntax at lines 82-82

Attributes/classifiers: none

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### rule at lines 83-83

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### rule at lines 84-84

Attributes/classifiers: none

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### rule at lines 85-85

Attributes/classifiers: none

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### syntax at lines 86-86

Attributes/classifiers: function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### rule at lines 87-87

Attributes/classifiers: concrete

```k
  rule toF(F:Float) => F        [concrete]
```

### rule at lines 88-92

Attributes/classifiers: concrete

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### syntax at lines 93-93

Attributes/classifiers: function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### rule at lines 94-94

Attributes/classifiers: concrete

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### rule at lines 95-98

Attributes/classifiers: concrete

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### rule at lines 99-102

Attributes/classifiers: no-evaluators, concrete

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### syntax at lines 103-103

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### rule at lines 104-104

Attributes/classifiers: concrete

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### rule at lines 105-106

Attributes/classifiers: none

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### syntax at lines 107-107

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### rule at lines 108-108

Attributes/classifiers: concrete

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### rule at lines 109-110

Attributes/classifiers: none

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### syntax at lines 111-111

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### rule at lines 112-112

Attributes/classifiers: concrete

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### rule at lines 113-114

Attributes/classifiers: none

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### syntax at lines 115-115

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### rule at lines 116-116

Attributes/classifiers: concrete

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### rule at lines 117-118

Attributes/classifiers: none

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### syntax at lines 119-119

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### rule at lines 120-120

Attributes/classifiers: concrete

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### rule at lines 121-124

Attributes/classifiers: none

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### syntax at lines 125-125

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### rule at lines 126-126

Attributes/classifiers: concrete

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### rule at lines 127-127

Attributes/classifiers: none

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### rule at lines 128-128

Attributes/classifiers: none

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### rule at lines 129-131

Attributes/classifiers: none

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### rule at lines 132-132

Attributes/classifiers: none

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### rule at lines 133-133

Attributes/classifiers: none

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### rule at lines 134-134

Attributes/classifiers: none

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### rule at lines 135-135

Attributes/classifiers: none

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### rule at lines 136-136

Attributes/classifiers: none

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### rule at lines 137-137

Attributes/classifiers: none

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### rule at lines 138-138

Attributes/classifiers: none

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### rule at lines 139-141

Attributes/classifiers: concrete

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### syntax at lines 142-142

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### rule at lines 143-143

Attributes/classifiers: concrete

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### rule at lines 144-144

Attributes/classifiers: none

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### rule at lines 145-145

Attributes/classifiers: none

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### rule at lines 146-146

Attributes/classifiers: none

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### rule at lines 147-147

Attributes/classifiers: none

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### rule at lines 148-148

Attributes/classifiers: none

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule at lines 149-149

Attributes/classifiers: none

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule at lines 150-150

Attributes/classifiers: none

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### rule at lines 151-153

Attributes/classifiers: none

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### rule at lines 154-154

Attributes/classifiers: none

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### rule at lines 155-159

Attributes/classifiers: concrete

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### syntax at lines 160-160

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### rule at lines 161-161

Attributes/classifiers: concrete

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### rule at lines 162-164

Attributes/classifiers: concrete

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### syntax at lines 165-165

Attributes/classifiers: function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### rule at lines 166-166

Attributes/classifiers: none

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### syntax at lines 167-167

Attributes/classifiers: function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### rule at lines 168-168

Attributes/classifiers: none

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### rule at lines 169-169

Attributes/classifiers: none

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### rule at lines 170-170

Attributes/classifiers: none

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### rule at lines 171-172

Attributes/classifiers: none

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### syntax at lines 173-173

Attributes/classifiers: function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### rule at lines 174-174

Attributes/classifiers: none

```k
  rule fracPart(.IntSeq) => 0
```

### rule at lines 175-175

Attributes/classifiers: none

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### rule at lines 176-176

Attributes/classifiers: none

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### rule at lines 177-177

Attributes/classifiers: none

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### rule at lines 178-178

Attributes/classifiers: none

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### syntax at lines 179-179

Attributes/classifiers: function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### rule at lines 180-180

Attributes/classifiers: none

```k
  rule fracScale(.IntSeq) => 1
```

### rule at lines 181-181

Attributes/classifiers: none

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### rule at lines 182-182

Attributes/classifiers: none

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### rule at lines 183-183

Attributes/classifiers: none

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### rule at lines 184-184

Attributes/classifiers: none

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### rule at lines 185-185

Attributes/classifiers: none

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### rule at lines 186-186

Attributes/classifiers: none

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### rule at lines 187-189

Attributes/classifiers: none

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### syntax at lines 190-190

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### rule at lines 191-191

Attributes/classifiers: concrete

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### rule at lines 192-194

Attributes/classifiers: none

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### syntax at lines 195-195

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### rule at lines 196-196

Attributes/classifiers: concrete

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### rule at lines 197-197

Attributes/classifiers: none

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### rule at lines 198-198

Attributes/classifiers: none

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### rule at lines 199-199

Attributes/classifiers: none

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### rule at lines 200-200

Attributes/classifiers: none

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### rule at lines 201-201

Attributes/classifiers: none

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### rule at lines 202-202

Attributes/classifiers: none

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### rule at lines 203-203

Attributes/classifiers: none

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule at lines 204-204

Attributes/classifiers: none

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule at lines 205-205

Attributes/classifiers: none

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### rule at lines 206-208

Attributes/classifiers: none

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### syntax at lines 209-209

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### rule at lines 210-210

Attributes/classifiers: concrete

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### rule at lines 211-212

Attributes/classifiers: none

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### rule at lines 213-213

Attributes/classifiers: none

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### rule at lines 214-216

Attributes/classifiers: none

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### syntax at lines 217-217

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### rule at lines 218-222

Attributes/classifiers: concrete

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### syntax at lines 223-223

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### rule at lines 224-226

Attributes/classifiers: concrete

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### rule at lines 227-227

Attributes/classifiers: none

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### rule at lines 228-229

Attributes/classifiers: none

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### syntax at lines 230-230

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### rule at lines 231-231

Attributes/classifiers: concrete

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### syntax at lines 232-232

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathSqrt"
```

### rule at lines 233-233

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### rule at lines 234-234

Attributes/classifiers: none

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### rule at lines 235-242

Attributes/classifiers: priority, concrete

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### syntax at lines 243-243

Attributes/classifiers: none

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### rule at lines 244-244

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule at lines 245-245

Attributes/classifiers: none

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### rule at lines 246-246

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### rule at lines 247-249

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### syntax at lines 250-250

Attributes/classifiers: none

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### rule at lines 251-251

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule at lines 252-252

Attributes/classifiers: none

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### rule at lines 253-253

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### rule at lines 254-260

Attributes/classifiers: concrete

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### syntax at lines 261-261

Attributes/classifiers: none

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### rule at lines 262-264

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### rule at lines 265-265

Attributes/classifiers: none

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### rule at lines 266-266

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### rule at lines 267-269

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### rule at lines 270-272

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### endmodule at lines 273-273

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/functions.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-FUNCTIONS
```

### imports at lines 4-7

Attributes/classifiers: none

```k
  imports MPY-CORE

  // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k;
  // this module owns the frame lifecycle (bind params, return, pop).
```

### syntax at lines 8-13

Attributes/classifiers: none

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### rule at lines 14-17

Attributes/classifiers: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### syntax at lines 18-18

Attributes/classifiers: none

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### rule at lines 19-26

Attributes/classifiers: none

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### syntax at lines 27-30

Attributes/classifiers: none

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### syntax at lines 31-32

Attributes/classifiers: none

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### rule at lines 33-35

Attributes/classifiers: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### rule at lines 36-41

Attributes/classifiers: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### rule at lines 42-46

Attributes/classifiers: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### rule at lines 47-49

Attributes/classifiers: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### rule at lines 50-52

Attributes/classifiers: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### rule at lines 53-58

Attributes/classifiers: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### rule at lines 59-62

Attributes/classifiers: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### rule at lines 63-63

Attributes/classifiers: none

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### rule at lines 64-67

Attributes/classifiers: none

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### rule at lines 68-77

Attributes/classifiers: priority

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

### rule at lines 78-79

Attributes/classifiers: none

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### rule at lines 80-84

Attributes/classifiers: none

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### rule at lines 85-90

Attributes/classifiers: none

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### endmodule at lines 91-91

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/int.k`

### module at lines 4-4

Attributes/classifiers: none

```k
module MPY-INT
```

### imports at lines 5-6

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### rule at lines 7-8

Attributes/classifiers: none

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### rule at lines 9-10

Attributes/classifiers: none

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### rule at lines 11-11

Attributes/classifiers: none

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### rule at lines 12-12

Attributes/classifiers: none

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### rule at lines 13-13

Attributes/classifiers: none

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### rule at lines 14-14

Attributes/classifiers: none

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### rule at lines 15-15

Attributes/classifiers: none

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### rule at lines 16-16

Attributes/classifiers: none

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### rule at lines 17-18

Attributes/classifiers: none

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### syntax at lines 19-19

Attributes/classifiers: function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### rule at lines 20-21

Attributes/classifiers: none

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### rule at lines 22-22

Attributes/classifiers: none

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### rule at lines 23-23

Attributes/classifiers: none

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### rule at lines 24-24

Attributes/classifiers: none

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### rule at lines 25-25

Attributes/classifiers: none

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### rule at lines 26-26

Attributes/classifiers: none

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### rule at lines 27-27

Attributes/classifiers: none

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### endmodule at lines 28-28

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/iter.k`

### module at lines 6-6

Attributes/classifiers: none

```k
module MPY-ITER
```

### imports at lines 7-7

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### syntax at lines 8-8

Attributes/classifiers: none

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### endmodule at lines 9-9

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/list.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-LIST
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### imports at lines 6-8

Attributes/classifiers: none

```k
  imports MPY-OPERATORS

  // ==== iteration (the iterator protocol's list case) =======================
```

### rule at lines 9-9

Attributes/classifiers: none

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### rule at lines 10-12

Attributes/classifiers: none

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### syntax at lines 13-13

Attributes/classifiers: none

```k
  syntax ApplyK ::= "toList"
```

### rule at lines 14-14

Attributes/classifiers: none

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### rule at lines 15-17

Attributes/classifiers: none

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### syntax at lines 18-18

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### rule at lines 19-19

Attributes/classifiers: none

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### rule at lines 20-23

Attributes/classifiers: priority

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### rule at lines 24-26

Attributes/classifiers: priority

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### rule at lines 27-27

Attributes/classifiers: none

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### rule at lines 28-32

Attributes/classifiers: concrete

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### syntax at lines 33-33

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### rule at lines 34-34

Attributes/classifiers: none

```k
  rule hasRefVS(.ValSeq)                => false
```

### rule at lines 35-36

Attributes/classifiers: none

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### syntax at lines 37-38

Attributes/classifiers: function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### rule at lines 39-39

Attributes/classifiers: none

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### rule at lines 40-40

Attributes/classifiers: none

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### rule at lines 41-41

Attributes/classifiers: none

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### rule at lines 42-44

Attributes/classifiers: none

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### rule at lines 45-46

Attributes/classifiers: none

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### rule at lines 47-48

Attributes/classifiers: none

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### rule at lines 49-49

Attributes/classifiers: none

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### rule at lines 50-52

Attributes/classifiers: owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### rule at lines 53-57

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### syntax at lines 58-58

Attributes/classifiers: none

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### rule at lines 59-59

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### rule at lines 60-60

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### rule at lines 61-61

Attributes/classifiers: none

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### rule at lines 62-62

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### rule at lines 63-64

Attributes/classifiers: none

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### rule at lines 65-66

Attributes/classifiers: none

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### rule at lines 67-67

Attributes/classifiers: none

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### endmodule at lines 68-68

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/methods.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-METHODS
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports K-EQUAL
```

### imports at lines 6-6

Attributes/classifiers: none

```k
  imports MPY-STR
```

### imports at lines 7-9

Attributes/classifiers: none

```k
  imports MPY-LIST

  // method-call routing + arg-eval live in call.k; this module owns applyMethod.
```

### syntax at lines 10-12

Attributes/classifiers: function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### rule at lines 13-13

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### rule at lines 14-14

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### rule at lines 15-15

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### rule at lines 16-18

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### rule at lines 19-19

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### rule at lines 20-20

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### rule at lines 21-25

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### rule at lines 26-26

Attributes/classifiers: none

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### syntax at lines 27-27

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### rule at lines 28-28

Attributes/classifiers: none

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### rule at lines 29-29

Attributes/classifiers: none

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### rule at lines 30-33

Attributes/classifiers: none

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### rule at lines 34-34

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### syntax at lines 35-35

Attributes/classifiers: function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### rule at lines 36-36

Attributes/classifiers: none

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### rule at lines 37-38

Attributes/classifiers: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### rule at lines 39-40

Attributes/classifiers: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### syntax at lines 41-41

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### rule at lines 42-42

Attributes/classifiers: none

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### rule at lines 43-43

Attributes/classifiers: owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### rule at lines 44-46

Attributes/classifiers: none

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### rule at lines 47-47

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### syntax at lines 48-48

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### rule at lines 49-49

Attributes/classifiers: none

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### rule at lines 50-50

Attributes/classifiers: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### rule at lines 51-51

Attributes/classifiers: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### syntax at lines 52-52

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### rule at lines 53-53

Attributes/classifiers: none

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### rule at lines 54-54

Attributes/classifiers: none

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### rule at lines 55-57

Attributes/classifiers: none

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### rule at lines 58-60

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### rule at lines 61-63

Attributes/classifiers: concrete

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### rule at lines 64-64

Attributes/classifiers: none

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### syntax at lines 65-65

Attributes/classifiers: function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### rule at lines 66-66

Attributes/classifiers: none

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### rule at lines 67-67

Attributes/classifiers: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### rule at lines 68-71

Attributes/classifiers: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### rule at lines 72-74

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### syntax at lines 75-75

Attributes/classifiers: function, token

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### rule at lines 76-76

Attributes/classifiers: none

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### rule at lines 77-78

Attributes/classifiers: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### rule at lines 79-81

Attributes/classifiers: token

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### syntax at lines 82-82

Attributes/classifiers: function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### rule at lines 83-83

Attributes/classifiers: none

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### rule at lines 84-84

Attributes/classifiers: none

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### syntax at lines 85-85

Attributes/classifiers: function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### rule at lines 86-88

Attributes/classifiers: none

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### rule at lines 89-93

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### rule at lines 94-96

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### syntax at lines 97-97

Attributes/classifiers: function, token

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### rule at lines 98-98

Attributes/classifiers: none

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### rule at lines 99-100

Attributes/classifiers: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### rule at lines 101-103

Attributes/classifiers: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### rule at lines 104-105

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### syntax at lines 106-106

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### rule at lines 107-107

Attributes/classifiers: none

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### rule at lines 108-108

Attributes/classifiers: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### rule at lines 109-111

Attributes/classifiers: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### syntax at lines 112-112

Attributes/classifiers: function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### rule at lines 113-114

Attributes/classifiers: none

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### syntax at lines 115-115

Attributes/classifiers: function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### rule at lines 116-117

Attributes/classifiers: none

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### syntax at lines 118-118

Attributes/classifiers: function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### rule at lines 119-120

Attributes/classifiers: none

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### syntax at lines 121-121

Attributes/classifiers: function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### rule at lines 122-123

Attributes/classifiers: none

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax at lines 124-124

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### rule at lines 125-125

Attributes/classifiers: none

```k
  rule hasUpper(.IntSeq) => false
```

### rule at lines 126-127

Attributes/classifiers: none

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### syntax at lines 128-128

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### rule at lines 129-129

Attributes/classifiers: none

```k
  rule hasLower(.IntSeq) => false
```

### rule at lines 130-131

Attributes/classifiers: none

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### syntax at lines 132-132

Attributes/classifiers: function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### rule at lines 133-133

Attributes/classifiers: none

```k
  rule allAlpha(.IntSeq) => true
```

### rule at lines 134-135

Attributes/classifiers: none

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### syntax at lines 136-136

Attributes/classifiers: function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### rule at lines 137-137

Attributes/classifiers: none

```k
  rule allDigit(.IntSeq) => true
```

### rule at lines 138-139

Attributes/classifiers: none

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### syntax at lines 140-141

Attributes/classifiers: function, total

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### rule at lines 142-142

Attributes/classifiers: none

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule at lines 143-144

Attributes/classifiers: owise

```k
  rule lowerC(C:Int) => C         [owise]
```

### syntax at lines 145-145

Attributes/classifiers: function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

### rule at lines 146-146

Attributes/classifiers: none

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule at lines 147-148

Attributes/classifiers: owise

```k
  rule upperC(C:Int) => C         [owise]
```

### syntax at lines 149-149

Attributes/classifiers: function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

### rule at lines 150-150

Attributes/classifiers: none

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule at lines 151-151

Attributes/classifiers: none

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule at lines 152-153

Attributes/classifiers: owise

```k
  rule swapC(C:Int) => C         [owise]
```

### syntax at lines 154-154

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### rule at lines 155-155

Attributes/classifiers: none

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### rule at lines 156-157

Attributes/classifiers: none

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### syntax at lines 158-158

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### rule at lines 159-159

Attributes/classifiers: none

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### rule at lines 160-161

Attributes/classifiers: none

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### syntax at lines 162-162

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### rule at lines 163-163

Attributes/classifiers: none

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### rule at lines 164-165

Attributes/classifiers: none

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### syntax at lines 166-166

Attributes/classifiers: function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### rule at lines 167-167

Attributes/classifiers: none

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### rule at lines 168-168

Attributes/classifiers: none

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at lines 169-169

Attributes/classifiers: none

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### endmodule at lines 170-170

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/operators.k`

### module at lines 6-6

Attributes/classifiers: none

```k
module MPY-OPERATORS
```

### imports at lines 7-7

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 8-9

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### rule at lines 10-11

Attributes/classifiers: none

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### rule at lines 12-14

Attributes/classifiers: none

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### context at lines 15-15

Attributes/classifiers: none

```k
  context Compare(HOLE, _)
```

### context at lines 16-16

Attributes/classifiers: none

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### rule at lines 17-18

Attributes/classifiers: owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### rule at lines 19-19

Attributes/classifiers: none

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### rule at lines 20-24

Attributes/classifiers: priority

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### rule at lines 25-27

Attributes/classifiers: priority

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at lines 28-33

Attributes/classifiers: priority

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### rule at lines 34-37

Attributes/classifiers: priority

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### rule at lines 38-43

Attributes/classifiers: priority

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### rule at lines 44-46

Attributes/classifiers: priority

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### endmodule at lines 47-47

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/range.k`

### module at lines 5-5

Attributes/classifiers: none

```k
module MPY-RANGE
```

### imports at lines 6-6

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 7-8

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### syntax at lines 9-9

Attributes/classifiers: function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### rule at lines 10-11

Attributes/classifiers: none

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### syntax at lines 12-12

Attributes/classifiers: function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### rule at lines 13-14

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### rule at lines 15-16

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### rule at lines 17-19

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### rule at lines 20-22

Attributes/classifiers: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### rule at lines 23-24

Attributes/classifiers: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### endmodule at lines 25-25

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/set.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-SET
```

### imports at lines 4-7

Attributes/classifiers: none

```k
  imports MPY-CORE

  // a set value, carried as its distinct codes in first-seen order (order is irrelevant
  // to membership/cardinality — the two observations sets support here).
```

### syntax at lines 8-10

Attributes/classifiers: none

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### syntax at lines 11-11

Attributes/classifiers: function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### rule at lines 12-12

Attributes/classifiers: none

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### rule at lines 13-15

Attributes/classifiers: none

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### syntax at lines 16-17

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### rule at lines 18-18

Attributes/classifiers: none

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### rule at lines 19-19

Attributes/classifiers: none

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### rule at lines 20-21

Attributes/classifiers: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### rule at lines 22-24

Attributes/classifiers: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### syntax at lines 25-25

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### rule at lines 26-26

Attributes/classifiers: none

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### rule at lines 27-30

Attributes/classifiers: none

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### syntax at lines 31-31

Attributes/classifiers: function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### rule at lines 32-32

Attributes/classifiers: none

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### rule at lines 33-34

Attributes/classifiers: none

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### syntax at lines 35-35

Attributes/classifiers: function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### rule at lines 36-38

Attributes/classifiers: none

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### rule at lines 39-39

Attributes/classifiers: none

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### endmodule at lines 40-40

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/sort.k`

### module at lines 10-10

Attributes/classifiers: none

```k
module MPY-SORT
```

### imports at lines 11-11

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### imports at lines 12-17

Attributes/classifiers: no-evaluators, concrete

```k
  imports MPY-SUBSCRIPT

  // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators);
  // concrete insertion sort for krun.
  // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal
  // (lemmas-only) is not available in the semantics. Int and str lists.
```

### syntax at lines 18-18

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### syntax at lines 19-19

Attributes/classifiers: function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### rule at lines 20-20

Attributes/classifiers: concrete

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### rule at lines 21-21

Attributes/classifiers: concrete

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### rule at lines 22-22

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### rule at lines 23-23

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### rule at lines 24-25

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### syntax at lines 26-26

Attributes/classifiers: function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### rule at lines 27-27

Attributes/classifiers: concrete

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### rule at lines 28-28

Attributes/classifiers: concrete

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### rule at lines 29-30

Attributes/classifiers: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### rule at lines 31-35

Attributes/classifiers: owise, concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### rule at lines 36-39

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### rule at lines 40-48

Attributes/classifiers: priority, concrete

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

### syntax at lines 49-50

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### syntax at lines 51-52

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### rule at lines 53-53

Attributes/classifiers: none

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### rule at lines 54-54

Attributes/classifiers: none

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### rule at lines 55-56

Attributes/classifiers: none

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### syntax at lines 57-57

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### rule at lines 58-58

Attributes/classifiers: none

```k
  rule condRev(S:ValSeq, false) => S
```

### rule at lines 59-60

Attributes/classifiers: none

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### rule at lines 61-62

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### rule at lines 63-64

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### rule at lines 65-71

Attributes/classifiers: total, concrete

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

### endmodule at lines 72-72

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/str.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-STR
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 5-7

Attributes/classifiers: none

```k
  imports MPY-ITER

  // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==
```

### rule at lines 8-8

Attributes/classifiers: none

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### rule at lines 9-12

Attributes/classifiers: none

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### syntax at lines 13-13

Attributes/classifiers: function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### rule at lines 14-14

Attributes/classifiers: none

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### rule at lines 15-15

Attributes/classifiers: none

```k
  rule strToCodes("") => .IntSeq
```

### rule at lines 16-19

Attributes/classifiers: none

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### syntax at lines 20-20

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### rule at lines 21-21

Attributes/classifiers: none

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### rule at lines 22-23

Attributes/classifiers: none

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### rule at lines 24-24

Attributes/classifiers: none

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### rule at lines 25-25

Attributes/classifiers: none

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### rule at lines 26-28

Attributes/classifiers: none

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### rule at lines 29-29

Attributes/classifiers: none

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### rule at lines 30-31

Attributes/classifiers: none

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### syntax at lines 32-32

Attributes/classifiers: function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### rule at lines 33-33

Attributes/classifiers: none

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### rule at lines 34-34

Attributes/classifiers: none

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at lines 35-36

Attributes/classifiers: none

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### syntax at lines 37-37

Attributes/classifiers: function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### rule at lines 38-38

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### rule at lines 39-39

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### rule at lines 40-47

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### syntax at lines 48-48

Attributes/classifiers: function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### rule at lines 49-49

Attributes/classifiers: none

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### rule at lines 50-50

Attributes/classifiers: none

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### rule at lines 51-51

Attributes/classifiers: none

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at lines 52-52

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### rule at lines 53-53

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### rule at lines 54-55

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### rule at lines 56-56

Attributes/classifiers: none

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### rule at lines 57-57

Attributes/classifiers: none

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### rule at lines 58-58

Attributes/classifiers: none

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### rule at lines 59-59

Attributes/classifiers: none

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### endmodule at lines 60-60

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/subscript.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-SUBSCRIPT
```

### imports at lines 4-10

Attributes/classifiers: total

```k
  imports MPY-CORE

  // ==== positional access + negative-index normalization (used only here) ===
  // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g.
  // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the
  // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total
  // atK. K trusts the [total] annotation; valid programs index in-bounds.
```

### syntax at lines 11-11

Attributes/classifiers: function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### rule at lines 12-12

Attributes/classifiers: none

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### rule at lines 13-15

Attributes/classifiers: none

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### syntax at lines 16-16

Attributes/classifiers: function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### rule at lines 17-17

Attributes/classifiers: none

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### rule at lines 18-20

Attributes/classifiers: none

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### syntax at lines 21-21

Attributes/classifiers: function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### rule at lines 22-22

Attributes/classifiers: none

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule at lines 23-26

Attributes/classifiers: strict

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### context at lines 27-27

Attributes/classifiers: none

```k
  context Subscript(HOLE, _)
```

### context at lines 28-30

Attributes/classifiers: none

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### rule at lines 31-34

Attributes/classifiers: priority

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at lines 35-36

Attributes/classifiers: none

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### syntax at lines 37-37

Attributes/classifiers: function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### rule at lines 38-38

Attributes/classifiers: none

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule at lines 39-39

Attributes/classifiers: none

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule at lines 40-43

Attributes/classifiers: none

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### syntax at lines 44-48

Attributes/classifiers: none

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### syntax at lines 49-49

Attributes/classifiers: none

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### rule at lines 50-50

Attributes/classifiers: none

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### rule at lines 51-51

Attributes/classifiers: none

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### rule at lines 52-53

Attributes/classifiers: none

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### rule at lines 54-54

Attributes/classifiers: none

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### rule at lines 55-55

Attributes/classifiers: none

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### rule at lines 56-57

Attributes/classifiers: none

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### rule at lines 58-60

Attributes/classifiers: priority

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### rule at lines 61-62

Attributes/classifiers: none

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### syntax at lines 63-63

Attributes/classifiers: function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### rule at lines 64-65

Attributes/classifiers: none

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule at lines 66-67

Attributes/classifiers: none

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule at lines 68-71

Attributes/classifiers: none

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### syntax at lines 72-72

Attributes/classifiers: function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### rule at lines 73-73

Attributes/classifiers: none

```k
  rule slStep(noB)          => 1
```

### rule at lines 74-75

Attributes/classifiers: none

```k
  rule slStep(someB(S:Int)) => S
```

### syntax at lines 76-76

Attributes/classifiers: function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### rule at lines 77-78

Attributes/classifiers: none

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### rule at lines 79-80

Attributes/classifiers: none

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### rule at lines 81-82

Attributes/classifiers: none

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax at lines 83-83

Attributes/classifiers: function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### rule at lines 84-85

Attributes/classifiers: none

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### rule at lines 86-87

Attributes/classifiers: none

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### rule at lines 88-89

Attributes/classifiers: none

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax at lines 90-90

Attributes/classifiers: function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### rule at lines 91-92

Attributes/classifiers: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### rule at lines 93-95

Attributes/classifiers: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### syntax at lines 96-96

Attributes/classifiers: function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### rule at lines 97-98

Attributes/classifiers: none

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### rule at lines 99-101

Attributes/classifiers: none

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### syntax at lines 102-102

Attributes/classifiers: function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### rule at lines 103-104

Attributes/classifiers: none

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### rule at lines 105-108

Attributes/classifiers: none

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### syntax at lines 109-109

Attributes/classifiers: function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### rule at lines 110-112

Attributes/classifiers: none

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### rule at lines 113-115

Attributes/classifiers: none

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### syntax at lines 116-116

Attributes/classifiers: function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### rule at lines 117-119

Attributes/classifiers: none

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### rule at lines 120-121

Attributes/classifiers: none

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### endmodule at lines 122-122

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/syntax.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-SYNTAX
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports INT-SYNTAX
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports FLOAT-SYNTAX
```

### imports at lines 6-6

Attributes/classifiers: none

```k
  imports BOOL-SYNTAX
```

### imports at lines 7-8

Attributes/classifiers: none

```k
  imports STRING-SYNTAX
```

### syntax at lines 9-31

Attributes/classifiers: macro, strict, seqstrict

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

### syntax at lines 32-32

Attributes/classifiers: none

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### syntax at lines 33-33

Attributes/classifiers: none

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### syntax at lines 34-34

Attributes/classifiers: none

```k
  syntax Entries  ::= List{Entry, ","}
```

### syntax at lines 35-35

Attributes/classifiers: none

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### syntax at lines 36-36

Attributes/classifiers: none

```k
  syntax CompFors ::= List{CompFor, ""}
```

### syntax at lines 37-37

Attributes/classifiers: none

```k
  syntax Exprs    ::= List{Expr, ","}
```

### syntax at lines 38-38

Attributes/classifiers: none

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### syntax at lines 39-40

Attributes/classifiers: none

```k
  syntax Bound    ::= Expr | "NoBound"
```

### syntax at lines 41-55

Attributes/classifiers: strict

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

### syntax at lines 56-56

Attributes/classifiers: none

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### syntax at lines 57-57

Attributes/classifiers: none

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### syntax at lines 58-58

Attributes/classifiers: none

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### syntax at lines 59-59

Attributes/classifiers: none

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### syntax at lines 60-60

Attributes/classifiers: none

```k
  syntax ParamNames ::= List{String, ","}
```

### syntax at lines 61-61

Attributes/classifiers: none

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### endmodule at lines 62-62

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics/tuple.k`

### module at lines 3-3

Attributes/classifiers: none

```k
module MPY-TUPLE
```

### imports at lines 4-4

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 5-5

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### imports at lines 6-6

Attributes/classifiers: none

```k
  imports MPY-LIST
```

### imports at lines 7-9

Attributes/classifiers: none

```k
  imports MPY-METHODS

  // ==== iteration (the iterator protocol's tuple case) ======================
```

### rule at lines 10-10

Attributes/classifiers: none

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### rule at lines 11-13

Attributes/classifiers: none

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### syntax at lines 14-14

Attributes/classifiers: none

```k
  syntax ApplyK ::= "toTuple"
```

### rule at lines 15-15

Attributes/classifiers: none

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### rule at lines 16-17

Attributes/classifiers: none

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### rule at lines 18-19

Attributes/classifiers: none

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### rule at lines 20-20

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### rule at lines 21-22

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### rule at lines 23-23

Attributes/classifiers: none

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### syntax at lines 24-24

Attributes/classifiers: function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### rule at lines 25-25

Attributes/classifiers: none

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### rule at lines 26-27

Attributes/classifiers: none

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### rule at lines 28-30

Attributes/classifiers: none

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### syntax at lines 31-31

Attributes/classifiers: none

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### rule at lines 32-34

Attributes/classifiers: none

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule at lines 35-41

Attributes/classifiers: priority

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### rule at lines 42-42

Attributes/classifiers: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule at lines 43-43

Attributes/classifiers: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule at lines 44-48

Attributes/classifiers: priority

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### syntax at lines 49-49

Attributes/classifiers: none

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### rule at lines 50-50

Attributes/classifiers: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule at lines 51-51

Attributes/classifiers: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule at lines 52-54

Attributes/classifiers: priority

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at lines 55-56

Attributes/classifiers: none

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### rule at lines 57-57

Attributes/classifiers: none

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### endmodule at lines 58-58

Attributes/classifiers: none

```k
endmodule
```

## `reference-semantics/semantics.k`

### requires at lines 34-34

Attributes/classifiers: none

```k
requires "semantics/syntax.k"
```

### requires at lines 35-35

Attributes/classifiers: none

```k
requires "semantics/core.k"
```

### requires at lines 36-36

Attributes/classifiers: none

```k
requires "semantics/iter.k"
```

### requires at lines 37-37

Attributes/classifiers: none

```k
requires "semantics/range.k"
```

### requires at lines 38-38

Attributes/classifiers: none

```k
requires "semantics/operators.k"
```

### requires at lines 39-39

Attributes/classifiers: none

```k
requires "semantics/int.k"
```

### requires at lines 40-40

Attributes/classifiers: none

```k
requires "semantics/bool.k"
```

### requires at lines 41-41

Attributes/classifiers: none

```k
requires "semantics/float.k"
```

### requires at lines 42-42

Attributes/classifiers: none

```k
requires "semantics/str.k"
```

### requires at lines 43-43

Attributes/classifiers: none

```k
requires "semantics/set.k"
```

### requires at lines 44-44

Attributes/classifiers: none

```k
requires "semantics/list.k"
```

### requires at lines 45-45

Attributes/classifiers: none

```k
requires "semantics/tuple.k"
```

### requires at lines 46-46

Attributes/classifiers: none

```k
requires "semantics/subscript.k"
```

### requires at lines 47-47

Attributes/classifiers: none

```k
requires "semantics/comprehension.k"
```

### requires at lines 48-48

Attributes/classifiers: none

```k
requires "semantics/methods.k"
```

### requires at lines 49-49

Attributes/classifiers: none

```k
requires "semantics/controls.k"
```

### requires at lines 50-50

Attributes/classifiers: none

```k
requires "semantics/functions.k"
```

### requires at lines 51-51

Attributes/classifiers: none

```k
requires "semantics/builtins.k"
```

### requires at lines 52-52

Attributes/classifiers: none

```k
requires "semantics/call.k"
```

### requires at lines 53-53

Attributes/classifiers: none

```k
requires "semantics/sort.k"
```

### requires at lines 54-54

Attributes/classifiers: none

```k
requires "semantics/assert.k"
```

### requires at lines 55-55

Attributes/classifiers: none

```k
requires "semantics/dict.k"
```

### requires at lines 56-57

Attributes/classifiers: concrete

```k
requires "semantics/concrete.k"
```

### module at lines 58-58

Attributes/classifiers: none

```k
module MPY
```

### imports at lines 59-59

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### imports at lines 60-60

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### imports at lines 61-61

Attributes/classifiers: none

```k
  imports MPY-RANGE
```

### imports at lines 62-62

Attributes/classifiers: none

```k
  imports MPY-OPERATORS
```

### imports at lines 63-63

Attributes/classifiers: none

```k
  imports MPY-INT
```

### imports at lines 64-64

Attributes/classifiers: none

```k
  imports MPY-BOOL
```

### imports at lines 65-65

Attributes/classifiers: none

```k
  imports MPY-FLOAT
```

### imports at lines 66-66

Attributes/classifiers: none

```k
  imports MPY-STR
```

### imports at lines 67-67

Attributes/classifiers: none

```k
  imports MPY-SET
```

### imports at lines 68-68

Attributes/classifiers: none

```k
  imports MPY-LIST
```

### imports at lines 69-69

Attributes/classifiers: none

```k
  imports MPY-TUPLE
```

### imports at lines 70-70

Attributes/classifiers: none

```k
  imports MPY-SUBSCRIPT
```

### imports at lines 71-71

Attributes/classifiers: none

```k
  imports MPY-COMPREHENSION
```

### imports at lines 72-72

Attributes/classifiers: none

```k
  imports MPY-METHODS
```

### imports at lines 73-73

Attributes/classifiers: none

```k
  imports MPY-CONTROLS
```

### imports at lines 74-74

Attributes/classifiers: none

```k
  imports MPY-FUNCTIONS
```

### imports at lines 75-75

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### imports at lines 76-76

Attributes/classifiers: none

```k
  imports MPY-CALL
```

### imports at lines 77-77

Attributes/classifiers: none

```k
  imports MPY-SORT
```

### imports at lines 78-78

Attributes/classifiers: none

```k
  imports MPY-ASSERT
```

### imports at lines 79-79

Attributes/classifiers: none

```k
  imports MPY-DICT
```

### endmodule at lines 80-86

Attributes/classifiers: concrete

```k
endmodule

// The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's
// real key calls, deep list equality). Verification builds import MPY and
// never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN —
// with plain MPY the concrete legs are silently absent (this was live for a
// while: sorted-key stuck and comprehension asserted wrong under krun).
```

### module at lines 87-87

Attributes/classifiers: none

```k
module MPY-KRUN
```

### imports at lines 88-88

Attributes/classifiers: none

```k
  imports MPY
```

### imports at lines 89-89

Attributes/classifiers: none

```k
  imports MPY-CONCRETE
```

### endmodule at lines 90-90

Attributes/classifiers: none

```k
endmodule
```

## `verification.k`

### requires at lines 1-2

Attributes/classifiers: none

```k
requires "reference-semantics/semantics.k"
```

### module at lines 3-3

Attributes/classifiers: none

```k
module BY-LENGTH-VERIFICATION
```

### imports at lines 4-8

Attributes/classifiers: function

```k
  imports MPY

  // The exact function body emitted in solution.mpy.  Keeping the source AST
  // here makes the proof execute the submitted implementation, not a second
  // hand-written algorithm.
```

### syntax at lines 9-9

Attributes/classifiers: function, total

```k
  syntax Stmts ::= "byLengthBody" [function, total]
```

### rule at lines 10-48

Attributes/classifiers: none

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

### syntax at lines 49-49

Attributes/classifiers: function, total

```k
  syntax Val ::= "byLengthClosure" [function, total]
```

### rule at lines 50-53

Attributes/classifiers: none

```k
  rule byLengthClosure => closureVal("arr", byLengthBody, 0)

  // Embed an arbitrary sequence of mathematical integers as Python values.
  // Quantifying IS:IntSeq in spec.k therefore covers every finite integer list.
```

### syntax at lines 54-54

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= intVals(IntSeq) [function, total]
```

### rule at lines 55-55

Attributes/classifiers: none

```k
  rule intVals(.IntSeq) => .ValSeq
```

### rule at lines 56-59

Attributes/classifiers: none

```k
  rule intVals(iCons(I:Int, IS:IntSeq)) => vCons(I, intVals(IS))

  // Contract-level filtering: retain exactly the values in [1, 9], preserving
  // duplicates and their relative order before the trusted sort.
```

### syntax at lines 60-60

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= filterDigits(ValSeq) [function, total]
```

### rule at lines 61-61

Attributes/classifiers: none

```k
  rule filterDigits(.ValSeq) => .ValSeq
```

### rule at lines 62-64

Attributes/classifiers: none

```k
  rule filterDigits(vCons(I:Int, REST:ValSeq))
    => vCons(I, filterDigits(REST))
    requires I >=Int 1 andBool I <=Int 9
```

### rule at lines 65-68

Attributes/classifiers: none

```k
  rule filterDigits(vCons(I:Int, REST:ValSeq))
    => filterDigits(REST)
    requires I <Int 1 orBool I >Int 9
```

### syntax at lines 69-69

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= "nameTable" [function, total]
```

### rule at lines 70-81

Attributes/classifiers: none

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

### syntax at lines 82-82

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= tableNames(ValSeq) [function, total]
```

### rule at lines 83-83

Attributes/classifiers: none

```k
  rule tableNames(.ValSeq) => .ValSeq
```

### rule at lines 84-88

Attributes/classifiers: none

```k
  rule tableNames(vCons(I:Int, REST:ValSeq))
    => vCons(valSeqAt(nameTable, I -Int 1), tableNames(REST))

  // Observe the structure of a returned heap list so that the postcondition
  // states the actual Python return value rather than an allocation address.
```

### syntax at lines 89-89

Attributes/classifiers: none

```k
  syntax KItem ::= "#observeList"
```

### rule at lines 90-97

Attributes/classifiers: none

```k
  rule <k> ref(H:Int) ~> #observeList => list(VS) ... </k>
       <heap> ... H |-> list(VS:ValSeq) ... </heap>

  // Symbolic summaries for the two source-level loops.  The supplied
  // semantics intentionally leaves sortVS opaque during proof, so a later
  // iteration over revVS(sortVS(...)) cannot constructor-unfold.  These exact
  // AST rules expose the loops' standard filter/map folds while leaving
  // sorted() itself governed by MPY-SORT.
```

### rule at lines 98-125

Attributes/classifiers: priority

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

### rule at lines 126-152

Attributes/classifiers: priority

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
```

### endmodule at lines 153-153

Attributes/classifiers: none

```k
endmodule
```

## `spec.k`

### requires at lines 1-2

Attributes/classifiers: none

```k
requires "verification.k"
```

### module at lines 3-3

Attributes/classifiers: none

```k
module BY-LENGTH-SPEC
```

### imports at lines 4-8

Attributes/classifiers: none

```k
  imports BY-LENGTH-VERIFICATION

  // For every finite list of integers, the implementation returns the
  // English names of exactly the 1..9 values, sorted in descending order.
  // MPY-SORT defines reverse=True as revVS(sortVS(...)).
```

### claim at lines 9-34

Attributes/classifiers: none

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
```

### endmodule at lines 35-35

Attributes/classifiers: none

```k
endmodule
```

# Per-file counts

- `reference-semantics/semantics/assert.k`: attr:priority=1, endmodule=1, imports=1, module=1, rule=3
- `reference-semantics/semantics/bool.k`: attr:priority=5, context=1, endmodule=1, imports=1, module=1, rule=13
- `reference-semantics/semantics/builtins.k`: attr:concrete=2, attr:function=29, attr:no-evaluators=1, attr:owise=11, attr:priority=1, attr:symbol=1, attr:total=22, endmodule=1, imports=7, module=1, rule=137, syntax=38
- `reference-semantics/semantics/call.k`: attr:function=1, attr:owise=3, attr:priority=5, attr:total=1, endmodule=1, imports=3, module=1, rule=21, syntax=3
- `reference-semantics/semantics/comprehension.k`: attr:macro=2, attr:macro-rec=1, endmodule=1, imports=5, module=1, rule=7, syntax=3
- `reference-semantics/semantics/concrete.k`: attr:concrete=1, attr:function=3, attr:owise=1, attr:priority=3, attr:total=1, endmodule=1, imports=1, module=1, rule=16, syntax=5
- `reference-semantics/semantics/controls.k`: attr:owise=3, attr:priority=7, endmodule=1, imports=3, module=1, rule=34, syntax=3
- `reference-semantics/semantics/core.k`: attr:concrete=1, attr:function=18, attr:owise=3, attr:priority=3, attr:total=10, configuration=1, endmodule=1, imports=7, module=1, rule=46, syntax=37
- `reference-semantics/semantics/dict.k`: attr:concrete=1, attr:function=8, attr:owise=2, attr:priority=2, attr:total=5, endmodule=1, imports=4, module=1, rule=28, syntax=12
- `reference-semantics/semantics/float.k`: attr:concrete=36, attr:function=26, attr:no-evaluators=22, attr:priority=6, attr:symbol=22, attr:total=25, endmodule=1, imports=3, module=1, rule=121, syntax=34
- `reference-semantics/semantics/functions.k`: attr:priority=1, endmodule=1, imports=1, module=1, rule=15, syntax=4
- `reference-semantics/semantics/int.k`: attr:function=1, endmodule=1, imports=1, module=1, rule=16, syntax=1
- `reference-semantics/semantics/iter.k`: endmodule=1, imports=1, module=1, syntax=1
- `reference-semantics/semantics/list.k`: attr:concrete=1, attr:function=3, attr:owise=1, attr:priority=3, attr:total=2, endmodule=1, imports=3, module=1, rule=27, syntax=5
- `reference-semantics/semantics/methods.k`: attr:concrete=1, attr:function=27, attr:owise=4, attr:priority=3, attr:token=3, attr:total=22, endmodule=1, imports=4, module=1, rule=75, syntax=27
- `reference-semantics/semantics/operators.k`: attr:owise=1, attr:priority=6, context=2, endmodule=1, imports=2, module=1, rule=10
- `reference-semantics/semantics/range.k`: attr:function=2, attr:total=1, endmodule=1, imports=2, module=1, rule=6, syntax=2
- `reference-semantics/semantics/set.k`: attr:function=5, attr:total=5, endmodule=1, imports=1, module=1, rule=12, syntax=6
- `reference-semantics/semantics/sort.k`: attr:concrete=12, attr:function=6, attr:no-evaluators=3, attr:owise=1, attr:priority=1, attr:symbol=2, attr:total=5, endmodule=1, imports=2, module=1, rule=19, syntax=6
- `reference-semantics/semantics/str.k`: attr:function=5, attr:total=4, endmodule=1, imports=2, module=1, rule=28, syntax=5
- `reference-semantics/semantics/subscript.k`: attr:function=13, attr:priority=2, attr:strict=1, attr:total=7, context=2, endmodule=1, imports=1, module=1, rule=40, syntax=15
- `reference-semantics/semantics/syntax.k`: attr:macro=1, attr:seqstrict=1, attr:strict=2, endmodule=1, imports=4, module=1, syntax=16
- `reference-semantics/semantics/tuple.k`: attr:function=1, attr:priority=3, endmodule=1, imports=4, module=1, rule=21, syntax=4
- `reference-semantics/semantics.k`: attr:concrete=2, endmodule=2, imports=23, module=2, requires=23
- `verification.k`: attr:function=7, attr:priority=2, attr:total=6, endmodule=1, imports=1, module=1, requires=1, rule=13, syntax=7
- `spec.k`: claim=1, endmodule=1, imports=1, module=1, requires=1

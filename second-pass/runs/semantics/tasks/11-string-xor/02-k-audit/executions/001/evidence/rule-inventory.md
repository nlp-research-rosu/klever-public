# Exhaustive K source inventory

This mechanical inventory covers every top-level module/include/import, configuration, syntax declaration, context, rule, priority declaration, and claim in the supplied semantics plus candidate proof sources.

## Counts

- claim: 2
- configuration: 1
- context: 5
- endmodule: 27
- equational-rule: 476
- import: 88
- module: 27
- operational-rule: 238
- require: 25
- syntax: 237
- total: 1126

### Attribute/classifier occurrences by record

- concrete: 58
- function: 159
- macro: 4
- macro-rec: 1
- no-evaluators: 26
- owise: 30
- priority: 52
- seqstrict: 1
- strict: 3
- symbol: 25
- total: 116

## /reference/reference-semantics/semantics.k

Records: 50

### line 34: require

Attributes/classifiers: none

```k
requires "semantics/syntax.k"
```

### line 35: require

Attributes/classifiers: none

```k
requires "semantics/core.k"
```

### line 36: require

Attributes/classifiers: none

```k
requires "semantics/iter.k"
```

### line 37: require

Attributes/classifiers: none

```k
requires "semantics/range.k"
```

### line 38: require

Attributes/classifiers: none

```k
requires "semantics/operators.k"
```

### line 39: require

Attributes/classifiers: none

```k
requires "semantics/int.k"
```

### line 40: require

Attributes/classifiers: none

```k
requires "semantics/bool.k"
```

### line 41: require

Attributes/classifiers: none

```k
requires "semantics/float.k"
```

### line 42: require

Attributes/classifiers: none

```k
requires "semantics/str.k"
```

### line 43: require

Attributes/classifiers: none

```k
requires "semantics/set.k"
```

### line 44: require

Attributes/classifiers: none

```k
requires "semantics/list.k"
```

### line 45: require

Attributes/classifiers: none

```k
requires "semantics/tuple.k"
```

### line 46: require

Attributes/classifiers: none

```k
requires "semantics/subscript.k"
```

### line 47: require

Attributes/classifiers: none

```k
requires "semantics/comprehension.k"
```

### line 48: require

Attributes/classifiers: none

```k
requires "semantics/methods.k"
```

### line 49: require

Attributes/classifiers: none

```k
requires "semantics/controls.k"
```

### line 50: require

Attributes/classifiers: none

```k
requires "semantics/functions.k"
```

### line 51: require

Attributes/classifiers: none

```k
requires "semantics/builtins.k"
```

### line 52: require

Attributes/classifiers: none

```k
requires "semantics/call.k"
```

### line 53: require

Attributes/classifiers: none

```k
requires "semantics/sort.k"
```

### line 54: require

Attributes/classifiers: none

```k
requires "semantics/assert.k"
```

### line 55: require

Attributes/classifiers: none

```k
requires "semantics/dict.k"
```

### line 56: require

Attributes/classifiers: concrete

```k
requires "semantics/concrete.k"
```

### line 58: module

Attributes/classifiers: none

```k
module MPY
```

### line 59: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 60: import

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### line 61: import

Attributes/classifiers: none

```k
  imports MPY-RANGE
```

### line 62: import

Attributes/classifiers: none

```k
  imports MPY-OPERATORS
```

### line 63: import

Attributes/classifiers: none

```k
  imports MPY-INT
```

### line 64: import

Attributes/classifiers: none

```k
  imports MPY-BOOL
```

### line 65: import

Attributes/classifiers: none

```k
  imports MPY-FLOAT
```

### line 66: import

Attributes/classifiers: none

```k
  imports MPY-STR
```

### line 67: import

Attributes/classifiers: none

```k
  imports MPY-SET
```

### line 68: import

Attributes/classifiers: none

```k
  imports MPY-LIST
```

### line 69: import

Attributes/classifiers: none

```k
  imports MPY-TUPLE
```

### line 70: import

Attributes/classifiers: none

```k
  imports MPY-SUBSCRIPT
```

### line 71: import

Attributes/classifiers: none

```k
  imports MPY-COMPREHENSION
```

### line 72: import

Attributes/classifiers: none

```k
  imports MPY-METHODS
```

### line 73: import

Attributes/classifiers: none

```k
  imports MPY-CONTROLS
```

### line 74: import

Attributes/classifiers: none

```k
  imports MPY-FUNCTIONS
```

### line 75: import

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### line 76: import

Attributes/classifiers: none

```k
  imports MPY-CALL
```

### line 77: import

Attributes/classifiers: none

```k
  imports MPY-SORT
```

### line 78: import

Attributes/classifiers: none

```k
  imports MPY-ASSERT
```

### line 79: import

Attributes/classifiers: none

```k
  imports MPY-DICT
```

### line 80: endmodule

Attributes/classifiers: concrete

```k
endmodule

// The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's
// real key calls, deep list equality). Verification builds import MPY and
// never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN —
// with plain MPY the concrete legs are silently absent (this was live for a
// while: sorted-key stuck and comprehension asserted wrong under krun).
```

### line 87: module

Attributes/classifiers: none

```k
module MPY-KRUN
```

### line 88: import

Attributes/classifiers: none

```k
  imports MPY
```

### line 89: import

Attributes/classifiers: none

```k
  imports MPY-CONCRETE
```

### line 90: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/assert.k

Records: 6

### line 3: module

Attributes/classifiers: none

```k
module MPY-ASSERT
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 6: operational-rule

Attributes/classifiers: none

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### line 8: operational-rule

Attributes/classifiers: none

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### line 13: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 16: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/bool.k

Records: 17

### line 5: module

Attributes/classifiers: none

```k
module MPY-BOOL
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 8: equational-rule

Attributes/classifiers: none

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### line 10: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### line 11: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### line 16: context

Attributes/classifiers: none

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### line 17: operational-rule

Attributes/classifiers: none

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### line 18: operational-rule

Attributes/classifiers: none

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### line 20: operational-rule

Attributes/classifiers: none

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### line 22: operational-rule

Attributes/classifiers: none

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### line 24: operational-rule

Attributes/classifiers: none

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### line 29: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### line 31: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### line 35: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### line 39: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### line 43: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### line 47: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/builtins.k

Records: 184

### line 3: module

Attributes/classifiers: none

```k
module MPY-BUILTINS
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 5: import

Attributes/classifiers: none

```k
  imports MPY-STR
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-SET
```

### line 7: import

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### line 8: import

Attributes/classifiers: none

```k
  imports MPY-RANGE
```

### line 9: import

Attributes/classifiers: none

```k
  imports MPY-INT
```

### line 10: import

Attributes/classifiers: none

```k
  imports MPY-METHODS

  // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup

  // Call routing + argument evaluation live in call.k, which also routes the fold
  // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to
  // applyBuiltin. This module owns applyBuiltin + the fold implementations.
```

### line 17: syntax

Attributes/classifiers: function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### line 20: syntax

Attributes/classifiers: function

```k
  syntax Int ::= seqLen(Val) [function]
```

### line 21: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### line 22: equational-rule

Attributes/classifiers: none

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### line 23: equational-rule

Attributes/classifiers: none

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### line 24: equational-rule

Attributes/classifiers: none

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### line 25: equational-rule

Attributes/classifiers: none

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### line 26: equational-rule

Attributes/classifiers: none

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### line 32: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### line 33: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### line 34: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### line 35: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### line 36: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### line 37: equational-rule

Attributes/classifiers: none

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### line 38: equational-rule

Attributes/classifiers: none

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### line 41: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### line 44: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### line 47: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### line 48: operational-rule

Attributes/classifiers: none

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### line 49: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### line 50: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### line 54: syntax

Attributes/classifiers: function

```k
  syntax Int ::= intOf(Val) [function]
```

### line 55: equational-rule

Attributes/classifiers: none

```k
  rule intOf(I:Int)  => I
```

### line 56: equational-rule

Attributes/classifiers: none

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### line 59: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### line 60: operational-rule

Attributes/classifiers: none

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### line 61: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### line 62: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### line 64: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### line 67: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### line 68: operational-rule

Attributes/classifiers: none

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### line 69: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### line 70: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### line 72: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### line 76: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### line 77: operational-rule

Attributes/classifiers: none

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### line 78: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### line 80: operational-rule

Attributes/classifiers: none

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### line 81: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### line 82: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### line 86: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### line 87: operational-rule

Attributes/classifiers: none

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### line 88: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### line 90: operational-rule

Attributes/classifiers: none

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### line 91: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### line 92: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### line 97: syntax

Attributes/classifiers: function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### line 98: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### line 99: equational-rule

Attributes/classifiers: none

```k
  rule maxVals(M:Int, .Vals)           => M
```

### line 100: equational-rule

Attributes/classifiers: none

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### line 102: syntax

Attributes/classifiers: function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### line 103: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### line 104: equational-rule

Attributes/classifiers: none

```k
  rule minVals(M:Int, .Vals)           => M
```

### line 105: equational-rule

Attributes/classifiers: none

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### line 108: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### line 111: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### line 114: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### line 115: equational-rule

Attributes/classifiers: none

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### line 116: equational-rule

Attributes/classifiers: none

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### line 117: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### line 118: equational-rule

Attributes/classifiers: none

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### line 119: equational-rule

Attributes/classifiers: none

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### line 124: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### line 126: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### line 127: equational-rule

Attributes/classifiers: none

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### line 128: equational-rule

Attributes/classifiers: none

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### line 132: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### line 134: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### line 135: equational-rule

Attributes/classifiers: none

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### line 136: equational-rule

Attributes/classifiers: none

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### line 137: equational-rule

Attributes/classifiers: none

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### line 140: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### line 143: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### line 144: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### line 148: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### line 149: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### line 152: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### line 156: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### line 158: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### line 159: equational-rule

Attributes/classifiers: none

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### line 160: equational-rule

Attributes/classifiers: none

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### line 163: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### line 164: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### line 167: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### line 169: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### line 170: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### line 171: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### line 173: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### line 174: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### line 177: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### line 178: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### line 179: equational-rule

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

### line 187: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### line 188: syntax

Attributes/classifiers: function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### line 189: equational-rule

Attributes/classifiers: none

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### line 192: syntax

Attributes/classifiers: none

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### line 194: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### line 195: equational-rule

Attributes/classifiers: none

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### line 196: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### line 197: equational-rule

Attributes/classifiers: none

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### line 198: equational-rule

Attributes/classifiers: owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### line 199: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### line 200: equational-rule

Attributes/classifiers: none

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### line 201: equational-rule

Attributes/classifiers: owise

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### line 203: syntax

Attributes/classifiers: function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### line 204: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### line 205: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### line 206: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### line 207: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### line 208: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### line 209: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### line 210: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### line 211: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### line 212: equational-rule

Attributes/classifiers: none

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### line 214: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### line 216: equational-rule

Attributes/classifiers: none

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### line 217: equational-rule

Attributes/classifiers: none

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### line 218: equational-rule

Attributes/classifiers: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### line 219: equational-rule

Attributes/classifiers: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### line 221: equational-rule

Attributes/classifiers: none

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### line 223: equational-rule

Attributes/classifiers: owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### line 225: syntax

Attributes/classifiers: none

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### line 226: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### line 227: equational-rule

Attributes/classifiers: none

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### line 228: equational-rule

Attributes/classifiers: owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### line 230: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### line 231: equational-rule

Attributes/classifiers: none

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### line 232: equational-rule

Attributes/classifiers: none

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### line 233: equational-rule

Attributes/classifiers: none

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### line 234: equational-rule

Attributes/classifiers: none

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### line 235: equational-rule

Attributes/classifiers: none

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### line 236: equational-rule

Attributes/classifiers: owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### line 238: syntax

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### line 239: equational-rule

Attributes/classifiers: none

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### line 240: equational-rule

Attributes/classifiers: none

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### line 241: equational-rule

Attributes/classifiers: none

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### line 243: equational-rule

Attributes/classifiers: owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### line 244: syntax

Attributes/classifiers: function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### line 245: equational-rule

Attributes/classifiers: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### line 246: equational-rule

Attributes/classifiers: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### line 247: syntax

Attributes/classifiers: function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### line 248: equational-rule

Attributes/classifiers: none

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### line 250: syntax

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### line 251: equational-rule

Attributes/classifiers: none

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### line 252: equational-rule

Attributes/classifiers: none

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### line 253: equational-rule

Attributes/classifiers: none

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### line 254: equational-rule

Attributes/classifiers: none

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### line 255: syntax

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### line 256: equational-rule

Attributes/classifiers: none

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### line 257: equational-rule

Attributes/classifiers: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### line 260: equational-rule

Attributes/classifiers: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### line 263: equational-rule

Attributes/classifiers: owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### line 265: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### line 266: equational-rule

Attributes/classifiers: none

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### line 267: equational-rule

Attributes/classifiers: none

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### line 268: equational-rule

Attributes/classifiers: owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### line 269: syntax

Attributes/classifiers: function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### line 270: equational-rule

Attributes/classifiers: none

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### line 271: equational-rule

Attributes/classifiers: none

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### line 272: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### line 273: equational-rule

Attributes/classifiers: none

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### line 274: equational-rule

Attributes/classifiers: concrete

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### line 279: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= "#md5"
```

### line 280: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### line 282: operational-rule

Attributes/classifiers: none

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### line 283: syntax

Attributes/classifiers: none

```k
  syntax Val ::= md5Obj(IntSeq)
```

### line 284: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### line 285: syntax

Attributes/classifiers: function, total, symbol, no-evaluators, owise, concrete

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### line 291: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### line 292: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### line 293: syntax

Attributes/classifiers: function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### line 294: equational-rule

Attributes/classifiers: none

```k
  rule isIntV(_:Int)         => true
```

### line 295: equational-rule

Attributes/classifiers: owise

```k
  rule isIntV(_:Val)         => false [owise]
```

### line 296: equational-rule

Attributes/classifiers: none

```k
  rule isStrV(str(_:IntSeq)) => true
```

### line 297: equational-rule

Attributes/classifiers: owise

```k
  rule isStrV(_:Val)         => false [owise]
```

### line 298: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/call.k

Records: 29

### line 10: module

Attributes/classifiers: none

```k
module MPY-CALL
```

### line 11: import

Attributes/classifiers: none

```k
  imports MPY-METHODS
```

### line 12: import

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### line 13: import

Attributes/classifiers: none

```k
  imports MPY-FUNCTIONS

  // a cooled attribute is a bound method value
```

### line 16: operational-rule

Attributes/classifiers: owise

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### line 19: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #callee(Exprs)
```

### line 20: operational-rule

Attributes/classifiers: owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### line 21: operational-rule

Attributes/classifiers: none

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### line 24: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### line 26: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### line 27: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### line 28: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### line 29: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### line 30: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### line 31: operational-rule

Attributes/classifiers: owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### line 32: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### line 38: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 42: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### line 47: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 52: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### line 53: equational-rule

Attributes/classifiers: none

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### line 56: operational-rule

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

### line 63: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### line 69: operational-rule

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

### line 80: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### line 87: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### line 88: operational-rule

Attributes/classifiers: none

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### line 89: operational-rule

Attributes/classifiers: none

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### line 95: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/comprehension.k

Records: 17

### line 3: module

Attributes/classifiers: none

```k
module MPY-COMPREHENSION
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 5: import

Attributes/classifiers: none

```k
  imports MPY-OPERATORS
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-LIST
```

### line 7: import

Attributes/classifiers: none

```k
  imports MPY-CONTROLS
```

### line 8: import

Attributes/classifiers: none

```k
  imports MPY-FUNCTIONS

  // A comprehension is pure syntactic sugar
```

### line 11: equational-rule

Attributes/classifiers: none

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### line 12: equational-rule

Attributes/classifiers: none

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### line 14: syntax

Attributes/classifiers: macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### line 15: equational-rule

Attributes/classifiers: none

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### line 18: syntax

Attributes/classifiers: macro, macro-rec

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### line 19: equational-rule

Attributes/classifiers: none

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### line 21: equational-rule

Attributes/classifiers: none

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### line 24: syntax

Attributes/classifiers: macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### line 25: equational-rule

Attributes/classifiers: none

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### line 26: equational-rule

Attributes/classifiers: none

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### line 27: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/concrete.k

Records: 24

### line 8: module

Attributes/classifiers: none

```k
module MPY-CONCRETE
```

### line 9: import

Attributes/classifiers: none

```k
  imports MPY

  // deep equality for list compares whose elements are heap objects
  // (list-of-lists): Python == is structural at every depth.
```

### line 13: operational-rule

Attributes/classifiers: none

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### line 16: operational-rule

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

### line 25: syntax

Attributes/classifiers: none

```k
  syntax Val ::= kvP(Val, Val)
```

### line 26: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### line 28: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### line 31: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### line 34: operational-rule

Attributes/classifiers: none

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### line 36: operational-rule

Attributes/classifiers: none

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### line 38: operational-rule

Attributes/classifiers: none

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### line 42: syntax

Attributes/classifiers: function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### line 43: equational-rule

Attributes/classifiers: none

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### line 44: equational-rule

Attributes/classifiers: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### line 47: equational-rule

Attributes/classifiers: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### line 51: syntax

Attributes/classifiers: function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### line 52: equational-rule

Attributes/classifiers: none

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### line 53: equational-rule

Attributes/classifiers: none

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### line 54: equational-rule

Attributes/classifiers: none

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### line 56: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### line 57: equational-rule

Attributes/classifiers: none

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### line 58: equational-rule

Attributes/classifiers: none

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### line 59: equational-rule

Attributes/classifiers: owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### line 60: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/controls.k

Records: 42

### line 3: module

Attributes/classifiers: none

```k
module MPY-CONTROLS
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 5: import

Attributes/classifiers: none

```k
  imports MPY-TUPLE
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-ITER

  // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==
```

### line 9: operational-rule

Attributes/classifiers: none

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### line 12: operational-rule

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

### line 20: operational-rule

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

### line 27: operational-rule

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

### line 35: operational-rule

Attributes/classifiers: none

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### line 36: operational-rule

Attributes/classifiers: owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### line 37: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### line 38: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### line 39: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### line 43: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### line 48: operational-rule

Attributes/classifiers: none

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### line 51: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### line 52: operational-rule

Attributes/classifiers: none

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### line 53: operational-rule

Attributes/classifiers: none

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### line 54: operational-rule

Attributes/classifiers: none

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### line 57: operational-rule

Attributes/classifiers: none

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### line 59: operational-rule

Attributes/classifiers: none

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### line 65: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### line 69: operational-rule

Attributes/classifiers: none

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### line 71: operational-rule

Attributes/classifiers: none

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### line 72: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### line 73: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### line 77: operational-rule

Attributes/classifiers: none

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### line 78: operational-rule

Attributes/classifiers: none

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### line 79: operational-rule

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### line 81: operational-rule

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### line 85: operational-rule

Attributes/classifiers: none

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### line 86: operational-rule

Attributes/classifiers: none

```k
  rule <k> Continue => #cont ... </k>
```

### line 87: operational-rule

Attributes/classifiers: none

```k
  rule <k> Break => #brk ... </k>
```

### line 88: operational-rule

Attributes/classifiers: none

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### line 89: operational-rule

Attributes/classifiers: owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### line 90: operational-rule

Attributes/classifiers: none

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### line 91: operational-rule

Attributes/classifiers: priority, owise

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### line 95: operational-rule

Attributes/classifiers: priority

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 98: operational-rule

Attributes/classifiers: priority

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 101: operational-rule

Attributes/classifiers: priority

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### line 106: operational-rule

Attributes/classifiers: priority

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 109: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/core.k

Records: 93

### line 3: module

Attributes/classifiers: none

```k
module MPY-CORE
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-SYNTAX
```

### line 5: import

Attributes/classifiers: none

```k
  imports INT
```

### line 6: import

Attributes/classifiers: none

```k
  imports BOOL
```

### line 7: import

Attributes/classifiers: none

```k
  imports STRING
```

### line 8: import

Attributes/classifiers: none

```k
  imports MAP
```

### line 9: import

Attributes/classifiers: none

```k
  imports LIST
```

### line 10: import

Attributes/classifiers: none

```k
  imports K-EQUAL

  // ==== values, the algebraic lists, and the scope heap =====================
```

### line 13: syntax

Attributes/classifiers: none

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### line 14: syntax

Attributes/classifiers: none

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### line 15: syntax

Attributes/classifiers: none

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### line 18: syntax

Attributes/classifiers: none

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### line 25: syntax

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

### line 36: syntax

Attributes/classifiers: none

```k
  syntax Parent   ::= "root" | parent(Int)
```

### line 37: syntax

Attributes/classifiers: none

```k
  syntax Scope    ::= scope(Map, Parent)
```

### line 38: syntax

Attributes/classifiers: none

```k
  syntax KResult  ::= Val
```

### line 39: syntax

Attributes/classifiers: none

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### line 40: syntax

Attributes/classifiers: none

```k
  syntax Vals     ::= List{Val, ","}
```

### line 41: syntax

Attributes/classifiers: none

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### line 42: syntax

Attributes/classifiers: none

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### line 49: configuration

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

### line 68: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### line 69: equational-rule

Attributes/classifiers: none

```k
  rule isRefV(ref(_:Int)) => true
```

### line 70: equational-rule

Attributes/classifiers: owise

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### line 75: syntax

Attributes/classifiers: none

```k
  syntax HeapVal ::= cellV(Val)
```

### line 76: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### line 77: equational-rule

Attributes/classifiers: none

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### line 78: equational-rule

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

### line 85: operational-rule

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

### line 95: syntax

Attributes/classifiers: none

```k
  syntax Val ::= kwV(String, Val)
```

### line 96: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #kwTag(String)
```

### line 97: operational-rule

Attributes/classifiers: none

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### line 98: operational-rule

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### line 100: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### line 101: equational-rule

Attributes/classifiers: none

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### line 102: equational-rule

Attributes/classifiers: owise

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### line 106: syntax

Attributes/classifiers: none

```k
  syntax Val ::= cellsMark(ParamNames)
```

### line 107: syntax

Attributes/classifiers: function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### line 108: equational-rule

Attributes/classifiers: none

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### line 109: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### line 110: equational-rule

Attributes/classifiers: none

```k
  rule pnMember(_:String, .ParamNames) => false
```

### line 111: equational-rule

Attributes/classifiers: none

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### line 113: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #cellW(Val, Val)
```

### line 114: operational-rule

Attributes/classifiers: none

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### line 117: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #alloc(Val)
```

### line 118: operational-rule

Attributes/classifiers: none

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### line 124: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #loadAll(Module)
```

### line 125: operational-rule

Attributes/classifiers: none

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### line 126: operational-rule

Attributes/classifiers: none

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### line 127: operational-rule

Attributes/classifiers: none

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### line 130: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #look(String, Int)
```

### line 131: operational-rule

Attributes/classifiers: none

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### line 132: operational-rule

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

### line 145: operational-rule

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

### line 152: operational-rule

Attributes/classifiers: none

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### line 157: syntax

Attributes/classifiers: function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### line 158: equational-rule

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

### line 185: syntax

Attributes/classifiers: none

```k
  syntax ApplyK ::= toCall(Val)
```

### line 186: syntax

Attributes/classifiers: none

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### line 189: operational-rule

Attributes/classifiers: none

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### line 190: operational-rule

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### line 191: operational-rule

Attributes/classifiers: none

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### line 194: operational-rule

Attributes/classifiers: none

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### line 195: operational-rule

Attributes/classifiers: none

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### line 196: operational-rule

Attributes/classifiers: none

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### line 199: syntax

Attributes/classifiers: function

```k
  syntax Bool ::= truthy(Val) [function]
```

### line 200: equational-rule

Attributes/classifiers: none

```k
  rule truthy(B:Bool)          => B
```

### line 201: equational-rule

Attributes/classifiers: none

```k
  rule truthy(noneV)           => false
```

### line 202: equational-rule

Attributes/classifiers: none

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### line 203: equational-rule

Attributes/classifiers: none

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### line 204: equational-rule

Attributes/classifiers: none

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### line 205: equational-rule

Attributes/classifiers: none

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### line 208: syntax

Attributes/classifiers: function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### line 209: syntax

Attributes/classifiers: function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### line 210: syntax

Attributes/classifiers: function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### line 213: syntax

Attributes/classifiers: function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### line 214: equational-rule

Attributes/classifiers: none

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### line 215: equational-rule

Attributes/classifiers: none

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### line 217: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### line 218: equational-rule

Attributes/classifiers: none

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### line 219: equational-rule

Attributes/classifiers: none

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### line 223: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### line 224: equational-rule

Attributes/classifiers: none

```k
  rule vsLen(.ValSeq)                => 0
```

### line 225: equational-rule

Attributes/classifiers: none

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### line 227: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### line 228: equational-rule

Attributes/classifiers: none

```k
  rule isLen(.IntSeq)                => 0
```

### line 229: equational-rule

Attributes/classifiers: total

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### line 233: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### line 234: equational-rule

Attributes/classifiers: none

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### line 235: equational-rule

Attributes/classifiers: none

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### line 236: equational-rule

Attributes/classifiers: none

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### line 238: equational-rule

Attributes/classifiers: none

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### line 240: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/dict.k

Records: 46

### line 13: module

Attributes/classifiers: none

```k
module MPY-DICT
```

### line 14: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 15: import

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### line 16: import

Attributes/classifiers: none

```k
  imports MPY-METHODS
```

### line 17: import

Attributes/classifiers: none

```k
  imports MPY-LIST

  // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).
```

### line 20: syntax

Attributes/classifiers: none

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### line 23: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### line 26: operational-rule

Attributes/classifiers: none

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### line 27: operational-rule

Attributes/classifiers: none

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### line 28: operational-rule

Attributes/classifiers: none

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### line 30: operational-rule

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### line 32: operational-rule

Attributes/classifiers: total, concrete

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### line 37: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### line 38: equational-rule

Attributes/classifiers: none

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### line 39: equational-rule

Attributes/classifiers: none

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### line 40: equational-rule

Attributes/classifiers: none

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### line 43: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### line 44: equational-rule

Attributes/classifiers: none

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### line 45: equational-rule

Attributes/classifiers: owise

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### line 49: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### line 50: equational-rule

Attributes/classifiers: none

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### line 52: equational-rule

Attributes/classifiers: none

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### line 54: equational-rule

Attributes/classifiers: owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### line 58: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### line 63: equational-rule

Attributes/classifiers: none

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### line 64: syntax

Attributes/classifiers: function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### line 65: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### line 70: syntax

Attributes/classifiers: function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### line 71: equational-rule

Attributes/classifiers: none

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### line 76: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #dsetK(String, Val)
```

### line 77: operational-rule

Attributes/classifiers: none

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### line 78: operational-rule

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### line 82: operational-rule

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### line 86: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### line 87: operational-rule

Attributes/classifiers: none

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### line 90: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### line 91: equational-rule

Attributes/classifiers: none

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### line 92: equational-rule

Attributes/classifiers: none

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### line 95: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### line 97: syntax

Attributes/classifiers: function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### line 98: equational-rule

Attributes/classifiers: none

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### line 99: equational-rule

Attributes/classifiers: none

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### line 101: syntax

Attributes/classifiers: function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### line 102: equational-rule

Attributes/classifiers: none

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### line 103: equational-rule

Attributes/classifiers: none

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### line 104: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/float.k

Records: 160

### line 14: module

Attributes/classifiers: none

```k
module MPY-FLOAT
```

### line 15: import

Attributes/classifiers: none

```k
  imports MPY-OPERATORS
```

### line 16: import

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### line 17: import

Attributes/classifiers: none

```k
  imports FLOAT

  // Float is a value; the float literal evaluates to the K Float.
```

### line 20: syntax

Attributes/classifiers: none

```k
  syntax Val ::= Float
```

### line 21: operational-rule

Attributes/classifiers: no-evaluators, concrete

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### line 24: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### line 25: equational-rule

Attributes/classifiers: concrete

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### line 27: equational-rule

Attributes/classifiers: concrete

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### line 30: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### line 31: equational-rule

Attributes/classifiers: concrete

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### line 32: equational-rule

Attributes/classifiers: concrete

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### line 37: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### line 38: equational-rule

Attributes/classifiers: concrete

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### line 39: equational-rule

Attributes/classifiers: concrete

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### line 43: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### line 44: equational-rule

Attributes/classifiers: no-evaluators, concrete

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### line 50: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### line 51: equational-rule

Attributes/classifiers: concrete

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### line 52: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### line 54: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### line 55: equational-rule

Attributes/classifiers: concrete

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### line 56: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### line 61: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### line 65: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathCeil"
```

### line 66: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### line 67: operational-rule

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### line 70: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathFloor"
```

### line 71: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### line 72: operational-rule

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### line 73: syntax

Attributes/classifiers: function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### line 74: equational-rule

Attributes/classifiers: concrete

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### line 75: equational-rule

Attributes/classifiers: concrete

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### line 78: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### line 79: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### line 82: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### line 83: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### line 84: operational-rule

Attributes/classifiers: none

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### line 85: operational-rule

Attributes/classifiers: none

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### line 86: syntax

Attributes/classifiers: function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### line 87: equational-rule

Attributes/classifiers: concrete

```k
  rule toF(F:Float) => F        [concrete]
```

### line 88: equational-rule

Attributes/classifiers: concrete

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### line 93: syntax

Attributes/classifiers: function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### line 94: equational-rule

Attributes/classifiers: concrete

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### line 95: equational-rule

Attributes/classifiers: concrete

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### line 99: equational-rule

Attributes/classifiers: no-evaluators, concrete

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### line 103: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### line 104: equational-rule

Attributes/classifiers: concrete

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### line 105: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### line 107: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### line 108: equational-rule

Attributes/classifiers: concrete

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### line 109: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### line 111: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### line 112: equational-rule

Attributes/classifiers: concrete

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### line 113: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### line 115: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### line 116: equational-rule

Attributes/classifiers: concrete

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### line 117: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### line 119: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### line 120: equational-rule

Attributes/classifiers: concrete

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### line 121: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### line 125: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### line 126: equational-rule

Attributes/classifiers: concrete

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### line 127: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### line 128: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### line 129: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### line 132: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### line 133: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### line 134: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### line 135: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### line 136: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### line 137: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### line 138: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### line 139: equational-rule

Attributes/classifiers: concrete

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### line 142: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### line 143: equational-rule

Attributes/classifiers: concrete

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### line 144: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### line 145: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### line 146: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### line 147: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### line 148: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### line 149: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### line 150: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### line 151: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### line 154: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### line 155: equational-rule

Attributes/classifiers: concrete

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### line 160: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### line 161: equational-rule

Attributes/classifiers: concrete

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### line 162: equational-rule

Attributes/classifiers: concrete

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### line 165: syntax

Attributes/classifiers: function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### line 166: equational-rule

Attributes/classifiers: none

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### line 167: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### line 168: equational-rule

Attributes/classifiers: none

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### line 169: equational-rule

Attributes/classifiers: none

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### line 170: equational-rule

Attributes/classifiers: none

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### line 171: equational-rule

Attributes/classifiers: none

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### line 173: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### line 174: equational-rule

Attributes/classifiers: none

```k
  rule fracPart(.IntSeq) => 0
```

### line 175: equational-rule

Attributes/classifiers: none

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### line 176: equational-rule

Attributes/classifiers: none

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### line 177: equational-rule

Attributes/classifiers: none

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### line 178: equational-rule

Attributes/classifiers: none

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### line 179: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### line 180: equational-rule

Attributes/classifiers: none

```k
  rule fracScale(.IntSeq) => 1
```

### line 181: equational-rule

Attributes/classifiers: none

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### line 182: equational-rule

Attributes/classifiers: none

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### line 183: equational-rule

Attributes/classifiers: none

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### line 184: equational-rule

Attributes/classifiers: none

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### line 185: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### line 186: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### line 187: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### line 190: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### line 191: equational-rule

Attributes/classifiers: concrete

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### line 192: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### line 195: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### line 196: equational-rule

Attributes/classifiers: concrete

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### line 197: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### line 198: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### line 199: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### line 200: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### line 201: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### line 202: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### line 203: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### line 204: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### line 205: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### line 206: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### line 209: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### line 210: equational-rule

Attributes/classifiers: concrete

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### line 211: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### line 213: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### line 214: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### line 217: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### line 218: equational-rule

Attributes/classifiers: concrete

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### line 223: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### line 224: equational-rule

Attributes/classifiers: concrete

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### line 227: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### line 228: equational-rule

Attributes/classifiers: none

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### line 230: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### line 231: equational-rule

Attributes/classifiers: concrete

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### line 232: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathSqrt"
```

### line 233: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### line 234: operational-rule

Attributes/classifiers: none

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### line 235: operational-rule

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

### line 243: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### line 244: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### line 245: operational-rule

Attributes/classifiers: none

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### line 246: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### line 247: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### line 250: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### line 251: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### line 252: operational-rule

Attributes/classifiers: none

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### line 253: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### line 254: operational-rule

Attributes/classifiers: concrete

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### line 261: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### line 262: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### line 265: operational-rule

Attributes/classifiers: none

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### line 266: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### line 267: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### line 270: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### line 273: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/functions.k

Records: 22

### line 3: module

Attributes/classifiers: none

```k
module MPY-FUNCTIONS
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE

  // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k;
  // this module owns the frame lifecycle (bind params, return, pop).
```

### line 8: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### line 14: operational-rule

Attributes/classifiers: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### line 18: syntax

Attributes/classifiers: none

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### line 19: operational-rule

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

### line 27: syntax

Attributes/classifiers: none

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### line 31: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### line 33: operational-rule

Attributes/classifiers: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### line 36: operational-rule

Attributes/classifiers: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### line 42: operational-rule

Attributes/classifiers: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### line 47: operational-rule

Attributes/classifiers: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### line 50: operational-rule

Attributes/classifiers: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### line 53: operational-rule

Attributes/classifiers: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### line 59: operational-rule

Attributes/classifiers: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### line 63: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### line 64: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### line 68: operational-rule

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

### line 78: operational-rule

Attributes/classifiers: none

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### line 80: operational-rule

Attributes/classifiers: none

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### line 85: operational-rule

Attributes/classifiers: none

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### line 91: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/int.k

Records: 20

### line 4: module

Attributes/classifiers: none

```k
module MPY-INT
```

### line 5: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 7: equational-rule

Attributes/classifiers: none

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### line 9: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### line 11: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### line 12: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### line 13: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### line 14: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### line 15: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### line 16: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### line 17: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### line 19: syntax

Attributes/classifiers: function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### line 20: equational-rule

Attributes/classifiers: none

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### line 22: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### line 23: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### line 24: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### line 25: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### line 26: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### line 27: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### line 28: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/iter.k

Records: 4

### line 6: module

Attributes/classifiers: none

```k
module MPY-ITER
```

### line 7: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 8: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### line 9: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/list.k

Records: 37

### line 3: module

Attributes/classifiers: none

```k
module MPY-LIST
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 5: import

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-OPERATORS

  // ==== iteration (the iterator protocol's list case) =======================
```

### line 9: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### line 10: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### line 13: syntax

Attributes/classifiers: none

```k
  syntax ApplyK ::= "toList"
```

### line 14: operational-rule

Attributes/classifiers: none

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### line 15: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### line 18: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### line 19: equational-rule

Attributes/classifiers: none

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### line 20: equational-rule

Attributes/classifiers: priority

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### line 24: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### line 27: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### line 28: equational-rule

Attributes/classifiers: concrete

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### line 33: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### line 34: equational-rule

Attributes/classifiers: none

```k
  rule hasRefVS(.ValSeq)                => false
```

### line 35: equational-rule

Attributes/classifiers: none

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### line 37: syntax

Attributes/classifiers: function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### line 39: equational-rule

Attributes/classifiers: none

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### line 40: equational-rule

Attributes/classifiers: none

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### line 41: equational-rule

Attributes/classifiers: none

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### line 42: equational-rule

Attributes/classifiers: none

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### line 45: equational-rule

Attributes/classifiers: none

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### line 47: equational-rule

Attributes/classifiers: none

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### line 49: equational-rule

Attributes/classifiers: none

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### line 50: equational-rule

Attributes/classifiers: owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### line 53: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### line 58: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### line 59: operational-rule

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### line 60: operational-rule

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### line 61: operational-rule

Attributes/classifiers: none

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### line 62: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### line 63: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### line 65: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### line 67: operational-rule

Attributes/classifiers: none

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### line 68: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/methods.k

Records: 108

### line 3: module

Attributes/classifiers: none

```k
module MPY-METHODS
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 5: import

Attributes/classifiers: none

```k
  imports K-EQUAL
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-STR
```

### line 7: import

Attributes/classifiers: none

```k
  imports MPY-LIST

  // method-call routing + arg-eval live in call.k; this module owns applyMethod.
```

### line 10: syntax

Attributes/classifiers: function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### line 13: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### line 14: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### line 15: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### line 16: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### line 19: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### line 20: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### line 21: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### line 26: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### line 27: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### line 28: equational-rule

Attributes/classifiers: none

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### line 29: equational-rule

Attributes/classifiers: none

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### line 30: equational-rule

Attributes/classifiers: none

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### line 34: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### line 35: syntax

Attributes/classifiers: function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### line 36: equational-rule

Attributes/classifiers: none

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### line 37: equational-rule

Attributes/classifiers: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### line 39: equational-rule

Attributes/classifiers: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### line 41: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### line 42: equational-rule

Attributes/classifiers: none

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### line 43: equational-rule

Attributes/classifiers: owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### line 44: equational-rule

Attributes/classifiers: none

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### line 47: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### line 48: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### line 49: equational-rule

Attributes/classifiers: none

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### line 50: equational-rule

Attributes/classifiers: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### line 51: equational-rule

Attributes/classifiers: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### line 52: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### line 53: equational-rule

Attributes/classifiers: none

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### line 54: equational-rule

Attributes/classifiers: none

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### line 55: equational-rule

Attributes/classifiers: none

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### line 58: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### line 61: equational-rule

Attributes/classifiers: concrete

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### line 64: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### line 65: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### line 66: equational-rule

Attributes/classifiers: none

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### line 67: equational-rule

Attributes/classifiers: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### line 68: equational-rule

Attributes/classifiers: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### line 72: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### line 75: syntax

Attributes/classifiers: function

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### line 76: equational-rule

Attributes/classifiers: none

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### line 77: equational-rule

Attributes/classifiers: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### line 79: equational-rule

Attributes/classifiers: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### line 82: syntax

Attributes/classifiers: function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### line 83: equational-rule

Attributes/classifiers: none

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### line 84: equational-rule

Attributes/classifiers: none

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### line 85: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### line 86: equational-rule

Attributes/classifiers: none

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### line 89: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### line 94: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### line 97: syntax

Attributes/classifiers: function

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### line 98: equational-rule

Attributes/classifiers: none

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### line 99: equational-rule

Attributes/classifiers: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### line 101: equational-rule

Attributes/classifiers: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### line 104: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### line 106: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### line 107: equational-rule

Attributes/classifiers: none

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### line 108: equational-rule

Attributes/classifiers: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### line 109: equational-rule

Attributes/classifiers: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### line 112: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### line 113: equational-rule

Attributes/classifiers: none

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### line 115: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### line 116: equational-rule

Attributes/classifiers: none

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### line 118: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### line 119: equational-rule

Attributes/classifiers: none

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### line 121: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### line 122: equational-rule

Attributes/classifiers: none

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### line 124: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### line 125: equational-rule

Attributes/classifiers: none

```k
  rule hasUpper(.IntSeq) => false
```

### line 126: equational-rule

Attributes/classifiers: none

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### line 128: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### line 129: equational-rule

Attributes/classifiers: none

```k
  rule hasLower(.IntSeq) => false
```

### line 130: equational-rule

Attributes/classifiers: none

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### line 132: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### line 133: equational-rule

Attributes/classifiers: none

```k
  rule allAlpha(.IntSeq) => true
```

### line 134: equational-rule

Attributes/classifiers: none

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### line 136: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### line 137: equational-rule

Attributes/classifiers: none

```k
  rule allDigit(.IntSeq) => true
```

### line 138: equational-rule

Attributes/classifiers: none

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### line 140: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### line 142: equational-rule

Attributes/classifiers: none

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### line 143: equational-rule

Attributes/classifiers: owise

```k
  rule lowerC(C:Int) => C         [owise]
```

### line 145: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

### line 146: equational-rule

Attributes/classifiers: none

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### line 147: equational-rule

Attributes/classifiers: owise

```k
  rule upperC(C:Int) => C         [owise]
```

### line 149: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

### line 150: equational-rule

Attributes/classifiers: none

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### line 151: equational-rule

Attributes/classifiers: none

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### line 152: equational-rule

Attributes/classifiers: owise

```k
  rule swapC(C:Int) => C         [owise]
```

### line 154: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### line 155: equational-rule

Attributes/classifiers: none

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### line 156: equational-rule

Attributes/classifiers: none

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### line 158: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### line 159: equational-rule

Attributes/classifiers: none

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### line 160: equational-rule

Attributes/classifiers: none

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### line 162: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### line 163: equational-rule

Attributes/classifiers: none

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### line 164: equational-rule

Attributes/classifiers: none

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### line 166: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### line 167: equational-rule

Attributes/classifiers: none

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### line 168: equational-rule

Attributes/classifiers: none

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### line 169: equational-rule

Attributes/classifiers: none

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### line 170: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/operators.k

Records: 16

### line 6: module

Attributes/classifiers: none

```k
module MPY-OPERATORS
```

### line 7: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 8: import

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### line 10: operational-rule

Attributes/classifiers: none

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### line 12: operational-rule

Attributes/classifiers: none

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### line 15: context

Attributes/classifiers: none

```k
  context Compare(HOLE, _)
```

### line 16: context

Attributes/classifiers: none

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### line 17: operational-rule

Attributes/classifiers: owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### line 19: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### line 20: equational-rule

Attributes/classifiers: priority

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### line 25: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 28: operational-rule

Attributes/classifiers: priority

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### line 34: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### line 38: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### line 44: operational-rule

Attributes/classifiers: priority

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 47: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/range.k

Records: 12

### line 5: module

Attributes/classifiers: none

```k
module MPY-RANGE
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 7: import

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### line 9: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### line 10: equational-rule

Attributes/classifiers: none

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### line 12: syntax

Attributes/classifiers: function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### line 13: equational-rule

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### line 15: equational-rule

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### line 17: equational-rule

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### line 20: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### line 23: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### line 25: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/set.k

Records: 21

### line 3: module

Attributes/classifiers: none

```k
module MPY-SET
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE

  // a set value, carried as its distinct codes in first-seen order (order is irrelevant
  // to membership/cardinality — the two observations sets support here).
```

### line 8: syntax

Attributes/classifiers: none

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### line 11: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### line 12: equational-rule

Attributes/classifiers: none

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### line 13: equational-rule

Attributes/classifiers: none

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### line 16: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### line 18: equational-rule

Attributes/classifiers: none

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### line 19: equational-rule

Attributes/classifiers: none

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### line 20: equational-rule

Attributes/classifiers: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### line 22: equational-rule

Attributes/classifiers: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### line 25: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### line 26: equational-rule

Attributes/classifiers: none

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### line 27: equational-rule

Attributes/classifiers: none

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### line 31: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### line 32: equational-rule

Attributes/classifiers: none

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### line 33: equational-rule

Attributes/classifiers: none

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### line 35: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### line 36: equational-rule

Attributes/classifiers: none

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### line 39: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### line 40: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/sort.k

Records: 29

### line 10: module

Attributes/classifiers: none

```k
module MPY-SORT
```

### line 11: import

Attributes/classifiers: none

```k
  imports MPY-BUILTINS
```

### line 12: import

Attributes/classifiers: no-evaluators, concrete

```k
  imports MPY-SUBSCRIPT

  // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators);
  // concrete insertion sort for krun.
  // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal
  // (lemmas-only) is not available in the semantics. Int and str lists.
```

### line 18: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### line 19: syntax

Attributes/classifiers: function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### line 20: equational-rule

Attributes/classifiers: concrete

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### line 21: equational-rule

Attributes/classifiers: concrete

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### line 22: equational-rule

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### line 23: equational-rule

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### line 24: equational-rule

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### line 26: syntax

Attributes/classifiers: function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### line 27: equational-rule

Attributes/classifiers: concrete

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### line 28: equational-rule

Attributes/classifiers: concrete

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### line 29: equational-rule

Attributes/classifiers: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### line 31: equational-rule

Attributes/classifiers: owise, concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### line 36: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### line 40: operational-rule

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

### line 49: syntax

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### line 51: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### line 53: equational-rule

Attributes/classifiers: none

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### line 54: equational-rule

Attributes/classifiers: none

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### line 55: equational-rule

Attributes/classifiers: none

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### line 57: syntax

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### line 58: equational-rule

Attributes/classifiers: none

```k
  rule condRev(S:ValSeq, false) => S
```

### line 59: equational-rule

Attributes/classifiers: none

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### line 61: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### line 63: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### line 65: operational-rule

Attributes/classifiers: total, concrete

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

### line 72: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/str.k

Records: 37

### line 3: module

Attributes/classifiers: none

```k
module MPY-STR
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 5: import

Attributes/classifiers: none

```k
  imports MPY-ITER

  // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==
```

### line 8: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### line 9: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### line 13: syntax

Attributes/classifiers: function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### line 14: operational-rule

Attributes/classifiers: none

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### line 15: equational-rule

Attributes/classifiers: none

```k
  rule strToCodes("") => .IntSeq
```

### line 16: equational-rule

Attributes/classifiers: none

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### line 20: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### line 21: equational-rule

Attributes/classifiers: none

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### line 22: equational-rule

Attributes/classifiers: none

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### line 24: equational-rule

Attributes/classifiers: none

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### line 25: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### line 26: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### line 29: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### line 30: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### line 32: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### line 33: equational-rule

Attributes/classifiers: none

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### line 34: equational-rule

Attributes/classifiers: none

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### line 35: equational-rule

Attributes/classifiers: none

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### line 37: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### line 38: equational-rule

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### line 39: equational-rule

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### line 40: equational-rule

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

### line 48: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### line 49: equational-rule

Attributes/classifiers: none

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### line 50: equational-rule

Attributes/classifiers: none

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### line 51: equational-rule

Attributes/classifiers: none

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### line 52: equational-rule

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### line 53: equational-rule

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### line 54: equational-rule

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### line 56: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### line 57: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### line 58: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### line 59: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### line 60: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/subscript.k

Records: 60

### line 3: module

Attributes/classifiers: none

```k
module MPY-SUBSCRIPT
```

### line 4: import

Attributes/classifiers: total

```k
  imports MPY-CORE

  // ==== positional access + negative-index normalization (used only here) ===
  // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g.
  // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the
  // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total
  // atK. K trusts the [total] annotation; valid programs index in-bounds.
```

### line 11: syntax

Attributes/classifiers: function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### line 12: equational-rule

Attributes/classifiers: none

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### line 13: equational-rule

Attributes/classifiers: none

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### line 16: syntax

Attributes/classifiers: function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### line 17: equational-rule

Attributes/classifiers: none

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### line 18: equational-rule

Attributes/classifiers: none

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### line 21: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### line 22: equational-rule

Attributes/classifiers: none

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### line 23: equational-rule

Attributes/classifiers: strict

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### line 27: context

Attributes/classifiers: none

```k
  context Subscript(HOLE, _)
```

### line 28: context

Attributes/classifiers: none

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### line 31: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 35: operational-rule

Attributes/classifiers: none

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### line 37: syntax

Attributes/classifiers: function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### line 38: equational-rule

Attributes/classifiers: none

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### line 39: equational-rule

Attributes/classifiers: none

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### line 40: equational-rule

Attributes/classifiers: none

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### line 44: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### line 49: syntax

Attributes/classifiers: none

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### line 50: operational-rule

Attributes/classifiers: none

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### line 51: operational-rule

Attributes/classifiers: none

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### line 52: operational-rule

Attributes/classifiers: none

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### line 54: operational-rule

Attributes/classifiers: none

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### line 55: operational-rule

Attributes/classifiers: none

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### line 56: operational-rule

Attributes/classifiers: none

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### line 58: operational-rule

Attributes/classifiers: priority

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### line 61: operational-rule

Attributes/classifiers: none

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### line 63: syntax

Attributes/classifiers: function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### line 64: equational-rule

Attributes/classifiers: none

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### line 66: equational-rule

Attributes/classifiers: none

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### line 68: equational-rule

Attributes/classifiers: none

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### line 72: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### line 73: equational-rule

Attributes/classifiers: none

```k
  rule slStep(noB)          => 1
```

### line 74: equational-rule

Attributes/classifiers: none

```k
  rule slStep(someB(S:Int)) => S
```

### line 76: syntax

Attributes/classifiers: function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### line 77: equational-rule

Attributes/classifiers: none

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### line 79: equational-rule

Attributes/classifiers: none

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### line 81: equational-rule

Attributes/classifiers: none

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### line 83: syntax

Attributes/classifiers: function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### line 84: equational-rule

Attributes/classifiers: none

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### line 86: equational-rule

Attributes/classifiers: none

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### line 88: equational-rule

Attributes/classifiers: none

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### line 90: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### line 91: equational-rule

Attributes/classifiers: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### line 93: equational-rule

Attributes/classifiers: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### line 96: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### line 97: equational-rule

Attributes/classifiers: none

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### line 99: equational-rule

Attributes/classifiers: none

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### line 102: syntax

Attributes/classifiers: function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### line 103: equational-rule

Attributes/classifiers: none

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### line 105: equational-rule

Attributes/classifiers: none

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### line 109: syntax

Attributes/classifiers: function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### line 110: equational-rule

Attributes/classifiers: none

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### line 113: equational-rule

Attributes/classifiers: none

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### line 116: syntax

Attributes/classifiers: function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### line 117: equational-rule

Attributes/classifiers: none

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### line 120: equational-rule

Attributes/classifiers: none

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### line 122: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/syntax.k

Records: 22

### line 3: module

Attributes/classifiers: none

```k
module MPY-SYNTAX
```

### line 4: import

Attributes/classifiers: none

```k
  imports INT-SYNTAX
```

### line 5: import

Attributes/classifiers: none

```k
  imports FLOAT-SYNTAX
```

### line 6: import

Attributes/classifiers: none

```k
  imports BOOL-SYNTAX
```

### line 7: import

Attributes/classifiers: none

```k
  imports STRING-SYNTAX
```

### line 9: syntax

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

### line 32: syntax

Attributes/classifiers: none

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### line 33: syntax

Attributes/classifiers: none

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### line 34: syntax

Attributes/classifiers: none

```k
  syntax Entries  ::= List{Entry, ","}
```

### line 35: syntax

Attributes/classifiers: none

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### line 36: syntax

Attributes/classifiers: none

```k
  syntax CompFors ::= List{CompFor, ""}
```

### line 37: syntax

Attributes/classifiers: none

```k
  syntax Exprs    ::= List{Expr, ","}
```

### line 38: syntax

Attributes/classifiers: none

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### line 39: syntax

Attributes/classifiers: none

```k
  syntax Bound    ::= Expr | "NoBound"
```

### line 41: syntax

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

### line 56: syntax

Attributes/classifiers: none

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### line 57: syntax

Attributes/classifiers: none

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### line 58: syntax

Attributes/classifiers: none

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### line 59: syntax

Attributes/classifiers: none

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### line 60: syntax

Attributes/classifiers: none

```k
  syntax ParamNames ::= List{String, ","}
```

### line 61: syntax

Attributes/classifiers: none

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### line 62: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /reference/reference-semantics/semantics/tuple.k

Records: 31

### line 3: module

Attributes/classifiers: none

```k
module MPY-TUPLE
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY-CORE
```

### line 5: import

Attributes/classifiers: none

```k
  imports MPY-ITER
```

### line 6: import

Attributes/classifiers: none

```k
  imports MPY-LIST
```

### line 7: import

Attributes/classifiers: none

```k
  imports MPY-METHODS

  // ==== iteration (the iterator protocol's tuple case) ======================
```

### line 10: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### line 11: operational-rule

Attributes/classifiers: none

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### line 14: syntax

Attributes/classifiers: none

```k
  syntax ApplyK ::= "toTuple"
```

### line 15: operational-rule

Attributes/classifiers: none

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### line 16: operational-rule

Attributes/classifiers: none

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### line 18: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### line 20: operational-rule

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### line 21: operational-rule

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### line 23: equational-rule

Attributes/classifiers: none

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### line 24: syntax

Attributes/classifiers: function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### line 25: equational-rule

Attributes/classifiers: none

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### line 26: equational-rule

Attributes/classifiers: none

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### line 28: equational-rule

Attributes/classifiers: none

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### line 31: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### line 32: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### line 35: operational-rule

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

### line 42: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### line 43: operational-rule

Attributes/classifiers: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### line 44: operational-rule

Attributes/classifiers: priority

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### line 49: syntax

Attributes/classifiers: none

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### line 50: operational-rule

Attributes/classifiers: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### line 51: operational-rule

Attributes/classifiers: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### line 52: operational-rule

Attributes/classifiers: priority

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### line 55: operational-rule

Attributes/classifiers: none

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### line 57: operational-rule

Attributes/classifiers: none

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### line 58: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /candidate/verification.k

Records: 33

### line 1: require

Attributes/classifiers: none

```k
requires "reference-semantics/semantics.k"
```

### line 3: module

Attributes/classifiers: none

```k
module STRING-XOR-VERIFICATION
```

### line 4: import

Attributes/classifiers: none

```k
  imports MPY

  // The mathematical result, expressed as an accumulator over the two
  // sequences of character codes.  The shorter input determines the length.
```

### line 8: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= binaryCode(Int) [function, total]
```

### line 9: equational-rule

Attributes/classifiers: none

```k
  rule binaryCode(C:Int) => C ==Int 48 orBool C ==Int 49
```

### line 11: syntax

Attributes/classifiers: function

```k
  syntax Int ::= xorCode(Int, Int) [function]
```

### line 12: equational-rule

Attributes/classifiers: none

```k
  rule xorCode(A:Int, B:Int) => 48
    requires binaryCode(A) andBool binaryCode(B) andBool A ==Int B
```

### line 14: equational-rule

Attributes/classifiers: none

```k
  rule xorCode(A:Int, B:Int) => 49
    requires binaryCode(A) andBool binaryCode(B) andBool A =/=Int B
```

### line 17: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= xorAcc(IntSeq, IntSeq, IntSeq) [function, total]
```

### line 18: equational-rule

Attributes/classifiers: none

```k
  rule xorAcc(P:IntSeq, .IntSeq, _:IntSeq) => P
```

### line 19: equational-rule

Attributes/classifiers: none

```k
  rule xorAcc(P:IntSeq, iCons(_:Int, _:IntSeq), .IntSeq) => P
```

### line 20: equational-rule

Attributes/classifiers: none

```k
  rule xorAcc(P:IntSeq, iCons(A:Int, AS:IntSeq), iCons(B:Int, BS:IntSeq))
    => xorAcc(seqConcat(P, iCons(xorCode(A, B), .IntSeq)), AS, BS)

  // The input predicate accepts only ASCII '0'/'1'.
```

### line 24: syntax

Attributes/classifiers: function, total

```k
  syntax Bool ::= binaryCodes(IntSeq) [function, total]
```

### line 25: equational-rule

Attributes/classifiers: none

```k
  rule binaryCodes(.IntSeq) => true
```

### line 26: equational-rule

Attributes/classifiers: total

```k
  rule binaryCodes(iCons(C:Int, REST:IntSeq))
    => binaryCode(C) andBool binaryCodes(REST)

  // Values left in the loop variables after zip terminates.  Initializing
  // x and y in solution.py makes these total even when the loop is empty.
```

### line 31: syntax

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= xorLastX(IntSeq, IntSeq, IntSeq) [function, total]
                  | xorLastY(IntSeq, IntSeq, IntSeq) [function, total]
```

### line 33: equational-rule

Attributes/classifiers: none

```k
  rule xorLastX(.IntSeq, _:IntSeq, X:IntSeq) => X
```

### line 34: equational-rule

Attributes/classifiers: none

```k
  rule xorLastX(iCons(_:Int, _:IntSeq), .IntSeq, X:IntSeq) => X
```

### line 35: equational-rule

Attributes/classifiers: none

```k
  rule xorLastX(iCons(A:Int, AS:IntSeq), iCons(_:Int, BS:IntSeq), _:IntSeq)
    => xorLastX(AS, BS, iCons(A, .IntSeq))
```

### line 37: equational-rule

Attributes/classifiers: none

```k
  rule xorLastY(.IntSeq, _:IntSeq, Y:IntSeq) => Y
```

### line 38: equational-rule

Attributes/classifiers: none

```k
  rule xorLastY(iCons(_:Int, _:IntSeq), .IntSeq, Y:IntSeq) => Y
```

### line 39: equational-rule

Attributes/classifiers: function

```k
  rule xorLastY(iCons(_:Int, AS:IntSeq), iCons(B:Int, BS:IntSeq), _:IntSeq)
    => xorLastY(AS, BS, iCons(B, .IntSeq))

  // Exact constructors emitted by py2mpy.py for the loop and function body.
```

### line 43: syntax

Attributes/classifiers: function

```k
  syntax Expr ::= "stringXorTarget" [function]
```

### line 44: equational-rule

Attributes/classifiers: none

```k
  rule stringXorTarget => TupleExpr(Name("x"), Name("y"))
```

### line 46: syntax

Attributes/classifiers: function

```k
  syntax Stmts ::= "stringXorLoopBody" [function]
```

### line 47: equational-rule

Attributes/classifiers: none

```k
  rule stringXorLoopBody
    => If(Compare(Name("x"), CmpOp("==", Name("y"))),
          Assign(Name("result"), BinOp("+", Name("result"), Str("0"))),
          Assign(Name("result"), BinOp("+", Name("result"), Str("1"))))
```

### line 52: syntax

Attributes/classifiers: function

```k
  syntax Stmts ::= "stringXorBody" [function]
```

### line 53: equational-rule

Attributes/classifiers: none

```k
  rule stringXorBody
    => Expr(Str("Return the bitwise XOR of two binary strings."))
       Assign(Name("result"), Str(""))
       Assign(Name("x"), Str(""))
       Assign(Name("y"), Str(""))
       For(stringXorTarget, Call(Name("zip"), Name("a"), Name("b")),
           stringXorLoopBody)
       Return(Name("result"))
```

### line 62: syntax

Attributes/classifiers: function

```k
  syntax Val ::= "stringXorClosure" [function]
```

### line 63: equational-rule

Attributes/classifiers: none

```k
  rule stringXorClosure
    => closureVal(("a", "b", .ParamNames), stringXorBody, 0)
```

### line 66: syntax

Attributes/classifiers: function

```k
  syntax Module ::= "stringXorModule" [function]
```

### line 67: equational-rule

Attributes/classifiers: none

```k
  rule stringXorModule
    => Module(
         ImportFrom("typing", "List")
         FuncDef("string_xor", Params("a", "b"), stringXorBody))
```

### line 71: endmodule

Attributes/classifiers: none

```k
endmodule
```

## /candidate/spec.k

Records: 6

### line 1: require

Attributes/classifiers: none

```k
requires "verification.k"
```

### line 3: module

Attributes/classifiers: none

```k
module STRING-XOR-SPEC
```

### line 4: import

Attributes/classifiers: none

```k
  imports STRING-XOR-VERIFICATION
```

### line 6: claim

Attributes/classifiers: none

```k
  claim [loop-invariant]:
    <k>
      #loop(zipObjS(A:IntSeq, B:IntSeq), stringXorTarget,
            stringXorLoopBody) ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(("a" |-> str(ORIGA:IntSeq))
                    ("b" |-> str(ORIGB:IntSeq))
                    ("result" |-> str(P:IntSeq))
                    ("x" |-> str(X:IntSeq))
                    ("y" |-> str(Y:IntSeq)),
                    PAR:Parent)) SC:Map
      =>
      (L |-> scope(("a" |-> str(ORIGA))
                    ("b" |-> str(ORIGB))
                    ("result" |-> str(xorAcc(P, A, B)))
                    ("x" |-> str(xorLastX(A, B, X)))
                    ("y" |-> str(xorLastY(A, B, Y))),
                    PAR)) SC
    </scopes>
    requires notBool (L in_keys(SC))
     andBool binaryCodes(A)
     andBool binaryCodes(B)
```

### line 32: claim

Attributes/classifiers: none

```k
  claim [solution-correct]:
    <k>
      #loadAll(stringXorModule)
      ~> Call(Name("string_xor"), str(A:IntSeq), str(B:IntSeq))
      => str(xorAcc(.IntSeq, A, B))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))) (-1 |-> builtinsScope)
      =>
      (0 |-> scope(("string_xor" |-> stringXorClosure), parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires binaryCodes(A) andBool binaryCodes(B)
```

### line 53: endmodule

Attributes/classifiers: none

```k
endmodule
```

# Exhaustive K sentence and rule inventory

Generated directly from the trusted supplied-semantics tree and the candidate proof/spec sources. Each record contains the complete source sentence, so multiline guards, cell footprints, and attributes remain visible.

## `trusted-reference-semantics/semantics.k`

- SHA-256: `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`
- Sentence counts: `{'endmodule': 2, 'imports': 23, 'module': 2, 'requires': 23}`
- Classification counts: `{'endmodule': 2, 'imports': 23, 'module': 2, 'requires': 23}`

### 1. requires (lines 34-34)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/syntax.k"
```

### 2. requires (lines 35-35)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/core.k"
```

### 3. requires (lines 36-36)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/iter.k"
```

### 4. requires (lines 37-37)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/range.k"
```

### 5. requires (lines 38-38)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/operators.k"
```

### 6. requires (lines 39-39)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/int.k"
```

### 7. requires (lines 40-40)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/bool.k"
```

### 8. requires (lines 41-41)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/float.k"
```

### 9. requires (lines 42-42)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/str.k"
```

### 10. requires (lines 43-43)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/set.k"
```

### 11. requires (lines 44-44)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/list.k"
```

### 12. requires (lines 45-45)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/tuple.k"
```

### 13. requires (lines 46-46)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/subscript.k"
```

### 14. requires (lines 47-47)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/comprehension.k"
```

### 15. requires (lines 48-48)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/methods.k"
```

### 16. requires (lines 49-49)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/controls.k"
```

### 17. requires (lines 50-50)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/functions.k"
```

### 18. requires (lines 51-51)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/builtins.k"
```

### 19. requires (lines 52-52)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/call.k"
```

### 20. requires (lines 53-53)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/sort.k"
```

### 21. requires (lines 54-54)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/assert.k"
```

### 22. requires (lines 55-55)

Class: `requires`. Attributes: `none`.

```k
requires "semantics/dict.k"
```

### 23. requires (lines 56-56)

Class: `requires`. Attributes: `concrete`.

```k
requires "semantics/concrete.k"
```

### 24. module (lines 58-58)

Class: `module`. Attributes: `none`.

```k
module MPY
```

### 25. imports (lines 59-59)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 26. imports (lines 60-60)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 27. imports (lines 61-61)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-RANGE
```

### 28. imports (lines 62-62)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-OPERATORS
```

### 29. imports (lines 63-63)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-INT
```

### 30. imports (lines 64-64)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-BOOL
```

### 31. imports (lines 65-65)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-FLOAT
```

### 32. imports (lines 66-66)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-STR
```

### 33. imports (lines 67-67)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-SET
```

### 34. imports (lines 68-68)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-LIST
```

### 35. imports (lines 69-69)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-TUPLE
```

### 36. imports (lines 70-70)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-SUBSCRIPT
```

### 37. imports (lines 71-71)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-COMPREHENSION
```

### 38. imports (lines 72-72)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-METHODS
```

### 39. imports (lines 73-73)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CONTROLS
```

### 40. imports (lines 74-74)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-FUNCTIONS
```

### 41. imports (lines 75-75)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-BUILTINS
```

### 42. imports (lines 76-76)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CALL
```

### 43. imports (lines 77-77)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-SORT
```

### 44. imports (lines 78-78)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ASSERT
```

### 45. imports (lines 79-79)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-DICT
```

### 46. endmodule (lines 80-80)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

### 47. module (lines 87-87)

Class: `module`. Attributes: `none`.

```k
module MPY-KRUN
```

### 48. imports (lines 88-88)

Class: `imports`. Attributes: `none`.

```k
  imports MPY
```

### 49. imports (lines 89-89)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CONCRETE
```

### 50. endmodule (lines 90-90)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/assert.k`

- SHA-256: `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b`
- Sentence counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'rule': 3}`
- Classification counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'ordinary-rule': 3}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-ASSERT
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. rule (lines 6-7)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### 4. rule (lines 8-11)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### 5. rule (lines 13-15)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 6. endmodule (lines 16-16)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/bool.k`

- SHA-256: `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd`
- Sentence counts: `{'context': 1, 'endmodule': 1, 'imports': 1, 'module': 1, 'rule': 13}`
- Classification counts: `{'context': 1, 'endmodule': 1, 'imports': 1, 'module': 1, 'ordinary-rule': 13}`

### 1. module (lines 5-5)

Class: `module`. Attributes: `none`.

```k
module MPY-BOOL
```

### 2. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. rule (lines 8-8)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### 4. rule (lines 10-10)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### 5. rule (lines 11-11)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### 6. context (lines 16-16)

Class: `context`. Attributes: `none`.

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### 7. rule (lines 17-17)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### 8. rule (lines 18-19)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### 9. rule (lines 20-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### 10. rule (lines 22-23)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### 11. rule (lines 24-25)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

### 12. rule (lines 29-30)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### 13. rule (lines 31-34)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### 14. rule (lines 35-38)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### 15. rule (lines 39-42)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### 16. rule (lines 43-46)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### 17. endmodule (lines 47-47)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/builtins.k`

- SHA-256: `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd`
- Sentence counts: `{'endmodule': 1, 'imports': 7, 'module': 1, 'rule': 137, 'syntax': 38}`
- Classification counts: `{'endmodule': 1, 'imports': 7, 'module': 1, 'opaque-symbol-declaration': 1, 'ordinary-rule': 137, 'syntax-declaration': 37}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-BUILTINS
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-STR
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-SET
```

### 5. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 6. imports (lines 8-8)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-RANGE
```

### 7. imports (lines 9-9)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-INT
```

### 8. imports (lines 10-10)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-METHODS
```

### 9. syntax (lines 17-17)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### 10. syntax (lines 20-20)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= seqLen(Val) [function]
```

### 11. rule (lines 21-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### 12. rule (lines 22-22)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### 13. rule (lines 23-23)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### 14. rule (lines 24-24)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### 15. rule (lines 25-25)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### 16. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### 17. rule (lines 32-32)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### 18. rule (lines 33-33)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### 19. rule (lines 34-34)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### 20. rule (lines 35-35)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### 21. syntax (lines 36-36)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### 22. rule (lines 37-37)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### 23. rule (lines 38-38)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### 24. rule (lines 41-41)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### 25. rule (lines 44-44)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### 26. syntax (lines 47-47)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### 27. rule (lines 48-48)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### 28. rule (lines 49-49)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### 29. rule (lines 50-52)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### 30. syntax (lines 54-54)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= intOf(Val) [function]
```

### 31. rule (lines 55-55)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intOf(I:Int)  => I
```

### 32. rule (lines 56-56)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### 33. syntax (lines 59-59)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### 34. rule (lines 60-60)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### 35. rule (lines 61-61)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### 36. rule (lines 62-63)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### 37. rule (lines 64-65)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### 38. syntax (lines 67-67)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### 39. rule (lines 68-68)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### 40. rule (lines 69-69)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### 41. rule (lines 70-71)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### 42. rule (lines 72-73)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

### 43. syntax (lines 76-76)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### 44. rule (lines 77-77)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### 45. rule (lines 78-79)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### 46. rule (lines 80-80)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### 47. rule (lines 81-81)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### 48. rule (lines 82-84)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### 49. syntax (lines 86-86)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### 50. rule (lines 87-87)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### 51. rule (lines 88-89)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### 52. rule (lines 90-90)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### 53. rule (lines 91-91)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### 54. rule (lines 92-94)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### 55. syntax (lines 97-97)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### 56. rule (lines 98-98)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### 57. rule (lines 99-99)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule maxVals(M:Int, .Vals)           => M
```

### 58. rule (lines 100-100)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### 59. syntax (lines 102-102)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### 60. rule (lines 103-103)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### 61. rule (lines 104-104)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule minVals(M:Int, .Vals)           => M
```

### 62. rule (lines 105-105)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### 63. rule (lines 108-109)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

### 64. rule (lines 111-113)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### 65. syntax (lines 114-114)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### 66. rule (lines 115-115)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### 67. rule (lines 116-116)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### 68. syntax (lines 117-117)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### 69. rule (lines 118-118)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### 70. rule (lines 119-121)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

### 71. rule (lines 124-125)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### 72. syntax (lines 126-126)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### 73. rule (lines 127-127)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### 74. rule (lines 128-129)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### 75. rule (lines 132-133)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### 76. syntax (lines 134-134)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### 77. rule (lines 135-135)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### 78. rule (lines 136-136)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### 79. rule (lines 137-137)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### 80. rule (lines 140-140)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### 81. rule (lines 143-143)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### 82. rule (lines 144-145)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

### 83. rule (lines 148-148)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### 84. rule (lines 149-149)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### 85. rule (lines 152-153)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

### 86. rule (lines 156-157)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### 87. syntax (lines 158-158)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### 88. rule (lines 159-159)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### 89. rule (lines 160-160)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### 90. rule (lines 163-163)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### 91. rule (lines 164-164)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### 92. rule (lines 167-168)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### 93. rule (lines 169-169)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### 94. rule (lines 170-170)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### 95. rule (lines 171-172)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### 96. rule (lines 173-173)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### 97. rule (lines 174-174)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### 98. rule (lines 177-177)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### 99. rule (lines 178-178)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### 100. rule (lines 179-180)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

### 101. rule (lines 187-187)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### 102. syntax (lines 188-188)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### 103. rule (lines 189-190)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### 104. syntax (lines 192-192)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### 105. syntax (lines 194-194)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### 106. rule (lines 195-195)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### 107. syntax (lines 196-196)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### 108. rule (lines 197-197)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### 109. rule (lines 198-198)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### 110. syntax (lines 199-199)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### 111. rule (lines 200-200)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### 112. rule (lines 201-201)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### 113. syntax (lines 203-203)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### 114. rule (lines 204-204)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### 115. rule (lines 205-205)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### 116. rule (lines 206-206)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### 117. rule (lines 207-207)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### 118. rule (lines 208-208)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### 119. rule (lines 209-209)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### 120. rule (lines 210-210)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### 121. rule (lines 211-211)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### 122. rule (lines 212-212)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### 123. syntax (lines 214-215)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### 124. rule (lines 216-216)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### 125. rule (lines 217-217)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### 126. rule (lines 218-218)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### 127. rule (lines 219-220)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### 128. rule (lines 221-222)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### 129. rule (lines 223-223)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### 130. syntax (lines 225-225)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### 131. syntax (lines 226-226)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### 132. rule (lines 227-227)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### 133. rule (lines 228-228)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### 134. syntax (lines 230-230)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### 135. rule (lines 231-231)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### 136. rule (lines 232-232)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### 137. rule (lines 233-233)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### 138. rule (lines 234-234)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### 139. rule (lines 235-235)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### 140. rule (lines 236-236)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### 141. syntax (lines 238-238)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### 142. rule (lines 239-239)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### 143. rule (lines 240-240)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### 144. rule (lines 241-242)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### 145. rule (lines 243-243)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### 146. syntax (lines 244-244)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### 147. rule (lines 245-245)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### 148. rule (lines 246-246)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### 149. syntax (lines 247-247)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### 150. rule (lines 248-248)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### 151. syntax (lines 250-250)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### 152. rule (lines 251-251)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### 153. rule (lines 252-252)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### 154. rule (lines 253-253)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### 155. rule (lines 254-254)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### 156. syntax (lines 255-255)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### 157. rule (lines 256-256)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### 158. rule (lines 257-259)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### 159. rule (lines 260-262)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### 160. rule (lines 263-264)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### 161. syntax (lines 265-265)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### 162. rule (lines 266-266)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### 163. rule (lines 267-267)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### 164. rule (lines 268-268)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### 165. syntax (lines 269-269)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### 166. rule (lines 270-270)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### 167. rule (lines 271-271)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### 168. syntax (lines 272-272)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### 169. rule (lines 273-273)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### 170. rule (lines 274-274)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### 171. syntax (lines 279-279)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= "#md5"
```

### 172. rule (lines 280-281)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### 173. rule (lines 282-282)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### 174. syntax (lines 283-283)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= md5Obj(IntSeq)
```

### 175. rule (lines 284-284)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### 176. syntax (lines 285-285)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### 177. rule (lines 291-291)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### 178. rule (lines 292-292)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### 179. syntax (lines 293-293)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### 180. rule (lines 294-294)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isIntV(_:Int)         => true
```

### 181. rule (lines 295-295)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule isIntV(_:Val)         => false [owise]
```

### 182. rule (lines 296-296)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isStrV(str(_:IntSeq)) => true
```

### 183. rule (lines 297-297)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule isStrV(_:Val)         => false [owise]
```

### 184. endmodule (lines 298-298)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/call.k`

- SHA-256: `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4`
- Sentence counts: `{'endmodule': 1, 'imports': 3, 'module': 1, 'rule': 21, 'syntax': 3}`
- Classification counts: `{'endmodule': 1, 'imports': 3, 'module': 1, 'ordinary-rule': 21, 'syntax-declaration': 3}`

### 1. module (lines 10-10)

Class: `module`. Attributes: `none`.

```k
module MPY-CALL
```

### 2. imports (lines 11-11)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-METHODS
```

### 3. imports (lines 12-12)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-BUILTINS
```

### 4. imports (lines 13-13)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-FUNCTIONS
```

### 5. rule (lines 16-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### 6. syntax (lines 19-19)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #callee(Exprs)
```

### 7. rule (lines 20-20)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### 8. rule (lines 21-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### 9. rule (lines 24-24)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### 10. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### 11. rule (lines 27-27)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### 12. rule (lines 28-28)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### 13. rule (lines 29-29)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### 14. rule (lines 30-30)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### 15. rule (lines 31-31)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### 16. rule (lines 32-32)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### 17. rule (lines 38-41)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 18. rule (lines 42-46)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### 19. rule (lines 47-50)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 20. syntax (lines 52-52)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### 21. rule (lines 53-55)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### 22. rule (lines 56-60)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

### 23. rule (lines 63-67)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### 24. rule (lines 69-74)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### 25. rule (lines 80-85)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### 26. syntax (lines 87-87)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### 27. rule (lines 88-88)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### 28. rule (lines 89-94)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### 29. endmodule (lines 95-95)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/comprehension.k`

- SHA-256: `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7`
- Sentence counts: `{'endmodule': 1, 'imports': 5, 'module': 1, 'rule': 7, 'syntax': 3}`
- Classification counts: `{'endmodule': 1, 'imports': 5, 'module': 1, 'ordinary-rule': 7, 'syntax-declaration': 3}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-COMPREHENSION
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-OPERATORS
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-LIST
```

### 5. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CONTROLS
```

### 6. imports (lines 8-8)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-FUNCTIONS
```

### 7. rule (lines 11-11)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### 8. rule (lines 12-12)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### 9. syntax (lines 14-14)

Class: `syntax-declaration`. Attributes: `macro`.

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### 10. rule (lines 15-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### 11. syntax (lines 18-18)

Class: `syntax-declaration`. Attributes: `macro-rec`.

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### 12. rule (lines 19-20)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### 13. rule (lines 21-22)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### 14. syntax (lines 24-24)

Class: `syntax-declaration`. Attributes: `macro`.

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### 15. rule (lines 25-25)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### 16. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### 17. endmodule (lines 27-27)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/concrete.k`

- SHA-256: `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305`
- Sentence counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'rule': 16, 'syntax': 5}`
- Classification counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'ordinary-rule': 16, 'syntax-declaration': 5}`

### 1. module (lines 8-8)

Class: `module`. Attributes: `none`.

```k
module MPY-CONCRETE
```

### 2. imports (lines 9-9)

Class: `imports`. Attributes: `none`.

```k
  imports MPY
```

### 3. rule (lines 13-15)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### 4. rule (lines 16-18)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### 5. syntax (lines 25-25)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= kvP(Val, Val)
```

### 6. syntax (lines 26-27)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### 7. rule (lines 28-30)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### 8. rule (lines 31-33)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### 9. rule (lines 34-35)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### 10. rule (lines 36-37)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### 11. rule (lines 38-40)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### 12. syntax (lines 42-42)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### 13. rule (lines 43-43)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### 14. rule (lines 44-46)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### 15. rule (lines 47-49)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### 16. syntax (lines 51-51)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### 17. rule (lines 52-52)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### 18. rule (lines 53-53)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### 19. rule (lines 54-54)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### 20. syntax (lines 56-56)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### 21. rule (lines 57-57)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### 22. rule (lines 58-58)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### 23. rule (lines 59-59)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### 24. endmodule (lines 60-60)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/controls.k`

- SHA-256: `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae`
- Sentence counts: `{'endmodule': 1, 'imports': 3, 'module': 1, 'rule': 34, 'syntax': 3}`
- Classification counts: `{'endmodule': 1, 'imports': 3, 'module': 1, 'ordinary-rule': 34, 'syntax-declaration': 3}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-CONTROLS
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-TUPLE
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 5. rule (lines 9-11)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### 6. rule (lines 12-18)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### 7. rule (lines 20-23)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

### 8. rule (lines 27-31)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

### 9. rule (lines 35-35)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### 10. rule (lines 36-36)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### 11. syntax (lines 37-37)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### 12. rule (lines 38-38)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### 13. rule (lines 39-42)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### 14. rule (lines 43-44)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### 15. rule (lines 48-48)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### 16. syntax (lines 51-51)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### 17. rule (lines 52-52)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### 18. rule (lines 53-53)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### 19. rule (lines 54-54)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### 20. rule (lines 57-58)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### 21. rule (lines 59-60)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

### 22. syntax (lines 65-67)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### 23. rule (lines 69-69)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### 24. rule (lines 71-71)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### 25. rule (lines 72-72)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### 26. rule (lines 73-74)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### 27. rule (lines 77-77)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### 28. rule (lines 78-78)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### 29. rule (lines 79-80)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### 30. rule (lines 81-82)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

### 31. rule (lines 85-85)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### 32. rule (lines 86-86)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Continue => #cont ... </k>
```

### 33. rule (lines 87-87)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Break => #brk ... </k>
```

### 34. rule (lines 88-88)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### 35. rule (lines 89-89)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### 36. rule (lines 90-90)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### 37. rule (lines 91-91)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### 38. rule (lines 95-97)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 39. rule (lines 98-100)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 40. rule (lines 101-103)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 41. rule (lines 106-108)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 42. endmodule (lines 109-109)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/core.k`

- SHA-256: `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e`
- Sentence counts: `{'configuration': 1, 'endmodule': 1, 'imports': 7, 'module': 1, 'rule': 46, 'syntax': 37}`
- Classification counts: `{'configuration': 1, 'endmodule': 1, 'imports': 7, 'module': 1, 'ordinary-rule': 46, 'syntax-declaration': 37}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-CORE
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-SYNTAX
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports INT
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports BOOL
```

### 5. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports STRING
```

### 6. imports (lines 8-8)

Class: `imports`. Attributes: `none`.

```k
  imports MAP
```

### 7. imports (lines 9-9)

Class: `imports`. Attributes: `none`.

```k
  imports LIST
```

### 8. imports (lines 10-10)

Class: `imports`. Attributes: `none`.

```k
  imports K-EQUAL
```

### 9. syntax (lines 13-13)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### 10. syntax (lines 14-14)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### 11. syntax (lines 15-15)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Str    ::= str(IntSeq)
```

### 12. syntax (lines 18-23)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### 13. syntax (lines 25-34)

Class: `syntax-declaration`. Attributes: `function`.

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

### 14. syntax (lines 36-36)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Parent   ::= "root" | parent(Int)
```

### 15. syntax (lines 37-37)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Scope    ::= scope(Map, Parent)
```

### 16. syntax (lines 38-38)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KResult  ::= Val
```

### 17. syntax (lines 39-39)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### 18. syntax (lines 40-40)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Vals     ::= List{Val, ","}
```

### 19. syntax (lines 41-41)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### 20. syntax (lines 42-42)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### 21. configuration (lines 49-60)

Class: `configuration`. Attributes: `none`.

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

### 22. syntax (lines 68-68)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### 23. rule (lines 69-69)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isRefV(ref(_:Int)) => true
```

### 24. rule (lines 70-70)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule isRefV(_:Val)      => false [owise]
```

### 25. syntax (lines 75-75)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax HeapVal ::= cellV(Val)
```

### 26. syntax (lines 76-76)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### 27. rule (lines 77-77)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### 28. rule (lines 78-78)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule isCellRef(_:Val)          => false [owise]
```

### 29. rule (lines 85-90)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

### 30. syntax (lines 95-95)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= kwV(String, Val)
```

### 31. syntax (lines 96-96)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #kwTag(String)
```

### 32. rule (lines 97-97)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### 33. rule (lines 98-99)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### 34. syntax (lines 100-100)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### 35. rule (lines 101-101)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### 36. rule (lines 102-102)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule isKwV(_:Val)                => false [owise]
```

### 37. syntax (lines 106-106)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= cellsMark(ParamNames)
```

### 38. syntax (lines 107-107)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### 39. rule (lines 108-108)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### 40. syntax (lines 109-109)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### 41. rule (lines 110-110)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule pnMember(_:String, .ParamNames) => false
```

### 42. rule (lines 111-111)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### 43. syntax (lines 113-113)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #cellW(Val, Val)
```

### 44. rule (lines 114-115)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### 45. syntax (lines 117-117)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #alloc(Val)
```

### 46. rule (lines 118-121)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### 47. syntax (lines 124-124)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #loadAll(Module)
```

### 48. rule (lines 125-125)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### 49. rule (lines 126-126)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### 50. rule (lines 127-127)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> .Stmts => .K ... </k>
```

### 51. syntax (lines 130-130)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #look(String, Int)
```

### 52. rule (lines 131-131)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### 53. rule (lines 132-134)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

### 54. rule (lines 145-151)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### 55. rule (lines 152-154)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

### 56. syntax (lines 157-157)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### 57. rule (lines 158-181)

Class: `ordinary-rule`. Attributes: `none`.

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

### 58. syntax (lines 185-185)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax ApplyK ::= toCall(Val)
```

### 59. syntax (lines 186-188)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### 60. rule (lines 189-189)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### 61. rule (lines 190-190)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### 62. rule (lines 191-191)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### 63. rule (lines 194-194)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### 64. rule (lines 195-195)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### 65. rule (lines 196-196)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> NoneVal      => noneV ... </k>
```

### 66. syntax (lines 199-199)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Bool ::= truthy(Val) [function]
```

### 67. rule (lines 200-200)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule truthy(B:Bool)          => B
```

### 68. rule (lines 201-201)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule truthy(noneV)           => false
```

### 69. rule (lines 202-202)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### 70. rule (lines 203-203)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### 71. rule (lines 204-204)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### 72. rule (lines 205-205)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### 73. syntax (lines 208-208)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### 74. syntax (lines 209-209)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### 75. syntax (lines 210-210)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### 76. syntax (lines 213-213)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### 77. rule (lines 214-214)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### 78. rule (lines 215-215)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### 79. syntax (lines 217-217)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### 80. rule (lines 218-218)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### 81. rule (lines 219-219)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### 82. syntax (lines 223-223)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### 83. rule (lines 224-224)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule vsLen(.ValSeq)                => 0
```

### 84. rule (lines 225-225)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### 85. syntax (lines 227-227)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### 86. rule (lines 228-228)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isLen(.IntSeq)                => 0
```

### 87. rule (lines 229-229)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### 88. syntax (lines 233-233)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### 89. rule (lines 234-234)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### 90. rule (lines 235-235)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### 91. rule (lines 236-237)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### 92. rule (lines 238-239)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### 93. endmodule (lines 240-240)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/dict.k`

- SHA-256: `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580`
- Sentence counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'rule': 28, 'syntax': 12}`
- Classification counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'ordinary-rule': 28, 'syntax-declaration': 12}`

### 1. module (lines 13-13)

Class: `module`. Attributes: `none`.

```k
module MPY-DICT
```

### 2. imports (lines 14-14)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 15-15)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 4. imports (lines 16-16)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-METHODS
```

### 5. imports (lines 17-17)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-LIST
```

### 6. syntax (lines 20-20)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### 7. syntax (lines 23-25)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### 8. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### 9. rule (lines 27-27)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### 10. rule (lines 28-29)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### 11. rule (lines 30-31)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### 12. rule (lines 32-33)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### 13. syntax (lines 37-37)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### 14. rule (lines 38-38)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### 15. rule (lines 39-39)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### 16. rule (lines 40-40)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### 17. syntax (lines 43-43)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### 18. rule (lines 44-44)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### 19. rule (lines 45-45)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### 20. syntax (lines 49-49)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### 21. rule (lines 50-51)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### 22. rule (lines 52-53)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### 23. rule (lines 54-54)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### 24. rule (lines 58-60)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### 25. rule (lines 63-63)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### 26. syntax (lines 64-64)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### 27. rule (lines 65-66)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### 28. syntax (lines 70-70)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### 29. rule (lines 71-71)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### 30. syntax (lines 76-76)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #dsetK(String, Val)
```

### 31. rule (lines 77-77)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### 32. rule (lines 78-81)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### 33. rule (lines 82-85)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### 34. syntax (lines 86-86)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### 35. rule (lines 87-88)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### 36. syntax (lines 90-90)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### 37. rule (lines 91-91)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### 38. rule (lines 92-92)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### 39. rule (lines 95-96)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### 40. syntax (lines 97-97)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### 41. rule (lines 98-98)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### 42. rule (lines 99-100)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### 43. syntax (lines 101-101)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### 44. rule (lines 102-102)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### 45. rule (lines 103-103)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### 46. endmodule (lines 104-104)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/float.k`

- SHA-256: `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f`
- Sentence counts: `{'endmodule': 1, 'imports': 3, 'module': 1, 'rule': 121, 'syntax': 34}`
- Classification counts: `{'concrete-only-rule': 26, 'endmodule': 1, 'imports': 3, 'module': 1, 'opaque-symbol-declaration': 19, 'ordinary-rule': 95, 'syntax-declaration': 15}`

### 1. module (lines 14-14)

Class: `module`. Attributes: `none`.

```k
module MPY-FLOAT
```

### 2. imports (lines 15-15)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-OPERATORS
```

### 3. imports (lines 16-16)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-BUILTINS
```

### 4. imports (lines 17-17)

Class: `imports`. Attributes: `none`.

```k
  imports FLOAT
```

### 5. syntax (lines 20-20)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= Float
```

### 6. rule (lines 21-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Float(F:Float) => F ... </k>
```

### 7. syntax (lines 24-24)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### 8. rule (lines 25-25)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### 9. rule (lines 27-27)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### 10. syntax (lines 30-30)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### 11. rule (lines 31-31)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### 12. rule (lines 32-32)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### 13. syntax (lines 37-37)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### 14. rule (lines 38-38)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### 15. rule (lines 39-39)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### 16. rule (lines 43-43)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### 17. rule (lines 44-44)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### 18. syntax (lines 50-50)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### 19. rule (lines 51-51)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### 20. rule (lines 52-52)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### 21. syntax (lines 54-54)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### 22. rule (lines 55-55)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### 23. rule (lines 56-56)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### 24. rule (lines 61-61)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Import(_:String) => .K ... </k>
```

### 25. syntax (lines 65-65)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= "#mathCeil"
```

### 26. rule (lines 66-66)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### 27. rule (lines 67-67)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### 28. syntax (lines 70-70)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= "#mathFloor"
```

### 29. rule (lines 71-71)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### 30. rule (lines 72-72)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### 31. syntax (lines 73-73)

Class: `syntax-declaration`. Attributes: `function, total, symbol`.

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### 32. rule (lines 74-74)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### 33. rule (lines 75-75)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### 34. rule (lines 78-78)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### 35. rule (lines 79-79)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### 36. syntax (lines 82-82)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### 37. rule (lines 83-83)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### 38. rule (lines 84-84)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### 39. rule (lines 85-85)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### 40. syntax (lines 86-86)

Class: `syntax-declaration`. Attributes: `function, total, symbol`.

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### 41. rule (lines 87-87)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule toF(F:Float) => F        [concrete]
```

### 42. rule (lines 88-88)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### 43. syntax (lines 93-93)

Class: `syntax-declaration`. Attributes: `function, total, symbol`.

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### 44. rule (lines 94-94)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### 45. rule (lines 95-95)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### 46. rule (lines 99-99)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### 47. syntax (lines 103-103)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### 48. rule (lines 104-104)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### 49. rule (lines 105-105)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### 50. syntax (lines 107-107)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### 51. rule (lines 108-108)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### 52. rule (lines 109-109)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### 53. syntax (lines 111-111)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### 54. rule (lines 112-112)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### 55. rule (lines 113-113)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### 56. syntax (lines 115-115)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### 57. rule (lines 116-116)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### 58. rule (lines 117-117)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### 59. syntax (lines 119-119)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### 60. rule (lines 120-120)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### 61. rule (lines 121-121)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### 62. syntax (lines 125-125)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### 63. rule (lines 126-126)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### 64. rule (lines 127-127)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### 65. rule (lines 128-128)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### 66. rule (lines 129-129)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### 67. rule (lines 132-132)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### 68. rule (lines 133-133)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### 69. rule (lines 134-134)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### 70. rule (lines 135-135)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### 71. rule (lines 136-136)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### 72. rule (lines 137-137)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### 73. rule (lines 138-138)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### 74. rule (lines 139-139)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### 75. syntax (lines 142-142)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### 76. rule (lines 143-143)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### 77. rule (lines 144-144)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### 78. rule (lines 145-145)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### 79. rule (lines 146-146)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### 80. rule (lines 147-147)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### 81. rule (lines 148-148)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### 82. rule (lines 149-149)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### 83. rule (lines 150-150)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### 84. rule (lines 151-151)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### 85. rule (lines 154-154)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### 86. rule (lines 155-155)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### 87. syntax (lines 160-160)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### 88. rule (lines 161-161)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### 89. rule (lines 162-164)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### 90. syntax (lines 165-165)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### 91. rule (lines 166-166)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### 92. syntax (lines 167-167)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### 93. rule (lines 168-168)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### 94. rule (lines 169-169)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### 95. rule (lines 170-170)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### 96. rule (lines 171-172)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### 97. syntax (lines 173-173)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### 98. rule (lines 174-174)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracPart(.IntSeq) => 0
```

### 99. rule (lines 175-175)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### 100. rule (lines 176-176)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### 101. rule (lines 177-177)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### 102. rule (lines 178-178)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### 103. syntax (lines 179-179)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### 104. rule (lines 180-180)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracScale(.IntSeq) => 1
```

### 105. rule (lines 181-181)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### 106. rule (lines 182-182)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### 107. rule (lines 183-183)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### 108. rule (lines 184-184)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### 109. rule (lines 185-185)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### 110. rule (lines 186-186)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### 111. rule (lines 187-187)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### 112. syntax (lines 190-190)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### 113. rule (lines 191-191)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### 114. rule (lines 192-192)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### 115. syntax (lines 195-195)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### 116. rule (lines 196-196)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### 117. rule (lines 197-197)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### 118. rule (lines 198-198)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### 119. rule (lines 199-199)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### 120. rule (lines 200-200)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### 121. rule (lines 201-201)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### 122. rule (lines 202-202)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### 123. rule (lines 203-203)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### 124. rule (lines 204-204)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### 125. rule (lines 205-205)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### 126. rule (lines 206-206)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### 127. syntax (lines 209-209)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### 128. rule (lines 210-210)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### 129. rule (lines 211-211)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### 130. rule (lines 213-213)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### 131. rule (lines 214-214)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### 132. syntax (lines 217-217)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### 133. rule (lines 218-222)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### 134. syntax (lines 223-223)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### 135. rule (lines 224-226)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### 136. rule (lines 227-227)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### 137. rule (lines 228-228)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### 138. syntax (lines 230-230)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### 139. rule (lines 231-231)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### 140. syntax (lines 232-232)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= "#mathSqrt"
```

### 141. rule (lines 233-233)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### 142. rule (lines 234-234)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### 143. rule (lines 235-235)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### 144. syntax (lines 243-243)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### 145. rule (lines 244-244)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### 146. rule (lines 245-245)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### 147. rule (lines 246-246)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### 148. rule (lines 247-248)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### 149. syntax (lines 250-250)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### 150. rule (lines 251-251)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### 151. rule (lines 252-252)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### 152. rule (lines 253-253)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### 153. rule (lines 254-255)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### 154. syntax (lines 261-261)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### 155. rule (lines 262-264)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### 156. rule (lines 265-265)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### 157. rule (lines 266-266)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### 158. rule (lines 267-269)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### 159. rule (lines 270-272)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### 160. endmodule (lines 273-273)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/functions.k`

- SHA-256: `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193`
- Sentence counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'rule': 15, 'syntax': 4}`
- Classification counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'ordinary-rule': 15, 'syntax-declaration': 4}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-FUNCTIONS
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. syntax (lines 8-11)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### 4. rule (lines 14-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### 5. syntax (lines 18-18)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### 6. rule (lines 19-20)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### 7. syntax (lines 27-27)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### 8. syntax (lines 31-32)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### 9. rule (lines 33-35)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### 10. rule (lines 36-41)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### 11. rule (lines 42-45)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### 12. rule (lines 47-49)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### 13. rule (lines 50-52)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### 14. rule (lines 53-58)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### 15. rule (lines 59-60)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### 16. rule (lines 63-63)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### 17. rule (lines 64-66)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### 18. rule (lines 68-75)

Class: `ordinary-rule`. Attributes: `priority`.

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

### 19. rule (lines 78-79)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### 20. rule (lines 80-81)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### 21. rule (lines 85-90)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### 22. endmodule (lines 91-91)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/int.k`

- SHA-256: `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5`
- Sentence counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'rule': 16, 'syntax': 1}`
- Classification counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'ordinary-rule': 16, 'syntax-declaration': 1}`

### 1. module (lines 4-4)

Class: `module`. Attributes: `none`.

```k
module MPY-INT
```

### 2. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. rule (lines 7-7)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### 4. rule (lines 9-9)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### 5. rule (lines 11-11)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### 6. rule (lines 12-12)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### 7. rule (lines 13-13)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### 8. rule (lines 14-14)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### 9. rule (lines 15-15)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### 10. rule (lines 16-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### 11. rule (lines 17-17)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### 12. syntax (lines 19-19)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### 13. rule (lines 20-20)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### 14. rule (lines 22-22)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### 15. rule (lines 23-23)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### 16. rule (lines 24-24)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### 17. rule (lines 25-25)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### 18. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### 19. rule (lines 27-27)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### 20. endmodule (lines 28-28)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/iter.k`

- SHA-256: `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f`
- Sentence counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'syntax': 1}`
- Classification counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'syntax-declaration': 1}`

### 1. module (lines 6-6)

Class: `module`. Attributes: `none`.

```k
module MPY-ITER
```

### 2. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. syntax (lines 8-8)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### 4. endmodule (lines 9-9)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/list.k`

- SHA-256: `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa`
- Sentence counts: `{'endmodule': 1, 'imports': 3, 'module': 1, 'rule': 27, 'syntax': 5}`
- Classification counts: `{'endmodule': 1, 'imports': 3, 'module': 1, 'ordinary-rule': 27, 'syntax-declaration': 5}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-LIST
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-OPERATORS
```

### 5. rule (lines 9-9)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### 6. rule (lines 10-10)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### 7. syntax (lines 13-13)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax ApplyK ::= "toList"
```

### 8. rule (lines 14-14)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### 9. rule (lines 15-15)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### 10. syntax (lines 18-18)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### 11. rule (lines 19-19)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### 12. rule (lines 20-20)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### 13. rule (lines 24-25)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### 14. rule (lines 27-27)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### 15. rule (lines 28-28)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### 16. syntax (lines 33-33)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### 17. rule (lines 34-34)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule hasRefVS(.ValSeq)                => false
```

### 18. rule (lines 35-35)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### 19. syntax (lines 37-38)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### 20. rule (lines 39-39)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### 21. rule (lines 40-40)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### 22. rule (lines 41-41)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### 23. rule (lines 42-43)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### 24. rule (lines 45-46)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### 25. rule (lines 47-48)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### 26. rule (lines 49-49)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### 27. rule (lines 50-50)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### 28. rule (lines 53-55)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### 29. syntax (lines 58-58)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### 30. rule (lines 59-59)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### 31. rule (lines 60-60)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### 32. rule (lines 61-61)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### 33. rule (lines 62-62)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### 34. rule (lines 63-64)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### 35. rule (lines 65-66)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### 36. rule (lines 67-67)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### 37. endmodule (lines 68-68)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/methods.k`

- SHA-256: `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743`
- Sentence counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'rule': 75, 'syntax': 27}`
- Classification counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'ordinary-rule': 75, 'syntax-declaration': 27}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-METHODS
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports K-EQUAL
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-STR
```

### 5. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-LIST
```

### 6. syntax (lines 10-10)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### 7. rule (lines 13-13)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### 8. rule (lines 14-14)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### 9. rule (lines 15-15)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### 10. rule (lines 16-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### 11. rule (lines 19-19)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### 12. rule (lines 20-20)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### 13. rule (lines 21-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### 14. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### 15. syntax (lines 27-27)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### 16. rule (lines 28-28)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### 17. rule (lines 29-29)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### 18. rule (lines 30-31)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### 19. rule (lines 34-34)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### 20. syntax (lines 35-35)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### 21. rule (lines 36-36)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### 22. rule (lines 37-38)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### 23. rule (lines 39-40)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### 24. syntax (lines 41-41)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### 25. rule (lines 42-42)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### 26. rule (lines 43-43)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### 27. rule (lines 44-44)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### 28. rule (lines 47-47)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### 29. syntax (lines 48-48)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### 30. rule (lines 49-49)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### 31. rule (lines 50-50)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### 32. rule (lines 51-51)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### 33. syntax (lines 52-52)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### 34. rule (lines 53-53)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### 35. rule (lines 54-54)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### 36. rule (lines 55-55)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### 37. rule (lines 58-58)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### 38. rule (lines 61-61)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### 39. rule (lines 64-64)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### 40. syntax (lines 65-65)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### 41. rule (lines 66-66)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### 42. rule (lines 67-67)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### 43. rule (lines 68-68)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### 44. rule (lines 72-74)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### 45. syntax (lines 75-75)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### 46. rule (lines 76-76)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### 47. rule (lines 77-78)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### 48. rule (lines 79-80)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

### 49. syntax (lines 82-82)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### 50. rule (lines 83-83)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### 51. rule (lines 84-84)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### 52. syntax (lines 85-85)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### 53. rule (lines 86-86)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### 54. rule (lines 89-91)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### 55. rule (lines 94-96)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### 56. syntax (lines 97-97)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### 57. rule (lines 98-98)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### 58. rule (lines 99-100)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### 59. rule (lines 101-102)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### 60. rule (lines 104-105)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### 61. syntax (lines 106-106)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### 62. rule (lines 107-107)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### 63. rule (lines 108-108)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### 64. rule (lines 109-109)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### 65. syntax (lines 112-112)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### 66. rule (lines 113-113)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### 67. syntax (lines 115-115)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### 68. rule (lines 116-116)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### 69. syntax (lines 118-118)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### 70. rule (lines 119-119)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### 71. syntax (lines 121-121)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### 72. rule (lines 122-122)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### 73. syntax (lines 124-124)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### 74. rule (lines 125-125)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule hasUpper(.IntSeq) => false
```

### 75. rule (lines 126-126)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### 76. syntax (lines 128-128)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### 77. rule (lines 129-129)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule hasLower(.IntSeq) => false
```

### 78. rule (lines 130-130)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### 79. syntax (lines 132-132)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### 80. rule (lines 133-133)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule allAlpha(.IntSeq) => true
```

### 81. rule (lines 134-134)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### 82. syntax (lines 136-136)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### 83. rule (lines 137-137)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule allDigit(.IntSeq) => true
```

### 84. rule (lines 138-138)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### 85. syntax (lines 140-140)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### 86. rule (lines 142-142)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### 87. rule (lines 143-143)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule lowerC(C:Int) => C         [owise]
```

### 88. syntax (lines 145-145)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= upperC(Int) [function, total]
```

### 89. rule (lines 146-146)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### 90. rule (lines 147-147)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule upperC(C:Int) => C         [owise]
```

### 91. syntax (lines 149-149)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= swapC(Int) [function, total]
```

### 92. rule (lines 150-150)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### 93. rule (lines 151-151)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### 94. rule (lines 152-152)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule swapC(C:Int) => C         [owise]
```

### 95. syntax (lines 154-154)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### 96. rule (lines 155-155)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### 97. rule (lines 156-156)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### 98. syntax (lines 158-158)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### 99. rule (lines 159-159)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### 100. rule (lines 160-160)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### 101. syntax (lines 162-162)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### 102. rule (lines 163-163)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### 103. rule (lines 164-164)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### 104. syntax (lines 166-166)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### 105. rule (lines 167-167)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### 106. rule (lines 168-168)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 107. rule (lines 169-169)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### 108. endmodule (lines 170-170)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/operators.k`

- SHA-256: `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b`
- Sentence counts: `{'context': 2, 'endmodule': 1, 'imports': 2, 'module': 1, 'rule': 10}`
- Classification counts: `{'context': 2, 'endmodule': 1, 'imports': 2, 'module': 1, 'ordinary-rule': 10}`

### 1. module (lines 6-6)

Class: `module`. Attributes: `none`.

```k
module MPY-OPERATORS
```

### 2. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 8-8)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 4. rule (lines 10-10)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### 5. rule (lines 12-12)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### 6. context (lines 15-15)

Class: `context`. Attributes: `none`.

```k
  context Compare(HOLE, _)
```

### 7. context (lines 16-16)

Class: `context`. Attributes: `none`.

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### 8. rule (lines 17-17)

Class: `ordinary-rule`. Attributes: `owise`.

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### 9. rule (lines 19-19)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### 10. rule (lines 20-20)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### 11. rule (lines 25-27)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 12. rule (lines 28-31)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

### 13. rule (lines 34-37)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### 14. rule (lines 38-42)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### 15. rule (lines 44-46)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 16. endmodule (lines 47-47)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/range.k`

- SHA-256: `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d`
- Sentence counts: `{'endmodule': 1, 'imports': 2, 'module': 1, 'rule': 6, 'syntax': 2}`
- Classification counts: `{'endmodule': 1, 'imports': 2, 'module': 1, 'ordinary-rule': 6, 'syntax-declaration': 2}`

### 1. module (lines 5-5)

Class: `module`. Attributes: `none`.

```k
module MPY-RANGE
```

### 2. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 4. syntax (lines 9-9)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### 5. rule (lines 10-10)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### 6. syntax (lines 12-12)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### 7. rule (lines 13-14)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### 8. rule (lines 15-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### 9. rule (lines 17-18)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### 10. rule (lines 20-22)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### 11. rule (lines 23-24)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### 12. endmodule (lines 25-25)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/set.k`

- SHA-256: `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7`
- Sentence counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'rule': 12, 'syntax': 6}`
- Classification counts: `{'endmodule': 1, 'imports': 1, 'module': 1, 'ordinary-rule': 12, 'syntax-declaration': 6}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-SET
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. syntax (lines 8-8)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Val ::= setV(IntSeq)
```

### 4. syntax (lines 11-11)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### 5. rule (lines 12-12)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### 6. rule (lines 13-13)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### 7. syntax (lines 16-17)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### 8. rule (lines 18-18)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### 9. rule (lines 19-19)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### 10. rule (lines 20-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### 11. rule (lines 22-23)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### 12. syntax (lines 25-25)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### 13. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### 14. rule (lines 27-27)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### 15. syntax (lines 31-31)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### 16. rule (lines 32-32)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### 17. rule (lines 33-33)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### 18. syntax (lines 35-35)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### 19. rule (lines 36-36)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### 20. rule (lines 39-39)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### 21. endmodule (lines 40-40)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/sort.k`

- SHA-256: `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a`
- Sentence counts: `{'endmodule': 1, 'imports': 2, 'module': 1, 'rule': 19, 'syntax': 6}`
- Classification counts: `{'concrete-only-rule': 9, 'endmodule': 1, 'imports': 2, 'module': 1, 'opaque-symbol-declaration': 2, 'ordinary-rule': 10, 'syntax-declaration': 4}`

### 1. module (lines 10-10)

Class: `module`. Attributes: `none`.

```k
module MPY-SORT
```

### 2. imports (lines 11-11)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-BUILTINS
```

### 3. imports (lines 12-12)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-SUBSCRIPT
```

### 4. syntax (lines 18-18)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### 5. syntax (lines 19-19)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### 6. rule (lines 20-20)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### 7. rule (lines 21-21)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### 8. rule (lines 22-22)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### 9. rule (lines 23-23)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### 10. rule (lines 24-24)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### 11. syntax (lines 26-26)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### 12. rule (lines 27-27)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### 13. rule (lines 28-28)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### 14. rule (lines 29-30)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### 15. rule (lines 31-32)

Class: `concrete-only-rule`. Attributes: `concrete`.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### 16. rule (lines 36-37)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### 17. rule (lines 40-42)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### 18. syntax (lines 49-49)

Class: `opaque-symbol-declaration`. Attributes: `function, total, symbol, no-evaluators`.

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### 19. syntax (lines 51-52)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### 20. rule (lines 53-53)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### 21. rule (lines 54-54)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### 22. rule (lines 55-55)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### 23. syntax (lines 57-57)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### 24. rule (lines 58-58)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule condRev(S:ValSeq, false) => S
```

### 25. rule (lines 59-59)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### 26. rule (lines 61-62)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### 27. rule (lines 63-64)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### 28. rule (lines 65-66)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

### 29. endmodule (lines 72-72)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/str.k`

- SHA-256: `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f`
- Sentence counts: `{'endmodule': 1, 'imports': 2, 'module': 1, 'rule': 28, 'syntax': 5}`
- Classification counts: `{'endmodule': 1, 'imports': 2, 'module': 1, 'ordinary-rule': 28, 'syntax-declaration': 5}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-STR
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 4. rule (lines 8-8)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### 5. rule (lines 9-10)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### 6. syntax (lines 13-13)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### 7. rule (lines 14-14)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### 8. rule (lines 15-15)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strToCodes("") => .IntSeq
```

### 9. rule (lines 16-17)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### 10. syntax (lines 20-20)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### 11. rule (lines 21-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### 12. rule (lines 22-22)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### 13. rule (lines 24-24)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### 14. rule (lines 25-25)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### 15. rule (lines 26-26)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### 16. rule (lines 29-29)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### 17. rule (lines 30-30)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### 18. syntax (lines 32-32)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### 19. rule (lines 33-33)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### 20. rule (lines 34-34)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 21. rule (lines 35-35)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### 22. syntax (lines 37-37)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### 23. rule (lines 38-38)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### 24. rule (lines 39-39)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### 25. rule (lines 40-41)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

### 26. syntax (lines 48-48)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### 27. rule (lines 49-49)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### 28. rule (lines 50-50)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### 29. rule (lines 51-51)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 30. rule (lines 52-52)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### 31. rule (lines 53-53)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### 32. rule (lines 54-54)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### 33. rule (lines 56-56)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### 34. rule (lines 57-57)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### 35. rule (lines 58-58)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### 36. rule (lines 59-59)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### 37. endmodule (lines 60-60)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/subscript.k`

- SHA-256: `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7`
- Sentence counts: `{'context': 2, 'endmodule': 1, 'imports': 1, 'module': 1, 'rule': 40, 'syntax': 15}`
- Classification counts: `{'context': 2, 'endmodule': 1, 'imports': 1, 'module': 1, 'ordinary-rule': 40, 'syntax-declaration': 15}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-SUBSCRIPT
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. syntax (lines 11-11)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### 4. rule (lines 12-12)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### 5. rule (lines 13-14)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### 6. syntax (lines 16-16)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### 7. rule (lines 17-17)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### 8. rule (lines 18-19)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### 9. syntax (lines 21-21)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### 10. rule (lines 22-22)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### 11. rule (lines 23-23)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### 12. context (lines 27-27)

Class: `context`. Attributes: `none`.

```k
  context Subscript(HOLE, _)
```

### 13. context (lines 28-28)

Class: `context`. Attributes: `none`.

```k
  context Subscript(_:Val, HOLE:Expr)
```

### 14. rule (lines 31-33)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 15. rule (lines 35-35)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### 16. syntax (lines 37-37)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### 17. rule (lines 38-38)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### 18. rule (lines 39-39)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### 19. rule (lines 40-41)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### 20. syntax (lines 44-47)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### 21. syntax (lines 49-49)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### 22. rule (lines 50-50)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### 23. rule (lines 51-51)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### 24. rule (lines 52-52)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### 25. rule (lines 54-54)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### 26. rule (lines 55-55)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### 27. rule (lines 56-56)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### 28. rule (lines 58-60)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### 29. rule (lines 61-61)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### 30. syntax (lines 63-63)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### 31. rule (lines 64-65)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### 32. rule (lines 66-67)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### 33. rule (lines 68-69)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### 34. syntax (lines 72-72)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### 35. rule (lines 73-73)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStep(noB)          => 1
```

### 36. rule (lines 74-74)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStep(someB(S:Int)) => S
```

### 37. syntax (lines 76-76)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### 38. rule (lines 77-78)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### 39. rule (lines 79-80)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### 40. rule (lines 81-81)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### 41. syntax (lines 83-83)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### 42. rule (lines 84-85)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### 43. rule (lines 86-87)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### 44. rule (lines 88-88)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### 45. syntax (lines 90-90)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### 46. rule (lines 91-92)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### 47. rule (lines 93-94)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### 48. syntax (lines 96-96)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### 49. rule (lines 97-98)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### 50. rule (lines 99-100)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### 51. syntax (lines 102-102)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### 52. rule (lines 103-104)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### 53. rule (lines 105-106)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

### 54. syntax (lines 109-109)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### 55. rule (lines 110-112)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### 56. rule (lines 113-114)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### 57. syntax (lines 116-116)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### 58. rule (lines 117-119)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### 59. rule (lines 120-121)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### 60. endmodule (lines 122-122)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/syntax.k`

- SHA-256: `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6`
- Sentence counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'syntax': 16}`
- Classification counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'syntax-declaration': 16}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-SYNTAX
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports INT-SYNTAX
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports FLOAT-SYNTAX
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports BOOL-SYNTAX
```

### 5. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports STRING-SYNTAX
```

### 6. syntax (lines 9-30)

Class: `syntax-declaration`. Attributes: `macro, strict, seqstrict`.

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

### 7. syntax (lines 32-32)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### 8. syntax (lines 33-33)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### 9. syntax (lines 34-34)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Entries  ::= List{Entry, ","}
```

### 10. syntax (lines 35-35)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### 11. syntax (lines 36-36)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax CompFors ::= List{CompFor, ""}
```

### 12. syntax (lines 37-37)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Exprs    ::= List{Expr, ","}
```

### 13. syntax (lines 38-38)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### 14. syntax (lines 39-39)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Bound    ::= Expr | "NoBound"
```

### 15. syntax (lines 41-54)

Class: `syntax-declaration`. Attributes: `strict`.

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

### 16. syntax (lines 56-56)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### 17. syntax (lines 57-57)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### 18. syntax (lines 58-58)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### 19. syntax (lines 59-59)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### 20. syntax (lines 60-60)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax ParamNames ::= List{String, ","}
```

### 21. syntax (lines 61-61)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### 22. endmodule (lines 62-62)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `trusted-reference-semantics/semantics/tuple.k`

- SHA-256: `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb`
- Sentence counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'rule': 21, 'syntax': 4}`
- Classification counts: `{'endmodule': 1, 'imports': 4, 'module': 1, 'ordinary-rule': 21, 'syntax-declaration': 4}`

### 1. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module MPY-TUPLE
```

### 2. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-CORE
```

### 3. imports (lines 5-5)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-ITER
```

### 4. imports (lines 6-6)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-LIST
```

### 5. imports (lines 7-7)

Class: `imports`. Attributes: `none`.

```k
  imports MPY-METHODS
```

### 6. rule (lines 10-10)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### 7. rule (lines 11-11)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### 8. syntax (lines 14-14)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax ApplyK ::= "toTuple"
```

### 9. rule (lines 15-15)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### 10. rule (lines 16-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### 11. rule (lines 18-18)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### 12. rule (lines 20-20)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### 13. rule (lines 21-21)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### 14. rule (lines 23-23)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### 15. syntax (lines 24-24)

Class: `syntax-declaration`. Attributes: `function`.

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### 16. rule (lines 25-25)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### 17. rule (lines 26-27)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### 18. rule (lines 28-28)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### 19. syntax (lines 31-31)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### 20. rule (lines 32-34)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### 21. rule (lines 35-41)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### 22. rule (lines 42-42)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### 23. rule (lines 43-43)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### 24. rule (lines 44-46)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 25. syntax (lines 49-49)

Class: `syntax-declaration`. Attributes: `none`.

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### 26. rule (lines 50-50)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### 27. rule (lines 51-51)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### 28. rule (lines 52-54)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 29. rule (lines 55-56)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### 30. rule (lines 57-57)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### 31. endmodule (lines 58-58)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `candidate/verification.k`

- SHA-256: `0d3584ed69a1fde72b18d542fc9a53ed206ccee12540192ab0d2ca3e9fdcca12`
- Sentence counts: `{'endmodule': 2, 'imports': 2, 'module': 2, 'requires': 1, 'rule': 9, 'syntax': 2}`
- Classification counts: `{'endmodule': 2, 'imports': 2, 'module': 2, 'ordinary-rule': 6, 'requires': 1, 'simplification-rule': 3, 'syntax-declaration': 2}`

### 1. requires (lines 1-1)

Class: `requires`. Attributes: `none`.

```k
requires "reference-semantics/semantics.k"
```

### 2. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module VERIFICATION-BASE
```

### 3. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports MPY
```

### 4. rule (lines 8-9)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #branch(C:Bool, T:Stmts, _:Stmts) => T ... </k>
       requires C
```

### 5. rule (lines 10-11)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule <k> #branch(C:Bool, _:Stmts, E:Stmts) => E ... </k>
       requires notBool C
```

### 6. syntax (lines 15-15)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax IntSeq ::= dropOne(IntSeq) [function, total]
```

### 7. rule (lines 16-16)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dropOne(.IntSeq)                 => .IntSeq
```

### 8. rule (lines 17-17)

Class: `ordinary-rule`. Attributes: `none`.

```k
  rule dropOne(iCons(_:Int, R:IntSeq)) => R
```

### 9. rule (lines 19-26)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule <k>
    Subscript(
      str(S:IntSeq),
      Slice(Int(1), NoBound, NoBound))
    => str(dropOne(S))
    ...
  </k>
  [priority(30)]
```

### 10. syntax (lines 31-31)

Class: `syntax-declaration`. Attributes: `function, total`.

```k
  syntax Bool ::= rotationsLoop(IntSeq, IntSeq, IntSeq) [function, total]
```

### 11. rule (lines 32-33)

Class: `simplification-rule`. Attributes: `simplification`.

```k
  rule rotationsLoop(_:IntSeq, _:IntSeq, .IntSeq) => false
       [simplification]
```

### 12. rule (lines 34-36)

Class: `simplification-rule`. Attributes: `simplification`.

```k
  rule rotationsLoop(A:IntSeq, P:IntSeq, iCons(_:Int, _:IntSeq)) => true
       requires strContains(P, A)
       [simplification]
```

### 13. rule (lines 37-43)

Class: `simplification-rule`. Attributes: `simplification`.

```k
  rule rotationsLoop(A:IntSeq, P:IntSeq, iCons(C:Int, R:IntSeq))
    => rotationsLoop(
         A,
         seqConcat(dropOne(P), iCons(C, .IntSeq)),
         R)
       requires notBool strContains(P, A)
       [simplification]
```

### 14. endmodule (lines 44-44)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

### 15. module (lines 46-46)

Class: `module`. Attributes: `none`.

```k
module VERIFICATION
```

### 16. imports (lines 47-47)

Class: `imports`. Attributes: `none`.

```k
  imports VERIFICATION-BASE
```

### 17. rule (lines 51-94)

Class: `ordinary-rule`. Attributes: `priority`.

```k
  rule
    <k>
      #loop(
        str(REM),
        Name("char"),
        If(
          Compare(Name("pattern"), CmpOp("in", Name("a"))),
          Return(Bool(true)),
          .Stmts)
        Assign(
          Name("pattern"),
          BinOp(
            "+",
            Subscript(
              Name("pattern"),
              Slice(Int(1), NoBound, NoBound)),
            Name("char")))
        .Stmts)
      ~> (Return(Bool(false)) .Stmts)
      ~> #endcall
    =>
      rotationsLoop(A, P, REM)
      ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
         ("a" |-> str(A))
         ("b" |-> str(B))
         ("char" |-> str(CH))
         ("pattern" |-> str(P)),
         parent(0))
       0 |-> scope(G, parent(-1))
       -1 |-> BS:Scope)
    =>
      (0 |-> scope(G, parent(-1))
       -1 |-> BS)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack>
      (ListItem(frame(CONT:K, 0, 1)) REST:List => REST)
    </stack>
    <ret> noRet </ret>
    [priority(30)]
```

### 18. endmodule (lines 95-95)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## `candidate/spec.k`

- SHA-256: `7810f899658c708d43581aa92626b390b8c197b29bf2055f168840f449f29cfd`
- Sentence counts: `{'claim': 2, 'endmodule': 2, 'imports': 2, 'module': 2, 'requires': 1}`
- Classification counts: `{'claim': 2, 'endmodule': 2, 'imports': 2, 'module': 2, 'requires': 1}`

### 1. requires (lines 1-1)

Class: `requires`. Attributes: `none`.

```k
requires "verification.k"
```

### 2. module (lines 3-3)

Class: `module`. Attributes: `none`.

```k
module SPEC-LEMMA
```

### 3. imports (lines 4-4)

Class: `imports`. Attributes: `none`.

```k
  imports VERIFICATION-BASE
```

### 4. claim (lines 6-48)

Class: `claim`. Attributes: `none`.

```k
  claim [loop-invariant]:
    <k>
      #loop(
        str(REM),
        Name("char"),
        If(
          Compare(Name("pattern"), CmpOp("in", Name("a"))),
          Return(Bool(true)),
          .Stmts)
        Assign(
          Name("pattern"),
          BinOp(
            "+",
            Subscript(
              Name("pattern"),
              Slice(Int(1), NoBound, NoBound)),
            Name("char")))
        .Stmts)
      ~> (Return(Bool(false)) .Stmts)
      ~> #endcall
    =>
      rotationsLoop(A, P, REM)
      ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
         ("a" |-> str(A))
         ("b" |-> str(B))
         ("char" |-> str(CH))
         ("pattern" |-> str(P)),
         parent(0))
       0 |-> scope(G, parent(-1))
       -1 |-> BS:Scope)
    =>
      (0 |-> scope(G, parent(-1))
       -1 |-> BS)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack>
      (ListItem(frame(CONT:K, 0, 1)) REST:List => REST)
    </stack>
    <ret> noRet </ret>
```

### 5. endmodule (lines 49-49)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

### 6. module (lines 51-51)

Class: `module`. Attributes: `none`.

```k
module SPEC
```

### 7. imports (lines 52-52)

Class: `imports`. Attributes: `none`.

```k
  imports VERIFICATION
```

### 8. claim (lines 54-99)

Class: `claim`. Attributes: `none`.

```k
  claim [entry-point]:
    <k>
      Call(
        Name("cycpattern_check"),
        str(A), str(B), .Exprs)
    =>
      rotationsLoop(A, B, B)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "cycpattern_check" |->
          closureVal(
            ("a", "b", .ParamNames),
            Assign(Name("pattern"), Name("b"))
            Assign(Name("char"), Str(""))
            For(
              Name("char"),
              Name("b"),
              If(
                Compare(
                  Name("pattern"),
                  CmpOp("in", Name("a"))),
                Return(Bool(true)),
                .Stmts)
              Assign(
                Name("pattern"),
                BinOp(
                  "+",
                  Subscript(
                    Name("pattern"),
                    Slice(Int(1), NoBound, NoBound)),
                  Name("char")))
              .Stmts)
            Return(Bool(false))
            .Stmts,
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
```

### 9. endmodule (lines 100-100)

Class: `endmodule`. Attributes: `none`.

```k
endmodule
```

## Global counts

- Sentence kinds: `{'claim': 2, 'configuration': 1, 'context': 5, 'endmodule': 29, 'imports': 90, 'module': 29, 'requires': 25, 'rule': 704, 'syntax': 229}`
- Classifications: `{'claim': 2, 'concrete-only-rule': 35, 'configuration': 1, 'context': 5, 'endmodule': 29, 'imports': 90, 'module': 29, 'opaque-symbol-declaration': 22, 'ordinary-rule': 666, 'requires': 25, 'simplification-rule': 3, 'syntax-declaration': 207}`
- Attributes: `{'concrete': 36, 'function': 148, 'macro': 3, 'macro-rec': 1, 'no-evaluators': 22, 'owise': 26, 'priority': 47, 'seqstrict': 1, 'simplification': 3, 'strict': 2, 'symbol': 25, 'total': 109}`

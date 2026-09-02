# Exhaustive K source inventory

Source: clean scratch copy; line numbers are within each named file.

## `semantics.k`

Counts: endmodule=2, imports=23, module=2, requires=23

- lines 34-34; kind `requires`; markers `none`

  ```k
  requires "semantics/syntax.k"
  ```

- lines 35-35; kind `requires`; markers `none`

  ```k
  requires "semantics/core.k"
  ```

- lines 36-36; kind `requires`; markers `none`

  ```k
  requires "semantics/iter.k"
  ```

- lines 37-37; kind `requires`; markers `none`

  ```k
  requires "semantics/range.k"
  ```

- lines 38-38; kind `requires`; markers `none`

  ```k
  requires "semantics/operators.k"
  ```

- lines 39-39; kind `requires`; markers `none`

  ```k
  requires "semantics/int.k"
  ```

- lines 40-40; kind `requires`; markers `none`

  ```k
  requires "semantics/bool.k"
  ```

- lines 41-41; kind `requires`; markers `none`

  ```k
  requires "semantics/float.k"
  ```

- lines 42-42; kind `requires`; markers `none`

  ```k
  requires "semantics/str.k"
  ```

- lines 43-43; kind `requires`; markers `none`

  ```k
  requires "semantics/set.k"
  ```

- lines 44-44; kind `requires`; markers `none`

  ```k
  requires "semantics/list.k"
  ```

- lines 45-45; kind `requires`; markers `none`

  ```k
  requires "semantics/tuple.k"
  ```

- lines 46-46; kind `requires`; markers `none`

  ```k
  requires "semantics/subscript.k"
  ```

- lines 47-47; kind `requires`; markers `none`

  ```k
  requires "semantics/comprehension.k"
  ```

- lines 48-48; kind `requires`; markers `none`

  ```k
  requires "semantics/methods.k"
  ```

- lines 49-49; kind `requires`; markers `none`

  ```k
  requires "semantics/controls.k"
  ```

- lines 50-50; kind `requires`; markers `function`

  ```k
  requires "semantics/functions.k"
  ```

- lines 51-51; kind `requires`; markers `none`

  ```k
  requires "semantics/builtins.k"
  ```

- lines 52-52; kind `requires`; markers `none`

  ```k
  requires "semantics/call.k"
  ```

- lines 53-53; kind `requires`; markers `none`

  ```k
  requires "semantics/sort.k"
  ```

- lines 54-54; kind `requires`; markers `none`

  ```k
  requires "semantics/assert.k"
  ```

- lines 55-55; kind `requires`; markers `none`

  ```k
  requires "semantics/dict.k"
  ```

- lines 56-56; kind `requires`; markers `concrete`

  ```k
  requires "semantics/concrete.k"
  ```

- lines 58-58; kind `module`; markers `none`

  ```k
  module MPY
  ```

- lines 59-59; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 60-60; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 61-61; kind `imports`; markers `none`

  ```k
    imports MPY-RANGE
  ```

- lines 62-62; kind `imports`; markers `none`

  ```k
    imports MPY-OPERATORS
  ```

- lines 63-63; kind `imports`; markers `none`

  ```k
    imports MPY-INT
  ```

- lines 64-64; kind `imports`; markers `none`

  ```k
    imports MPY-BOOL
  ```

- lines 65-65; kind `imports`; markers `none`

  ```k
    imports MPY-FLOAT
  ```

- lines 66-66; kind `imports`; markers `none`

  ```k
    imports MPY-STR
  ```

- lines 67-67; kind `imports`; markers `none`

  ```k
    imports MPY-SET
  ```

- lines 68-68; kind `imports`; markers `none`

  ```k
    imports MPY-LIST
  ```

- lines 69-69; kind `imports`; markers `none`

  ```k
    imports MPY-TUPLE
  ```

- lines 70-70; kind `imports`; markers `none`

  ```k
    imports MPY-SUBSCRIPT
  ```

- lines 71-71; kind `imports`; markers `none`

  ```k
    imports MPY-COMPREHENSION
  ```

- lines 72-72; kind `imports`; markers `none`

  ```k
    imports MPY-METHODS
  ```

- lines 73-73; kind `imports`; markers `none`

  ```k
    imports MPY-CONTROLS
  ```

- lines 74-74; kind `imports`; markers `function`

  ```k
    imports MPY-FUNCTIONS
  ```

- lines 75-75; kind `imports`; markers `none`

  ```k
    imports MPY-BUILTINS
  ```

- lines 76-76; kind `imports`; markers `none`

  ```k
    imports MPY-CALL
  ```

- lines 77-77; kind `imports`; markers `none`

  ```k
    imports MPY-SORT
  ```

- lines 78-78; kind `imports`; markers `none`

  ```k
    imports MPY-ASSERT
  ```

- lines 79-79; kind `imports`; markers `none`

  ```k
    imports MPY-DICT
  ```

- lines 80-80; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

- lines 87-87; kind `module`; markers `none`

  ```k
  module MPY-KRUN
  ```

- lines 88-88; kind `imports`; markers `none`

  ```k
    imports MPY
  ```

- lines 89-89; kind `imports`; markers `concrete`

  ```k
    imports MPY-CONCRETE
  ```

- lines 90-90; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/assert.k`

Counts: endmodule=1, imports=1, module=1, rule=3

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-ASSERT
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 6-7; kind `rule`; markers `none`

  ```k
    rule <k> Assert(V:Val) => .K ... </k>
         requires truthy(V)
  ```

- lines 8-11; kind `rule`; markers `none`

  ```k
    rule <k> Assert(V:Val) ~> _ => .K </k>
         <exc> NoExc => AssertionError </exc>
         <exit-code> _ => 1 </exit-code>
         requires notBool truthy(V)
  ```

- lines 13-15; kind `rule`; markers `priority`

  ```k
    rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 16-16; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/bool.k`

Counts: context=1, endmodule=1, imports=1, module=1, rule=13

- lines 5-5; kind `module`; markers `none`

  ```k
  module MPY-BOOL
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 8-8; kind `rule`; markers `none`

  ```k
    rule applyUn("not", V:Val) => notBool truthy(V)
  ```

- lines 10-10; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
  ```

- lines 11-12; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
  ```

- lines 16-16; kind `context`; markers `none`

  ```k
    context BoolOp(_, (HOLE:Expr, _:Exprs))
  ```

- lines 17-17; kind `rule`; markers `none`

  ```k
    rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
  ```

- lines 18-19; kind `rule`; markers `none`

  ```k
    rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
         requires truthy(V)
  ```

- lines 20-21; kind `rule`; markers `none`

  ```k
    rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
         requires notBool truthy(V)
  ```

- lines 22-23; kind `rule`; markers `none`

  ```k
    rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
         requires truthy(V)
  ```

- lines 24-26; kind `rule`; markers `none`

  ```k
    rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
         requires notBool truthy(V)
  ```

- lines 29-30; kind `rule`; markers `priority`

  ```k
    rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
         [priority(40)]
  ```

- lines 31-34; kind `rule`; markers `priority`

  ```k
    rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires truthy(V)
         [priority(40)]
  ```

- lines 35-38; kind `rule`; markers `priority`

  ```k
    rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool truthy(V)
         [priority(40)]
  ```

- lines 39-42; kind `rule`; markers `priority`

  ```k
    rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires truthy(V)
         [priority(40)]
  ```

- lines 43-46; kind `rule`; markers `priority`

  ```k
    rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool truthy(V)
         [priority(40)]
  ```

- lines 47-47; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/builtins.k`

Counts: endmodule=1, imports=7, module=1, rule=137, syntax=38

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-BUILTINS
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports MPY-STR
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-SET
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 8-8; kind `imports`; markers `none`

  ```k
    imports MPY-RANGE
  ```

- lines 9-9; kind `imports`; markers `none`

  ```k
    imports MPY-INT
  ```

- lines 10-10; kind `imports`; markers `none`

  ```k
    imports MPY-METHODS
  ```

- lines 17-18; kind `syntax:function`; markers `function`

  ```k
    syntax Val ::= applyBuiltin(String, Vals) [function]
  ```

- lines 20-20; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= seqLen(Val) [function]
  ```

- lines 21-21; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
  ```

- lines 22-22; kind `rule`; markers `none`

  ```k
    rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
  ```

- lines 23-23; kind `rule`; markers `none`

  ```k
    rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
  ```

- lines 24-24; kind `rule`; markers `none`

  ```k
    rule seqLen(str(IS:IntSeq))                   => isLen(IS)
  ```

- lines 25-25; kind `rule`; markers `none`

  ```k
    rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
  ```

- lines 26-27; kind `rule`; markers `none`

  ```k
    rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
  ```

- lines 32-32; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
  ```

- lines 33-33; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
  ```

- lines 34-34; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
  ```

- lines 35-35; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
  ```

- lines 36-36; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= charsOf(IntSeq) [function, total]
  ```

- lines 37-37; kind `rule`; markers `none`

  ```k
    rule charsOf(.IntSeq)                => .ValSeq
  ```

- lines 38-39; kind `rule`; markers `none`

  ```k
    rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
  ```

- lines 41-42; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
  ```

- lines 44-45; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
  ```

- lines 47-47; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
  ```

- lines 48-48; kind `rule`; markers `none`

  ```k
    rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
  ```

- lines 49-49; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
  ```

- lines 50-52; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
          => #sumAcc(R, ACC +Int intOf(V)) ... </k>
         requires isInt(V) orBool isBool(V)
  ```

- lines 54-54; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= intOf(Val) [function]
  ```

- lines 55-55; kind `rule`; markers `none`

  ```k
    rule intOf(I:Int)  => I
  ```

- lines 56-57; kind `rule`; markers `none`

  ```k
    rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
  ```

- lines 59-59; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #allAcc(Iterable) | "#allCont"
  ```

- lines 60-60; kind `rule`; markers `none`

  ```k
    rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
  ```

- lines 61-61; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #allCont => true ... </k>
  ```

- lines 62-63; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
         requires truthy(V)
  ```

- lines 64-65; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
         requires notBool truthy(V)
  ```

- lines 67-67; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
  ```

- lines 68-68; kind `rule`; markers `none`

  ```k
    rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
  ```

- lines 69-69; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #anyCont => false ... </k>
  ```

- lines 70-71; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
         requires truthy(V)
  ```

- lines 72-74; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
         requires notBool truthy(V)
  ```

- lines 76-76; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
  ```

- lines 77-77; kind `rule`; markers `none`

  ```k
    rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
  ```

- lines 78-79; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
         requires isInt(V)
  ```

- lines 80-80; kind `rule`; markers `none`

  ```k
    rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
  ```

- lines 81-81; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
  ```

- lines 82-84; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
          => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
         requires isInt(V)
  ```

- lines 86-86; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
  ```

- lines 87-87; kind `rule`; markers `none`

  ```k
    rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
  ```

- lines 88-89; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
         requires isInt(V)
  ```

- lines 90-90; kind `rule`; markers `none`

  ```k
    rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
  ```

- lines 91-91; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
  ```

- lines 92-95; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
          => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
         requires isInt(V)
  ```

- lines 97-97; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= maxVals(Int, Vals) [function]
  ```

- lines 98-98; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
  ```

- lines 99-99; kind `rule`; markers `none`

  ```k
    rule maxVals(M:Int, .Vals)           => M
  ```

- lines 100-100; kind `rule`; markers `none`

  ```k
    rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
  ```

- lines 102-102; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= minVals(Int, Vals) [function]
  ```

- lines 103-103; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
  ```

- lines 104-104; kind `rule`; markers `none`

  ```k
    rule minVals(M:Int, .Vals)           => M
  ```

- lines 105-106; kind `rule`; markers `none`

  ```k
    rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
  ```

- lines 108-109; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
         requires N >=Int 0
  ```

- lines 111-113; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("bin", N:Int, .Vals)
      => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
         requires N <Int 0
  ```

- lines 114-114; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= binCodes(Int) [function, total]
  ```

- lines 115-115; kind `rule`; markers `none`

  ```k
    rule binCodes(0) => iCons(48, .IntSeq)
  ```

- lines 116-116; kind `rule`; markers `none`

  ```k
    rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
  ```

- lines 117-117; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
  ```

- lines 118-118; kind `rule`; markers `none`

  ```k
    rule binAcc(0, ACC:IntSeq) => ACC
  ```

- lines 119-122; kind `rule`; markers `none`

  ```k
    rule binAcc(N:Int, ACC:IntSeq)
      => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
         requires N >Int 0
  ```

- lines 124-125; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
          => #alloc(list(enumVS(VS, 0))) ... </k>
  ```

- lines 126-126; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
  ```

- lines 127-127; kind `rule`; markers `none`

  ```k
    rule enumVS(.ValSeq, _:Int) => .ValSeq
  ```

- lines 128-130; kind `rule`; markers `none`

  ```k
    rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
      => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
  ```

- lines 132-133; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
          => #alloc(list(mapStrVS(VS))) ... </k>
  ```

- lines 134-134; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
  ```

- lines 135-135; kind `rule`; markers `none`

  ```k
    rule mapStrVS(.ValSeq) => .ValSeq
  ```

- lines 136-136; kind `rule`; markers `none`

  ```k
    rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
  ```

- lines 137-138; kind `rule`; markers `none`

  ```k
    rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
  ```

- lines 140-141; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("int", I:Int, .Vals) => I
  ```

- lines 143-143; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
  ```

- lines 144-146; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
         requires 0 <=Int I andBool I <Int 128
  ```

- lines 148-148; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
  ```

- lines 149-150; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
  ```

- lines 152-154; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
         requires 48 <=Int C andBool C <=Int 57
  ```

- lines 156-157; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
         requires isLen(CS) >=Int 2
  ```

- lines 158-158; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
  ```

- lines 159-159; kind `rule`; markers `none`

  ```k
    rule intDigAcc(.IntSeq, ACC:Int)             => ACC
  ```

- lines 160-161; kind `rule`; markers `none`

  ```k
    rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
  ```

- lines 163-163; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
  ```

- lines 164-165; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
  ```

- lines 167-168; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
          => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
  ```

- lines 169-169; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
  ```

- lines 170-170; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
  ```

- lines 171-172; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
          => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
  ```

- lines 173-173; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
  ```

- lines 174-175; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
  ```

- lines 177-177; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
  ```

- lines 178-178; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
  ```

- lines 179-181; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
         requires S =/=Int 0
  ```

- lines 187-187; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
  ```

- lines 188-188; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= evalArith(IntSeq) [function]
  ```

- lines 189-190; kind `rule`; markers `none`

  ```k
    rule evalArith(CS:IntSeq)
      => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
  ```

- lines 192-192; kind `syntax`; markers `none`

  ```k
    syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
  ```

- lines 194-194; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= evDigit(Int) [function, total]
  ```

- lines 195-195; kind `rule`; markers `none`

  ```k
    rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
  ```

- lines 196-196; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= evHead42(IntSeq) [function, total]
  ```

- lines 197-197; kind `rule`; markers `none`

  ```k
    rule evHead42(iCons(42, _:IntSeq)) => true
  ```

- lines 198-198; kind `rule`; markers `owise`

  ```k
    rule evHead42(_:IntSeq)            => false [owise]
  ```

- lines 199-199; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= evHead47(IntSeq) [function, total]
  ```

- lines 200-200; kind `rule`; markers `none`

  ```k
    rule evHead47(iCons(47, _:IntSeq)) => true
  ```

- lines 201-201; kind `rule`; markers `owise`

  ```k
    rule evHead47(_:IntSeq)            => false [owise]
  ```

- lines 203-203; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax OpSeq ::= tokOps(IntSeq) [function, total]
  ```

- lines 204-204; kind `rule`; markers `none`

  ```k
    rule tokOps(.IntSeq)                 => .OpSeq
  ```

- lines 205-205; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
  ```

- lines 206-206; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
  ```

- lines 207-207; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
  ```

- lines 208-208; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
  ```

- lines 209-209; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
  ```

- lines 210-210; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
  ```

- lines 211-211; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
  ```

- lines 212-212; kind `rule`; markers `none`

  ```k
    rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
  ```

- lines 214-215; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= tokNds(IntSeq) [function, total]
                    | tokNdAcc(Int, IntSeq) [function, total]
  ```

- lines 216-216; kind `rule`; markers `none`

  ```k
    rule tokNds(.IntSeq)                => .IntSeq
  ```

- lines 217-217; kind `rule`; markers `none`

  ```k
    rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
  ```

- lines 218-218; kind `rule`; markers `none`

  ```k
    rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
  ```

- lines 219-220; kind `rule`; markers `none`

  ```k
    rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
         requires notBool evDigit(C) andBool C =/=Int 32
  ```

- lines 221-222; kind `rule`; markers `none`

  ```k
    rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
         requires evDigit(C)
  ```

- lines 223-223; kind `rule`; markers `owise`

  ```k
    rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
  ```

- lines 225-225; kind `syntax`; markers `none`

  ```k
    syntax EvPair ::= evp(OpSeq, IntSeq)
  ```

- lines 226-226; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= firstNdE(EvPair) [function, total]
  ```

- lines 227-227; kind `rule`; markers `none`

  ```k
    rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
  ```

- lines 228-228; kind `rule`; markers `owise`

  ```k
    rule firstNdE(_:EvPair) => 0 [owise]
  ```

- lines 230-230; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= applyOpE(String, Int, Int) [function, total]
  ```

- lines 231-231; kind `rule`; markers `none`

  ```k
    rule applyOpE("+",  A:Int, B:Int) => A +Int B
  ```

- lines 232-232; kind `rule`; markers `none`

  ```k
    rule applyOpE("-",  A:Int, B:Int) => A -Int B
  ```

- lines 233-233; kind `rule`; markers `none`

  ```k
    rule applyOpE("*",  A:Int, B:Int) => A *Int B
  ```

- lines 234-234; kind `rule`; markers `none`

  ```k
    rule applyOpE("//", A:Int, B:Int) => A divInt B
  ```

- lines 235-235; kind `rule`; markers `none`

  ```k
    rule applyOpE("**", A:Int, B:Int) => A ^Int B
  ```

- lines 236-236; kind `rule`; markers `owise`

  ```k
    rule applyOpE(_:String, A:Int, _:Int) => A [owise]
  ```

- lines 238-238; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
  ```

- lines 239-239; kind `rule`; markers `none`

  ```k
    rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
  ```

- lines 240-240; kind `rule`; markers `none`

  ```k
    rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
  ```

- lines 241-242; kind `rule`; markers `none`

  ```k
    rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
         requires O =/=String "**"
  ```

- lines 243-243; kind `rule`; markers `owise`

  ```k
    rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
  ```

- lines 244-244; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax EvPair ::= powCombE(Int, EvPair) [function, total]
  ```

- lines 245-245; kind `rule`; markers `none`

  ```k
    rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
  ```

- lines 246-246; kind `rule`; markers `none`

  ```k
    rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
  ```

- lines 247-247; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
  ```

- lines 248-248; kind `rule`; markers `none`

  ```k
    rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
  ```

- lines 250-250; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
  ```

- lines 251-251; kind `rule`; markers `none`

  ```k
    rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
  ```

- lines 252-252; kind `rule`; markers `none`

  ```k
    rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
  ```

- lines 253-253; kind `rule`; markers `none`

  ```k
    rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
  ```

- lines 254-254; kind `rule`; markers `none`

  ```k
    rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
  ```

- lines 255-255; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
  ```

- lines 256-256; kind `rule`; markers `none`

  ```k
    rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
  ```

- lines 257-259; kind `rule`; markers `none`

  ```k
    rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
      => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
         requires inLevelE(L, O)
  ```

- lines 260-262; kind `rule`; markers `none`

  ```k
    rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
      => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
         requires notBool inLevelE(L, O)
  ```

- lines 263-264; kind `rule`; markers `owise`

  ```k
    rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
      => evp(OO, appendIE(ON, CUR)) [owise]
  ```

- lines 265-265; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= inLevelE(String, String) [function, total]
  ```

- lines 266-266; kind `rule`; markers `none`

  ```k
    rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
  ```

- lines 267-267; kind `rule`; markers `none`

  ```k
    rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
  ```

- lines 268-268; kind `rule`; markers `owise`

  ```k
    rule inLevelE(_:String, _:String) => false [owise]
  ```

- lines 269-269; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
  ```

- lines 270-270; kind `rule`; markers `none`

  ```k
    rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
  ```

- lines 271-271; kind `rule`; markers `none`

  ```k
    rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
  ```

- lines 272-272; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
  ```

- lines 273-273; kind `rule`; markers `none`

  ```k
    rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
  ```

- lines 274-275; kind `rule`; markers `none`

  ```k
    rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
  ```

- lines 279-279; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= "#md5"
  ```

- lines 280-281; kind `rule`; markers `priority`

  ```k
    rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
         [priority(40)]
  ```

- lines 282-282; kind `rule`; markers `none`

  ```k
    rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
  ```

- lines 283-283; kind `syntax`; markers `none`

  ```k
    syntax Val ::= md5Obj(IntSeq)
  ```

- lines 284-284; kind `rule`; markers `none`

  ```k
    rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
  ```

- lines 285-286; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
  ```

- lines 291-291; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
  ```

- lines 292-292; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
  ```

- lines 293-293; kind `syntax:function`; markers `function`

  ```k
    syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
  ```

- lines 294-294; kind `rule`; markers `none`

  ```k
    rule isIntV(_:Int)         => true
  ```

- lines 295-295; kind `rule`; markers `owise`

  ```k
    rule isIntV(_:Val)         => false [owise]
  ```

- lines 296-296; kind `rule`; markers `none`

  ```k
    rule isStrV(str(_:IntSeq)) => true
  ```

- lines 297-297; kind `rule`; markers `owise`

  ```k
    rule isStrV(_:Val)         => false [owise]
  ```

- lines 298-298; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/call.k`

Counts: endmodule=1, imports=3, module=1, rule=21, syntax=3

- lines 10-10; kind `module`; markers `none`

  ```k
  module MPY-CALL
  ```

- lines 11-11; kind `imports`; markers `none`

  ```k
    imports MPY-METHODS
  ```

- lines 12-12; kind `imports`; markers `none`

  ```k
    imports MPY-BUILTINS
  ```

- lines 13-13; kind `imports`; markers `function`

  ```k
    imports MPY-FUNCTIONS
  ```

- lines 16-17; kind `rule`; markers `none`

  ```k
    rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
  ```

- lines 19-19; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #callee(Exprs)
  ```

- lines 20-20; kind `rule`; markers `owise`

  ```k
    rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
  ```

- lines 21-22; kind `rule`; markers `none`

  ```k
    rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
  ```

- lines 24-24; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
  ```

- lines 26-26; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
  ```

- lines 27-27; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
  ```

- lines 28-28; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
  ```

- lines 29-29; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
  ```

- lines 30-30; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
  ```

- lines 31-31; kind `rule`; markers `owise`

  ```k
    rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
  ```

- lines 32-33; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
  ```

- lines 38-41; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 42-46; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
          => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(A)
         [priority(40)]
  ```

- lines 47-50; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 52-52; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isMutMethod(String) [function, total]
  ```

- lines 53-55; kind `rule`; markers `none`

  ```k
    rule isMutMethod(M:String)
      => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
         orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
  ```

- lines 56-60; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
          => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isMutMethod(M)
         [priority(40)]
  ```

- lines 63-67; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
         [priority(40)]
  ```

- lines 69-75; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
          => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
         <env>     CALLERL:Int => NEWL </env>
         <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
         <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
         <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
  ```

- lines 80-85; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
          => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
         <env>     CALLERL:Int => NEWL </env>
         <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
         <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
         <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
  ```

- lines 87-87; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #allocCells(ParamNames)
  ```

- lines 88-88; kind `rule`; markers `none`

  ```k
    rule <k> #allocCells(.ParamNames) => .K ... </k>
  ```

- lines 89-94; kind `rule`; markers `none`

  ```k
    rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
         <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
         <heapLoc> N:Int => N +Int 1 </heapLoc>
         requires notBool N in_keys(H)
  ```

- lines 95-95; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/comprehension.k`

Counts: endmodule=1, imports=5, module=1, rule=7, syntax=3

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-COMPREHENSION
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports MPY-OPERATORS
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-LIST
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports MPY-CONTROLS
  ```

- lines 8-8; kind `imports`; markers `function`

  ```k
    imports MPY-FUNCTIONS
  ```

- lines 11-11; kind `rule`; markers `none`

  ```k
    rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
  ```

- lines 12-12; kind `rule`; markers `none`

  ```k
    rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
  ```

- lines 14-14; kind `syntax:macro`; markers `macro`

  ```k
    syntax Stmts ::= compBody(CompFors, Expr) [macro]
  ```

- lines 15-16; kind `rule`; markers `none`

  ```k
    rule compBody(Gs:CompFors, ELT:Expr)
      => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
  ```

- lines 18-18; kind `syntax:macro`; markers `macro`

  ```k
    syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
  ```

- lines 19-20; kind `rule`; markers `none`

  ```k
    rule compNest(.CompFors, ELT:Expr)
      => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
  ```

- lines 21-22; kind `rule`; markers `none`

  ```k
    rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
      => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
  ```

- lines 24-24; kind `syntax:macro`; markers `macro`

  ```k
    syntax Expr ::= compGuard(Exprs) [macro]
  ```

- lines 25-25; kind `rule`; markers `none`

  ```k
    rule compGuard(.Exprs)             => Bool(true)
  ```

- lines 26-26; kind `rule`; markers `none`

  ```k
    rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
  ```

- lines 27-27; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/concrete.k`

Counts: endmodule=1, imports=1, module=1, rule=16, syntax=5

- lines 8-8; kind `module`; markers `concrete`

  ```k
  module MPY-CONCRETE
  ```

- lines 9-9; kind `imports`; markers `none`

  ```k
    imports MPY
  ```

- lines 13-15; kind `rule`; markers `none`

  ```k
    rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
         <heap> HP:Map </heap>
         requires hasRefVS(A) orBool hasRefVS(B)
  ```

- lines 16-19; kind `rule`; markers `none`

  ```k
    rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
         <heap> HP:Map </heap>
         requires hasRefVS(A) orBool hasRefVS(B)
  ```

- lines 25-25; kind `syntax`; markers `none`

  ```k
    syntax Val ::= kvP(Val, Val)
  ```

- lines 26-27; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                   | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
  ```

- lines 28-30; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
          => #ksort(VS, KV, .ValSeq, false) ... </k>
         [priority(40)]
  ```

- lines 31-33; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
          => #ksort(VS, KV, .ValSeq, RB) ... </k>
         [priority(40)]
  ```

- lines 34-35; kind `rule`; markers `none`

  ```k
    rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
          => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
  ```

- lines 36-37; kind `rule`; markers `none`

  ```k
    rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
          => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
  ```

- lines 38-40; kind `rule`; markers `none`

  ```k
    rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
          => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
         requires notBool isKwV(K)
  ```

- lines 42-42; kind `syntax:function`; markers `function`

  ```k
    syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
  ```

- lines 43-43; kind `rule`; markers `none`

  ```k
    rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
  ```

- lines 44-46; kind `rule`; markers `none`

  ```k
    rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
      => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
         requires kLt(K, K2)
  ```

- lines 47-49; kind `rule`; markers `none`

  ```k
    rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
      => vCons(kvP(K2, V2), insPair(R, K, V))
         requires notBool kLt(K, K2)
  ```

- lines 51-51; kind `syntax:function`; markers `function`

  ```k
    syntax Bool ::= kLt(Val, Val) [function]
  ```

- lines 52-52; kind `rule`; markers `none`

  ```k
    rule kLt(I1:Int, I2:Int)             => I1 <Int I2
  ```

- lines 53-53; kind `rule`; markers `none`

  ```k
    rule kLt(F1:Float, F2:Float)         => F1 <Float F2
  ```

- lines 54-54; kind `rule`; markers `none`

  ```k
    rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
  ```

- lines 56-56; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= unpairVS(ValSeq) [function, total]
  ```

- lines 57-57; kind `rule`; markers `none`

  ```k
    rule unpairVS(.ValSeq) => .ValSeq
  ```

- lines 58-58; kind `rule`; markers `none`

  ```k
    rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
  ```

- lines 59-59; kind `rule`; markers `owise`

  ```k
    rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
  ```

- lines 60-60; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/controls.k`

Counts: endmodule=1, imports=3, module=1, rule=34, syntax=3

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-CONTROLS
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports MPY-TUPLE
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 9-11; kind `rule`; markers `none`

  ```k
    rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
  ```

- lines 12-18; kind `rule`; markers `priority`

  ```k
    rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires "$cells" in_keys(M)
          andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
          andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
         [priority(40)]
  ```

- lines 20-23; kind `rule`; markers `none`

  ```k
    rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
         requires X in_keys(M)
  ```

- lines 27-32; kind `rule`; markers `priority`

  ```k
    rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires X in_keys(M) andBool isRefV({M[X]}:>Val)
         [priority(40)]
  ```

- lines 35-35; kind `rule`; markers `none`

  ```k
    rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
  ```

- lines 36-36; kind `rule`; markers `owise`

  ```k
    rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
  ```

- lines 37-37; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #bindImports(ParamNames)
  ```

- lines 38-38; kind `rule`; markers `none`

  ```k
    rule <k> #bindImports(.ParamNames) => .K ... </k>
  ```

- lines 39-42; kind `rule`; markers `none`

  ```k
    rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
         requires N ==String "floor" orBool N ==String "ceil"
  ```

- lines 43-45; kind `rule`; markers `none`

  ```k
    rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
         requires notBool (N ==String "floor" orBool N ==String "ceil")
  ```

- lines 48-49; kind `rule`; markers `none`

  ```k
    rule <k> Expr(_:Val) => .K ... </k>
  ```

- lines 51-51; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #branch(Bool, Stmts, Stmts)
  ```

- lines 52-52; kind `rule`; markers `none`

  ```k
    rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
  ```

- lines 53-53; kind `rule`; markers `none`

  ```k
    rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
  ```

- lines 54-55; kind `rule`; markers `none`

  ```k
    rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
  ```

- lines 57-58; kind `rule`; markers `none`

  ```k
    rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
         requires truthy(V)
  ```

- lines 59-61; kind `rule`; markers `none`

  ```k
    rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
         requires notBool truthy(V)
  ```

- lines 65-67; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                   | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                   | #loopLbl(K) | "#cont" | "#brk"
  ```

- lines 69-69; kind `rule`; markers `none`

  ```k
    rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
  ```

- lines 71-71; kind `rule`; markers `none`

  ```k
    rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
  ```

- lines 72-72; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
  ```

- lines 73-75; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
          => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
  ```

- lines 77-77; kind `rule`; markers `none`

  ```k
    rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
  ```

- lines 78-78; kind `rule`; markers `none`

  ```k
    rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
  ```

- lines 79-80; kind `rule`; markers `none`

  ```k
    rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
         requires truthy(V)
  ```

- lines 81-83; kind `rule`; markers `none`

  ```k
    rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
         requires notBool truthy(V)
  ```

- lines 85-85; kind `rule`; markers `none`

  ```k
    rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
  ```

- lines 86-86; kind `rule`; markers `none`

  ```k
    rule <k> Continue => #cont ... </k>
  ```

- lines 87-87; kind `rule`; markers `none`

  ```k
    rule <k> Break => #brk ... </k>
  ```

- lines 88-88; kind `rule`; markers `none`

  ```k
    rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
  ```

- lines 89-89; kind `rule`; markers `owise`

  ```k
    rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
  ```

- lines 90-90; kind `rule`; markers `none`

  ```k
    rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
  ```

- lines 91-92; kind `rule`; markers `owise`

  ```k
    rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
  ```

- lines 95-97; kind `rule`; markers `priority`

  ```k
    rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 98-100; kind `rule`; markers `priority`

  ```k
    rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 101-103; kind `rule`; markers `priority`

  ```k
    rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 106-108; kind `rule`; markers `priority`

  ```k
    rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 109-109; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/core.k`

Counts: configuration=1, endmodule=1, imports=7, module=1, rule=46, syntax=37

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-CORE
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-SYNTAX
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports INT
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports BOOL
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports STRING
  ```

- lines 8-8; kind `imports`; markers `none`

  ```k
    imports MAP
  ```

- lines 9-9; kind `imports`; markers `none`

  ```k
    imports LIST
  ```

- lines 10-10; kind `imports`; markers `none`

  ```k
    imports K-EQUAL
  ```

- lines 13-13; kind `syntax`; markers `none`

  ```k
    syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  ```

- lines 14-14; kind `syntax`; markers `none`

  ```k
    syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
  ```

- lines 15-16; kind `syntax`; markers `none`

  ```k
    syntax Str    ::= str(IntSeq)
  ```

- lines 18-23; kind `syntax`; markers `none`

  ```k
    syntax Iterable ::= list(ValSeq)
                      | tuple(ValSeq)
                      | Str
                      | rangeObj(Int, Int, Int)
                      | zipObj(ValSeq, ValSeq)
                      | zipObjS(IntSeq, IntSeq)
  ```

- lines 25-34; kind `syntax`; markers `function`

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

- lines 36-36; kind `syntax`; markers `none`

  ```k
    syntax Parent   ::= "root" | parent(Int)
  ```

- lines 37-37; kind `syntax`; markers `none`

  ```k
    syntax Scope    ::= scope(Map, Parent)
  ```

- lines 38-38; kind `syntax`; markers `none`

  ```k
    syntax KResult  ::= Val
  ```

- lines 39-39; kind `syntax`; markers `none`

  ```k
    syntax Expr     ::= Val   // cooling puts results back into expression holes
  ```

- lines 40-40; kind `syntax`; markers `none`

  ```k
    syntax Vals     ::= List{Val, ","}
  ```

- lines 41-41; kind `syntax`; markers `none`

  ```k
    syntax Exc      ::= "NoExc" | "AssertionError"
  ```

- lines 42-43; kind `syntax`; markers `none`

  ```k
    syntax RetState ::= "noRet" | retV(Val)
  ```

- lines 49-61; kind `configuration`; markers `none`

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

- lines 68-68; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isRefV(Val) [function, total]
  ```

- lines 69-69; kind `rule`; markers `none`

  ```k
    rule isRefV(ref(_:Int)) => true
  ```

- lines 70-71; kind `rule`; markers `owise`

  ```k
    rule isRefV(_:Val)      => false [owise]
  ```

- lines 75-75; kind `syntax`; markers `none`

  ```k
    syntax HeapVal ::= cellV(Val)
  ```

- lines 76-76; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isCellRef(Val) [function, total]
  ```

- lines 77-77; kind `rule`; markers `none`

  ```k
    rule isCellRef(cellRef(_:Int)) => true
  ```

- lines 78-78; kind `rule`; markers `owise`

  ```k
    rule isCellRef(_:Val)          => false [owise]
  ```

- lines 85-91; kind `rule`; markers `priority`

  ```k
    rule <k> cellRef(H:Int) => V ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         <heap> ... H |-> cellV(V:Val) ... </heap>
         requires "$cells" in_keys(M)
         [priority(40)]
  ```

- lines 95-95; kind `syntax`; markers `none`

  ```k
    syntax Val ::= kwV(String, Val)
  ```

- lines 96-96; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #kwTag(String)
  ```

- lines 97-97; kind `rule`; markers `none`

  ```k
    rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
  ```

- lines 98-99; kind `rule`; markers `none`

  ```k
    rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
         requires notBool isKwV(V)
  ```

- lines 100-100; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isKwV(Val) [function, total]
  ```

- lines 101-101; kind `rule`; markers `none`

  ```k
    rule isKwV(kwV(_:String, _:Val)) => true
  ```

- lines 102-103; kind `rule`; markers `owise`

  ```k
    rule isKwV(_:Val)                => false [owise]
  ```

- lines 106-106; kind `syntax`; markers `none`

  ```k
    syntax Val ::= cellsMark(ParamNames)
  ```

- lines 107-107; kind `syntax:function`; markers `function`

  ```k
    syntax ParamNames ::= cellsOf(Val) [function]
  ```

- lines 108-108; kind `rule`; markers `none`

  ```k
    rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
  ```

- lines 109-109; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= pnMember(String, ParamNames) [function, total]
  ```

- lines 110-110; kind `rule`; markers `none`

  ```k
    rule pnMember(_:String, .ParamNames) => false
  ```

- lines 111-111; kind `rule`; markers `none`

  ```k
    rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
  ```

- lines 113-113; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #cellW(Val, Val)
  ```

- lines 114-115; kind `rule`; markers `none`

  ```k
    rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
         <heap> ... H |-> cellV(_:Val => V) ... </heap>
  ```

- lines 117-117; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #alloc(Val)
  ```

- lines 118-122; kind `rule`; markers `none`

  ```k
    rule <k> #alloc(V:Val) => ref(N) ... </k>
         <heap>    H:Map => (N |-> V) H </heap>
         <heapLoc> N:Int => N +Int 1 </heapLoc>
         requires notBool N in_keys(H)
  ```

- lines 124-124; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #loadAll(Module)
  ```

- lines 125-125; kind `rule`; markers `none`

  ```k
    rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
  ```

- lines 126-126; kind `rule`; markers `none`

  ```k
    rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
  ```

- lines 127-128; kind `rule`; markers `none`

  ```k
    rule <k> .Stmts => .K ... </k>
  ```

- lines 130-130; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #look(String, Int)
  ```

- lines 131-131; kind `rule`; markers `none`

  ```k
    rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
  ```

- lines 132-134; kind `rule`; markers `none`

  ```k
    rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
         <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
         requires X in_keys(M)
  ```

- lines 145-151; kind `rule`; markers `priority`

  ```k
    rule <k> #look(X:String, L:Int) => V ... </k>
         <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
         <heap> ... H |-> cellV(V:Val) ... </heap>
         requires X in_keys(M) andBool "$cells" in_keys(M)
          andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
          andBool {M[X]}:>Val ==K cellRef(H)
         [priority(40)]
  ```

- lines 152-155; kind `rule`; markers `none`

  ```k
    rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
         <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
         requires notBool (X in_keys(M))
  ```

- lines 157-157; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Scope ::= "builtinsScope" [function, total]
  ```

- lines 158-182; kind `rule`; markers `none`

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

- lines 185-185; kind `syntax`; markers `none`

  ```k
    syntax ApplyK ::= toCall(Val)
  ```

- lines 186-188; kind `syntax`; markers `none`

  ```k
    syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                    | #evalArgCont(Exprs, Vals, ApplyK)
                    | #applyK(ApplyK, Vals)
  ```

- lines 189-189; kind `rule`; markers `none`

  ```k
    rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
  ```

- lines 190-190; kind `rule`; markers `none`

  ```k
    rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
  ```

- lines 191-192; kind `rule`; markers `none`

  ```k
    rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
  ```

- lines 194-194; kind `rule`; markers `none`

  ```k
    rule <k> Int(I:Int)   => I ... </k>
  ```

- lines 195-195; kind `rule`; markers `none`

  ```k
    rule <k> Bool(B:Bool) => B ... </k>
  ```

- lines 196-197; kind `rule`; markers `none`

  ```k
    rule <k> NoneVal      => noneV ... </k>
  ```

- lines 199-199; kind `syntax:function`; markers `function`

  ```k
    syntax Bool ::= truthy(Val) [function]
  ```

- lines 200-200; kind `rule`; markers `none`

  ```k
    rule truthy(B:Bool)          => B
  ```

- lines 201-201; kind `rule`; markers `none`

  ```k
    rule truthy(noneV)           => false
  ```

- lines 202-202; kind `rule`; markers `none`

  ```k
    rule truthy(I:Int)           => I =/=Int 0
  ```

- lines 203-203; kind `rule`; markers `none`

  ```k
    rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
  ```

- lines 204-204; kind `rule`; markers `none`

  ```k
    rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
  ```

- lines 205-206; kind `rule`; markers `none`

  ```k
    rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
  ```

- lines 208-208; kind `syntax:function`; markers `function`

  ```k
    syntax Val  ::= applyUn(String, Val) [function]
  ```

- lines 209-209; kind `syntax:function`; markers `function`

  ```k
    syntax Val  ::= applyBin(String, Val, Val) [function]
  ```

- lines 210-211; kind `syntax:function`; markers `function`

  ```k
    syntax Bool ::= applyCmp(String, Val, Val) [function]
  ```

- lines 213-213; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Vals ::= appendVal(Vals, Val) [function, total]
  ```

- lines 214-214; kind `rule`; markers `none`

  ```k
    rule appendVal(.Vals, V:Val)              => V , .Vals
  ```

- lines 215-215; kind `rule`; markers `none`

  ```k
    rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
  ```

- lines 217-217; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= vals2valSeq(Vals) [function, total]
  ```

- lines 218-218; kind `rule`; markers `none`

  ```k
    rule vals2valSeq(.Vals)            => .ValSeq
  ```

- lines 219-220; kind `rule`; markers `none`

  ```k
    rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
  ```

- lines 223-223; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= vsLen(ValSeq) [function, total]
  ```

- lines 224-224; kind `rule`; markers `none`

  ```k
    rule vsLen(.ValSeq)                => 0
  ```

- lines 225-225; kind `rule`; markers `none`

  ```k
    rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
  ```

- lines 227-227; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= isLen(IntSeq) [function, total]
  ```

- lines 228-228; kind `rule`; markers `none`

  ```k
    rule isLen(.IntSeq)                => 0
  ```

- lines 229-230; kind `rule`; markers `none`

  ```k
    rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
  ```

- lines 233-233; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
  ```

- lines 234-234; kind `rule`; markers `none`

  ```k
    rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
  ```

- lines 235-235; kind `rule`; markers `none`

  ```k
    rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
  ```

- lines 236-237; kind `rule`; markers `none`

  ```k
    rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
         requires I >Int 0
  ```

- lines 238-239; kind `rule`; markers `none`

  ```k
    rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
         requires I <Int 0
  ```

- lines 240-240; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/dict.k`

Counts: endmodule=1, imports=4, module=1, rule=28, syntax=12

- lines 13-13; kind `module`; markers `none`

  ```k
  module MPY-DICT
  ```

- lines 14-14; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 15-15; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 16-16; kind `imports`; markers `none`

  ```k
    imports MPY-METHODS
  ```

- lines 17-17; kind `imports`; markers `none`

  ```k
    imports MPY-LIST
  ```

- lines 20-21; kind `syntax`; markers `none`

  ```k
    syntax Val ::= dictV(ValSeq, ValSeq)
  ```

- lines 23-25; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                   | #dictKey(Expr, Entries, ValSeq, ValSeq)
                   | #dictVal(Val, Entries, ValSeq, ValSeq)
  ```

- lines 26-26; kind `rule`; markers `none`

  ```k
    rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
  ```

- lines 27-27; kind `rule`; markers `none`

  ```k
    rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
  ```

- lines 28-29; kind `rule`; markers `none`

  ```k
    rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
          => K ~> #dictKey(V, REST, KS, VS) ... </k>
  ```

- lines 30-31; kind `rule`; markers `none`

  ```k
    rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
          => V ~> #dictVal(KV, REST, KS, VS) ... </k>
  ```

- lines 32-34; kind `rule`; markers `none`

  ```k
    rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
          => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
  ```

- lines 37-37; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
  ```

- lines 38-38; kind `rule`; markers `none`

  ```k
    rule dHasKey(.ValSeq, _:Val)                => false
  ```

- lines 39-39; kind `rule`; markers `none`

  ```k
    rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
  ```

- lines 40-41; kind `rule`; markers `none`

  ```k
    rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
  ```

- lines 43-43; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
  ```

- lines 44-44; kind `rule`; markers `none`

  ```k
    rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
  ```

- lines 45-46; kind `rule`; markers `none`

  ```k
    rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
  ```

- lines 49-49; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
  ```

- lines 50-51; kind `rule`; markers `none`

  ```k
    rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
         requires A ==K K
  ```

- lines 52-53; kind `rule`; markers `none`

  ```k
    rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
         requires notBool (A ==K K)
  ```

- lines 54-55; kind `rule`; markers `owise`

  ```k
    rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
  ```

- lines 58-61; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
          => #alloc(list(KS)) ... </k>
         [priority(40)]
  ```

- lines 63-63; kind `rule`; markers `none`

  ```k
    rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
  ```

- lines 64-64; kind `syntax:function`; markers `function`

  ```k
    syntax Val ::= applyIndexD(Val, Val) [function]
  ```

- lines 65-67; kind `rule`; markers `priority`

  ```k
    rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
         [priority(45)]
  ```

- lines 70-70; kind `syntax:function`; markers `function`

  ```k
    syntax Val ::= dictSet(Val, Val, Val) [function]
  ```

- lines 71-72; kind `rule`; markers `none`

  ```k
    rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
  ```

- lines 76-76; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #dsetK(String, Val)
  ```

- lines 77-77; kind `rule`; markers `none`

  ```k
    rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
  ```

- lines 78-81; kind `rule`; markers `none`

  ```k
    rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
         requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
  ```

- lines 82-85; kind `rule`; markers `none`

  ```k
    rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires X in_keys(M) andBool isRefV({M[X]}:>Val)
  ```

- lines 86-86; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #dsetV(Val, Val, Val)
  ```

- lines 87-88; kind `rule`; markers `none`

  ```k
    rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
         <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  ```

- lines 90-90; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= normIdxD(Int, Int) [function, total]
  ```

- lines 91-91; kind `rule`; markers `none`

  ```k
    rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
  ```

- lines 92-93; kind `rule`; markers `none`

  ```k
    rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
  ```

- lines 95-96; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
      => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
  ```

- lines 97-97; kind `syntax:function`; markers `function`

  ```k
    syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
  ```

- lines 98-98; kind `rule`; markers `none`

  ```k
    rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
  ```

- lines 99-100; kind `rule`; markers `none`

  ```k
    rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
      => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
  ```

- lines 101-101; kind `syntax:function`; markers `function`

  ```k
    syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
  ```

- lines 102-102; kind `rule`; markers `none`

  ```k
    rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
  ```

- lines 103-103; kind `rule`; markers `none`

  ```k
    rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
  ```

- lines 104-104; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/float.k`

Counts: endmodule=1, imports=3, module=1, rule=121, syntax=34

- lines 14-14; kind `module`; markers `none`

  ```k
  module MPY-FLOAT
  ```

- lines 15-15; kind `imports`; markers `none`

  ```k
    imports MPY-OPERATORS
  ```

- lines 16-16; kind `imports`; markers `none`

  ```k
    imports MPY-BUILTINS
  ```

- lines 17-17; kind `imports`; markers `none`

  ```k
    imports FLOAT
  ```

- lines 20-20; kind `syntax`; markers `none`

  ```k
    syntax Val ::= Float
  ```

- lines 21-22; kind `rule`; markers `none`

  ```k
    rule <k> Float(F:Float) => F ... </k>
  ```

- lines 24-24; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
  ```

- lines 25-25; kind `rule`; markers `concrete`

  ```k
    rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
  ```

- lines 27-28; kind `rule`; markers `none`

  ```k
    rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
  ```

- lines 30-30; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
  ```

- lines 31-31; kind `rule`; markers `concrete`

  ```k
    rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
  ```

- lines 32-33; kind `rule`; markers `none`

  ```k
    rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
  ```

- lines 37-37; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
  ```

- lines 38-38; kind `rule`; markers `concrete`

  ```k
    rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
  ```

- lines 39-40; kind `rule`; markers `none`

  ```k
    rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
  ```

- lines 43-43; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
  ```

- lines 44-45; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
  ```

- lines 50-50; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
  ```

- lines 51-51; kind `rule`; markers `concrete`

  ```k
    rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
  ```

- lines 52-52; kind `rule`; markers `none`

  ```k
    rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
  ```

- lines 54-54; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
  ```

- lines 55-55; kind `rule`; markers `concrete`

  ```k
    rule absF(F:Float) => absFloat(F) [concrete]
  ```

- lines 56-57; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
  ```

- lines 61-62; kind `rule`; markers `none`

  ```k
    rule <k> Import(_:String) => .K ... </k>
  ```

- lines 65-65; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= "#mathCeil"
  ```

- lines 66-66; kind `rule`; markers `priority`

  ```k
    rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
  ```

- lines 67-68; kind `rule`; markers `none`

  ```k
    rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
  ```

- lines 70-70; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= "#mathFloor"
  ```

- lines 71-71; kind `rule`; markers `priority`

  ```k
    rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
  ```

- lines 72-72; kind `rule`; markers `none`

  ```k
    rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
  ```

- lines 73-73; kind `syntax:function,total,symbol`; markers `function,total,symbol`

  ```k
    syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
  ```

- lines 74-74; kind `rule`; markers `concrete`

  ```k
    rule floorFI(I:Int)   => I                        [concrete]
  ```

- lines 75-76; kind `rule`; markers `concrete`

  ```k
    rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
  ```

- lines 78-78; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
  ```

- lines 79-80; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
  ```

- lines 82-82; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
  ```

- lines 83-83; kind `rule`; markers `priority`

  ```k
    rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
  ```

- lines 84-84; kind `rule`; markers `none`

  ```k
    rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
  ```

- lines 85-85; kind `rule`; markers `none`

  ```k
    rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
  ```

- lines 86-86; kind `syntax:function,total,symbol`; markers `function,total,symbol`

  ```k
    syntax Float ::= toF(Val) [function, total, symbol(toF)]
  ```

- lines 87-87; kind `rule`; markers `concrete`

  ```k
    rule toF(F:Float) => F        [concrete]
  ```

- lines 88-89; kind `rule`; markers `concrete`

  ```k
    rule toF(I:Int)   => intToF(I) [concrete]
  ```

- lines 93-93; kind `syntax:function,total,symbol`; markers `function,total,symbol`

  ```k
    syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
  ```

- lines 94-94; kind `rule`; markers `concrete`

  ```k
    rule ceilF(I:Int)   => I                       [concrete]
  ```

- lines 95-96; kind `rule`; markers `concrete`

  ```k
    rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
  ```

- lines 99-100; kind `rule`; markers `none`

  ```k
    rule applyUn("-", F:Float) => 0.0 -Float F
  ```

- lines 103-103; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
  ```

- lines 104-104; kind `rule`; markers `concrete`

  ```k
    rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
  ```

- lines 105-105; kind `rule`; markers `none`

  ```k
    rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
  ```

- lines 107-107; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
  ```

- lines 108-108; kind `rule`; markers `concrete`

  ```k
    rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
  ```

- lines 109-109; kind `rule`; markers `none`

  ```k
    rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
  ```

- lines 111-111; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
  ```

- lines 112-112; kind `rule`; markers `concrete`

  ```k
    rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
  ```

- lines 113-113; kind `rule`; markers `none`

  ```k
    rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
  ```

- lines 115-115; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
  ```

- lines 116-116; kind `rule`; markers `concrete`

  ```k
    rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
  ```

- lines 117-117; kind `rule`; markers `none`

  ```k
    rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
  ```

- lines 119-119; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
  ```

- lines 120-120; kind `rule`; markers `concrete`

  ```k
    rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
  ```

- lines 121-122; kind `rule`; markers `none`

  ```k
    rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
  ```

- lines 125-125; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
  ```

- lines 126-126; kind `rule`; markers `concrete`

  ```k
    rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
  ```

- lines 127-127; kind `rule`; markers `none`

  ```k
    rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
  ```

- lines 128-128; kind `rule`; markers `none`

  ```k
    rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
  ```

- lines 129-130; kind `rule`; markers `none`

  ```k
    rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
  ```

- lines 132-132; kind `rule`; markers `none`

  ```k
    rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
  ```

- lines 133-133; kind `rule`; markers `none`

  ```k
    rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
  ```

- lines 134-134; kind `rule`; markers `none`

  ```k
    rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
  ```

- lines 135-135; kind `rule`; markers `none`

  ```k
    rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
  ```

- lines 136-136; kind `rule`; markers `none`

  ```k
    rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
  ```

- lines 137-137; kind `rule`; markers `none`

  ```k
    rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
  ```

- lines 138-138; kind `rule`; markers `none`

  ```k
    rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
  ```

- lines 139-140; kind `rule`; markers `none`

  ```k
    rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
  ```

- lines 142-142; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
  ```

- lines 143-143; kind `rule`; markers `concrete`

  ```k
    rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
  ```

- lines 144-144; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
  ```

- lines 145-145; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
  ```

- lines 146-146; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
  ```

- lines 147-147; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
  ```

- lines 148-148; kind `rule`; markers `none`

  ```k
    rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
  ```

- lines 149-149; kind `rule`; markers `none`

  ```k
    rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
  ```

- lines 150-150; kind `rule`; markers `none`

  ```k
    rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
  ```

- lines 151-152; kind `rule`; markers `none`

  ```k
    rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
  ```

- lines 154-154; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", V:Val, noneV) => V ==K noneV
  ```

- lines 155-156; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
  ```

- lines 160-160; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
  ```

- lines 161-161; kind `rule`; markers `concrete`

  ```k
    rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
  ```

- lines 162-164; kind `rule`; markers `concrete`

  ```k
    rule decStrToF(CS:IntSeq)
      => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
         requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
  ```

- lines 165-165; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= headIS(IntSeq) [function]
  ```

- lines 166-166; kind `rule`; markers `none`

  ```k
    rule headIS(iCons(C:Int, _:IntSeq)) => C
  ```

- lines 167-167; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
  ```

- lines 168-168; kind `rule`; markers `none`

  ```k
    rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
  ```

- lines 169-169; kind `rule`; markers `none`

  ```k
    rule intPartAcc(.IntSeq, A:Int) => A
  ```

- lines 170-170; kind `rule`; markers `none`

  ```k
    rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
  ```

- lines 171-172; kind `rule`; markers `none`

  ```k
    rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
         requires C =/=Int 46
  ```

- lines 173-173; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
  ```

- lines 174-174; kind `rule`; markers `none`

  ```k
    rule fracPart(.IntSeq) => 0
  ```

- lines 175-175; kind `rule`; markers `none`

  ```k
    rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
  ```

- lines 176-176; kind `rule`; markers `none`

  ```k
    rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
  ```

- lines 177-177; kind `rule`; markers `none`

  ```k
    rule fracAcc(.IntSeq, A:Int) => A
  ```

- lines 178-178; kind `rule`; markers `none`

  ```k
    rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
  ```

- lines 179-179; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
  ```

- lines 180-180; kind `rule`; markers `none`

  ```k
    rule fracScale(.IntSeq) => 1
  ```

- lines 181-181; kind `rule`; markers `none`

  ```k
    rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
  ```

- lines 182-182; kind `rule`; markers `none`

  ```k
    rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
  ```

- lines 183-183; kind `rule`; markers `none`

  ```k
    rule fscAcc(.IntSeq, A:Int) => A
  ```

- lines 184-184; kind `rule`; markers `none`

  ```k
    rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
  ```

- lines 185-185; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
  ```

- lines 186-186; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
  ```

- lines 187-188; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("float", F:Float, .Vals)        => F
  ```

- lines 190-190; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
  ```

- lines 191-191; kind `rule`; markers `concrete`

  ```k
    rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
  ```

- lines 192-193; kind `rule`; markers `none`

  ```k
    rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
  ```

- lines 195-195; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
  ```

- lines 196-196; kind `rule`; markers `concrete`

  ```k
    rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
  ```

- lines 197-197; kind `rule`; markers `none`

  ```k
    rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
  ```

- lines 198-198; kind `rule`; markers `none`

  ```k
    rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
  ```

- lines 199-199; kind `rule`; markers `none`

  ```k
    rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
  ```

- lines 200-200; kind `rule`; markers `none`

  ```k
    rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
  ```

- lines 201-201; kind `rule`; markers `none`

  ```k
    rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
  ```

- lines 202-202; kind `rule`; markers `none`

  ```k
    rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
  ```

- lines 203-203; kind `rule`; markers `none`

  ```k
    rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
  ```

- lines 204-204; kind `rule`; markers `none`

  ```k
    rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
  ```

- lines 205-205; kind `rule`; markers `none`

  ```k
    rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
  ```

- lines 206-207; kind `rule`; markers `none`

  ```k
    rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
  ```

- lines 209-209; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
  ```

- lines 210-210; kind `rule`; markers `concrete`

  ```k
    rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
  ```

- lines 211-211; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
  ```

- lines 213-213; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
  ```

- lines 214-215; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("float", F:Float, .Vals) => F
  ```

- lines 217-217; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
  ```

- lines 218-222; kind `rule`; markers `concrete`

  ```k
    rule roundF(F:Float)
      => #if (F -Float floorFloat(F)) ==Float 0.5
         #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
                #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
         #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
  ```

- lines 223-223; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
  ```

- lines 224-226; kind `rule`; markers `concrete`

  ```k
    rule roundFN(F:Float, N:Int)
      => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
         /Float Int2Float(10 ^Int N, 53, 11) [concrete]
  ```

- lines 227-227; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
  ```

- lines 228-228; kind `rule`; markers `none`

  ```k
    rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
  ```

- lines 230-230; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
  ```

- lines 231-231; kind `rule`; markers `concrete`

  ```k
    rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
  ```

- lines 232-232; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= "#mathSqrt"
  ```

- lines 233-233; kind `rule`; markers `priority`

  ```k
    rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
  ```

- lines 234-234; kind `rule`; markers `none`

  ```k
    rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
  ```

- lines 235-236; kind `rule`; markers `none`

  ```k
    rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
  ```

- lines 243-243; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
  ```

- lines 244-244; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
  ```

- lines 245-245; kind `rule`; markers `none`

  ```k
    rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
  ```

- lines 246-246; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
  ```

- lines 247-248; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```

- lines 250-250; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
  ```

- lines 251-251; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
  ```

- lines 252-252; kind `rule`; markers `none`

  ```k
    rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
  ```

- lines 253-253; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
  ```

- lines 254-256; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```

- lines 261-261; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
  ```

- lines 262-264; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
          => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
         requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
  ```

- lines 265-265; kind `rule`; markers `none`

  ```k
    rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
  ```

- lines 266-266; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
  ```

- lines 267-269; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
          => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```

- lines 270-272; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
          => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
         requires isInt(V) orBool isBool(V)
  ```

- lines 273-273; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/functions.k`

Counts: endmodule=1, imports=1, module=1, rule=15, syntax=4

- lines 3-3; kind `module`; markers `function`

  ```k
  module MPY-FUNCTIONS
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 8-12; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                   | #bindP(ParamNames, Vals)
                   | "#pop"
                   | "#endcall"
  ```

- lines 14-16; kind `rule`; markers `none`

  ```k
    rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
  ```

- lines 18-18; kind `syntax`; markers `none`

  ```k
    syntax Expr ::= closureExpr(ParamNames, Stmts)
  ```

- lines 19-21; kind `rule`; markers `none`

  ```k
    rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
         <env> L:Int </env>
  ```

- lines 27-28; kind `syntax`; markers `none`

  ```k
    syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
  ```

- lines 31-32; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                   | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
  ```

- lines 33-35; kind `rule`; markers `none`

  ```k
    rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                     FreeVars(FVS:ParamNames), BODY:Stmts)
          => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
  ```

- lines 36-41; kind `rule`; markers `none`

  ```k
    rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                        (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
          => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires FV in_keys(M)
  ```

- lines 42-45; kind `rule`; markers `none`

  ```k
    rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                        .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
  ```

- lines 47-49; kind `rule`; markers `none`

  ```k
    rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
          => closureVal(PNS, Return(E) .Stmts, L) ... </k>
         <env> L:Int </env>
  ```

- lines 50-52; kind `rule`; markers `none`

  ```k
    rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                    FreeVars(FVS:ParamNames), E:Expr)
          => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
  ```

- lines 53-58; kind `rule`; markers `none`

  ```k
    rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                       (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
          => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires FV in_keys(M)
  ```

- lines 59-61; kind `rule`; markers `none`

  ```k
    rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
          => closureValC(PNS, CVS, BODY, CM) ... </k>
  ```

- lines 63-63; kind `rule`; markers `none`

  ```k
    rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
  ```

- lines 64-66; kind `rule`; markers `none`

  ```k
    rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  ```

- lines 68-76; kind `rule`; markers `priority`

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

- lines 78-79; kind `rule`; markers `none`

  ```k
    rule <k> Return(V:Val) ~> _ => #pop </k>
         <ret> noRet => retV(V) </ret>
  ```

- lines 80-81; kind `rule`; markers `none`

  ```k
    rule <k> #endcall => #pop ... </k>
         <ret> noRet => retV(noneV) </ret>
  ```

- lines 85-90; kind `rule`; markers `none`

  ```k
    rule <k> #pop => V ~> CONT </k>
         <ret>   retV(V) => noRet </ret>
         <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
         <env>   L:Int => CALLERL </env>
         <scopes> SC:Map => SC [ L <- undef ] </scopes>
         <scopeLoc> _ => SAVEDL </scopeLoc>
  ```

- lines 91-91; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/int.k`

Counts: endmodule=1, imports=1, module=1, rule=16, syntax=1

- lines 4-4; kind `module`; markers `none`

  ```k
  module MPY-INT
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 7-7; kind `rule`; markers `none`

  ```k
    rule applyUn("-", I:Int) => 0 -Int I
  ```

- lines 9-9; kind `rule`; markers `none`

  ```k
    rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  ```

- lines 11-11; kind `rule`; markers `none`

  ```k
    rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
  ```

- lines 12-12; kind `rule`; markers `none`

  ```k
    rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
  ```

- lines 13-13; kind `rule`; markers `none`

  ```k
    rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
  ```

- lines 14-14; kind `rule`; markers `none`

  ```k
    rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
  ```

- lines 15-15; kind `rule`; markers `none`

  ```k
    rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
  ```

- lines 16-16; kind `rule`; markers `none`

  ```k
    rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
  ```

- lines 17-17; kind `rule`; markers `none`

  ```k
    rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
  ```

- lines 19-19; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= pyMod(Int, Int) [function]
  ```

- lines 20-20; kind `rule`; markers `none`

  ```k
    rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
  ```

- lines 22-22; kind `rule`; markers `none`

  ```k
    rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
  ```

- lines 23-23; kind `rule`; markers `none`

  ```k
    rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
  ```

- lines 24-24; kind `rule`; markers `none`

  ```k
    rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
  ```

- lines 25-25; kind `rule`; markers `none`

  ```k
    rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
  ```

- lines 26-26; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
  ```

- lines 27-27; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
  ```

- lines 28-28; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/iter.k`

Counts: endmodule=1, imports=1, module=1, syntax=1

- lines 6-6; kind `module`; markers `none`

  ```k
  module MPY-ITER
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 8-8; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
  ```

- lines 9-9; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/list.k`

Counts: endmodule=1, imports=3, module=1, rule=27, syntax=5

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-LIST
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-OPERATORS
  ```

- lines 9-9; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
  ```

- lines 10-11; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
  ```

- lines 13-13; kind `syntax`; markers `none`

  ```k
    syntax ApplyK ::= "toList"
  ```

- lines 14-14; kind `rule`; markers `none`

  ```k
    rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
  ```

- lines 15-16; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
  ```

- lines 18-18; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
  ```

- lines 19-19; kind `rule`; markers `none`

  ```k
    rule valSeqConcat(.ValSeq, T:ValSeq)                => T
  ```

- lines 20-21; kind `rule`; markers `none`

  ```k
    rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
  ```

- lines 24-25; kind `rule`; markers `priority`

  ```k
    rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
         [priority(45)]
  ```

- lines 27-27; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
  ```

- lines 28-29; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
  ```

- lines 33-33; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= hasRefVS(ValSeq) [function, total]
  ```

- lines 34-34; kind `rule`; markers `none`

  ```k
    rule hasRefVS(.ValSeq)                => false
  ```

- lines 35-35; kind `rule`; markers `none`

  ```k
    rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
  ```

- lines 37-38; kind `syntax:function`; markers `function`

  ```k
    syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                  | deepEqV(Val, Val, Map)        [function]
  ```

- lines 39-39; kind `rule`; markers `none`

  ```k
    rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
  ```

- lines 40-40; kind `rule`; markers `none`

  ```k
    rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
  ```

- lines 41-41; kind `rule`; markers `none`

  ```k
    rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
  ```

- lines 42-43; kind `rule`; markers `none`

  ```k
    rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
      => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
  ```

- lines 45-46; kind `rule`; markers `none`

  ```k
    rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
         requires H in_keys(HP)
  ```

- lines 47-48; kind `rule`; markers `none`

  ```k
    rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
         requires notBool isRefV(A) andBool H in_keys(HP)
  ```

- lines 49-49; kind `rule`; markers `none`

  ```k
    rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
  ```

- lines 50-51; kind `rule`; markers `owise`

  ```k
    rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
  ```

- lines 53-56; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
         <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
         [priority(40)]
  ```

- lines 58-58; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
  ```

- lines 59-59; kind `rule`; markers `none`

  ```k
    rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
  ```

- lines 60-60; kind `rule`; markers `none`

  ```k
    rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
  ```

- lines 61-61; kind `rule`; markers `none`

  ```k
    rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
  ```

- lines 62-62; kind `rule`; markers `none`

  ```k
    rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
  ```

- lines 63-64; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
         requires E ==K V
  ```

- lines 65-66; kind `rule`; markers `none`

  ```k
    rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
         requires notBool (E ==K V)
  ```

- lines 67-67; kind `rule`; markers `none`

  ```k
    rule <k> B:Bool ~> #notB => notBool B ... </k>
  ```

- lines 68-68; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/methods.k`

Counts: endmodule=1, imports=4, module=1, rule=75, syntax=27

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-METHODS
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports K-EQUAL
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-STR
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports MPY-LIST
  ```

- lines 10-11; kind `syntax:function`; markers `function`

  ```k
    syntax Val ::= applyMethod(Val, String, Vals) [function]
  ```

- lines 13-13; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
  ```

- lines 14-14; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
  ```

- lines 15-15; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
  ```

- lines 16-17; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
  ```

- lines 19-19; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
  ```

- lines 20-20; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
  ```

- lines 21-22; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
  ```

- lines 26-26; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
  ```

- lines 27-27; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
  ```

- lines 28-28; kind `rule`; markers `none`

  ```k
    rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
  ```

- lines 29-29; kind `rule`; markers `none`

  ```k
    rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
  ```

- lines 30-32; kind `rule`; markers `none`

  ```k
    rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
      => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
  ```

- lines 34-34; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
  ```

- lines 35-35; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= cntSub(IntSeq, IntSeq) [function]
  ```

- lines 36-36; kind `rule`; markers `none`

  ```k
    rule cntSub(.IntSeq, _:IntSeq) => 0
  ```

- lines 37-38; kind `rule`; markers `none`

  ```k
    rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
         requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
  ```

- lines 39-40; kind `rule`; markers `none`

  ```k
    rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
         requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
  ```

- lines 41-41; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
  ```

- lines 42-42; kind `rule`; markers `none`

  ```k
    rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
  ```

- lines 43-43; kind `rule`; markers `owise`

  ```k
    rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
  ```

- lines 44-45; kind `rule`; markers `none`

  ```k
    rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
  ```

- lines 47-47; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
  ```

- lines 48-48; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= trimWS(IntSeq) [function, total]
  ```

- lines 49-49; kind `rule`; markers `none`

  ```k
    rule trimWS(.IntSeq) => .IntSeq
  ```

- lines 50-50; kind `rule`; markers `none`

  ```k
    rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
  ```

- lines 51-51; kind `rule`; markers `none`

  ```k
    rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
  ```

- lines 52-52; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
  ```

- lines 53-53; kind `rule`; markers `none`

  ```k
    rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
  ```

- lines 54-54; kind `rule`; markers `none`

  ```k
    rule revISAcc(.IntSeq, A:IntSeq) => A
  ```

- lines 55-56; kind `rule`; markers `none`

  ```k
    rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
  ```

- lines 58-59; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
  ```

- lines 61-62; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
  ```

- lines 64-64; kind `rule`; markers `none`

  ```k
    rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
  ```

- lines 65-65; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
  ```

- lines 66-66; kind `rule`; markers `none`

  ```k
    rule cntOccVS(.ValSeq, _:Val)                => 0
  ```

- lines 67-67; kind `rule`; markers `none`

  ```k
    rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
  ```

- lines 68-69; kind `rule`; markers `none`

  ```k
    rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
  ```

- lines 72-74; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
          => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
         [priority(40)]
  ```

- lines 75-75; kind `syntax:function`; markers `function`

  ```k
    syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
  ```

- lines 76-76; kind `rule`; markers `none`

  ```k
    rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
  ```

- lines 77-78; kind `rule`; markers `none`

  ```k
    rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
         requires isWSC(C)
  ```

- lines 79-80; kind `rule`; markers `none`

  ```k
    rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
         requires notBool isWSC(C)
  ```

- lines 82-82; kind `syntax:function`; markers `function`

  ```k
    syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
  ```

- lines 83-83; kind `rule`; markers `none`

  ```k
    rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
  ```

- lines 84-84; kind `rule`; markers `none`

  ```k
    rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
  ```

- lines 85-85; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isWSC(Int) [function, total]
  ```

- lines 86-87; kind `rule`; markers `none`

  ```k
    rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
  ```

- lines 89-92; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
          => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
         [priority(39)]
  ```

- lines 94-96; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
          => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
         [priority(40)]
  ```

- lines 97-97; kind `syntax:function`; markers `function`

  ```k
    syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
  ```

- lines 98-98; kind `rule`; markers `none`

  ```k
    rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
  ```

- lines 99-100; kind `rule`; markers `none`

  ```k
    rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
         requires C ==Int SEP
  ```

- lines 101-102; kind `rule`; markers `none`

  ```k
    rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
         requires notBool (C ==Int SEP)
  ```

- lines 104-105; kind `rule`; markers `none`

  ```k
    rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
      => str(replaceC(CS, A, B))
  ```

- lines 106-106; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
  ```

- lines 107-107; kind `rule`; markers `none`

  ```k
    rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
  ```

- lines 108-108; kind `rule`; markers `none`

  ```k
    rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
  ```

- lines 109-110; kind `rule`; markers `none`

  ```k
    rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
  ```

- lines 112-112; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isUpperC(Int) [function, total]
  ```

- lines 113-113; kind `rule`; markers `none`

  ```k
    rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
  ```

- lines 115-115; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isLowerC(Int) [function, total]
  ```

- lines 116-116; kind `rule`; markers `none`

  ```k
    rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
  ```

- lines 118-118; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isAlphaC(Int) [function, total]
  ```

- lines 119-119; kind `rule`; markers `none`

  ```k
    rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
  ```

- lines 121-121; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= isDigitC(Int) [function, total]
  ```

- lines 122-122; kind `rule`; markers `none`

  ```k
    rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
  ```

- lines 124-124; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= hasUpper(IntSeq) [function, total]
  ```

- lines 125-125; kind `rule`; markers `none`

  ```k
    rule hasUpper(.IntSeq) => false
  ```

- lines 126-126; kind `rule`; markers `none`

  ```k
    rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
  ```

- lines 128-128; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= hasLower(IntSeq) [function, total]
  ```

- lines 129-129; kind `rule`; markers `none`

  ```k
    rule hasLower(.IntSeq) => false
  ```

- lines 130-130; kind `rule`; markers `none`

  ```k
    rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
  ```

- lines 132-132; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= allAlpha(IntSeq) [function, total]
  ```

- lines 133-133; kind `rule`; markers `none`

  ```k
    rule allAlpha(.IntSeq) => true
  ```

- lines 134-134; kind `rule`; markers `none`

  ```k
    rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
  ```

- lines 136-136; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= allDigit(IntSeq) [function, total]
  ```

- lines 137-137; kind `rule`; markers `none`

  ```k
    rule allDigit(.IntSeq) => true
  ```

- lines 138-138; kind `rule`; markers `none`

  ```k
    rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
  ```

- lines 140-140; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= lowerC(Int) [function, total]
  ```

- lines 142-142; kind `rule`; markers `none`

  ```k
    rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
  ```

- lines 143-143; kind `rule`; markers `owise`

  ```k
    rule lowerC(C:Int) => C         [owise]
  ```

- lines 145-145; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= upperC(Int) [function, total]
  ```

- lines 146-146; kind `rule`; markers `none`

  ```k
    rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
  ```

- lines 147-147; kind `rule`; markers `owise`

  ```k
    rule upperC(C:Int) => C         [owise]
  ```

- lines 149-149; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= swapC(Int) [function, total]
  ```

- lines 150-150; kind `rule`; markers `none`

  ```k
    rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
  ```

- lines 151-151; kind `rule`; markers `none`

  ```k
    rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
  ```

- lines 152-152; kind `rule`; markers `owise`

  ```k
    rule swapC(C:Int) => C         [owise]
  ```

- lines 154-154; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= mapLower(IntSeq) [function, total]
  ```

- lines 155-155; kind `rule`; markers `none`

  ```k
    rule mapLower(.IntSeq) => .IntSeq
  ```

- lines 156-156; kind `rule`; markers `none`

  ```k
    rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
  ```

- lines 158-158; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= mapUpper(IntSeq) [function, total]
  ```

- lines 159-159; kind `rule`; markers `none`

  ```k
    rule mapUpper(.IntSeq) => .IntSeq
  ```

- lines 160-160; kind `rule`; markers `none`

  ```k
    rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
  ```

- lines 162-162; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= mapSwap(IntSeq) [function, total]
  ```

- lines 163-163; kind `rule`; markers `none`

  ```k
    rule mapSwap(.IntSeq) => .IntSeq
  ```

- lines 164-164; kind `rule`; markers `none`

  ```k
    rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
  ```

- lines 166-166; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
  ```

- lines 167-167; kind `rule`; markers `none`

  ```k
    rule startsWith(.IntSeq, _:IntSeq)               => true
  ```

- lines 168-168; kind `rule`; markers `none`

  ```k
    rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```

- lines 169-169; kind `rule`; markers `none`

  ```k
    rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
  ```

- lines 170-170; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/operators.k`

Counts: context=2, endmodule=1, imports=2, module=1, rule=10

- lines 6-6; kind `module`; markers `none`

  ```k
  module MPY-OPERATORS
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 8-8; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 10-10; kind `rule`; markers `none`

  ```k
    rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
  ```

- lines 12-13; kind `rule`; markers `none`

  ```k
    rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
  ```

- lines 15-15; kind `context`; markers `none`

  ```k
    context Compare(HOLE, _)
  ```

- lines 16-16; kind `context`; markers `none`

  ```k
    context Compare(_:Val, CmpOp(_, HOLE))
  ```

- lines 17-17; kind `rule`; markers `owise`

  ```k
    rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
  ```

- lines 19-19; kind `rule`; markers `none`

  ```k
    rule applyCmp("is",     V:Val, noneV) => V ==K noneV
  ```

- lines 20-21; kind `rule`; markers `none`

  ```k
    rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
  ```

- lines 25-27; kind `rule`; markers `priority`

  ```k
    rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 28-32; kind `rule`; markers `priority`

  ```k
    rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(L)
         [priority(40)]
  ```

- lines 34-37; kind `rule`; markers `priority`

  ```k
    rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires OP =/=String "in" andBool OP =/=String "not in"
         [priority(40)]
  ```

- lines 38-42; kind `rule`; markers `priority`

  ```k
    rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(L)
          orBool OP ==String "in" orBool OP ==String "not in"
         [priority(40)]
  ```

- lines 44-46; kind `rule`; markers `priority`

  ```k
    rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 47-47; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/range.k`

Counts: endmodule=1, imports=2, module=1, rule=6, syntax=2

- lines 5-5; kind `module`; markers `none`

  ```k
  module MPY-RANGE
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 9-9; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= inRange(Int, Int, Int) [function, total]
  ```

- lines 10-10; kind `rule`; markers `none`

  ```k
    rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
  ```

- lines 12-12; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= rangeLen(Int, Int, Int) [function]
  ```

- lines 13-14; kind `rule`; markers `none`

  ```k
    rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
         requires ST >Int 0 andBool HI >Int LO
  ```

- lines 15-16; kind `rule`; markers `none`

  ```k
    rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
         requires ST <Int 0 andBool HI <Int LO
  ```

- lines 17-18; kind `rule`; markers `none`

  ```k
    rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
         requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
  ```

- lines 20-22; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
          => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
         requires inRange(I, HI, ST)
  ```

- lines 23-24; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
         requires notBool inRange(I, HI, ST)
  ```

- lines 25-25; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/set.k`

Counts: endmodule=1, imports=1, module=1, rule=12, syntax=6

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-SET
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 8-9; kind `syntax`; markers `none`

  ```k
    syntax Val ::= setV(IntSeq)
  ```

- lines 11-11; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= codeIn(Int, IntSeq) [function, total]
  ```

- lines 12-12; kind `rule`; markers `none`

  ```k
    rule codeIn(_:Int, .IntSeq)                => false
  ```

- lines 13-14; kind `rule`; markers `none`

  ```k
    rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
  ```

- lines 16-17; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                    | dedupFrom(IntSeq, IntSeq)  [function, total]
  ```

- lines 18-18; kind `rule`; markers `none`

  ```k
    rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
  ```

- lines 19-19; kind `rule`; markers `none`

  ```k
    rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
  ```

- lines 20-21; kind `rule`; markers `none`

  ```k
    rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
         requires codeIn(C, ACC)
  ```

- lines 22-23; kind `rule`; markers `none`

  ```k
    rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
         requires notBool codeIn(C, ACC)
  ```

- lines 25-25; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
  ```

- lines 26-26; kind `rule`; markers `none`

  ```k
    rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
  ```

- lines 27-28; kind `rule`; markers `none`

  ```k
    rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
  ```

- lines 31-31; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
  ```

- lines 32-32; kind `rule`; markers `none`

  ```k
    rule subsetCodes(.IntSeq, _:IntSeq)                => true
  ```

- lines 33-33; kind `rule`; markers `none`

  ```k
    rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
  ```

- lines 35-35; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
  ```

- lines 36-37; kind `rule`; markers `none`

  ```k
    rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
  ```

- lines 39-39; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
  ```

- lines 40-40; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/sort.k`

Counts: endmodule=1, imports=2, module=1, rule=19, syntax=6

- lines 10-10; kind `module`; markers `none`

  ```k
  module MPY-SORT
  ```

- lines 11-11; kind `imports`; markers `none`

  ```k
    imports MPY-BUILTINS
  ```

- lines 12-12; kind `imports`; markers `none`

  ```k
    imports MPY-SUBSCRIPT
  ```

- lines 18-18; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
  ```

- lines 19-19; kind `syntax:function`; markers `function`

  ```k
    syntax ValSeq ::= insVS(Int, ValSeq) [function]
  ```

- lines 20-20; kind `rule`; markers `concrete`

  ```k
    rule sortVS(.ValSeq)                => .ValSeq          [concrete]
  ```

- lines 21-21; kind `rule`; markers `concrete`

  ```k
    rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
  ```

- lines 22-22; kind `rule`; markers `concrete`

  ```k
    rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
  ```

- lines 23-23; kind `rule`; markers `concrete`

  ```k
    rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
  ```

- lines 24-24; kind `rule`; markers `concrete`

  ```k
    rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  ```

- lines 26-26; kind `syntax:function`; markers `function`

  ```k
    syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
  ```

- lines 27-27; kind `rule`; markers `concrete`

  ```k
    rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
  ```

- lines 28-28; kind `rule`; markers `concrete`

  ```k
    rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
  ```

- lines 29-30; kind `rule`; markers `concrete`

  ```k
    rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
         requires strLt(A, B) orBool A ==K B [concrete]
  ```

- lines 31-33; kind `rule`; markers `concrete`

  ```k
    rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
         requires notBool (strLt(A, B) orBool A ==K B) [concrete]
  ```

- lines 36-38; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
          => #alloc(list(sortVS(VS))) ... </k>
  ```

- lines 40-43; kind `rule`; markers `priority`

  ```k
    rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
         <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
         [priority(40)]
  ```

- lines 49-49; kind `syntax:function,total,symbol,no-evaluators`; markers `function,total,symbol,no-evaluators`

  ```k
    syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
  ```

- lines 51-52; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= revVS(ValSeq) [function, total]
                    | revVSAcc(ValSeq, ValSeq) [function, total]
  ```

- lines 53-53; kind `rule`; markers `none`

  ```k
    rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
  ```

- lines 54-54; kind `rule`; markers `none`

  ```k
    rule revVSAcc(.ValSeq, A:ValSeq) => A
  ```

- lines 55-55; kind `rule`; markers `none`

  ```k
    rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
  ```

- lines 57-57; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
  ```

- lines 58-58; kind `rule`; markers `none`

  ```k
    rule condRev(S:ValSeq, false) => S
  ```

- lines 59-59; kind `rule`; markers `none`

  ```k
    rule condRev(S:ValSeq, true)  => revVS(S)
  ```

- lines 61-62; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
          => #alloc(list(sortKeyVS(VS, KV))) ... </k>
  ```

- lines 63-64; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
          => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
  ```

- lines 65-67; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
          => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
  ```

- lines 72-72; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/str.k`

Counts: endmodule=1, imports=2, module=1, rule=28, syntax=5

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-STR
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 8-8; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
  ```

- lines 9-11; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
          => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
  ```

- lines 13-13; kind `syntax:function`; markers `function`

  ```k
    syntax IntSeq ::= strToCodes(String) [function]
  ```

- lines 14-14; kind `rule`; markers `none`

  ```k
    rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
  ```

- lines 15-15; kind `rule`; markers `none`

  ```k
    rule strToCodes("") => .IntSeq
  ```

- lines 16-18; kind `rule`; markers `none`

  ```k
    rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
      requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
  ```

- lines 20-20; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
  ```

- lines 21-21; kind `rule`; markers `none`

  ```k
    rule seqConcat(.IntSeq, T:IntSeq)                => T
  ```

- lines 22-22; kind `rule`; markers `none`

  ```k
    rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
  ```

- lines 24-24; kind `rule`; markers `none`

  ```k
    rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
  ```

- lines 25-25; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
  ```

- lines 26-27; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
  ```

- lines 29-29; kind `rule`; markers `none`

  ```k
    rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
  ```

- lines 30-30; kind `rule`; markers `none`

  ```k
    rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
  ```

- lines 32-32; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
  ```

- lines 33-33; kind `rule`; markers `none`

  ```k
    rule strPrefix(.IntSeq, _:IntSeq)               => true
  ```

- lines 34-34; kind `rule`; markers `none`

  ```k
    rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```

- lines 35-35; kind `rule`; markers `none`

  ```k
    rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
  ```

- lines 37-37; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
  ```

- lines 38-38; kind `rule`; markers `none`

  ```k
    rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
  ```

- lines 39-39; kind `rule`; markers `none`

  ```k
    rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
  ```

- lines 40-42; kind `rule`; markers `none`

  ```k
    rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
         requires notBool strPrefix(P, iCons(C, Xs))
  ```

- lines 48-48; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
  ```

- lines 49-49; kind `rule`; markers `none`

  ```k
    rule strLt(.IntSeq, .IntSeq)                => false
  ```

- lines 50-50; kind `rule`; markers `none`

  ```k
    rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
  ```

- lines 51-51; kind `rule`; markers `none`

  ```k
    rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```

- lines 52-52; kind `rule`; markers `none`

  ```k
    rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
  ```

- lines 53-53; kind `rule`; markers `none`

  ```k
    rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
  ```

- lines 54-54; kind `rule`; markers `none`

  ```k
    rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
  ```

- lines 56-56; kind `rule`; markers `none`

  ```k
    rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
  ```

- lines 57-57; kind `rule`; markers `none`

  ```k
    rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
  ```

- lines 58-58; kind `rule`; markers `none`

  ```k
    rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
  ```

- lines 59-59; kind `rule`; markers `none`

  ```k
    rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
  ```

- lines 60-60; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/subscript.k`

Counts: context=2, endmodule=1, imports=1, module=1, rule=40, syntax=15

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-SUBSCRIPT
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 11-11; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
  ```

- lines 12-12; kind `rule`; markers `none`

  ```k
    rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
  ```

- lines 13-14; kind `rule`; markers `none`

  ```k
    rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
         requires I >Int 0
  ```

- lines 16-16; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= intSeqAt(IntSeq, Int) [function]
  ```

- lines 17-17; kind `rule`; markers `none`

  ```k
    rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
  ```

- lines 18-19; kind `rule`; markers `none`

  ```k
    rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
         requires I >Int 0
  ```

- lines 21-21; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= normIdx(Int, Int) [function, total]
  ```

- lines 22-22; kind `rule`; markers `none`

  ```k
    rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
  ```

- lines 23-24; kind `rule`; markers `none`

  ```k
    rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
  ```

- lines 27-27; kind `context`; markers `none`

  ```k
    context Subscript(HOLE, _)
  ```

- lines 28-29; kind `context`; markers `none`

  ```k
    context Subscript(_:Val, HOLE:Expr)
  ```

- lines 31-33; kind `rule`; markers `priority`

  ```k
    rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 35-35; kind `rule`; markers `none`

  ```k
    rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
  ```

- lines 37-37; kind `syntax:function`; markers `function`

  ```k
    syntax Val ::= applyIndex(Val, Int) [function]
  ```

- lines 38-38; kind `rule`; markers `none`

  ```k
    rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
  ```

- lines 39-39; kind `rule`; markers `none`

  ```k
    rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
  ```

- lines 40-42; kind `rule`; markers `none`

  ```k
    rule applyIndex(str(IS:IntSeq),   I:Int)
      => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
  ```

- lines 44-47; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #evalB(Bound) | "#toSome"
                   | #slLo(Val, Bound, Bound)
                   | #slHi(Val, OptInt, Bound)
                   | #slStep(Val, OptInt, OptInt)
  ```

- lines 49-49; kind `syntax`; markers `none`

  ```k
    syntax OptInt ::= "noB" | someB(Int)
  ```

- lines 50-50; kind `rule`; markers `none`

  ```k
    rule <k> #evalB(NoBound)  => noB ... </k>
  ```

- lines 51-51; kind `rule`; markers `none`

  ```k
    rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
  ```

- lines 52-52; kind `rule`; markers `none`

  ```k
    rule <k> I:Int ~> #toSome => someB(I) ... </k>
  ```

- lines 54-54; kind `rule`; markers `none`

  ```k
    rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
  ```

- lines 55-55; kind `rule`; markers `none`

  ```k
    rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
  ```

- lines 56-56; kind `rule`; markers `none`

  ```k
    rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  ```

- lines 58-60; kind `rule`; markers `priority`

  ```k
    rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
          => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
         [priority(45)]
  ```

- lines 61-61; kind `rule`; markers `none`

  ```k
    rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
  ```

- lines 63-63; kind `syntax:function`; markers `function`

  ```k
    syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
  ```

- lines 64-65; kind `rule`; markers `none`

  ```k
    rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
  ```

- lines 66-67; kind `rule`; markers `none`

  ```k
    rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
  ```

- lines 68-70; kind `rule`; markers `none`

  ```k
    rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
  ```

- lines 72-72; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= slStep(OptInt) [function, total]
  ```

- lines 73-73; kind `rule`; markers `none`

  ```k
    rule slStep(noB)          => 1
  ```

- lines 74-74; kind `rule`; markers `none`

  ```k
    rule slStep(someB(S:Int)) => S
  ```

- lines 76-76; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= slStart(OptInt, OptInt, Int) [function]
  ```

- lines 77-78; kind `rule`; markers `none`

  ```k
    rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
         requires slStep(ST) >Int 0
  ```

- lines 79-80; kind `rule`; markers `none`

  ```k
    rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
         requires slStep(ST) <Int 0
  ```

- lines 81-81; kind `rule`; markers `none`

  ```k
    rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
  ```

- lines 83-83; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= slStop(OptInt, OptInt, Int) [function]
  ```

- lines 84-85; kind `rule`; markers `none`

  ```k
    rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
         requires slStep(ST) >Int 0
  ```

- lines 86-87; kind `rule`; markers `none`

  ```k
    rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
         requires slStep(ST) <Int 0
  ```

- lines 88-88; kind `rule`; markers `none`

  ```k
    rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
  ```

- lines 90-90; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= slAdjust(Int, Int, Int) [function, total]
  ```

- lines 91-92; kind `rule`; markers `none`

  ```k
    rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
         requires I  <Int 0
  ```

- lines 93-94; kind `rule`; markers `none`

  ```k
    rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
         requires I >=Int 0
  ```

- lines 96-96; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= clampLo(Int, Int) [function, total]
  ```

- lines 97-98; kind `rule`; markers `none`

  ```k
    rule clampLo(J:Int, _STEP:Int) => J
         requires J >=Int 0
  ```

- lines 99-100; kind `rule`; markers `none`

  ```k
    rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
         requires J <Int 0
  ```

- lines 102-102; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Int ::= clampHi(Int, Int, Int) [function, total]
  ```

- lines 103-104; kind `rule`; markers `none`

  ```k
    rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
         requires I  <Int LEN
  ```

- lines 105-107; kind `rule`; markers `none`

  ```k
    rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
         requires I >=Int LEN
  ```

- lines 109-109; kind `syntax:function`; markers `function`

  ```k
    syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
  ```

- lines 110-112; kind `rule`; markers `none`

  ```k
    rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
      => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
         requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
  ```

- lines 113-114; kind `rule`; markers `none`

  ```k
    rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
         requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
  ```

- lines 116-116; kind `syntax:function`; markers `function`

  ```k
    syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
  ```

- lines 117-119; kind `rule`; markers `none`

  ```k
    rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
      => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
         requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
  ```

- lines 120-121; kind `rule`; markers `none`

  ```k
    rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
         requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
  ```

- lines 122-122; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/syntax.k`

Counts: endmodule=1, imports=4, module=1, syntax=16

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-SYNTAX
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports INT-SYNTAX
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports FLOAT-SYNTAX
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports BOOL-SYNTAX
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports STRING-SYNTAX
  ```

- lines 9-30; kind `syntax`; markers `macro`

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

- lines 32-32; kind `syntax`; markers `none`

  ```k
    syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
  ```

- lines 33-33; kind `syntax`; markers `none`

  ```k
    syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
  ```

- lines 34-34; kind `syntax`; markers `none`

  ```k
    syntax Entries  ::= List{Entry, ","}
  ```

- lines 35-35; kind `syntax`; markers `none`

  ```k
    syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  ```

- lines 36-36; kind `syntax`; markers `none`

  ```k
    syntax CompFors ::= List{CompFor, ""}
  ```

- lines 37-37; kind `syntax`; markers `none`

  ```k
    syntax Exprs    ::= List{Expr, ","}
  ```

- lines 38-38; kind `syntax`; markers `none`

  ```k
    syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
  ```

- lines 39-39; kind `syntax`; markers `none`

  ```k
    syntax Bound    ::= Expr | "NoBound"
  ```

- lines 41-54; kind `syntax`; markers `none`

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

- lines 56-56; kind `syntax`; markers `none`

  ```k
    syntax Stmts      ::= List{Stmt, ""}
  ```

- lines 57-57; kind `syntax`; markers `none`

  ```k
    syntax Params     ::= "Params" "(" ParamNames ")"
  ```

- lines 58-58; kind `syntax`; markers `none`

  ```k
    syntax CellVars   ::= "CellVars" "(" ParamNames ")"
  ```

- lines 59-59; kind `syntax`; markers `none`

  ```k
    syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
  ```

- lines 60-60; kind `syntax`; markers `none`

  ```k
    syntax ParamNames ::= List{String, ","}
  ```

- lines 61-61; kind `syntax`; markers `none`

  ```k
    syntax Module     ::= "Module" "(" Stmts ")"
  ```

- lines 62-62; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `semantics/tuple.k`

Counts: endmodule=1, imports=4, module=1, rule=21, syntax=4

- lines 3-3; kind `module`; markers `none`

  ```k
  module MPY-TUPLE
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY-CORE
  ```

- lines 5-5; kind `imports`; markers `none`

  ```k
    imports MPY-ITER
  ```

- lines 6-6; kind `imports`; markers `none`

  ```k
    imports MPY-LIST
  ```

- lines 7-7; kind `imports`; markers `none`

  ```k
    imports MPY-METHODS
  ```

- lines 10-10; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
  ```

- lines 11-12; kind `rule`; markers `none`

  ```k
    rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
  ```

- lines 14-14; kind `syntax`; markers `none`

  ```k
    syntax ApplyK ::= "toTuple"
  ```

- lines 15-15; kind `rule`; markers `none`

  ```k
    rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
  ```

- lines 16-16; kind `rule`; markers `none`

  ```k
    rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
  ```

- lines 18-18; kind `rule`; markers `none`

  ```k
    rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  ```

- lines 20-20; kind `rule`; markers `none`

  ```k
    rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
  ```

- lines 21-21; kind `rule`; markers `none`

  ```k
    rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  ```

- lines 23-23; kind `rule`; markers `none`

  ```k
    rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
  ```

- lines 24-24; kind `syntax:function`; markers `function`

  ```k
    syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
  ```

- lines 25-25; kind `rule`; markers `none`

  ```k
    rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
  ```

- lines 26-27; kind `rule`; markers `none`

  ```k
    rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
         requires notBool (A ==K V)
  ```

- lines 28-29; kind `rule`; markers `none`

  ```k
    rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
  ```

- lines 31-31; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #bindTgt(Expr, Val)
  ```

- lines 32-34; kind `rule`; markers `none`

  ```k
    rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
  ```

- lines 35-41; kind `rule`; markers `priority`

  ```k
    rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires "$cells" in_keys(M)
          andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
          andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
         [priority(40)]
  ```

- lines 42-42; kind `rule`; markers `none`

  ```k
    rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
  ```

- lines 43-43; kind `rule`; markers `none`

  ```k
    rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
  ```

- lines 44-47; kind `rule`; markers `priority`

  ```k
    rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 49-49; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= #unpackSeq(Exprs, ValSeq)
  ```

- lines 50-50; kind `rule`; markers `none`

  ```k
    rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
  ```

- lines 51-51; kind `rule`; markers `none`

  ```k
    rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
  ```

- lines 52-54; kind `rule`; markers `priority`

  ```k
    rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- lines 55-56; kind `rule`; markers `none`

  ```k
    rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
          => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
  ```

- lines 57-57; kind `rule`; markers `none`

  ```k
    rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
  ```

- lines 58-58; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## `verification.k`

Counts: endmodule=1, imports=1, module=1, requires=1, rule=9, syntax=6

- lines 1-1; kind `requires`; markers `none`

  ```k
  requires "reference-semantics/semantics.k"
  ```

- lines 3-3; kind `module`; markers `none`

  ```k
  module ORDER-BY-POINTS-VERIFICATION
  ```

- lines 4-4; kind `imports`; markers `none`

  ```k
    imports MPY
  ```

- lines 6-6; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Stmts ::= "digitSumBody" [function, total]
  ```

- lines 7-25; kind `rule`; markers `total`

  ```k
    rule digitSumBody =>
      Assign(Name("negative"), Compare(Name("n"), CmpOp("<", Int(0))))
      Assign(Name("n"), Call(Name("abs"), (Name("n"), .Exprs)))
      Assign(Name("total"), Int(0))
      Assign(Name("most_significant"), Int(0))
      While(Name("n"),
        Assign(Name("most_significant"), BinOp("%", Name("n"), Int(10)))
        AugAssign(Name("total"), "+", Name("most_significant"))
        AugAssign(Name("n"), "//", Int(10))
        .Stmts)
      If(Name("negative"),
        AugAssign(
          Name("total"),
          "-",
          BinOp("*", Int(2), Name("most_significant")))
        .Stmts,
        .Stmts)
      Return(Name("total"))
      .Stmts
  ```

- lines 27-27; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Stmts ::= "orderByPointsBody" [function, total]
  ```

- lines 28-35; kind `rule`; markers `none`

  ```k
    rule orderByPointsBody =>
      Return(
        Call(
          Name("sorted"),
          (Name("nums"),
           KwArg("key", Name("digit_sum")),
           .Exprs)))
      .Stmts
  ```

- lines 37-38; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Val ::= "digitSumClosure" [function, total]
                 | "orderByPointsClosure" [function, total]
  ```

- lines 39-40; kind `rule`; markers `none`

  ```k
    rule digitSumClosure =>
      closureVal(("n", .ParamNames), digitSumBody, 0)
  ```

- lines 41-42; kind `rule`; markers `none`

  ```k
    rule orderByPointsClosure =>
      closureVal(("nums", .ParamNames), orderByPointsBody, 0)
  ```

- lines 44-44; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Module ::= "solutionModule" [function, total]
  ```

- lines 45-52; kind `rule`; markers `none`

  ```k
    rule solutionModule =>
      Module(
        FuncDef("digit_sum", Params(("n", .ParamNames)), digitSumBody)
        FuncDef(
          "order_by_points",
          Params(("nums", .ParamNames)),
          orderByPointsBody)
        .Stmts)
  ```

- lines 54-55; kind `syntax:function,total`; markers `function,total`

  ```k
    syntax Map ::= "initialScopes" [function, total]
                 | "loadedScopes" [function, total]
  ```

- lines 56-58; kind `rule`; markers `none`

  ```k
    rule initialScopes =>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
  ```

- lines 59-65; kind `rule`; markers `none`

  ```k
    rule loadedScopes =>
      (0 |-> scope(
        .Map
          [ "digit_sum" <- digitSumClosure ]
          [ "order_by_points" <- orderByPointsClosure ],
        parent(-1)))
      (-1 |-> builtinsScope)
  ```

- lines 67-68; kind `syntax`; markers `none`

  ```k
    syntax KItem ::= "#runDigitSum" "(" Int ")"
                   | "#runOrderByPoints" "(" Val ")"
  ```

- lines 69-72; kind `rule`; markers `none`

  ```k
    rule <k> #runDigitSum(N:Int)
          => #loadAll(solutionModule)
          ~> Call(Name("digit_sum"), (N, .Exprs))
          ... </k>
  ```

- lines 73-76; kind `rule`; markers `none`

  ```k
    rule <k> #runOrderByPoints(V:Val)
          => #loadAll(solutionModule)
          ~> Call(Name("order_by_points"), (V, .Exprs))
          ... </k>
  ```

- lines 77-77; kind `endmodule`; markers `none`

  ```k
  endmodule
  ```

## Overall counts

- configuration: 1
- context: 5
- endmodule: 26
- imports: 87
- module: 26
- requires: 24
- rule: 704
- syntax: 233

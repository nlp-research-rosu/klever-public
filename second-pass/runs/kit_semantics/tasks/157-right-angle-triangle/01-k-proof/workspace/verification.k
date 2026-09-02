requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact translated body of solution.py, named only to keep the eight
  // Int/Float sort-combination claims identical at the call boundary.
  syntax Val ::= rightAngleTriangleClosure() [function, total]
  rule rightAngleTriangleClosure()
    => closureVal(
         ("a", "b", "c"),
         Return(
           BoolOp(
             "or",
             Compare(
               BinOp("*", Name("a"), Name("a")),
               CmpOp(
                 "==",
                 BinOp(
                   "+",
                   BinOp("*", Name("b"), Name("b")),
                   BinOp("*", Name("c"), Name("c"))
                 )
               )
             ),
             Compare(
               BinOp("*", Name("b"), Name("b")),
               CmpOp(
                 "==",
                 BinOp(
                   "+",
                   BinOp("*", Name("a"), Name("a")),
                   BinOp("*", Name("c"), Name("c"))
                 )
               )
             ),
             Compare(
               BinOp("*", Name("c"), Name("c")),
               CmpOp(
                 "==",
                 BinOp(
                   "+",
                   BinOp("*", Name("a"), Name("a")),
                   BinOp("*", Name("b"), Name("b"))
                 )
               )
             )
           )
         ),
         0
       )

  // MPY's Float equality delegates to the FLOAT.eq hook, which the LLVM
  // backend implements but the Haskell backend does not.  This symbol is the
  // explicit trusted primitive for that fixed external operation.
  syntax Bool ::= trustedFloatEq(Float, Float)
    [function, total, symbol(trustedFloatEq), no-evaluators]
  rule trustedFloatEq(F1:Float, F2:Float)
    => F1 ==Float F2
    [concrete]

  // Arguments are already evaluated Float values here.  Equality is pure:
  // it reads no cells and returns one Bool into the same continuation.
  rule <k>
         Compare(F1:Float, CmpOp("==", F2:Float))
         =>
         trustedFloatEq(F1, F2)
         ...
       </k>
       [priority(40)]

  // Mathematical description of the exact numeric operations used by the
  // candidate.  These functions occur only in postconditions.
  syntax Val ::= ratSquare(Val) [function]
               | ratAdd(Val, Val) [function]
  syntax Bool ::= ratEq(Val, Val) [function]
                | ratExpected(Val, Val, Val) [function]

  rule ratSquare(I:Int)   => I *Int I
  rule ratSquare(F:Float) => mulF(F, F)

  rule ratAdd(I1:Int,   I2:Int)   => I1 +Int I2
  rule ratAdd(F1:Float, F2:Float) => addF(F1, F2)
  rule ratAdd(I:Int,    F:Float)  => addF(intToF(I), F)
  rule ratAdd(F:Float,  I:Int)    => addF(F, intToF(I))

  rule ratEq(I1:Int,   I2:Int)   => I1 ==Int I2
  rule ratEq(F1:Float, F2:Float) => trustedFloatEq(F1, F2)
  rule ratEq(I:Int,    F:Float)  => eqIF(I, F)
  rule ratEq(F:Float,  I:Int)    => eqIF(I, F)

  rule ratExpected(A:Val, B:Val, C:Val)
    => ratEq(ratSquare(A), ratAdd(ratSquare(B), ratSquare(C)))
       orBool ratEq(ratSquare(B), ratAdd(ratSquare(A), ratSquare(C)))
       orBool ratEq(ratSquare(C), ratAdd(ratSquare(A), ratSquare(B)))
endmodule

requires "reference-semantics/semantics.k"

module CHOOSE-NUM-VERIFICATION
  imports MPY

  // This is the exact function body emitted in solution.mpy, packaged as a
  // callable closure so that claims can supply symbolic integer arguments.
  syntax KItem ::= "#chooseNum" "(" Int "," Int ")"

  // Mathematical contract: remove the parity remainder from Y to obtain the
  // greatest even integer at or below it, then test interval membership.
  syntax Int ::= largestEvenInRange(Int, Int) [function, total]
  rule largestEvenInRange(X:Int, Y:Int)
    => #if X <=Int Y -Int pyMod(Y, 2)
       #then Y -Int pyMod(Y, 2)
       #else -1
       #fi

  rule <k> #chooseNum(X:Int, Y:Int)
        => Call(
             closureVal(
               ("x", "y"),
               If(
                 Compare(BinOp("%", Name("y"), Int(2)), CmpOp("==", Int(0))),
                 If(
                   Compare(Name("y"), CmpOp(">=", Name("x"))),
                   Return(Name("y")),
                   .Stmts)
                 Return(UnaryOp("-", Int(1))),
                 .Stmts)
               If(
                 Compare(
                   BinOp("-", Name("y"), Int(1)),
                   CmpOp(">=", Name("x"))),
                 Return(BinOp("-", Name("y"), Int(1))),
                 .Stmts)
               Return(UnaryOp("-", Int(1))),
               0),
             X, Y)
        ... </k>
endmodule

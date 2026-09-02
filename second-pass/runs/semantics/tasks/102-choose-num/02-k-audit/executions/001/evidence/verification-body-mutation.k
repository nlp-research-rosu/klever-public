requires "reference-semantics/semantics.k"

module CHOOSE-NUM-VERIFICATION-BODY-MUTATION
  imports MPY

  syntax KItem ::= "#chooseNumBodyMutation" "(" Int "," Int ")"
  syntax Int ::= largestEvenBodyMutation(Int, Int) [function, total]
  rule largestEvenBodyMutation(X:Int, Y:Int)
    => #if X <=Int Y -Int pyMod(Y, 2)
       #then Y -Int pyMod(Y, 2)
       #else -1
       #fi

  // Reviewer mutation: only the even/in-range return is changed from y to y+2.
  rule <k> #chooseNumBodyMutation(X:Int, Y:Int)
        => Call(
             closureVal(
               ("x", "y"),
               If(
                 Compare(BinOp("%", Name("y"), Int(2)), CmpOp("==", Int(0))),
                 If(
                   Compare(Name("y"), CmpOp(">=", Name("x"))),
                   Return(BinOp("+", Name("y"), Int(2))),
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

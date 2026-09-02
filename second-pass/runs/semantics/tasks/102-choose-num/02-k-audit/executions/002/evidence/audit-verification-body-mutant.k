requires "reference-semantics/semantics.k"

module AUDIT-BODY-MUTANT
  imports MPY

  syntax KItem ::= "#chooseNumMutant" "(" Int "," Int ")"

  syntax Int ::= largestEvenInRangeMutant(Int, Int) [function, total]
  rule largestEvenInRangeMutant(X:Int, Y:Int)
    => #if X <=Int Y -Int pyMod(Y, 2)
       #then Y -Int pyMod(Y, 2)
       #else -1
       #fi

  // Material body mutation: the even/in-range branch returns Y - 2, not Y.
  rule <k> #chooseNumMutant(X:Int, Y:Int)
        => Call(
             closureVal(
               ("x", "y"),
               If(
                 Compare(BinOp("%", Name("y"), Int(2)), CmpOp("==", Int(0))),
                 If(
                   Compare(Name("y"), CmpOp(">=", Name("x"))),
                   Return(BinOp("-", Name("y"), Int(2))),
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

requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  syntax KItem ::= "#invokeStartsOneEnds" "(" Int ")"
  syntax Stmts ::= "startsOneEndsBody" [function]

  rule startsOneEndsBody
    => Expr(Str("\n    Given a positive integer n, return the count of the numbers of n-digit\n    positive integers that start or end with 1.\n    "))
       If(Compare(Name("n"), CmpOp("==", Int(1))),
          Return(Int(1)),
          .Stmts)
       Return(BinOp("*", Int(18),
                    BinOp("**", Int(10), BinOp("-", Name("n"), Int(2)))))
       .Stmts

  rule <k> #invokeStartsOneEnds(N:Int)
         => Call(Name("starts_one_ends"), Int(N)) ... </k>
endmodule

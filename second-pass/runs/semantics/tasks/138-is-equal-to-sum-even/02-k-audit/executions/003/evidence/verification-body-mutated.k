requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTATED
  imports MPY

  syntax KItem ::= "#isEqualToSumEven" "(" Int ")"

  // Auditor mutation: threshold 8 is materially changed to 10 in the body
  // actually called by the claim. The original postcondition is unchanged.
  rule <k> #isEqualToSumEven(N:Int)
        => Call(
             closureVal(
               ("n", .ParamNames),
               (Return(
                  BoolOp(
                    "and",
                    ( Compare(Name("n"), CmpOp(">=", Int(10)))
                    , Compare(
                        BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0)))
                    , .Exprs)))
                .Stmts),
               0),
             (N, .Exprs))
           ... </k>
endmodule

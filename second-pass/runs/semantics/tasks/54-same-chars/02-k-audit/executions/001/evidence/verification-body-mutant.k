requires "reference-semantics/semantics.k"

module SAME-CHARS-VERIFICATION
  imports MPY

  // This closure is the constructor-level form of solution.mpy.  Calling it
  // directly keeps the module scope unchanged across a proof claim.
  syntax KItem ::= "#sameChars" "(" IntSeq "," IntSeq ")"

  rule <k> #sameChars(S0:IntSeq, S1:IntSeq)
        => Call(
             closureVal(
               ("s0", "s1", .ParamNames),
               (Return(
                  Compare(
                    Call(Name("set"), (Name("s0"), .Exprs)),
                    CmpOp("==",
                      Call(Name("set"), (Name("s0"), .Exprs)))))
                .Stmts),
               0),
             (str(S0), str(S1), .Exprs))
           ...
       </k>
endmodule

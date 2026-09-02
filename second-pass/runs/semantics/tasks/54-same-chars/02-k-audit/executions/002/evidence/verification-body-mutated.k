requires "reference-semantics/semantics.k"

module SAME-CHARS-BODY-MUTATED
  imports MPY

  syntax KItem ::= "#sameCharsBodyMut" "(" IntSeq "," IntSeq ")"

  // Deliberately false source-body mutation: compare set(s0) with itself.
  rule <k> #sameCharsBodyMut(S0:IntSeq, S1:IntSeq)
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

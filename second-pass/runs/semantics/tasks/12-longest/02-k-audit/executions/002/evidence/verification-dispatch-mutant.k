requires "verification.k"

module VERIFICATION-DISPATCH-MUTANT
  imports VERIFICATION

  // Deliberately wrong implementation: it executes the submitted loop but
  // discards the accumulator and always returns None.
  syntax Val ::= "longestMutant" [macro]
  rule longestMutant
    => closureVal("strings",
         Assign(Name("result"), NoneVal)
         Assign(Name("string"), NoneVal)
         For(Name("string"), Name("strings"),
           If(Compare(Name("result"), CmpOp("is", NoneVal)),
             Assign(Name("result"), Name("string")),
             If(Compare(
               Call(Name("len"), Name("string")),
               CmpOp("<=", Call(Name("len"), Name("result")))),
               Assign(Name("result"), Name("result")),
               If(Compare(
                 Call(Name("len"), Name("string")),
                 CmpOp(">", Call(Name("len"), Name("result")))),
                 Assign(Name("result"), Name("string")),
                 .Stmts))))
         Return(NoneVal),
         0)
endmodule

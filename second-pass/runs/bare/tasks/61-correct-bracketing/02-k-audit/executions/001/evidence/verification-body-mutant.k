requires "verification.k"

module MPY-VERIFICATION-BODY-MUTANT
  imports MPY-VERIFICATION

  // Reviewer body-sensitivity mutation: initialize count to one.
  syntax Pgm ::= "mutatedSolutionProgram" [function, total]
  rule mutatedSolutionProgram =>
    Module(
      FuncDef("correct_bracketing", Params("brackets"),
        Assign(Name("count"), Int(1))
        For(Name("bracket"), Name("brackets"),
          If(Compare(Name("bracket"), CmpOp("==", Str("("))),
            Assign(Name("count"),
              BinOp("+", Name("count"), Int(1))),
            If(Compare(Name("count"), CmpOp("==", Int(0))),
              Return(Bool(false)),
              .Stmts)
            Assign(Name("count"),
              BinOp("-", Name("count"), Int(1)))))
        Return(Compare(Name("count"), CmpOp("==", Int(0))))))
endmodule

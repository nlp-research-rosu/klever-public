requires "semantic.k"

module BODY-MUTANT-VERIFICATION
  imports MPY

  // Reviewer mutation: the positive branch subtracts half instead of adding it.
  syntax Program ::= "bodyMutantProgram" [function]
  rule bodyMutantProgram =>
    Module(
      ImportFrom("decimal", "Decimal")
      FuncDef("closest_integer", Params("value"),
        Assign(Name("number"), Call(Name("Decimal"), Name("value")))
        Assign(Name("half"), Call(Name("Decimal"), Str("0.5")))
        If(Compare(Name("number"), CmpOp(">=", Int(0))),
          Return(Call(Name("int"),
                      BinOp("-", Name("number"), Name("half")))),
          .Stmts)
        Return(Call(Name("int"),
                    BinOp("-", Name("number"), Name("half"))))))
endmodule

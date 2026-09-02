requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  // The right-hand side is the submitted, trusted-translator-regenerated
  // solution.mpy term. Closure shows that the inline program constant used by
  // every target claim expands to that exact parsed constructor term.
  claim
    <k> solutionProgram =>
      Module(
        ImportFrom("decimal", "Decimal")
        FuncDef("closest_integer", Params("value"),
          Assign(Name("number"), Call(Name("Decimal"), Name("value")))
          Assign(Name("half"), Call(Name("Decimal"), Str("0.5")))
          If(Compare(Name("number"), CmpOp(">=", Int(0))),
            Return(
              Call(Name("int"), BinOp("+", Name("number"), Name("half")))),
            .Stmts)
          Return(Call(Name("int"),
                      BinOp("-", Name("number"), Name("half"))))))
    </k>
    <arg> V:Value </arg>
    <env> ENV:Map </env>
    <result> R:Result </result>
endmodule

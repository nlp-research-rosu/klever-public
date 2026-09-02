requires "semantic.k"

module VERIFICATION
  imports MPY

  // The exact AST emitted in solution.mpy.  Keeping it as a function makes
  // each claim execute the translated program while avoiding repetition.
  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      ImportFrom("decimal", "Decimal")
      FuncDef("closest_integer", Params("value"),
        Assign(Name("number"), Call(Name("Decimal"), Name("value")))
        Assign(Name("half"), Call(Name("Decimal"), Str("0.5")))
        If(Compare(Name("number"), CmpOp(">=", Int(0))),
          Return(Call(Name("int"),
                      BinOp("+", Name("number"), Name("half")))),
          .Stmts)
        Return(Call(Name("int"),
                    BinOp("-", Name("number"), Name("half"))))))

  // Mathematical reference: add a half in the direction away from zero,
  // then truncate toward zero.  N/D denotes an exact number and D is positive.
  syntax Int ::= roundNearestAway(Int, Int) [function]
  rule roundNearestAway(N, D) =>
    ((N *Int 10) +Int (5 *Int D)) /Int (D *Int 10)
    requires N >=Int 0 andBool D >Int 0
  rule roundNearestAway(N, D) =>
    ((N *Int 10) -Int (5 *Int D)) /Int (D *Int 10)
    requires N <Int 0 andBool D >Int 0
endmodule

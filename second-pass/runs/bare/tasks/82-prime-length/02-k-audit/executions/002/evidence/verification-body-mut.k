requires "semantic.k"

module VERIFICATION-BODY-MUT
  imports SEMANTIC

  // Auditor mutation: the actually executed program term uses n >= 3.
  syntax Program ::= "mutatedSolutionProgram" [macro]
  rule mutatedSolutionProgram =>
    Module(
      FuncDef("prime_length", Params("string"), CellVars("n"), FreeVars(.Strings),
        Assign(Name("n"), Call(Name("len"), Name("string")))
        Return(
          BoolOp(
            "and",
            Compare(Name("n"), CmpOp(">=", Int(3))),
            Call(
              Name("all"),
              GenExp(
                Compare(
                  BinOp("%", Name("n"), Name("i")),
                  CmpOp("!=", Int(0))),
                CompFor(
                  Name("i"),
                  Call(Name("range"), Int(2), Name("n")),
                  Bool(true))))))))

  syntax Bool ::= isPrimeMutTarget(Int) [function, total]
  rule isPrimeMutTarget(N) => (N >=Int 2 andBool noDivisors(N, 2, N))
endmodule

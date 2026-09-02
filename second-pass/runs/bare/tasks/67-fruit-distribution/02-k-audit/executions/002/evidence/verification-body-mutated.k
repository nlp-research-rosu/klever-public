requires "semantic.k"

module VERIFICATION-BODY-MUTATED
  imports MPY-SEMANTIC

  // Reviewer mutation: the second subscript is 0 instead of 3, so the
  // executed body subtracts the apple count twice.
  syntax Program ::= "solutionProgramMutated" [macro]
  rule solutionProgramMutated =>
    Module(
      FuncDef("fruit_distribution", Params("s", "n"),
        Assign(Name("words"), Call(Attribute(Name("s"), "split"), ))
        Return(
          BinOp(
            "-",
            BinOp(
              "-",
              Name("n"),
              Call(Name("int"), Subscript(Name("words"), Int(0)))),
            Call(Name("int"), Subscript(Name("words"), Int(0)))))))
endmodule

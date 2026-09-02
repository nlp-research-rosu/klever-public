requires "semantic.k"

module VERIFICATION-BODY-MUT
  imports MPY-SEMANTIC

  // Reviewer mutation of the executed program body: subtract words[0] twice.
  syntax Program ::= "solutionProgramMut" [macro]
  rule solutionProgramMut =>
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

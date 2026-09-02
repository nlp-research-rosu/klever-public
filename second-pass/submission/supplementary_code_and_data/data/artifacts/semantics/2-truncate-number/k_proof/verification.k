requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The translated solution, named so every proof claim executes precisely
  // the program represented by solution.mpy.
  syntax Module ::= "solutionProgram" [macro]
  rule solutionProgram
    => Module(
         FuncDef("truncate_number", Params("number"),
           Return(BinOp("%", Name("number"), Float(1.0)))))
endmodule

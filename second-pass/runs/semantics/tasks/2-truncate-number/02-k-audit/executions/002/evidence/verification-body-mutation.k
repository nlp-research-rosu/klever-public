requires "reference-semantics/semantics.k"

module AUDITOR-VERIFICATION-BODY-MUTATION
  imports MPY

  // Material body mutation: execute addition instead of modulo.
  syntax Module ::= "mutatedSolutionProgram" [macro]
  rule mutatedSolutionProgram
    => Module(
         FuncDef("truncate_number", Params("number"),
           Return(BinOp("+", Name("number"), Float(1.0)))))
endmodule

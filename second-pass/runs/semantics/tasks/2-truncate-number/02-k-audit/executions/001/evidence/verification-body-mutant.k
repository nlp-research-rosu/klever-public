requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Module ::= "solutionProgram" [macro]
  rule solutionProgram
    => Module(
         FuncDef("truncate_number", Params("number"),
           Return(Float(0.0))))
endmodule

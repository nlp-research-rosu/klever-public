requires "semantic.k"

module VERIFICATION-BODY-MUTANT
  imports SEMANTIC

  // Reviewer mutation: the executed function body now returns None.
  syntax Stmts ::= "solutionBodyMutant" [function]
  rule solutionBodyMutant => Return(NoneVal) .Stmts

  syntax Program ::= "solutionProgramMutant" [function]
  rule solutionProgramMutant =>
    Module(
      Import("hashlib")
      FuncDef("string_to_md5", Params("text"), solutionBodyMutant))
endmodule

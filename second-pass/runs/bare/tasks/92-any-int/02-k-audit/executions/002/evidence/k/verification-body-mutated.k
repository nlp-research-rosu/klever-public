requires "semantic.k"

module ANY-INT-VERIFICATION-BODY-MUTATED
  imports MPY-SEMANTICS

  // Reviewer mutation: the executed function body now returns False.
  syntax Program ::= "solutionProgramBodyMutated" [macro]
  rule solutionProgramBodyMutated =>
    Module(
      FuncDef("any_int", Params("x", "y", "z"),
        Return(Bool(false))))

  syntax KItem ::= "RunAnyIntBodyMutated" "(" Val "," Val "," Val ")" [macro]
  rule RunAnyIntBodyMutated(X, Y, Z)
    => Invoke(solutionProgramBodyMutated, X, Y, Z)
endmodule

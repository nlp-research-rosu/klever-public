requires "semantic.k"

module MPY-VERIFICATION-BODY-MUTATION
  imports MPY-SEMANTICS

  // Material body mutation: the call reads unbound "x" instead of parameter "l".
  syntax Program ::= "solutionProgramBodyMutation" [function, total]
  rule solutionProgramBodyMutation =>
    Module(
      FuncDef("max_element", Params("l"),
        Return(Call(Name("max"), Name("x")))))

  syntax Int ::= expectedMaximumBodyMutation(IntSeq) [function, total]
  rule expectedMaximumBodyMutation(IS) => maxInts(IS)
endmodule

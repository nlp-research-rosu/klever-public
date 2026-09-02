requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTICS

  // Auditor mutation: the executed program body returns l instead of max(l).
  syntax Program ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      FuncDef("max_element", Params("l"),
        Return(Name("l"))))

  syntax Int ::= expectedMaximum(IntSeq) [function, total]
  rule expectedMaximum(IS) => maxInts(IS)
endmodule

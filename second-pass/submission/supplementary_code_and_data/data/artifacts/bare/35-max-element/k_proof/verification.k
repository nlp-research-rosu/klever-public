requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTICS

  // This nullary function expands to the exact AST in solution.mpy.  Keeping
  // it here makes each reachability claim visibly about the translated code.
  syntax Program ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      FuncDef("max_element", Params("l"),
        Return(Call(Name("max"), Name("l")))))

  // The postcondition is stated at the contract level, independently of the
  // interpreter's result cell.  maxInts is the mathematical maximum defined
  // over the semantics' non-empty integer-list domain.
  syntax Int ::= expectedMaximum(IntSeq) [function, total]
  rule expectedMaximum(IS) => maxInts(IS)
endmodule

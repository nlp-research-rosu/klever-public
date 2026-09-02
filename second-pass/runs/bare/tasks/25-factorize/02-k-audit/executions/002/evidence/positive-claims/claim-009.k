requires "verification.k"

module SPEC-CLAIM-009
  imports VERIFICATION

  claim Run(SolutionMachine(31))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(31)))))
endmodule

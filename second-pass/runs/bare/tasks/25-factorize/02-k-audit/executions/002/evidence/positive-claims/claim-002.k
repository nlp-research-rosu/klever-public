requires "verification.k"

module SPEC-CLAIM-002
  imports VERIFICATION

  claim Run(SolutionMachine(2))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)))))
endmodule

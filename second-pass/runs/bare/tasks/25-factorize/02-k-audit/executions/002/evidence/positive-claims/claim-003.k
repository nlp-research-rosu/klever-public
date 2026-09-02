requires "verification.k"

module SPEC-CLAIM-003
  imports VERIFICATION

  claim Run(SolutionMachine(3))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(3)))))
endmodule

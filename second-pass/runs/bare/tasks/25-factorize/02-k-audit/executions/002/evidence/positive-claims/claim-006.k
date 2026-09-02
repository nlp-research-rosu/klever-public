requires "verification.k"

module SPEC-CLAIM-006
  imports VERIFICATION

  claim Run(SolutionMachine(9))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(3)) ListItem(IntVal(3)))))
endmodule

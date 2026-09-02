requires "verification.k"

module SPEC-CLAIM-008
  imports VERIFICATION

  claim Run(SolutionMachine(25))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(5)) ListItem(IntVal(5)))))
endmodule

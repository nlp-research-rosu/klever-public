requires "verification.k"

module SPEC-CLAIM-004
  imports VERIFICATION

  claim Run(SolutionMachine(4))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2)))))
endmodule

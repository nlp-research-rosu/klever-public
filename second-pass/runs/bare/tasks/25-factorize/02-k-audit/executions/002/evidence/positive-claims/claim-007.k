requires "verification.k"

module SPEC-CLAIM-007
  imports VERIFICATION

  claim Run(SolutionMachine(13))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(13)))))
endmodule

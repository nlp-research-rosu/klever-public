requires "verification.k"

module SPEC-CLAIM-005
  imports VERIFICATION

  claim Run(SolutionMachine(8))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2))
                 ListItem(IntVal(2)))))
endmodule

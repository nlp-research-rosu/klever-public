requires "verification.k"

module SPEC-CLAIM-010
  imports VERIFICATION

  claim Run(SolutionMachine(70))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(5))
                 ListItem(IntVal(7)))))
endmodule

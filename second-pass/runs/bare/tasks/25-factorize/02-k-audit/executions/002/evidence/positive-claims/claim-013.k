requires "verification.k"

module SPEC-CLAIM-013
  imports VERIFICATION

  claim Run(SolutionMachine(999))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(3)) ListItem(IntVal(3))
                 ListItem(IntVal(3)) ListItem(IntVal(37)))))
endmodule

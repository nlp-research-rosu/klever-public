requires "verification.k"

module SPEC-CLAIM-012
  imports VERIFICATION

  claim Run(SolutionMachine(360))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2))
                 ListItem(IntVal(2)) ListItem(IntVal(3))
                 ListItem(IntVal(3)) ListItem(IntVal(5)))))
endmodule

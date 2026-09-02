requires "verification.k"

module SPEC-CLAIM-011
  imports VERIFICATION

  claim Run(SolutionMachine(100))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2))
                 ListItem(IntVal(5)) ListItem(IntVal(5)))))
endmodule

requires "body-sensitivity-verification.k"

module BODY-SENSITIVITY-SPEC
  imports VERIFICATION

  claim Run(SolutionMachine(4))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2)))))
endmodule

requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  // Deliberately wrong: the semantics must not prove that 70 factors as [2, 5].
  claim Run(SolutionMachine(70))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(5)))))
endmodule

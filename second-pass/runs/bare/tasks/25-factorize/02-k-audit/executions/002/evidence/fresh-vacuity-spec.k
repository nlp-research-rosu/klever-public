requires "verification.k"

module FRESH-VACUITY-SPEC
  imports VERIFICATION

  // Fresh auditor mutation. False at the satisfiable ground input n = 25:
  // the executed result is [5, 5], not [5].
  claim Run(SolutionMachine(25))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(5)))))
endmodule

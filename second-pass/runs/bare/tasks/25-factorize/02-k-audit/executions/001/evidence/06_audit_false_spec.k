requires "verification.k"

module AUDIT-FALSE-SPEC
  imports VERIFICATION

  // Fresh auditor mutation: 25 does not factorize to the one-element list [5].
  claim Run(SolutionMachine(25))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(5)))))
endmodule


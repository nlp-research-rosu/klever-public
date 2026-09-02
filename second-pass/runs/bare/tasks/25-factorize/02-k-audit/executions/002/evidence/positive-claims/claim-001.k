requires "verification.k"

module SPEC-CLAIM-001
  imports VERIFICATION

  claim Run(SolutionMachine(1))
    => Run(Halted(.Map, SolutionFunctions(), .List, ListVal(.List)))
endmodule

requires "verification.k"

module SPEC-CLAIM-020
  imports VERIFICATION

  claim Observe(ValidFactorization(13, MachineValue(SolutionMachine(13))))
    => Observe(true)
endmodule

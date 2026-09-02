requires "verification.k"

module SPEC-CLAIM-021
  imports VERIFICATION

  claim Observe(ValidFactorization(25, MachineValue(SolutionMachine(25))))
    => Observe(true)
endmodule

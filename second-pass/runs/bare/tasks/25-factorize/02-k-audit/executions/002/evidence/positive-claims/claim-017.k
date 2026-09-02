requires "verification.k"

module SPEC-CLAIM-017
  imports VERIFICATION

  claim Observe(ValidFactorization(4, MachineValue(SolutionMachine(4))))
    => Observe(true)
endmodule

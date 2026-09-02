requires "verification.k"

module SPEC-CLAIM-016
  imports VERIFICATION

  claim Observe(ValidFactorization(3, MachineValue(SolutionMachine(3))))
    => Observe(true)
endmodule

requires "verification.k"

module SPEC-CLAIM-015
  imports VERIFICATION

  claim Observe(ValidFactorization(2, MachineValue(SolutionMachine(2))))
    => Observe(true)
endmodule

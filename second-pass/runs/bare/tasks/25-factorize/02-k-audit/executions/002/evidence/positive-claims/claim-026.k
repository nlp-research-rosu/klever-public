requires "verification.k"

module SPEC-CLAIM-026
  imports VERIFICATION

  claim Observe(ValidFactorization(999, MachineValue(SolutionMachine(999))))
    => Observe(true)
endmodule

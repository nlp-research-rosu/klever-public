requires "verification.k"

module SPEC-CLAIM-025
  imports VERIFICATION

  claim Observe(ValidFactorization(360, MachineValue(SolutionMachine(360))))
    => Observe(true)
endmodule

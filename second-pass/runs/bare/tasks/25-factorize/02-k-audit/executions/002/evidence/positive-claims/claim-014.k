requires "verification.k"

module SPEC-CLAIM-014
  imports VERIFICATION

  claim Observe(ValidFactorization(1, MachineValue(SolutionMachine(1))))
    => Observe(true)
endmodule

requires "verification.k"

module SPEC-CLAIM-022
  imports VERIFICATION

  claim Observe(ValidFactorization(31, MachineValue(SolutionMachine(31))))
    => Observe(true)
endmodule

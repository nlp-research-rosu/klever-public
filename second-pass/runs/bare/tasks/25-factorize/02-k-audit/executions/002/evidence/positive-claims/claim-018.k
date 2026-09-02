requires "verification.k"

module SPEC-CLAIM-018
  imports VERIFICATION

  claim Observe(ValidFactorization(8, MachineValue(SolutionMachine(8))))
    => Observe(true)
endmodule

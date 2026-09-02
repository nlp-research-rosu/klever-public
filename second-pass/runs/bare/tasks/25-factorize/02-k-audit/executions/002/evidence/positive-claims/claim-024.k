requires "verification.k"

module SPEC-CLAIM-024
  imports VERIFICATION

  claim Observe(ValidFactorization(100, MachineValue(SolutionMachine(100))))
    => Observe(true)
endmodule

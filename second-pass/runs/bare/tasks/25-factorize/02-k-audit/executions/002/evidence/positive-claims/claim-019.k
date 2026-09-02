requires "verification.k"

module SPEC-CLAIM-019
  imports VERIFICATION

  claim Observe(ValidFactorization(9, MachineValue(SolutionMachine(9))))
    => Observe(true)
endmodule

requires "verification.k"

module SPEC-CLAIM-023
  imports VERIFICATION

  claim Observe(ValidFactorization(70, MachineValue(SolutionMachine(70))))
    => Observe(true)
endmodule

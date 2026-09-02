requires "verification.k"

module PROOF-FUNCTION-GROUND
  imports VERIFICATION

  claim [count-one]: qualifyingCount(1) => 1
  claim [count-two]: qualifyingCount(2) => 18
  claim [count-three]: qualifyingCount(3) => 180
  claim [count-five]: qualifyingCount(5) => 18000
endmodule

requires "verification.k"

module WITNESS
  imports VERIFICATION

  // Ground interpretation used only to exhibit a satisfying entry state for
  // ID = 68, LENGTH = 3, corresponding to Python input [4, 2, 3].
  rule arrayAt(68, 0) => 4
  rule arrayAt(68, 1) => 2
  rule arrayAt(68, 2) => 3
endmodule

requires "verification.k"

module VERIFICATION-NEGATIVE-MODEL
  imports VERIFICATION

  // Model completion permitted by the candidate target rule: unlike fixed
  // Subscript semantics, its raw valSeqAt(VS, -1) has no defining equation.
  rule valSeqAt(vCons(5, .ValSeq), -1) => 6
endmodule

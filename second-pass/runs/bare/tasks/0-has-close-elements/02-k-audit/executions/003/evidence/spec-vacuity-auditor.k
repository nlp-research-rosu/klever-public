requires "/tmp/audit-work/candidate-src/verification.k"

module SPEC-VACUITY-AUDITOR
  imports VERIFICATION

  // Deliberately false: both Python implementations and the original K claim
  // return false on the satisfying input ([], 0).
  claim [false-empty-result]:
    <k> verify(VList(.PValues), VInt(0)) => VBool(true) </k>
endmodule

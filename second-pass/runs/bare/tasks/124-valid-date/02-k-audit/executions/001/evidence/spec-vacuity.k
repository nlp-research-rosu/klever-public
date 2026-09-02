requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-SPEC-VACUITY
  imports VALID-DATE-VERIFICATION

  // Fresh false mutation of submitted claim 1: this reachable input returns true.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-2000")))
          => boolVal(false) </k>
endmodule

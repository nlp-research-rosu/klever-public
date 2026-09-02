requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-001
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-2000")))
          => boolVal(true) </k>
endmodule

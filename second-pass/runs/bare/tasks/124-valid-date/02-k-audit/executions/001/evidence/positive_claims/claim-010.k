requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-010
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-1a-2000")))
          => boolVal(false) </k>
endmodule

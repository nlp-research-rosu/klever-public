requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-026
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("01-31-0000")))
          => boolVal(true) </k>
endmodule

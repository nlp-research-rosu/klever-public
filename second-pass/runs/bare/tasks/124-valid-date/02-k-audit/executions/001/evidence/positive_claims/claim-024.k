requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-024
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("11-30-2020")))
          => boolVal(true) </k>
endmodule

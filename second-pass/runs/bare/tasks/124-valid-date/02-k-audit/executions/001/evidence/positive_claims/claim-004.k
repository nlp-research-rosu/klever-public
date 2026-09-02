requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-004
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("06-04-2020")))
          => boolVal(true) </k>
endmodule

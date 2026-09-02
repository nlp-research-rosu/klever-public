requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-032
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("12-31-2020")))
          => boolVal(true) </k>
endmodule

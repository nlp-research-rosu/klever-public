requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-021
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("06-31-2020")))
          => boolVal(false) </k>
endmodule

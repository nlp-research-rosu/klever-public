requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-014
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("12-00-2020")))
          => boolVal(false) </k>
endmodule

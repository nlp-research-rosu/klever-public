requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-013
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("13-01-2020")))
          => boolVal(false) </k>
endmodule

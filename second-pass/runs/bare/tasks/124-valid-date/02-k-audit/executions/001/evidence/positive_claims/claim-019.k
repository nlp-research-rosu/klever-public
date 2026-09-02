requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-019
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("04-31-2020")))
          => boolVal(false) </k>
endmodule

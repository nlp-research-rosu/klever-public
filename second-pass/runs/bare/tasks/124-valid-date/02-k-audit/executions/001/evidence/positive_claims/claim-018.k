requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-018
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("04-30-2020")))
          => boolVal(true) </k>
endmodule

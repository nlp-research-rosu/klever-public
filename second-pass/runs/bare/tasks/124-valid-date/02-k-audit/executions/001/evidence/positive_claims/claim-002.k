requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-002
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("15-01-2012")))
          => boolVal(false) </k>
endmodule

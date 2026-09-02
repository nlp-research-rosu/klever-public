requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-012
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("00-01-2020")))
          => boolVal(false) </k>
endmodule

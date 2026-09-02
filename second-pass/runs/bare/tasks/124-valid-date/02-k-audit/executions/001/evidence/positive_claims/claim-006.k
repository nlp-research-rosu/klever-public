requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-006
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("")))
          => boolVal(false) </k>
endmodule

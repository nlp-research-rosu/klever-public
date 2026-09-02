requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-016
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("02-29-1900")))
          => boolVal(true) </k>
endmodule

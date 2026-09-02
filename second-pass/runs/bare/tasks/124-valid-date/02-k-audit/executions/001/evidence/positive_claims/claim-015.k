requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-015
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("02-01-2020")))
          => boolVal(true) </k>
endmodule

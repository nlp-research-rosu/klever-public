requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-017
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("02-30-2020")))
          => boolVal(false) </k>
endmodule

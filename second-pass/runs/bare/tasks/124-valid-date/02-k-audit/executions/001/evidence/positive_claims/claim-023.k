requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-023
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("09-31-2020")))
          => boolVal(false) </k>
endmodule

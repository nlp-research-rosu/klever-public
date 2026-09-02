requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-003
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("04-0-2040")))
          => boolVal(false) </k>
endmodule

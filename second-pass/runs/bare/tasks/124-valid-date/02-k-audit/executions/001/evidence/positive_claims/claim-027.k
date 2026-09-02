requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-027
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-31-9999")))
          => boolVal(true) </k>
endmodule

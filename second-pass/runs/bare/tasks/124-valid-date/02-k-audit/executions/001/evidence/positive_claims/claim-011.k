requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-011
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-20x0")))
          => boolVal(false) </k>
endmodule

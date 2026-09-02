requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-008
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("003-11-2000")))
          => boolVal(false) </k>
endmodule

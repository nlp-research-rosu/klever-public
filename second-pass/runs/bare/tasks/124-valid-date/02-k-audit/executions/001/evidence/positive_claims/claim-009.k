requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-009
  imports VALID-DATE-VERIFICATION

  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("aa-bb-cccc")))
          => boolVal(false) </k>
endmodule

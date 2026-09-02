requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-UNIVERSAL-TARGET
  imports VALID-DATE-VERIFICATION

  // This is the missing result-constraining theorem over the formal String domain.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal(S:String)))
          => boolVal(validDateSpec(S)) </k>
endmodule

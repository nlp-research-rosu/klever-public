requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-043
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(8, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
endmodule

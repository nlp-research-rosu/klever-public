requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-042
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(7, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
endmodule

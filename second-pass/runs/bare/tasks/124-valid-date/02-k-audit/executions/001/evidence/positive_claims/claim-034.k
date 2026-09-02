requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-034
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(2, D))
          => boolVal(D >=Int 1 andBool D <=Int 29) </k>
endmodule

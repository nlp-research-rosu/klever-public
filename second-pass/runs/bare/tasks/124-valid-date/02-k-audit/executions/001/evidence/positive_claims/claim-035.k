requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-035
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(4, D))
          => boolVal(D >=Int 1 andBool D <=Int 30) </k>
endmodule

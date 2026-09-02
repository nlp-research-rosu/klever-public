requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-038
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(11, D))
          => boolVal(D >=Int 1 andBool D <=Int 30) </k>
endmodule

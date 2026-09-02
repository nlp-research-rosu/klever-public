requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-036
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(6, D))
          => boolVal(D >=Int 1 andBool D <=Int 30) </k>
endmodule

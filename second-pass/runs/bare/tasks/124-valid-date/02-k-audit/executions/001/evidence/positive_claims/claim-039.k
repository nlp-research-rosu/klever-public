requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-039
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(1, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
endmodule

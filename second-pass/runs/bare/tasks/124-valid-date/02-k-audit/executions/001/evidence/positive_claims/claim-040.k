requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-040
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(3, D))
          => boolVal(D >=Int 1 andBool D <=Int 31) </k>
endmodule

requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-047
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(M, D)) => boolVal(false) </k>
    requires M >=Int 1 andBool M <=Int 12 andBool D <Int 1
endmodule

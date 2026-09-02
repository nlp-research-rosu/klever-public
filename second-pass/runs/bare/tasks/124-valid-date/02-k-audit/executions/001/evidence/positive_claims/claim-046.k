requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-CLAIM-046
  imports VALID-DATE-VERIFICATION

  claim <k> boolVal(validMonthDay(M, _D)) => boolVal(false) </k>
    requires M <Int 1 orBool M >Int 12
endmodule

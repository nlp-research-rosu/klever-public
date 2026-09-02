requires "verification.k"

module AUDIT-WITNESS-SPEC
  imports COUNT-NUMS-VERIFICATION-BASE

  // Ground substitutions for the helper summaries and the final entry result.
  claim <k> positiveDigitSum(109) => 10 </k>
  claim <k> negativeDigitSum(109) => 8 </k>
  claim <k> signedDigitSum(-109) => 8 </k>
  claim <k> signedDigitSum(-123) => 4 </k>
  claim <k> allInts(vCons(-1, vCons(11, vCons(-11, .ValSeq)))) => true </k>
  claim <k> countPositive(vCons(-1, vCons(11, vCons(-11, .ValSeq)))) => 1 </k>
endmodule

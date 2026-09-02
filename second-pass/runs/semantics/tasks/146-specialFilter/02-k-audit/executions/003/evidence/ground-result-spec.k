requires "verification.k"

module GROUND-RESULT-SPEC
  imports SPECIALFILTER-VERIFICATION-LOOP

  // Python and the trusted concrete semantics both return 1 for [11].
  claim <k> specialCount(iCons(11, .IntSeq)) => 1 </k>
endmodule

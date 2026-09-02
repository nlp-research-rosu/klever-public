requires "verification.k"

module SAFEAT-CORRECT
  imports VERIFICATION-BASE

  claim <k> safeAt(iCons(97, iCons(98, iCons(99, .IntSeq))), 0) => 97 </k>
  claim <k> safeAt(iCons(97, iCons(98, iCons(99, .IntSeq))), 2) => 99 </k>
  claim <k> intSeqAt(iCons(97, iCons(98, iCons(99, .IntSeq))), 1) => 98 </k>
endmodule

module SAFEAT-WRONG-OPPOSITE
  imports VERIFICATION-BASE

  // Deliberately false opposite interpretation of the first ground witness.
  claim <k> safeAt(iCons(97, iCons(98, iCons(99, .IntSeq))), 0) => 98 </k>
endmodule

requires "verification.k"

module AUDIT-ABSTRACTION-OPPOSITE-LOWER-STRING
  imports VERIFICATION

  // False opposite interpretation: ASCII "a" is lower-case.
  claim [wrong]:
    <k> lowerKey(str(iCons(97, .IntSeq))) => false </k>
endmodule

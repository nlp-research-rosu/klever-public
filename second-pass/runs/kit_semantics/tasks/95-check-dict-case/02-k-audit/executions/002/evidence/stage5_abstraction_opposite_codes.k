requires "verification.k"

module AUDIT-ABSTRACTION-OPPOSITE-CODES
  imports VERIFICATION

  // False opposite interpretation: stringCodes("a") is exactly [97].
  claim [wrong]:
    <k> stringCodes(str(iCons(97, .IntSeq))) => .IntSeq </k>
endmodule

requires "verification-base.k"

module REVIEWER-LOOPDIGITS-GROUND
  imports VERIFICATION-BASE

  claim [two-produces-zero]:
    <k> loopDigits(2, .IntSeq) => iCons(48, .IntSeq) </k>

  claim [three-produces-one]:
    <k> loopDigits(3, .IntSeq) => iCons(49, .IntSeq) </k>

  claim [false-opposite-for-two]:
    <k> loopDigits(2, .IntSeq) => iCons(49, .IntSeq) </k>
endmodule

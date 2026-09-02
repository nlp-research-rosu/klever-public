requires "verification.k"

module OPPOSITE-EVEN-SPEC
  imports VERIFICATION-BASE

  // False opposite interpretation: 2 % 2 == 0 is true, not false.
  claim [opposite-even]:
    <k> applyCmp("==", applyBin("%", 2, 2), 0) => false </k>
endmodule

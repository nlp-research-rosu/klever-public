requires "verification.k"

module OPPOSITE-ODD-SPEC
  imports VERIFICATION-BASE

  // False opposite interpretation: 1 % 2 == 0 is false, not true.
  claim [opposite-odd]:
    <k> applyCmp("==", applyBin("%", 1, 2), 0) => true </k>
endmodule

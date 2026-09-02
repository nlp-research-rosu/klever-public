requires "verification.k"

module COMPARISON-OPPOSITE-SPEC
  imports VERIFICATION

  // Deliberately opposite to 0 < 1.
  claim <k> applyCmp("<", 0, 1) => false </k>
    [label(compare-opposite-witness)]
endmodule

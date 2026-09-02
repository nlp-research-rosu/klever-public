requires "verification.k"

module COMPARISON-VALUE-SPEC
  imports VERIFICATION

  claim <k> applyCmp("<", 0, 1) => true </k>
    [label(compare-true-witness)]

  claim <k> applyCmp("<", 1, 0) => false </k>
    [label(compare-false-witness)]
endmodule

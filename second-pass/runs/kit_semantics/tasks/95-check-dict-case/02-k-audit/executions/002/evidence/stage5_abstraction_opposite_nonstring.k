requires "verification.k"

module AUDIT-ABSTRACTION-OPPOSITE-NONSTRING
  imports VERIFICATION

  // False opposite interpretation: an integer key is not lower-case.
  claim [wrong]:
    <k> lowerKey(8) => true </k>
endmodule

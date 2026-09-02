requires "verification.k"

module CONNECTION-WRONG-SPEC
  imports VERIFICATION-BASE

  // Deliberately opposite interpretation for a satisfiable ground witness.
  claim [wrong-even-value]:
    <k>
      applyCmp("==", applyBin("%", 2, 2), 0)
      => false
    </k>
endmodule

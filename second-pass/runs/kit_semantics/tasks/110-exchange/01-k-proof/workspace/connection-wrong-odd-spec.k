requires "verification.k"

module CONNECTION-WRONG-ODD-SPEC
  imports VERIFICATION-BASE

  // Deliberately opposite interpretation for a distinct odd witness.
  claim [wrong-odd-value]:
    <k>
      applyCmp("==", applyBin("%", 1, 2), 0)
      => true
    </k>
endmodule

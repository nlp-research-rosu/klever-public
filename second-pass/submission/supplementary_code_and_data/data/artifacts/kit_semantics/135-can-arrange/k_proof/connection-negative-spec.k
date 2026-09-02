requires "verification.k"

module CONNECTION-NEGATIVE-SPEC
  imports VERIFICATION-BASE

  // Deliberately false opposite interpretation: 2 >= 1 is true.
  claim [wrong-ge]:
    <k> applyCmp(">=", 2, 1) => false </k>
endmodule

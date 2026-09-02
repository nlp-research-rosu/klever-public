requires "verification.k"

module REVIEWER-OPPOSITE-COMPARISON
  imports VERIFICATION-BASE

  // Deliberately false under fixed semantics: 2 >= 1 cannot be false.
  claim [wrong-opposite]:
    <k> applyCmp(">=", 2, 1) => false </k>
endmodule

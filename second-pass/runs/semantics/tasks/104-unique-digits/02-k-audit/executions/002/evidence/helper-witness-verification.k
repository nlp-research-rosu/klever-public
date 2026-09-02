requires "verification.k"

module UNIQUE-DIGITS-HELPER-FALSE-WITNESS
  imports UNIQUE-DIGITS-WITH-HELPER

  // This is the opposite of the fixed helper's actual result at 2. It is
  // admitted because oddDigits has no candidate equations or connection proof.
  rule oddDigits(2) => true [simplification]
endmodule

requires "semantic.k"

module VERIFICATION
  imports MPY

  // Mathematical postcondition used by the proof.  Restricting N to the
  // natural-number domain in spec.k matches "numbers from 1 to n".
  syntax Int ::= "sumSpec" "(" Int ")" [function]
  rule sumSpec(N) => (N *Int (N +Int 1)) /Int 2
endmodule

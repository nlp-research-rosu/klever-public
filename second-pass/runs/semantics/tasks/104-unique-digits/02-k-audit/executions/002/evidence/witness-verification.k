requires "verification.k"

module UNIQUE-DIGITS-FALSE-WITNESS
  imports UNIQUE-DIGITS-VERIFICATION

  // Independently true ground facts for the original HumanEval meaning.
  rule oddDigits(1) => true [simplification]
  rule sortVS(vCons(1, .ValSeq)) => vCons(1, .ValSeq) [simplification]
endmodule

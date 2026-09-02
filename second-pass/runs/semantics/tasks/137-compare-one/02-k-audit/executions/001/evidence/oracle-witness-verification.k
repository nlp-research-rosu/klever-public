requires "verification.k"

// Opposite interpretations admitted because candidate symbols have no equations.
module ORACLE-WITNESS-VERIFICATION
  imports VERIFICATION

  // False interpretation for distinct floats.
  rule sameFloat(1.0, 2.0) => true

  // Truthful equality on 0.0, paired with a false decimal interpretation.
  rule sameFloat(0.0, 0.0) => true
  rule commaDecimal(iCons(50, iCons(44, iCons(51, .IntSeq)))) => 0.0
endmodule

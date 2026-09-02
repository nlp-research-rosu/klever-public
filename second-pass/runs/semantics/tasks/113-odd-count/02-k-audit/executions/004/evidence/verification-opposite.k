requires "verification.k"

module ODD-COUNT-OPPOSITE-VERIFICATION
  imports ODD-COUNT-VERIFICATION

  // A ground interpretation admitted by the otherwise unconstrained
  // decimalCodes symbol.  This deliberately maps the integer 1 to "9".
  rule decimalCodes(1) => iCons(57, .IntSeq)
endmodule

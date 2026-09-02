requires "verification.k"

module OPPOSITE-DECIMAL-INTERPRETATION
  imports SPECIALFILTER-VERIFICATION-SYNTAX

  rule decimalLength(12) => 2
  rule decimalCodeAt(12, 0) => 49
  rule decimalCodeAt(12, 1) => 49
endmodule

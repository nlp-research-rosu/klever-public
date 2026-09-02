requires "verification.k"

module OPPOSITE-DECIMAL-INTERPRETATION
  imports SPECIALFILTER-VERIFICATION-SYNTAX

  // A consistent opposite interpretation admitted by the three opaque
  // decimal abstractions on symbolic integers: every integer appears to have
  // two characters, both ASCII '1'.
  rule decimalLength(_:Int) => 2
  rule decimalCodeAt(_:Int, _:Int) => 49
endmodule

requires "verification.k"

module WRONG-FLOAT-ORACLE
  imports VERIFICATION

  // Admissible opposite interpretation of the otherwise equation-free symbol.
  rule sameFloat(_:Float, _:Float) => true
endmodule

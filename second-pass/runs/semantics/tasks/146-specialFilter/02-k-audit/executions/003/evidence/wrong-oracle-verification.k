requires "verification.k"

module SPECIALFILTER-WRONG-ORACLE
  imports SPECIALFILTER-VERIFICATION

  // A ground interpretation admitted by the candidate's otherwise
  // unconstrained proof-local decimal symbols.
  rule decimalCodes(_:Int) => .IntSeq
  rule decimalLength(_:Int) => 0
  rule decimalCodeAt(_:Int, _:Int) => 48
endmodule

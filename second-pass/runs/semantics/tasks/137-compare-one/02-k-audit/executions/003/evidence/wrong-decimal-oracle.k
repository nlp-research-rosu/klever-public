requires "verification.k"

module WRONG-DECIMAL-ORACLE
  imports VERIFICATION

  // An admissible but false interpretation: the numeric string "1" parses as 3.0.
  rule commaDecimal(iCons(49, .IntSeq)) => 3.0

  // Ground, mathematically correct float facts for the resulting comparison.
  rule sameFloat(3.0, 2.0) => false
  rule <k> Compare(3.0, CmpOp(">", 2.0)) => true ... </k>
    [priority(40)]
endmodule

requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A mathematical presentation of the required wrapper around the usual
  // base-two digit expansion.  Keeping it separate from expression evaluation
  // makes the reachability claim state the contract rather than an AST result.
  syntax String ::= decimalToBinarySpec(Int) [function]

  rule decimalToBinarySpec(I)
    => "db" +String binDigits(I) +String "db"
    requires I >=Int 0
  rule decimalToBinarySpec(I)
    => ("db" +String ("b" +String binDigits(0 -Int I))) +String "db"
    requires I <Int 0
endmodule

requires "semantic.k"

module VERIFICATION
  imports MPY

  // Mathematical reference function for the contract.  Because base <= 9,
  // every remainder is a single decimal digit, exactly as required by the
  // prompt's string representation.
  syntax String ::= baseString(Int, Int) [function]

  rule baseString(X, B) => Int2String(X)
    requires X <Int B

  rule baseString(X, B)
        => baseString(X /Int B, B) +String Int2String(X %Int B)
    requires B <=Int X andBool 0 <Int B
endmodule

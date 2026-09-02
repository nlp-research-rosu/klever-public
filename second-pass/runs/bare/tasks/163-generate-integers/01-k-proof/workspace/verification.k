requires "semantic.k"

module VERIFICATION
  imports MPY

  syntax List ::= expectedDigit(Int, Int, Int) [function]
  syntax List ::= expected(Int, Int) [function]

  rule expectedDigit(A, B, D) => ListItem(D)
    requires (A <=Int D andBool D <=Int B)
      orBool (B <=Int D andBool D <=Int A)
  rule expectedDigit(A, B, D) => .List
    requires notBool (
      (A <=Int D andBool D <=Int B)
        orBool (B <=Int D andBool D <=Int A))

  rule expected(A, B)
    => expectedDigit(A, B, 2)
       expectedDigit(A, B, 4)
       expectedDigit(A, B, 6)
       expectedDigit(A, B, 8)
endmodule

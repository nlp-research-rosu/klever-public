requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical postcondition for the ordered list of even decimal digits
  // lying in the inclusive interval whose endpoints are A and B.
  syntax Bool ::= inClosedSpan(Int, Int, Int) [function, total]
  rule inClosedSpan(A, B, D)
    => ((A <=Int D andBool D <=Int B)
        orBool (B <=Int D andBool D <=Int A))

  syntax ValSeq ::= keepDigit(Bool, Int, ValSeq) [function, total]
  rule keepDigit(true,  D, REST) => vCons(D, REST)
  rule keepDigit(false, _, REST) => REST

  syntax ValSeq ::= expectedDigits(Int, Int) [function, total]
  rule expectedDigits(A, B)
    => keepDigit(inClosedSpan(A, B, 2), 2,
         keepDigit(inClosedSpan(A, B, 4), 4,
           keepDigit(inClosedSpan(A, B, 6), 6,
             keepDigit(inClosedSpan(A, B, 8), 8, .ValSeq))))
endmodule

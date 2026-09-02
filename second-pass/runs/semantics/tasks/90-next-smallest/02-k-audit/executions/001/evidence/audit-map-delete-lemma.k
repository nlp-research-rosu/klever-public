requires "verification.k"

module AUDIT-MAP-DELETE-LEMMA
  imports NEXT-SMALLEST-VERIFICATION

  // Extensional MAP law needed only because the Haskell backend leaves this
  // built-in update symbolic: deleting a freshly disjoint key removes its entry.
  rule ((I:Int |-> S:Scope) M:Map) [ I <- undef ] => M
    requires notBool I in_keys(M)
    [simplification]
endmodule

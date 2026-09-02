requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTIC

  rule notBool notBool B => B [simplification]

  // Mathematical contract: in a nonempty list, either the head has its
  // additive inverse at a later (therefore distinct) position, or the pair is
  // wholly in the tail.  These guarded equations also serve as the invariant
  // used by the circular reachability proof.
  rule hasZeroPair(L) => false
    requires isEmpty(L) [simplification]
  rule hasZeroPair(L)
    => member(0 -Int first(L), rest(L)) orBool hasZeroPair(rest(L))
    requires notBool isEmpty(L) [simplification]
endmodule

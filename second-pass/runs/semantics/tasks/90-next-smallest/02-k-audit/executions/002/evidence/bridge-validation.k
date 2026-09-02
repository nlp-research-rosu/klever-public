requires "verification.k"

module BRIDGE-VALIDATION
  imports NEXT-SMALLEST-VERIFICATION

  // K's finite-map update with `undef` deletes a key.  This lemma makes the
  // otherwise opaque symbolic deletion normalization available to the prover.
  rule ((SC:Map 1 |-> S:Scope) [1 <- undef]) => SC
    requires notBool (1 in_keys(SC))
    [simplification]
endmodule

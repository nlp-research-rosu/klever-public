requires "projection.k"

module VERIFICATION
  imports INT-PROJECTION

  // True exactly when X has a distinct-position additive inverse in FULL.
  syntax Bool ::= hasInverse(Int, ValSeq) [function, total]
  rule hasInverse(X, FULL)
    => ((X ==Int 0) andBool (cntOccVS(FULL, 0) >Int 1))
       orBool
       ((X =/=Int 0) andBool
         (cntOccVS(FULL, 0 -Int X) >Int 0))

  // True exactly when some integer in REM has an inverse partner in FULL.
  // Non-Int elements are ignored, making the definition total; the theorem's
  // allInts precondition excludes that branch.
  syntax Bool ::= anyInverse(ValSeq, ValSeq) [function, total]
  rule anyInverse(.ValSeq, _FULL) => false
  rule anyInverse(vCons(X:Val, REM), FULL)
    => (isInt(X) andBool hasInverse(intProj(X), FULL))
       orBool anyInverse(REM, FULL)

  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(X:Val, REM)) => isInt(X) andBool allInts(REM)

  // Sort-recovery bridges. Their guards say that the Val is an injected Int;
  // connection-spec.k proves the corresponding fixed-semantics equalities
  // without importing this module.
  rule applyCmp("==", V:Val, I:Int) => intProj(V) ==Int I
    requires isInt(V)
    [simplification]

  rule applyUn("-", V:Val) => 0 -Int intProj(V)
    requires isInt(V)
    [simplification]
endmodule

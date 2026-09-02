requires "semantic.k"

module VERIFICATION
  imports MPY
  imports BOOL
  imports K-EQUAL
  imports MAP-SYMBOLIC

  // #incPrefix(L, I) is the canonical abstraction of the first I elements of
  // L, each incremented by one. MPY gives its empty base and one-step append
  // equation. SPEC supplies and discharges the loop invariant; there are no
  // trusted reachability rules here.
  rule { #incPrefix(L, I) #Equals #incPrefix(L, J) }
    => { I #Equals J }
    [simplification]

  rule 0 <=Int size(_L:List) => true [simplification]
endmodule

requires "semantic.k"

module VERIFICATION
  imports MPY
  imports BOOL
  imports K-EQUAL
  imports MAP-SYMBOLIC

  // Audit diagnostic: candidate's unguarded #incPrefix injectivity
  // simplification has been removed. The nonnegative-size lemma remains.
  rule 0 <=Int size(_L:List) => true [simplification]
endmodule

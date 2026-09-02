requires "base-verification.k"

module VERIFICATION-LOOPS
  imports VERIFICATION-BASE

  // Derived dispatch lemma. connection-spec.k proves each complete numeric
  // sort case without importing this module.
  rule applyCmp("<", V:Val, T:Int) => numericLt(V, T)
    requires numericVal(V)
    [simplification]
endmodule

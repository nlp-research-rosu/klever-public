requires "reference-semantics/semantics.k"

module FIXED-SEMANTICS-LEMMA
  imports MPY

  // Bridge-free audit theorem for verification.k's sole simplification.
  // This spec is proved against a definition that excludes verification.k.
  claim [guarded-int-equality]:
    <k>
      applyCmp("==", V:Val, I:Int)
      =>
      {V}:>Int ==Int I
      ...
    </k>
    requires isInt(V)
endmodule

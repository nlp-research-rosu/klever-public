requires "reference-semantics/semantics.k"

module FIXED-SEMANTICS-LEMMA
  imports MPY

  // First bounded audit attempt.  The backend rejects functional claims before
  // proof execution, as recorded in the matching log.
  claim [guarded-int-equality]:
    applyCmp("==", V:Val, I:Int)
    =>
    {V}:>Int ==Int I
    requires isInt(V)
endmodule

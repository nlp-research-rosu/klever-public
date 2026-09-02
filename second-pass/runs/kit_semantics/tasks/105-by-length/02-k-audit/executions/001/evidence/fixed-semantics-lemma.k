requires "reference-semantics/semantics.k"

module FIXED-SEMANTICS-LEMMA
  imports MPY

  // Bridge-free fixed-semantics equation underlying verification.k's guarded
  // sort-refinement simplification.  The additional step from V:Val with
  // isInt(V) to X:Int is the generated K sort-predicate/cast contract.
  claim [int-equality]:
    <k>
      applyCmp("==", X:Int, I:Int)
      =>
      X ==Int I
      ...
    </k>
endmodule

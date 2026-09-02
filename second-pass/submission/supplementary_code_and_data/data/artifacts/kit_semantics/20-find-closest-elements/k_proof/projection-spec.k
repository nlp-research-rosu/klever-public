requires "reference-semantics/semantics.k"

module PROJECTION-SPEC
  imports MPY

  claim [index-zero-fixed]:
    <k>
      applyIndex(
        tuple(vCons(I:Int, vCons(F:Float, .ValSeq))),
        0)
      =>
      I
      ...
    </k>

  claim [index-one-fixed]:
    <k>
      applyIndex(
        tuple(vCons(I:Int, vCons(F:Float, .ValSeq))),
        1)
      =>
      F
      ...
    </k>
endmodule

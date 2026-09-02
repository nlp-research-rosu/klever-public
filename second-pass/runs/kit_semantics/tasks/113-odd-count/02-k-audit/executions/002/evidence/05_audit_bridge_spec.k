requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-SPEC
  imports MPY

  claim [complete-count-domain]:
    <k>
      applyMethod(V:Val, "count", str(PATTERN:IntSeq), .Vals)
      =>
      cntSub(?CODES:IntSeq, PATTERN)
    </k>
    requires isStrV(V)
    ensures V ==K str(?CODES)

  claim [count-zero]:
    <k>
      applyMethod(
        str(iCons(50, iCons(48, .IntSeq))),
        "count",
        str(iCons(49, .IntSeq)),
        .Vals)
      =>
      0
    </k>

  claim [count-two]:
    <k>
      applyMethod(
        str(iCons(49, iCons(49, .IntSeq))),
        "count",
        str(iCons(49, .IntSeq)),
        .Vals)
      =>
      2
    </k>
endmodule

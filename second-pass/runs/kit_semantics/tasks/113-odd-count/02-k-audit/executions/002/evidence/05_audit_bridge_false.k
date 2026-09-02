requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-FALSE
  imports MPY

  claim [wrong-count]:
    <k>
      applyMethod(
        str(iCons(49, iCons(49, .IntSeq))),
        "count",
        str(iCons(49, .IntSeq)),
        .Vals)
      =>
      1
    </k>
endmodule

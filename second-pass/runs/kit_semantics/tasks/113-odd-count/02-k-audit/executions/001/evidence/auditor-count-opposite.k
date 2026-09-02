requires "reference-semantics/semantics.k"

module AUDITOR-COUNT-OPPOSITE
  imports MPY

  // Fixed semantics says "11".count("1") is 2, not 1.
  claim [false-count-interpretation]:
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

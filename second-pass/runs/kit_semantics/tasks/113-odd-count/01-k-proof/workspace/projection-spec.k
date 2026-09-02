requires "reference-semantics/semantics.k"

module PROJECTION-SPEC
  imports MPY

  claim [count-connection]:
    <k>
      applyMethod(
        str(CODES:IntSeq),
        "count",
        str(PATTERN:IntSeq),
        .Vals)
      =>
      cntSub(CODES, PATTERN)
    </k>
endmodule
